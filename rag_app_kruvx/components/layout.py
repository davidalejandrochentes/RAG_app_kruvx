"""Layout components: Navbar, Footer - matching base.html exactly."""

import reflex as rx
from typing import Callable, Optional


# ─── Navbar State ────────────────────────────────────────────────────────

class NavbarState(rx.State):
    """State for navbar interactions."""
    mobile_menu_open: bool = False
    pwa_banner_visible: bool = False
    user_authenticated: bool = False
    user_has_business: bool = False
    business_onboarding_completed: bool = False
    referrer_session_active: bool = False

    def toggle_mobile_menu(self):
        self.mobile_menu_open = not self.mobile_menu_open

    def close_mobile_menu(self):
        self.mobile_menu_open = False

    def dismiss_pwa_banner(self):
        self.pwa_banner_visible = False


# ─── Navbar - Component matching base.html EXACTLY ──────────────────────

def navbar() -> rx.Component:
    """Main navbar matching base.html exactly.

    Uses EXACT Tailwind classes from base.html (kruvx.cloud):
    - Desktop nav links: font-label-sm text-label-sm (14px, 600, -0.01em tracking)
    - Mobile nav links: font-label-md text-label-md (16px, 400, normal tracking)
    - Gap: space-lg (2.4rem = 38.4px) between desktop links
    - Gutters: px-gutter-mobile (1.6rem = 25.6px) / md:px-gutter-desktop (4rem = 64px)
    - Container: max-w-max-width-content (1440px)
    - Heights: h-16 (64px) mobile / md:h-[99px] desktop
    - Transitions: transition-colors + active:scale-[0.95] transition-transform
    - Active scale: exactly 0.95 (not 95)
    """
    return rx.el.header(
        # Top bar - exact classes from base.html line 50-51
        rx.el.div(
            # Logo - exact: flex items-center gap-2
            rx.link(
                rx.image(
                    src="/kruvx_logo.png",
                    alt="Kruvx Logo",
                    class_name="h-8 md:h-10 object-contain",
                ),
                href="https://kruvx.cloud/",
                class_name="flex items-center gap-2",
            ),

            # Desktop navigation - EXACT from base.html line 77-82
            # hidden md:flex gap-space-lg
            # Each link: font-label-sm text-label-sm text-on-surface-variant hover:text-luminous-accent
            # transition-colors active:scale-[0.95] transition-transform
            rx.el.nav(
                rx.el.a(
                    "Sobre Kruvx",
                    href="https://kruvx.cloud/sobre-kruvx/",
                    class_name="font-label-sm text-label-sm text-on-surface-variant hover:text-luminous-accent transition-colors active:scale-[0.95] transition-transform",
                ),
                rx.el.a(
                    "Cómo funciona",
                    href="https://kruvx.cloud/como-funciona/",
                    class_name="font-label-sm text-label-sm text-on-surface-variant hover:text-luminous-accent transition-colors active:scale-[0.95] transition-transform",
                ),
                rx.el.a(
                    "Precios",
                    href="https://kruvx.cloud/precios/",
                    class_name="font-label-sm text-label-sm text-on-surface-variant hover:text-luminous-accent transition-colors active:scale-[0.95] transition-transform",
                ),
                rx.el.a(
                    "Calculadora",
                    href="https://kruvx.cloud/calculadora-referidos/",
                    class_name="font-label-sm text-label-sm text-on-surface-variant hover:text-luminous-accent transition-colors active:scale-[0.95] transition-transform",
                ),
                rx.el.a(
                    "FAQ",
                    href="https://kruvx.cloud/preguntas-frecuentes/",
                    class_name="font-label-sm text-label-sm text-on-surface-variant hover:text-luminous-accent transition-colors active:scale-[0.95] transition-transform",
                ),
                rx.el.a(
                    "kruvi chat",
                    href="/",
                    class_name="font-label-sm text-label-sm text-on-surface-variant hover:text-luminous-accent transition-colors active:scale-[0.95] transition-transform",
                ),
                class_name="hidden md:flex gap-space-lg",
                aria_label="Navegación principal",
            ),

            # Right side actions - exact: flex items-center gap-space-md
            rx.el.div(
                # Desktop: conditional buttons - exact classes from base.html
                rx.el.div(
                    _navbar_right_actions_desktop(),
                    class_name="hidden sm:flex items-center gap-space-md",
                ),
                # Mobile menu toggle - exact classes from base.html line 115-122
                # Uses HTML button (not rx.button) to avoid Radix theming
                rx.el.button(
                    # Material Symbols Outlined "menu" icon - exact from base.html
                    rx.el.span(
                        "menu",
                        class_name="material-symbols-outlined",
                        style={"font_size": "26px"},
                    ),
                    on_click=NavbarState.toggle_mobile_menu,
                    class_name=(
                        "md:hidden h-12 w-12 flex items-center justify-center "
                        "text-on-surface-variant hover:text-luminous-accent "
                        "rounded-full transition-colors "
                        "active:scale-[0.95]"
                    ),
                    aria_label="Abrir menú de navegación",
                    aria_expanded=NavbarState.mobile_menu_open,
                    aria_controls="nav-mobile-menu",
                    id="nav-toggle",
                    type="button",
                ),
                class_name="flex items-center gap-space-md",
            ),

            # Inner container - EXACT match to base.html line 51
            # px-gutter-mobile md:px-gutter-desktop max-w-max-width-content mx-auto h-16 md:h-[99px]
            class_name="flex justify-between items-center w-full px-gutter-mobile md:px-gutter-desktop max-w-max-width-content mx-auto h-16 md:h-[99px]",
        ),

        # Mobile menu drawer - EXACT match base.html lines 126-144
        # Desktop: md:hidden hidden
        # Open: md:hidden border-t border-outline-variant/20 bg-surface-container-low
        rx.el.div(
            rx.el.div(
                rx.el.nav(
                    rx.el.a(
                        "Sobre Kruvx",
                        href="https://kruvx.cloud/sobre-kruvx/",
                        on_click=NavbarState.close_mobile_menu,
                        class_name="block font-label-md text-label-md text-on-surface-variant hover:text-luminous-accent py-3 transition-colors",
                    ),
                    rx.el.a(
                        "Cómo funciona",
                        href="https://kruvx.cloud/como-funciona/",
                        on_click=NavbarState.close_mobile_menu,
                        class_name="block font-label-md text-label-md text-on-surface-variant hover:text-luminous-accent py-3 transition-colors",
                    ),
                    rx.el.a(
                        "Precios",
                        href="https://kruvx.cloud/precios/",
                        on_click=NavbarState.close_mobile_menu,
                        class_name="block font-label-md text-label-md text-on-surface-variant hover:text-luminous-accent py-3 transition-colors",
                    ),
                    rx.el.a(
                        "Calculadora",
                        href="https://kruvx.cloud/calculadora-referidos/",
                        on_click=NavbarState.close_mobile_menu,
                        class_name="block font-label-md text-label-md text-on-surface-variant hover:text-luminous-accent py-3 transition-colors",
                    ),
                    rx.el.a(
                        "FAQ",
                        href="https://kruvx.cloud/preguntas-frecuentes/",
                        on_click=NavbarState.close_mobile_menu,
                        class_name="block font-label-md text-label-md text-on-surface-variant hover:text-luminous-accent py-3 transition-colors",
                    ),
                    rx.el.a(
                        "kruvi chat",
                        href="/",
                        on_click=NavbarState.close_mobile_menu,
                        class_name="block font-label-md text-label-md text-on-surface-variant hover:text-luminous-accent py-3 transition-colors",
                    ),
                    rx.el.div(
                        _navbar_right_actions_mobile(),
                        class_name="pt-2 mt-2 border-t border-outline-variant/20",
                    ),
                    class_name="px-gutter-mobile py-2 space-y-1",  # px-gutter-mobile = 1.6rem
                    aria_label="Navegación mobile",
                ),
                class_name="md:hidden",
                id="nav-mobile-menu",
            ),
            class_name=rx.cond(
                NavbarState.mobile_menu_open,
                "md:hidden border-t border-outline-variant/20 bg-surface-container-low",
                "hidden",
            ),
        ),

        # PWA Install Banner
        _pwa_install_banner(),

        # Header classes - exact from base.html line 50
        class_name=(
            "bg-surface-container-low sticky top-0 z-50 "
            "border-b border-outline-variant/20 "
            "shadow-nav"
        ),
    )


def _navbar_right_actions_desktop() -> rx.Component:
    """Right side actions for desktop - EXACT button classes from base.html.

    Desktop CTA (lines 88-103 in base.html):
    - h-12 px-4 sm:px-6 bg-luminous-accent text-white
    - font-label-sm text-label-sm (14px, 600, -0.01em)
    - rounded-pill btn-interactive flex items-center justify-center gap-2
    - transition-all duration-200 hover:bg-primary-container active:scale-[0.95]

    Referrer link (line 109 in base.html):
    - h-12 px-4 sm:px-5 border border-outline-variant bg-surface-container-low
    - text-on-surface-variant font-label-sm text-label-sm (14px, 600)
    - font-medium tracking-tight rounded-pill btn-interactive
    - transition-all duration-200 hover:bg-surface-container hover:text-luminous-accent active:scale-[0.95]
    """
    return rx.fragment(
        # Always show "Tengo un negocio" as the primary CTA
        rx.link(
            rx.button(
                # Material Symbols Outlined "store" icon (FILL 1) - exact from base.html
                rx.el.span(
                    "store",
                    class_name="material-symbols-outlined",
                    style={"font_variation_settings": "'FILL' 1", "font_size": "18px"},
                ),
                rx.el.span("Tengo un negocio", class_name="hidden sm:inline"),
                on_click=rx.redirect("https://kruvx.cloud/dashboard/"),
                class_name=(
                    "h-12 px-4 sm:px-6 bg-luminous-accent text-white "
                    "font-label-sm text-label-sm "
                    "rounded-pill btn-interactive flex items-center justify-center gap-2 "
                    "transition-all duration-200 hover:bg-primary-container active:scale-[0.95] w-full"
                ),
                style={"color": "white"},
                type="button",
            ),
            href="https://kruvx.cloud/dashboard/",
            class_name="w-auto no-underline hover:no-underline",
            style={"textDecoration": "none"},
            aria_label="Tengo un negocio",
            title="Tengo un negocio",
        ),
        # Show referrer code link if in referrer session
        rx.cond(
            NavbarState.referrer_session_active,
            rx.link(
                # Material Symbols Outlined "confirmation_number" icon (FILL 0) - exact from base.html
                rx.el.span(
                    "confirmation_number",
                    class_name="material-symbols-outlined",
                    style={"font_variation_settings": "'FILL' 0", "font_size": "18px"},
                ),
                rx.el.span("Mi código de referente", class_name="hidden sm:inline"),
                href="/referidos/mi-codigo",
                class_name=(
                    "h-12 px-4 sm:px-5 border border-outline-variant bg-surface-container-low "
                    "text-on-surface-variant font-label-sm text-label-sm font-medium tracking-tight "
                    "rounded-pill btn-interactive flex items-center justify-center gap-2 "
                    "transition-all duration-200 hover:bg-surface-container hover:text-luminous-accent hover:no-underline "
                    "active:scale-[0.95]"
                ),
                aria_label="Mi código de referente",
                title="Mi código de referente",
            ),
        ),
    )


def _navbar_right_actions_mobile() -> rx.Component:
    """Right side actions for mobile menu - EXACT styles from base.html (lines 136-158).

    Mobile action links (base.html lines 136, 141, 148, 156):
    - flex items-center gap-2
    - font-label-md text-label-md (16px, 400, normal tracking)
    - text-on-surface-variant hover:text-luminous-accent
    - py-3 transition-colors
    - Icon size: 22px via style attribute
    """
    mobile_action_class = (
        "flex items-center gap-2 "
        "font-label-md text-label-md "
        "text-on-surface-variant hover:text-luminous-accent "
        "py-3 transition-colors"
    )

    # Always show "Tengo un negocio" as the primary action in mobile menu
    primary_action = rx.el.a(
        rx.el.span(
            "store",
            class_name="material-symbols-outlined",
            style={"font_variation_settings": "'FILL' 1", "font_size": "22px"},
        ),
        "Tengo un negocio",
        href="https://kruvx.cloud/dashboard/",
        on_click=NavbarState.close_mobile_menu,
        class_name=mobile_action_class,
    )

    return rx.fragment(
        primary_action,
        rx.cond(
            NavbarState.referrer_session_active,
            rx.el.a(
                rx.el.span(
                    "confirmation_number",
                    class_name="material-symbols-outlined",
                    style={"font_variation_settings": "'FILL' 0", "font_size": "22px"},
                ),
                "Mi código de referente",
                href="/referidos/mi-codigo",
                on_click=NavbarState.close_mobile_menu,
                class_name=mobile_action_class,
            ),
        ),
        # Dashboard and profile links for authenticated users (secondary in mobile menu)
        rx.cond(
            NavbarState.user_authenticated & NavbarState.user_has_business & NavbarState.business_onboarding_completed,
            rx.el.a(
                rx.el.span(
                    "dashboard",
                    class_name="material-symbols-outlined",
                    style={"font_variation_settings": "'FILL' 1", "font_size": "22px"},
                ),
                "Ir al dashboard",
                href="https://kruvx.cloud/dashboard/",
                on_click=NavbarState.close_mobile_menu,
                class_name=mobile_action_class,
            ),
        ),
        rx.cond(
            NavbarState.user_authenticated & NavbarState.user_has_business & ~NavbarState.business_onboarding_completed,
            rx.el.a(
                rx.el.span(
                    "edit_note",
                    class_name="material-symbols-outlined",
                    style={"font_variation_settings": "'FILL' 1", "font_size": "22px"},
                ),
                "Completar perfil",
                href="/onboarding",
                on_click=NavbarState.close_mobile_menu,
                class_name=mobile_action_class,
            ),
        ),
    )


def _pwa_install_banner() -> rx.Component:
    """PWA install banner matching base.html with green-accent colors."""
    return rx.box(
        # Material Symbols Outlined "install_mobile" icon
        rx.el.span(
            "install_mobile",
            class_name="material-symbols-outlined text-luminous-accent",
            style={"font_size": "28px"},
        ),
        rx.el.div(
            rx.text("Instala Kruvx", class_name="font-label text-label-md font-semibold tracking-tight text-on-surface"),
            rx.text("Acceso directo desde tu pantalla de inicio", class_name="text-sm text-on-surface-variant"),
            class_name="flex-1",
        ),
        rx.button("Instalar", class_name="px-4 py-2 bg-luminous-accent text-white font-label text-label-sm font-semibold tracking-tight rounded-full btn-interactive", on_click=rx.window_alert("PWA install prompt")),
        rx.button("×", on_click=NavbarState.dismiss_pwa_banner, class_name="p-1 text-on-surface-variant hover:text-on-surface rounded-full transition-colors duration-150 active:scale-[0.95]", aria_label="Cerrar"),
        class_name=rx.cond(
            NavbarState.pwa_banner_visible,
            "fixed bottom-4 left-1/2 -translate-x-1/2 z-[60] w-[calc(100%-2rem)] max-w-md bg-surface-container-high border border-outline-variant rounded-2xl shadow-lg p-4 flex items-center gap-3 transition-colors duration-200",
            "fixed bottom-4 left-1/2 -translate-x-1/2 z-[60] w-[calc(100%-2rem)] max-w-md bg-surface-container-high border border-outline-variant rounded-2xl shadow-lg p-4 flex items-center gap-3 opacity-0 pointer-events-none translate-y-4 transition-colors duration-200",
        ),
        id="pwa-install-banner",
    )


# ─── Footer - Component matching base.html exactly ─────────────────────

def footer() -> rx.Component:
    """Footer matching base.html exactly.

    Uses Tailwind arbitrary values to match base.html custom spacing EXACTLY:
    - px-gutter-desktop (4rem = 64px)
    - max-w-max-width-content (1440px)
    - gap-space-md (1rem = 16px) → gap-4
    """
    return rx.el.footer(
        # Inner div - exact: max-w-max-width-content mx-auto py-16
        rx.el.div(
            # Grid - exact: grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-12
            rx.el.div(
                # Col 1: Marca
                rx.el.div(
                    rx.image(src="/kruvx_logo.png", alt="Kruvx Logo", class_name="h-8 object-contain mb-4"),
                    rx.el.p("2026 Kruvx", class_name="font-body-md text-body-md text-soft-mint/70"),
                ),
                # Col 2: Producto
                rx.el.div(
                    rx.el.h3("Producto", class_name="font-label-sm text-label-sm text-soft-mint/60 uppercase tracking-[0.1em] mb-4"),
                    rx.el.ul(
                        rx.el.li(_footer_link("Cómo funciona", "https://kruvx.cloud/como-funciona/")),
                        rx.el.li(_footer_link("Precios", "https://kruvx.cloud/precios/")),
                        rx.el.li(_footer_link("Preguntas frecuentes", "https://kruvx.cloud/preguntas-frecuentes/")),
                        rx.el.li(_footer_link("Sobre Kruvx", "https://kruvx.cloud/sobre-kruvx/")),
                        rx.el.li(_footer_link("kruvi chat", "/")),
                        class_name="space-y-3",
                    ),
                ),
                # Col 3: Soporte
                rx.el.div(
                    rx.el.h3("Soporte", class_name="font-label-sm text-label-sm text-soft-mint/60 uppercase tracking-[0.1em] mb-4"),
                    rx.el.ul(
                        rx.el.li(_footer_link("support@kruvx.cloud", "mailto:support@kruvx.cloud")),
                        rx.el.li(_footer_link("WhatsApp", "https://wa.me/+5354214040", is_external=True)),
                        class_name="space-y-3",
                    ),
                ),
                # Col 4: Para referentes
                rx.el.div(
                    rx.el.h3("Para referentes", class_name="font-label-sm text-label-sm text-soft-mint/60 uppercase tracking-[0.1em] mb-4"),
                    rx.el.ul(
                        rx.el.li(_footer_link("Recuperar mis códigos", "/referidos/recuperar")),
                        class_name="space-y-3",
                    ),
                ),
                # Col 5: Legal
                rx.el.div(
                    rx.el.h3("Legal", class_name="font-label-sm text-label-sm text-soft-mint/60 uppercase tracking-[0.1em] mb-4"),
                    rx.el.ul(
                        rx.el.li(_footer_link("Términos de uso", "/terminos")),
                        rx.el.li(_footer_link("Política de privacidad", "/privacidad")),
                        class_name="space-y-3",
                    ),
                ),
                # Col 6: Comunidad
                rx.el.div(
                    rx.el.h3("Comunidad", class_name="font-label-sm text-label-sm text-soft-mint/60 uppercase tracking-[0.1em] mb-4"),
                    rx.el.div(
                        rx.link(_instagram_icon(), href="#", aria_label="Instagram de kruvx", class_name="w-10 h-10 rounded-full bg-white/10 hover:bg-white hover:text-luminous-accent flex items-center justify-center text-white transition-colors active:scale-[0.95]"),
                        rx.link(_youtube_icon(), href="https://www.youtube.com/@kruvx-oficial", aria_label="YouTube de kruvx", is_external=True, class_name="w-10 h-10 rounded-full bg-white/10 hover:bg-white hover:text-luminous-accent flex items-center justify-center text-white transition-colors active:scale-[0.95]"),
                        class_name="flex items-center gap-4",
                    ),
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-12",
            ),
            class_name="max-w-max-width-content mx-auto py-16",  # max-w-max-width-content = 1440px
        ),
        # Footer classes - exact from base.html line 219
        # px-gutter-desktop = 4rem
        class_name="bg-[#152823] w-full px-gutter-desktop border-t border-white/10",
    )


def _footer_link(text: str, href: str, is_external: bool = False, **props) -> rx.Component:
    return rx.link(text, href=href, is_external=is_external, class_name="font-label-sm text-label-sm text-soft-mint/80 hover:text-white transition-colors duration-200", **props)


def _instagram_icon() -> rx.Component:
    return rx.el.svg(rx.el.path(d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"), viewBox="0 0 24 24", width="20", height="20", fill="currentColor", aria_hidden="true")


def _youtube_icon() -> rx.Component:
    return rx.el.svg(rx.el.path(d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"), viewBox="0 0 24 24", width="20", height="20", fill="currentColor", aria_hidden="true")


# ─── Main Layout Wrapper ────────────────────────────────────────────────

def layout(content: rx.Component) -> rx.Component:
    """Main layout wrapper - exact match to base.html structure.

    base.html body: class="font-body-md text-text-primary antialiased bg-neutral-warm"
    We use font-body (Manrope) with tracking-tight via fontSize config.
    """
    return rx.box(
        navbar(),
        rx.el.main(content),  # No extra classes - exact match to base.html <main>
        footer(),
        class_name="min-h-screen bg-neutral-warm font-body antialiased tracking-tight",
    )


def layout_no_footer(content: rx.Component) -> rx.Component:
    """Layout wrapper without footer - for full-screen chat."""
    return rx.box(
        navbar(),
        rx.el.main(content),
        class_name="min-h-screen bg-neutral-warm font-body antialiased tracking-tight",
    )


def page_layout(
    content: rx.Component,
    title: str = "Kruvx",
    description: str = "Tu boca a boca, ahora recompensado",
) -> rx.Component:
    return rx.fragment(
        rx.el.title(title),
        rx.el.meta(name="description", content=description),
        rx.el.meta(property="og:title", content=title),
        rx.el.meta(property="og:description", content=description),
        rx.el.meta(property="og:type", content="website"),
        rx.el.meta(name="twitter:card", content="summary_large_image"),
        rx.el.meta(name="twitter:title", content=title),
        rx.el.meta(name="twitter:description", content=description),
        rx.el.link(rel="icon", href="/icon-192.png", type="image/png"),
        rx.el.link(rel="apple-touch-icon", href="/icon-192.png"),
        rx.el.link(rel="manifest", href="/site.webmanifest"),
        layout(content),
    )


def page_layout_no_footer(
    content: rx.Component,
    title: str = "Kruvx",
    description: str = "Tu boca a boca, ahora recompensado",
) -> rx.Component:
    """Page layout without footer."""
    return rx.fragment(
        rx.el.title(title),
        rx.el.meta(name="description", content=description),
        rx.el.meta(property="og:title", content=title),
        rx.el.meta(property="og:description", content=description),
        rx.el.meta(property="og:type", content="website"),
        rx.el.meta(name="twitter:card", content="summary_large_image"),
        rx.el.meta(name="twitter:title", content=title),
        rx.el.meta(name="twitter:description", content=description),
        rx.el.link(rel="icon", href="/icon-192.png", type="image/png"),
        rx.el.link(rel="apple-touch-icon", href="/icon-192.png"),
        rx.el.link(rel="manifest", href="/site.webmanifest"),
        layout_no_footer(content),
    )