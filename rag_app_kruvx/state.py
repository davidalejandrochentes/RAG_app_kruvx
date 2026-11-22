"""Chat State with streaming support for NVIDIA API + RAG."""

import os
import asyncio
import time
import hashlib
import reflex as rx
from openai import AsyncOpenAI
from dotenv import load_dotenv

from .rag_engine import is_kruvx_related, get_rag_engine

load_dotenv()


# ─── NVIDIA Client (eager init at startup) ────────────────────────────────

_nvidia_client: AsyncOpenAI


def _init_client() -> AsyncOpenAI:
    """Initialize the NVIDIA OpenAI-compatible client at module load."""
    api_key = os.getenv("NVIDIA_API_KEY")
    base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY not found in environment")
    return AsyncOpenAI(api_key=api_key, base_url=base_url)


# Eager initialization - runs once when module is imported (app startup)
_nvidia_client = _init_client()


def _get_client() -> AsyncOpenAI:
    """Get the pre-initialized NVIDIA OpenAI-compatible client (singleton)."""
    return _nvidia_client


def _get_model() -> str:
    """Get model from env or default."""
    return os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning")


# ─── System Prompts ──────────────────────────────────────────────────────

SYSTEM_PROMPT_BASE = """Eres Kruvi, el asistente virtual de Kruvx. Tu misión es ayudar a los usuarios a entender todo sobre Kruvx: cómo funciona, precios, referidos, onboarding, dashboard, y cualquier duda sobre la plataforma.

REGLAS ESTRICTAS:
1. SOLO respondes preguntas relacionadas con Kruvx (la app, sus características, precios, referidos, negocios, usuarios, términos, soporte, etc.)
2. Si la pregunta NO es sobre Kruvx (ej. fútbol, política, cocina, programación, viajes, salud, finanzas, cine, música, ciencia, etc.), respondes EXACTAMENTE:
   "Lo siento, solo puedo ayudarte con preguntas relacionadas con Kruvx 😊. ¿Tienes alguna duda sobre cómo funciona la app, los referidos, precios, o tu negocio en Kruvx?"
3. Basas tus respuestas EN LA INFORMACIÓN PROPORCIONADA en el contexto. NO inventas información.
4. Si el contexto no tiene la respuesta, dices: "No tengo esa información en mi base de conocimiento de Kruvx. ¿Te gustaría que te ayude con otra duda sobre la plataforma?"
5. Respondes en español, de forma natural, amigable y conversacional.
6. Usas emojis moderadamente para dar calidez.
7. Eres conciso pero completo."""

SYSTEM_PROMPT_WITH_CONTEXT = SYSTEM_PROMPT_BASE + """

CONTEXTO DE KRUVX (usa esta información para responder):
{context}"""


# ─── Chat State ──────────────────────────────────────────────────────────

class ChatState(rx.State):
    """State for the streaming chat interface with RAG."""

    # Chat messages: list of dicts with role and content
    messages: list[dict[str, str]] = []

    # Input state
    current_input: str = ""

    # Loading/streaming state
    is_streaming: bool = False

    # Welcome message tracking
    welcome_shown: bool = False

    # ─── Protection Layer: Rate Limiting ─────────────────────────────────
    request_timestamps: list[float] = []
    requests_today: int = 0
    last_reset_date: str = ""

    # ─── Protection Layer: Budget Tracking ───────────────────────────────
    total_tokens_used: int = 0
    total_chars_input: int = 0

    # ─── Protection Layer: Debounce ──────────────────────────────────────
    last_request_time: float = 0.0

    # ─── Protection Layer: Response Cache ────────────────────────────────
    response_cache: dict[str, str] = {}
    cache_timestamps: dict[str, float] = {}

    # ─── Configuration Constants ─────────────────────────────────────────
    MAX_REQ_PER_MINUTE: int = 10
    MAX_REQ_PER_HOUR: int = 50
    MAX_REQ_PER_DAY: int = 200

    MAX_CHARS_PER_MESSAGE: int = 2000
    MIN_CHARS_PER_MESSAGE: int = 2

    MAX_TOKENS_PER_SESSION: int = 50000
    MAX_CHARS_PER_SESSION: int = 100000

    MIN_REQUEST_INTERVAL: float = 2.0

    CACHE_TTL: int = 3600
    CACHE_MAX_ENTRIES: int = 50

    # ─── Injection Patterns (basic) ──────────────────────────────────────
    INJECTION_PATTERNS: tuple[str, ...] = (
        "ignore previous",
        "ignore all previous",
        "system prompt",
        "you are now",
        "forget everything",
        "forget all",
        "new instructions",
        "override",
        "disregard",
        "prompt injection",
        "jailbreak",
        "dan mode",
        "developer mode",
    )

    def set_input(self, value: str):
        """Update the current input value."""
        self.current_input = value

    # ─── Protection Helper Methods ───────────────────────────────────────

    def _get_current_date(self) -> str:
        """Get current date as YYYY-MM-DD string."""
        return time.strftime("%Y-%m-%d")

    def _clean_old_timestamps(self, now: float) -> None:
        """Remove timestamps older than 1 hour."""
        cutoff = now - 3600
        self.request_timestamps = [ts for ts in self.request_timestamps if ts > cutoff]

    def _check_rate_limit(self) -> tuple[bool, str]:
        """Check rate limits per minute, hour, and day."""
        now = time.time()
        today = self._get_current_date()

        # Reset daily counter if date changed
        if self.last_reset_date != today:
            self.requests_today = 0
            self.last_reset_date = today

        # Clean old timestamps
        self._clean_old_timestamps(now)

        # Count requests in last minute and hour
        minute_cutoff = now - 60
        hour_cutoff = now - 3600

        req_last_minute = sum(1 for ts in self.request_timestamps if ts > minute_cutoff)
        req_last_hour = sum(1 for ts in self.request_timestamps if ts > hour_cutoff)

        if req_last_minute >= self.MAX_REQ_PER_MINUTE:
            return False, "Demasiados mensajes rápidos. Espera un momento."

        if req_last_hour >= self.MAX_REQ_PER_HOUR:
            return False, "Límite horario alcanzado. Intenta más tarde."

        if self.requests_today >= self.MAX_REQ_PER_DAY:
            return False, "Límite diario alcanzado. Vuelve mañana."

        return True, ""

    def _check_input_valid(self, text: str) -> tuple[bool, str]:
        """Validate input length and check for injection patterns."""
        if len(text) < self.MIN_CHARS_PER_MESSAGE:
            return False, "Mensaje demasiado corto."

        if len(text) > self.MAX_CHARS_PER_MESSAGE:
            return False, f"Mensaje muy largo (máx. {self.MAX_CHARS_PER_MESSAGE} caracteres)."

        text_lower = text.lower()
        for pattern in self.INJECTION_PATTERNS:
            if pattern in text_lower:
                return False, "Entrada no válida."

        return True, ""

    def _check_budget(self, text: str) -> tuple[bool, str]:
        """Check token and character budget for session."""
        estimated_tokens = self._estimate_tokens(text)
        new_total_tokens = self.total_tokens_used + estimated_tokens
        new_total_chars = self.total_chars_input + len(text)

        if new_total_tokens > self.MAX_TOKENS_PER_SESSION:
            return False, "Límite de uso alcanzado para esta sesión."

        if new_total_chars > self.MAX_CHARS_PER_SESSION:
            return False, "Límite de caracteres alcanzado para esta sesión."

        return True, ""

    def _check_debounce(self) -> tuple[bool, str]:
        """Check minimum interval between requests."""
        now = time.time()
        if now - self.last_request_time < self.MIN_REQUEST_INTERVAL:
            return False, "Espera un momento antes de enviar otro mensaje."
        return True, ""

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation: ~4 chars = 1 token in Spanish."""
        return max(1, len(text) // 4)

    def _get_cache_key(self, text: str) -> str:
        """Generate normalized cache key from query."""
        normalized = text.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]

    def _clean_cache(self, now: float) -> None:
        """Remove expired cache entries and enforce max size."""
        # Remove expired
        expired_keys = [
            k for k, ts in self.cache_timestamps.items()
            if now - ts > self.CACHE_TTL
        ]
        for k in expired_keys:
            self.response_cache.pop(k, None)
            self.cache_timestamps.pop(k, None)

        # Enforce max entries (FIFO)
        if len(self.response_cache) > self.CACHE_MAX_ENTRIES:
            # Sort by timestamp, remove oldest
            sorted_keys = sorted(self.cache_timestamps.keys(), key=lambda k: self.cache_timestamps[k])
            to_remove = sorted_keys[:len(self.response_cache) - self.CACHE_MAX_ENTRIES]
            for k in to_remove:
                self.response_cache.pop(k, None)
                self.cache_timestamps.pop(k, None)

    def _check_cache(self, key: str) -> str | None:
        """Check cache for existing response."""
        now = time.time()
        self._clean_cache(now)

        if key in self.response_cache:
            return self.response_cache[key]
        return None

    def _store_cache(self, key: str, response: str) -> None:
        """Store response in cache with timestamp."""
        now = time.time()
        self._clean_cache(now)
        self.response_cache[key] = response
        self.cache_timestamps[key] = now

    def _record_request(self) -> None:
        """Record request timestamp and increment counters."""
        now = time.time()
        self.request_timestamps.append(now)
        self.requests_today += 1
        self.last_request_time = now

    def _update_budget(self, response: str, user_message: str) -> None:
        """Update token and character counters."""
        self.total_tokens_used += self._estimate_tokens(user_message) + self._estimate_tokens(response)
        self.total_chars_input += len(user_message)

    def _show_error(self, msg: str):
        """Show error message in chat as assistant response."""
        self.messages.append({"role": "assistant", "content": f"⚠️ {msg}"})
        return rx.call_script("document.getElementById('chat-bottom-anchor')?.scrollIntoView({behavior: 'smooth'})")

    async def _stream_cached_response(self, response: str):
        """Stream a cached response with typing effect."""
        self.messages.append({"role": "assistant", "content": ""})
        yield

        typed = ""
        for char in response:
            typed += char
            self.messages[-1]["content"] = typed
            yield
            # Faster typing for cached responses
            await asyncio.sleep(0.005)

        self.is_streaming = False
        yield
        yield rx.call_script("document.getElementById('chat-bottom-anchor')?.scrollIntoView({behavior: 'smooth'})")

    # ─── Main Message Handler ────────────────────────────────────────────

    async def send_message(self):
        """Send user message, retrieve context, and stream assistant response."""
        user_message = self.current_input.strip()
        if not user_message or self.is_streaming:
            return

        # ─── Protection Checks (early return on failure) ───

        # Input validation
        ok, msg = self._check_input_valid(user_message)
        if not ok:
            yield self._show_error(msg)
            return

        # Rate limiting
        ok, msg = self._check_rate_limit()
        if not ok:
            yield self._show_error(msg)
            return

        # Debounce
        ok, msg = self._check_debounce()
        if not ok:
            yield self._show_error(msg)
            return

        # Budget check
        ok, msg = self._check_budget(user_message)
        if not ok:
            yield self._show_error(msg)
            return

        # Add user message immediately
        self.messages.append({"role": "user", "content": user_message})
        self.current_input = ""
        self.is_streaming = True
        yield

        # ─── Cache Check (before guardrail + RAG) ───
        cache_key = self._get_cache_key(user_message)
        cached = self._check_cache(cache_key)
        if cached:
            async for _ in self._stream_cached_response(cached):
                yield
            self._record_request()
            return

        # ─── GUARDRAIL: Check if question is Kruvx-related ───

        if not is_kruvx_related(user_message):
            # Off-topic response (no API call needed)
            self.messages.append({"role": "assistant", "content": ""})
            yield

            off_topic_msg = (
                "Lo siento, solo puedo ayudarte con preguntas relacionadas con Kruvx 😊. "
                "¿Tienes alguna duda sobre cómo funciona la app, los referidos, precios, "
                "o tu negocio en Kruvx?"
            )
            typed = ""
            for char in off_topic_msg:
                typed += char
                self.messages[-1]["content"] = typed
                yield
                await asyncio.sleep(0.015)

            self.is_streaming = False
            yield
            yield rx.call_script("document.getElementById('chat-bottom-anchor')?.scrollIntoView({behavior: 'smooth'})")
            self._record_request()
            return

        # ─── RAG: Retrieve relevant context (pre-initialized engine) ───
        rag_engine = get_rag_engine()
        context = rag_engine.get_context(user_message)

        # Build system prompt with context
        if context:
            system_prompt = SYSTEM_PROMPT_WITH_CONTEXT.format(context=context)
        else:
            system_prompt = SYSTEM_PROMPT_BASE + "\n\n(No se encontró información específica en la base de conocimiento para esta pregunta.)"

        # Prepare messages for API
        api_messages = [
            {"role": "system", "content": system_prompt},
            *self.messages,
        ]

        # Start assistant message placeholder
        self.messages.append({"role": "assistant", "content": ""})
        yield

        # Use pre-initialized module-level singleton client
        client = _get_client()
        model = _get_model()

        try:
            # Stream response from NVIDIA API
            stream = await client.chat.completions.create(
                model=model,
                messages=api_messages,
                stream=True,
                temperature=0.3,  # Lower temperature for factual RAG responses
                max_tokens=2048,
            )

            # Accumulate streaming response
            full_response = ""
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    self.messages[-1]["content"] = full_response
                    yield

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.messages[-1]["content"] = error_msg
            yield
            full_response = error_msg

        finally:
            self.is_streaming = False
            yield
            # Auto-scroll to bottom after message completes
            yield rx.call_script("document.getElementById('chat-bottom-anchor')?.scrollIntoView({behavior: 'smooth'})")

        # ─── Post-processing: record, budget, cache ───
        self._record_request()
        self._update_budget(full_response, user_message)
        if full_response and not full_response.startswith("Error:"):
            self._store_cache(cache_key, full_response)

    def clear_chat(self):
        """Clear all messages and reset protection state."""
        self.messages = []
        self.current_input = ""
        self.is_streaming = False
        self.welcome_shown = False
        # Reset protection state
        self.request_timestamps = []
        self.requests_today = 0
        self.last_reset_date = ""
        self.total_tokens_used = 0
        self.total_chars_input = 0
        self.last_request_time = 0.0
        self.response_cache = {}
        self.cache_timestamps = {}

    async def show_welcome_message(self):
        """Show welcome message with typing effect - no API call needed."""
        if self.welcome_shown:
            return

        welcome_text = "¡Hola! 👋 Soy Kruvi, y estoy aquí para ayudarte a entender cualquier duda respecto a Kruvx 😊. Puedes preguntarme lo que quieras ✨."

        # Add assistant message placeholder
        self.messages.append({"role": "assistant", "content": ""})
        self.welcome_shown = True
        yield

        # Simulate typing effect - character by character
        typed_text = ""
        for char in welcome_text:
            typed_text += char
            self.messages[-1]["content"] = typed_text
            yield
            await asyncio.sleep(0.03)

        # Auto-scroll to bottom after welcome message
        yield rx.call_script("document.getElementById('chat-bottom-anchor')?.scrollIntoView({behavior: 'smooth'})")