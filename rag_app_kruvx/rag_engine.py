"""RAG Engine for Kruvx - TF-IDF + Cosine Similarity (lightweight, no ML deps).

Zero heavy ML dependencies. Uses scikit-learn TF-IDF for semantic retrieval.
Perfect for single-document RAG with consistent terminology.

Eager initialization at module import time to avoid blocking the event loop
on first request.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple
import markdown
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ─── Configuration ────────────────────────────────────────────────────────

CHUNK_SIZE = 500        # target chars per chunk
CHUNK_OVERLAP = 50      # overlap between chunks
TOP_K = 3               # chunks to retrieve
MIN_SIMILARITY = 0.02   # minimum cosine similarity threshold (lower = more recall for natural language)
DOC_PATH = Path(__file__).parent.parent / "assets" / "kruvx-guia-usuario.md"

# Kruvx domain keywords for guardrail
KRUVX_KEYWORDS = {
    "kruvx", "kruvi", "referido", "referidos", "código", "codigo", "recompensa",
    "negocio", "onboarding", "dashboard", "precio", "calculadora", "faq",
    "soporte", "whatsapp", "términos", "terminos", "privacidad", "comunidad",
    "boca a boca", "recomendación", "recomendacion", "cliente", "usuario",
    "registro", "login", "autenticación", "autenticacion", "perfil", "empresa",
    "comercio", "tienda", "local", "físico", "fisico", "online", "digital",
    "marketing", "campaña", "campana", "conversión", "conversion", "venta",
    "promoción", "promocion", "descuento", "beneficio", "ventaja", "plan",
    "suscripción", "suscripcion", "pago", "factura", "impuesto", "legal",
    "condiciones", "política", "politica", "dato", "protección", "proteccion",
    "kruvx.cloud", "support@kruvx.cloud", "nvidia", "nemotron", "asistente",
    "chat", "ayuda", "duda", "pregunta", "respuesta", "información", "informacion",
    "guía", "guia", "manual", "tutorial", "cómo", "como", "qué", "que",
    "cuál", "cual", "cuándo", "cuando", "dónde", "donde", "por qué", "porque",
    "magic link", "sesión", "sesion", "recuperar", "marketplace", "slug",
    "categoría", "categoria", "ciudad", "reseña", "resena", "disputa",
    "reputación", "reputacion", "eliminación", "eliminacion", "anonimización",
    "anonimizacion", "rate limit", "desechable", "debounce", "expiración",
    "expiracion", "qr", "pdf", "email", "teléfono", "telefono", "beneficio referido",
    "recompensa referente", "anti-abuso", "antiabuso", "nowpayments", "turnstile",
    "validación", "validacion", "reclamo", "meta", "tramo", "gratis", "pago",
    "corta duración", "corta duracion", "larga duración", "larga duracion",
    "prueba gratuita", "campaña", "campana", "referente", "referido"
}

NON_KRUVX_KEYWORDS = {
    "fútbol", "futbol", "futbol", "deporte", "deportes", "liga", "champions",
    "mundial", "copa", "equipo", "jugador", "gol", "partido", "entrenador",
    "política", "politica", "político", "politico", "gobierno", "presidente",
    "elecciones", "votar", "partido político", "congreso", "senado",
    "religión", "religion", "dios", "iglesia", "bíblia", "biblia", "cristo",
    "ciencia", "física", "fisica", "química", "quimica", "biología", "biologia",
    "matemáticas", "matematicas", "álgebra", "algebra", "cálculo", "calculo",
    "programación", "programacion", "python", "javascript", "java", "c++",
    "react", "vue", "angular", "docker", "kubernetes", "aws", "azure", "gcp",
    "receta", "cocina", "comida", "restaurante", "ingrediente", "horno",
    "película", "pelicula", "cine", "serie", "netflix", "actor", "director",
    "música", "musica", "canción", "cancion", "artista", "concierto", "spotify",
    "viaje", "turismo", "hotel", "vuelo", "avión", "avion", "playa", "montaña",
    "salud", "médico", "medico", "hospital", "enfermedad", "medicina", "farmacia",
    "finanzas", "bolsa", "acción", "accion", "cripto", "bitcoin", "ethereum",
    "inversión", "inversion", "banco", "préstamo", "prestamo", "hipoteca"
}


# ─── Document Processing ──────────────────────────────────────────────────

def load_markdown_document(path: Path) -> str:
    """Load and return raw markdown text."""
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")
    return path.read_text(encoding="utf-8")


def chunk_markdown_by_headers(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split markdown by headers (# ## ###) preserving semantic structure."""
    header_pattern = r'^(#{1,3}\s+.+)$'
    lines = text.split('\n')
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for line in lines:
        line_stripped = line.strip()
        is_header = bool(re.match(header_pattern, line_stripped, re.MULTILINE))
        
        if is_header and current_chunk and current_length > 100:
            chunk_text = '\n'.join(current_chunk).strip()
            if chunk_text:
                chunks.append(chunk_text)
            overlap_lines = current_chunk[-3:] if len(current_chunk) > 3 else current_chunk
            current_chunk = overlap_lines + [line]
            current_length = sum(len(l) for l in current_chunk)
        else:
            current_chunk.append(line)
            current_length += len(line)
            
            if current_length > chunk_size * 2:
                chunk_text = '\n'.join(current_chunk).strip()
                if chunk_text:
                    chunks.append(chunk_text)
                current_chunk = []
                current_length = 0
    
    if current_chunk:
        chunk_text = '\n'.join(current_chunk).strip()
        if chunk_text:
            chunks.append(chunk_text)
    
    # Post-process: merge too-small chunks
    merged_chunks = []
    buffer = ""
    for chunk in chunks:
        buffer += "\n\n" + chunk if buffer else chunk
        if len(buffer) >= chunk_size * 0.5:
            merged_chunks.append(buffer.strip())
            buffer = ""
    if buffer:
        merged_chunks.append(buffer.strip())
    
    return merged_chunks


# ─── TF-IDF Vector Store ──────────────────────────────────────────────────

class RAGEngine:
    """RAG Engine with TF-IDF vectorization and cosine similarity."""
    
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.chunks = []
    
    def initialize(self) -> None:
        """Load document, create TF-IDF vectors."""
        print("🔄 Inicializando RAG Engine (TF-IDF)...")
        
        # 1. Load and chunk document
        raw_text = load_markdown_document(DOC_PATH)
        self.chunks = chunk_markdown_by_headers(raw_text)
        print(f"📄 Documento cargado: {len(self.chunks)} chunks")
        
        # 2. Create TF-IDF vectorizer
        # - ngram_range=(1, 2): unigrams + bigrams for phrase matching
        # - min_df=1: keep all terms (small doc)
        # - max_df=0.95: ignore terms in >95% of chunks
        # - sublinear_tf: log scaling for term frequency
        print("🔤 Construyendo vocabulario TF-IDF...")
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            lowercase=True,
            strip_accents='unicode',
            analyzer='word',
        )
        
        # 3. Fit and transform chunks
        print("📊 Vectorizando chunks...")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)
        
        vocab_size = len(self.vectorizer.vocabulary_)
        print(f"✅ RAG Engine listo: {self.tfidf_matrix.shape[0]} chunks, {vocab_size} términos en vocabulario")
    
    def retrieve(self, query: str, top_k: int = TOP_K) -> List[Tuple[str, float]]:
        """Retrieve top-k relevant chunks for query using cosine similarity."""
        # Transform query using fitted vectorizer
        query_vec = self.vectorizer.transform([query])
        
        # Compute cosine similarities
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= MIN_SIMILARITY and idx < len(self.chunks):
                results.append((self.chunks[idx], score))
        
        return results
    
    def get_context(self, query: str) -> str:
        """Get formatted context string for prompt injection."""
        results = self.retrieve(query)
        if not results:
            return ""
        
        context_parts = []
        for i, (chunk, score) in enumerate(results, 1):
            context_parts.append(f"[Fuente {i} - Relevancia: {score:.2f}]\n{chunk}")
        
        return "\n\n---\n\n".join(context_parts)


# ─── Eager Initialization (at module import time) ────────────────────────

_rag_engine: RAGEngine


def _init_rag_engine() -> RAGEngine:
    """Initialize the RAG engine at module load (app startup)."""
    engine = RAGEngine()
    engine.initialize()
    return engine


# This runs ONCE when module is imported (during app startup)
# NOT during first request - avoids blocking the event loop
_rag_engine = _init_rag_engine()


# ─── Guardrail ────────────────────────────────────────────────────────────

def is_kruvx_related(query: str) -> bool:
    """Check if query is related to Kruvx domain using keyword matching."""
    query_lower = query.lower()
    
    has_kruvx = any(kw in query_lower for kw in KRUVX_KEYWORDS)
    has_non_kruvx = any(kw in query_lower for kw in NON_KRUVX_KEYWORDS)
    
    if has_non_kruvx and not has_kruvx:
        return False
    
    if has_kruvx:
        return True
    
    word_count = len(query_lower.split())
    if word_count <= 8:
        return True
    
    return False


# ─── Public API ───────────────────────────────────────────────────────────

def get_rag_engine() -> RAGEngine:
    """Get the pre-initialized RAG engine instance (singleton)."""
    return _rag_engine