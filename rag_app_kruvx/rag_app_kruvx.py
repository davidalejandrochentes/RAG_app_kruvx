"""Kruvx - Tu boca a boca, ahora recompensado.

Reflex app with Kruvx design system (navbar, footer, UI components).
"""

import reflex as rx
from rxconfig import config

from .state import ChatState
from .components.layout import page_layout_no_footer
from .components.chat import chat_container


# ─── Pages ──────────────────────────────────────────────────────────────

def index() -> rx.Component:
    """Home page - Full-screen chat interface with navbar only."""
    return page_layout_no_footer(
        rx.box(
            chat_container(),
            on_mount=ChatState.show_welcome_message,
        ),
        title="Kruvx — Chat con Asistente IA",
        description="Chatea con el asistente de Kruvx potenciado por NVIDIA Nemotron",
    )


# ─── App ────────────────────────────────────────────────────────────────

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap",
        "https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Literata:opsz,wght@7..72,500&display=swap",
        "/styles.css",
    ],
)
app.add_page(index, route="/", title="Kruvx — Chat con Asistente IA")