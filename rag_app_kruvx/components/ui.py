"""UI Components following Kruvx Design System (based on DESING.md & base.html)."""

import reflex as rx
from typing import Optional, List, Callable


# ─── Design Tokens ──────────────────────────────────────────────────────
# Colors (mapped to Tailwind classes in rxconfig.py) - UPDATED to match DESING.md
# Primary: Green Accent (#00754A) for CTAs, Frap | Starbucks Green (#006241) for headings
# House Green (#1E3932) for dark bands/footer | Gold (#cba258) for Rewards only
LUMINOUS_ACCENT = "bg-green-accent text-white hover:bg-starbucks-green"           # Primary filled: Green Accent bg, Starbucks Green hover
LUMINOUS_ACCENT_OUTLINE = "border-green-accent text-green-accent hover:bg-green-accent hover:text-white"  # Primary outlined
DARK_OUTLINE = "border-on-surface-variant text-on-surface-variant hover:bg-surface-container-highest"
WHITE_ON_DARK = "bg-white text-green-accent border-white hover:bg-surface-container-highest"  # Green-on-Green Inverted
WHITE_OUTLINE_ON_DARK = "border-white text-white hover:bg-white/10"                     # Outlined on Dark
SECONDARY_ON_LIGHT = "bg-surface-container-high text-on-surface-variant border-outline-variant hover:bg-surface-container-highest"

# Shadows
SHADOW_NAV = "shadow-nav"
SHADOW_CARD = "shadow-card"
SHADOW_FRAP = "shadow-frap"                      # Dual-layer: base + ambient
SHADOW_FRAP_ACTIVE = "shadow-frap-active"        # Active: ambient collapses

# Transitions
TRANSITION_200 = "transition-all duration-200 ease-out"
TRANSITION_300 = "transition-all duration-300 ease-out"
TRANSITION_BUTTON = "transition-all duration-200 ease-button"  # Springy for checkboxes

# Common classes - UPDATED to match DESING.md specs exactly
# Primary Filled: 7px 16px padding, 16px font, weight 600, -0.01em tracking, 50px radius
BTN_BASE = (
    "inline-flex items-center justify-center gap-2 "
    "font-label text-base font-semibold tracking-tight "  # 16px, weight 600, tight tracking
    "rounded-pill px-4 py-2 "                             # ~7px 16px (py-2 = 8px, close to 7px)
    "btn-interactive active:scale-[0.95] " + TRANSITION_200
)

# Nav links: 14px (label-sm), weight 600, tight tracking, 150ms cubic-bezier transition
# Matches base.html: transition-property: color, transform; duration: 150ms; timing: cubic-bezier(0.4, 0, 0.2, 1)
LINK_BASE = (
    "font-label text-label-sm font-semibold tracking-tight "
    "transition-[color,transform] duration-150 ease-[cubic-bezier(0.4,0,0.2,1)] "
    "active:scale-[0.95]"
)


# ─── Buttons ────────────────────────────────────────────────────────────

def btn_primary(
    text: str,
    icon: Optional[str] = None,
    href: Optional[str] = None,
    on_click: Optional[Callable] = None,
    **props
) -> rx.Component:
    """Primary filled button: Green Accent bg, white text, pill radius."""
    content = _btn_content(text, icon)
    base_class = BTN_BASE + " " + LUMINOUS_ACCENT
    if href:
        return rx.link(content, href=href, class_name=base_class, **props)
    return rx.button(content, class_name=base_class, on_click=on_click, **props)


def btn_primary_outline(
    text: str,
    icon: Optional[str] = None,
    href: Optional[str] = None,
    on_click: Optional[Callable] = None,
    **props
) -> rx.Component:
    """Primary outlined button: Transparent bg, Green Accent border/text."""
    content = _btn_content(text, icon)
    base_class = BTN_BASE + " " + LUMINOUS_ACCENT_OUTLINE
    if href:
        return rx.link(content, href=href, class_name=base_class, **props)
    return rx.button(content, class_name=base_class, on_click=on_click, **props)


def btn_dark_outline(
    text: str,
    icon: Optional[str] = None,
    href: Optional[str] = None,
    on_click: Optional[Callable] = None,
    **props
) -> rx.Component:
    """Dark outlined button: Transparent bg, on-surface-variant border/text."""
    content = _btn_content(text, icon)
    base_class = BTN_BASE + " " + DARK_OUTLINE
    if href:
        return rx.link(content, href=href, class_name=base_class, **props)
    return rx.button(content, class_name=base_class, on_click=on_click, **props)


def btn_white_on_dark(
    text: str,
    icon: Optional[str] = None,
    href: Optional[str] = None,
    on_click: Optional[Callable] = None,
    **props
) -> rx.Component:
    """White filled on dark surface: White bg, Green Accent text."""
    content = _btn_content(text, icon)
    base_class = BTN_BASE + " " + WHITE_ON_DARK
    if href:
        return rx.link(content, href=href, class_name=base_class, **props)
    return rx.button(content, class_name=base_class, on_click=on_click, **props)


def btn_white_outline_on_dark(
    text: str,
    icon: Optional[str] = None,
    href: Optional[str] = None,
    on_click: Optional[Callable] = None,
    **props
) -> rx.Component:
    """White outlined on dark surface: Transparent bg, White border/text."""
    content = _btn_content(text, icon)
    base_class = BTN_BASE + " " + WHITE_OUTLINE_ON_DARK
    if href:
        return rx.link(content, href=href, class_name=base_class, **props)
    return rx.button(content, class_name=base_class, on_click=on_click, **props)


def btn_secondary(
    text: str,
    icon: Optional[str] = None,
    href: Optional[str] = None,
    on_click: Optional[Callable] = None,
    **props
) -> rx.Component:
    """Secondary button on light surface."""
    content = _btn_content(text, icon)
    base_class = BTN_BASE + " " + SECONDARY_ON_LIGHT
    if href:
        return rx.link(content, href=href, class_name=base_class, **props)
    return rx.button(content, class_name=base_class, on_click=on_click, **props)


def btn_frap(
    icon: str = "shopping_bag",
    on_click: Optional[Callable] = None,
    **props
) -> rx.Component:
    """Floating circular Frap button - signature elevation element.
    
    DESING.md specs: 56px diameter, Green Accent (#00754A) fill, white icon.
    Dual shadow: base 0 0 6px rgba(0,0,0,0.24) + ambient 0 8px 12px rgba(0,0,0,0.14).
    Active: ambient collapses to 0, scale(0.95).
    Fixed bottom-right with touch offset.
    """
    return rx.button(
        rx.icon(icon, size=24, color="white"),
        class_name=(
            "fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full "
            "bg-green-accent text-white "
            + SHADOW_FRAP + " " + TRANSITION_200 +
            " active:scale-[0.95] " + SHADOW_FRAP_ACTIVE
        ),
        on_click=on_click,
        aria_label="Realizar pedido",
        **props
    )


def _btn_content(text: str, icon: Optional[str]) -> rx.Component:
    if icon:
        return rx.hstack(
            rx.icon(icon, size=18, style={"fontVariationSettings": "'FILL' 1"}),
            rx.text(text, white_space="nowrap"),
            spacing="2",
            align="center",
        )
    return rx.text(text, white_space="nowrap")


# ─── Links ──────────────────────────────────────────────────────────────

def nav_link(text: str, href: str, active: bool = False, **props) -> rx.Component:
    """Navigation link for desktop navbar.
    
    DESING.md: font-label-sm (14px), weight 400-600, tight tracking, 
    text-on-surface-variant → hover:text-green-accent
    """
    cls = (
        LINK_BASE + " "
        + ("text-green-accent font-semibold" if active else "text-on-surface-variant hover:text-green-accent")
    )
    return rx.link(text, href=href, class_name=cls, **props)


def footer_link(text: str, href: str, **props) -> rx.Component:
    """Footer link.
    
    base.html: font-label-sm text-label-sm text-soft-mint/80 hover:text-white
    """
    cls = (
        "font-label text-label-sm font-medium tracking-tight text-soft-mint/80 hover:text-white " 
        + TRANSITION_200
    )
    return rx.link(text, href=href, class_name=cls, **props)


def mobile_nav_link(text: str, href: str, icon: Optional[str] = None, **props) -> rx.Component:
    """Mobile navigation link with optional icon.
    
    base.html: flex items-center gap-2 font-label-md text-label-md 
    text-on-surface-variant hover:text-green-accent py-3
    """
    cls = "flex items-center gap-2 font-label text-label-md font-medium tracking-tight text-on-surface-variant hover:text-green-accent py-3 " + TRANSITION_200
    content = [rx.text(text)]
    if icon:
        content.insert(0, rx.icon(icon, size=22))
    return rx.link(*content, href=href, class_name=cls, **props)


# ─── Cards ──────────────────────────────────────────────────────────────

def card(children: rx.Component, class_name: str = "", **props) -> rx.Component:
    """Content card: White bg, 12px radius, whisper-soft shadow.
    
    DESING.md: White (#ffffff) background, 12px radius, 
    dual shadow: 0 0 0.5px rgba(0,0,0,0.14) + 0 1px 1px rgba(0,0,0,0.24)
    Padding: 16-24px (space-3 to space-4)
    """
    base_class = "bg-white rounded-card p-4 sm:p-6 " + SHADOW_CARD
    combined_class = f"{base_class} {class_name}".strip()
    return rx.box(
        children,
        class_name=combined_class,
        **props
    )


def card_interactive(children: rx.Component, href: str, **props) -> rx.Component:
    """Interactive card (link wrapper)."""
    return rx.link(
        card(children),
        href=href,
        class_name="block hover:shadow-lg " + TRANSITION_300,
        **props
    )


# ─── Inputs & Forms ─────────────────────────────────────────────────────

def floating_input(
    label: str,
    placeholder: str = "",
    type: str = "text",
    name: Optional[str] = None,
    value: Optional[str] = None,
    on_change: Optional[Callable] = None,
    **props
) -> rx.Component:
    """Floating label input following Material Design 3 spec.
    
    Uses Green Accent for focus border, tight tracking for labels.
    """
    return rx.el.div(
        rx.input(
            placeholder=placeholder,
            type=type,
            name=name,
            value=value,
            on_change=on_change,
            class_name=(
                "w-full px-3 py-3 bg-transparent border-b-2 border-outline-variant "
                "text-on-surface placeholder:text-transparent tracking-tight "
                "focus:outline-none focus:border-green-accent "
                "peer " + TRANSITION_200
            ),
            **props
        ),
        rx.el.label(
            label,
            class_name=(
                "absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant tracking-tight "
                "peer-focus:top-0 peer-focus:-translate-y-full peer-focus:text-green-accent "
                "peer-focus:text-label-sm peer-valid:top-0 peer-valid:-translate-y-full peer-valid:text-label-sm "
                "transition-all duration-300 ease-out pointer-events-none "
                "font-label text-label-md font-medium"
            ),
        ),
        class_name="relative w-full",
    )


# ─── Message/Alert ──────────────────────────────────────────────────────

def alert_message(
    message: str,
    type: str = "info",  # success, error, warning, info
    on_dismiss: Optional[Callable] = None,
    **props
) -> rx.Component:
    """Django-style alert message with auto-dismiss.
    
    Uses color tokens from rxconfig.py (success-bg, error-bg, etc.)
    """
    configs = {
        "success": ("success-bg", "success-border", "success-text", "check_circle"),
        "error": ("error-bg", "error-border", "error-text", "error"),
        "warning": ("warning-bg", "warning-border", "warning-text", "warning"),
        "info": ("info-bg", "info-border", "info-text", "info"),
    }
    bg, border, text, icon_name = configs.get(type, configs["info"])

    return rx.el.div(
        rx.icon(icon_name, size=18, class_name="shrink-0"),
        rx.text(message, class_name="text-sm leading-relaxed flex-1"),
        rx.button(
            "×",
            on_click=on_dismiss,
            class_name="shrink-0 opacity-60 hover:opacity-100 text-xl leading-none",
            aria_label="Cerrar mensaje",
        ),
        class_name=(
            f"flex items-start gap-3 p-4 rounded-xl border "
            f"bg-{bg} border-{border} text-{text} "
            "auto-dismiss-message"
        ),
        role="alert",
        **props
    )


# ─── Layout Helpers ─────────────────────────────────────────────────────

def container(*children: rx.Component, class_name: str = "", **props) -> rx.Component:
    """Main container with responsive gutters matching base.html exactly.
    
    base.html values: px-gutter-mobile (1.6rem), md:px-gutter-desktop (4rem), max-w-max-width-content (1440px)
    """
    base_class = "px-[1.6rem] md:px-[4rem] max-w-[1440px] mx-auto w-full"
    combined_class = f"{base_class} {class_name}".strip()
    return rx.container(
        *children,
        class_name=combined_class,
        **props
    )


def section(children: rx.Component, **props) -> rx.Component:
    """Section wrapper with vertical spacing."""
    return rx.box(children, class_name="py-12 md:py-16", **props)


# ─── Icon Button (for navbar actions) ──────────────────────────────────

def icon_button(
    icon: str,
    text: str,
    variant: str = "primary",  # primary, secondary, ghost
    href: Optional[str] = None,
    on_click: Optional[Callable] = None,
    **props
) -> rx.Component:
    """Icon + text button used in navbar right section.
    
    Matches base.html navbar buttons exactly:
    - Primary: h-12 px-4 sm:px-6 bg-green-accent text-white rounded-full
    - Secondary (referrer): h-12 px-4 sm:px-5 border border-outline-variant bg-surface-container-low text-on-surface-variant
    """
    variants = {
        "primary": LUMINOUS_ACCENT,  # bg-green-accent text-white hover:bg-starbucks-green
        "secondary": "border-outline-variant bg-surface-container-low text-on-surface-variant hover:bg-surface-container hover:text-green-accent",
        "ghost": "text-on-surface-variant hover:text-green-accent",
    }
    base = BTN_BASE + " " + variants.get(variant, variants["primary"])
    content = rx.hstack(
        rx.icon(icon, size=18, style={"fontVariationSettings": "'FILL' 1"}),
        rx.text(text, class_name="hidden sm:inline"),
        spacing="2",
        align="center",
    )
    if href:
        return rx.link(content, href=href, class_name=base, **props)
    return rx.button(content, class_name=base, on_click=on_click, **props)