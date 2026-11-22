"""Chat components following Kruvx Design System."""

import reflex as rx
from typing import Optional
from ..state import ChatState


# ─── Message Bubble ────────────────────────────────────────────────────────

def message_bubble(message: dict[str, str]) -> rx.Component:
    """Single message bubble - user or assistant."""
    is_user = message["role"] == "user"
    content = message["content"]

    # Avatar component
    avatar = rx.cond(
        is_user,
        rx.el.div(
            rx.icon("user", size=20, color="white"),
            class_name="w-8 h-8 rounded-pill bg-green-accent flex items-center justify-center flex-shrink-0",
        ),
        rx.el.div(
            rx.icon("bot", size=20, color="white"),
            class_name="w-8 h-8 rounded-pill bg-starbucks-green flex items-center justify-center flex-shrink-0",
        ),
    )

    # Message content
    msg_content = rx.el.div(
        rx.markdown(
            content,
            class_name=rx.cond(
                is_user,
                "prose prose-sm max-w-none text-white font-body text-text-3",
                "prose prose-sm max-w-none text-on-surface font-body text-text-3",
            ),
        ),
        class_name=rx.cond(
            is_user,
            "bg-green-accent text-white rounded-2xl rounded-tr-sm px-4 py-3 max-w-[75%] shadow-card",
            "bg-white text-on-surface rounded-2xl rounded-tl-sm px-4 py-3 max-w-[75%] shadow-card border border-outline-variant/20",
        ),
    )

    return rx.el.div(
        # For user: content first, then avatar (right side)
        # For assistant: avatar first, then content (left side)
        rx.cond(
            is_user,
            rx.fragment(msg_content, avatar),
            rx.fragment(avatar, msg_content),
        ),
        class_name=rx.cond(
            is_user,
            "flex items-end gap-2 justify-end",
            "flex items-end gap-2 justify-start",
        ),
    )


# ─── Chat Messages Container ────────────────────────────────────────────────

def chat_messages() -> rx.Component:
    """Scrollable container with all messages."""
    return rx.el.div(
        rx.foreach(
            ChatState.messages,
            lambda msg: message_bubble(msg),
        ),
        # Auto-scroll anchor
        rx.el.div(id="chat-bottom-anchor"),
        class_name=(
            "flex flex-col gap-4 "
            "overflow-y-auto "
            "pb-32 pt-4 "  # pb-32 = 128px padding for fixed input (covers expanded textarea); pt-4 from navbar
            "scroll-smooth"
        ),
        id="chat-messages",
    )


# ─── Chat Input ─────────────────────────────────────────────────────────────

def chat_input() -> rx.Component:
    """Floating input bar with send button."""
    return rx.el.div(
        rx.el.form(
            rx.el.div(
                # Textarea with floating label style
                rx.el.textarea(
                    placeholder="Escribe tu mensaje...",
                    value=ChatState.current_input,
                    on_change=ChatState.set_input,
                    class_name=(
                        "w-full min-h-[56px] max-h-48 "
                        "bg-white border border-outline-variant/50 "
                        "rounded-xl px-4 py-3 "
                        "text-on-surface placeholder:text-on-surface-variant/60 "
                        "font-body text-text-3 "
                        "focus:outline-none focus:border-green-accent focus:ring-2 focus:ring-green-accent/20 "
                        "resize-none "
                        "transition-all duration-200"
                    ),
                    style={"lineHeight": "1.5"},
                    id="chat-input",
                    disabled=ChatState.is_streaming,
                    aria_label="Mensaje para el asistente",
                ),
                # Send button
                rx.button(
                    rx.cond(
                        ChatState.is_streaming,
                        rx.icon("loader", size=20, class_name="animate-spin"),
                        rx.icon("send", size=20),
                    ),
                    type_="submit",
                    disabled=rx.cond(
                        ChatState.is_streaming | (ChatState.current_input.strip() == ""),
                        True,
                        False,
                    ),
                    class_name=(
                        "ml-3 flex-shrink-0 w-12 h-12 rounded-pill "
                        "bg-green-accent text-white "
                        "hover:bg-starbucks-green "
                        "disabled:opacity-50 disabled:cursor-not-allowed "
                        "transition-all duration-200 "
                        "active:scale-[0.95] "
                        "shadow-frap"
                    ),
                    aria_label="Enviar mensaje",
                ),
                class_name="flex items-end gap-2",
            ),
            on_submit=ChatState.send_message,
            class_name="w-full",
        ),
        class_name=(
            "fixed bottom-0 left-0 right-0 "
            "px-[1.6rem] md:px-[4rem] max-w-[1440px] mx-auto "
            "pb-6 pt-4 "
            "bg-gradient-to-t from-neutral-warm to-transparent "
            "z-10"
        ),
    )


# ─── Chat Container ─────────────────────────────────────────────────────────

def chat_container() -> rx.Component:
    """Main chat interface container - full screen, no header."""
    return rx.box(
        # Messages area
        chat_messages(),
        # Input area (fixed at bottom)
        chat_input(),
        class_name=(
            "flex flex-col "
            "h-[calc(100vh-99px)] "  # 99px = navbar height
            "bg-neutral-warm "
            "px-[1.6rem] md:px-[4rem] max-w-[1440px] mx-auto w-full "
            "relative"
        ),
    )


# ─── Clear Chat Button (optional) ──────────────────────────────────────────

def clear_chat_button() -> rx.Component:
    """Button to clear chat history."""
    return rx.button(
        rx.hstack(
            rx.icon("trash-2", size=16),
            rx.text("Limpiar chat", class_name="hidden sm:inline"),
            spacing="2",
        ),
        on_click=ChatState.clear_chat,
        class_name=(
            "fixed bottom-24 right-6 z-40 "
            "h-12 px-4 rounded-pill "
            "bg-surface-container-high text-on-surface-variant "
            "border border-outline-variant "
            "hover:bg-surface-container-highest hover:text-green-accent "
            "font-label text-label-sm font-semibold tracking-tight "
            "shadow-card transition-all duration-200 "
            "active:scale-[0.95]"
        ),
        aria_label="Limpiar historial de chat",
    )