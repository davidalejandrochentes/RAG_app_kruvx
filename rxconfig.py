import reflex as rx

# Tailwind config - complete Kruvx design system (matching DESING.md & base.html EXACTLY)
tailwind_config = {
    "theme": {
        "extend": {
            "colors": {
                # Primary brand greens (four-tier system from DESING.md)
                "starbucks-green": "#006241",      # Brand headings, primary signal
                "green-accent": "#00754A",         # Primary CTA, Frap button - THE KEY COLOR
                "house-green": "#1E3932",          # Footer, feature bands, dark surfaces
                "green-uplift": "#2b5148",         # Decorative accents
                "green-light": "#d4e9e2",          # Form valid state tint

                # Gold (Rewards ceremony only)
                "gold": "#cba258",
                "gold-light": "#dfc49d",
                "gold-lightest": "#faf6ee",

                # Surface & Background (warm neutrals - NOT pure white)
                "neutral-warm": "#f2f0eb",         # Primary page canvas (Neutral Warm)
                "ceramic": "#edebe9",              # Zone separators, soft washes (Ceramic)
                "white": "#ffffff",                # Card/modal surface
                "neutral-cool": "#f9f9f9",         # Dropdown menus, form wraps

                # Semantic mappings used in base.html (EXACT colors from base.html inspector - kruvx.cloud)
                "surface-container-low": "#f5f3ee",      # Navbar background
                "surface-container-high": "#ffffff",
                "surface-container-highest": "#edebe9",
                "outline-variant": "#bec9c0",            # Navbar bottom border
                "on-surface-variant": "#3f4943",         # Nav link color (rgb 63 73 67)
                "on-surface": "#1d1b20",

                # Primary CTA color (Green Accent)
                "luminous-accent": "#00754A",      # Primary CTA fill
                "primary-container": "#006241",    # Hover state for primary (Starbucks Green)
                "soft-mint": "#d4e9e2",            # Footer text color

                # Text colors (with alpha for warmth)
                "text-primary": "rgba(0, 0, 0, 0.87)",      # Text Black - headings/body on light
                "text-secondary": "rgba(0, 0, 0, 0.58)",    # Text Black Soft - metadata on light
                "text-on-dark": "rgba(255, 255, 255, 1)",   # Text White - headings on dark green
                "text-on-dark-soft": "rgba(255, 255, 255, 0.70)",  # Text White Soft - secondary on dark
                "rewards-green": "#33433d",                 # Rewards page text

                # Semantic states
                "success-bg": "#e8f5e9",
                "success-border": "#a5d6a7",
                "success-text": "#2e7d32",
                "error-bg": "#fdecec",
                "error-border": "#ef9a9a",
                "error-text": "#c62828",
                "warning-bg": "#fff8e1",
                "warning-border": "#ffe082",
                "warning-text": "#f57f17",
                "info-bg": "#e3f2fd",
                "info-border": "#90caf9",
                "info-text": "#1565c0",
            },
            "fontFamily": {
                "body": ["Manrope", "sans-serif"],           # Substitute for SoDoSans
                "heading": ["Literata", "serif"],            # Substitute for Lander Tall (Rewards display)
                "label": ["Manrope", "sans-serif"],          # Substitute for SoDoSans (UI labels)
                "label-sm": ["Manrope", "sans-serif"],       # Label small - 14px, 600
                "label-md": ["Manrope", "sans-serif"],       # Label medium - 16px, 400
            },
            "fontSize": {
                # Semantic scale (standard rem = 16px)
                "text-1": ["0.8125rem", {"lineHeight": "1.5", "letterSpacing": "-0.01em"}],   # ~13px Micro
                "text-2": ["0.875rem", {"lineHeight": "1.5", "letterSpacing": "-0.01em"}],    # ~14px Small (label-sm)
                "text-3": ["1rem", {"lineHeight": "1.5", "letterSpacing": "-0.01em"}],        # 16px Body (DEFAULT)
                "text-4": ["1.1875rem", {"lineHeight": "1.5", "letterSpacing": "-0.01em"}],   # ~19px Body Large
                "text-5": ["1.5rem", {"lineHeight": "1.2", "letterSpacing": "-0.01em"}],      # 24px H1/H2
                "text-6": ["1.75rem", {"lineHeight": "1.2", "letterSpacing": "-0.01em"}],     # ~28px
                "text-7": ["2.25rem", {"lineHeight": "1.2", "letterSpacing": "-0.01em"}],     # ~36px
                "text-8": ["2.8125rem", {"lineHeight": "1.2", "letterSpacing": "-0.01em"}],   # 45px Hero Large
                "text-9": ["3.625rem", {"lineHeight": "1.2", "letterSpacing": "-0.01em"}],    # 58px Jumbo
                "text-10": ["5rem", {"lineHeight": "1.2", "letterSpacing": "-0.01em"}],       # 80px Display

                # Label aliases matching base.html exactly
                "label-sm": ["0.875rem", {"lineHeight": "1.5", "letterSpacing": "-0.01em", "fontWeight": "600"}],  # 14px, weight 600
                "label-md": ["1rem", {"lineHeight": "1.5", "letterSpacing": "0", "fontWeight": "400"}],            # 16px, weight 400
            },
            "letterSpacing": {
                "tight": "-0.01em",      # Universal tight tracking (KEY from DESING.md)
                "normal": "0",
                "loose": "0.1em",        # Uppercase labels
                "looser": "0.15em",      # Extreme emphasis
            },
            "borderRadius": {
                "pill": "50px",          # Full pill - ALL buttons
                "card": "12px",          # Cards, modals
                "full": "9999px",        # Circular (Frap, avatars)
            },
            "boxShadow": {
                "nav": "0 1px 3px rgba(0,0,0,0.1), 0 2px 2px rgba(0,0,0,0.06), 0 0 2px rgba(0,0,0,0.07)",
                "card": "0 0 0.5px rgba(0,0,0,0.14), 0 1px 1px rgba(0,0,0,0.24)",
                "frap": "0 0 6px rgba(0,0,0,0.24), 0 8px 12px rgba(0,0,0,0.14)",
                "frap-active": "0 0 6px rgba(0,0,0,0.24), 0 8px 12px rgba(0,0,0,0)",
            },
            "spacing": {
                # Gutter tokens (EXACT from base.html)
                "gutter-mobile": "1.6rem",       # 25.6px - default outer gutter (px-gutter-mobile)
                "gutter-desktop": "4rem",        # 64px - desktop (px-gutter-desktop)
                "space-lg": "2.4rem",            # 38.4px - gap-space-lg (desktop nav links)
                "space-md": "1.6rem",            # 25.6px - gap-space-md (right actions)
                "space-sm": "0.8rem",            # 12.8px - gap-space-sm
                "space-xs": "0.4rem",            # 6.4px - gap-space-xs
                "max-width-content": "90rem",    # 1440px - max-w-max-width-content
            },
            "transitionDuration": {
                "150": "150ms",   # Nav link transition
                "200": "200ms",   # Button transitions
                "300": "300ms",   # Expander/modal transitions
            },
            "transitionTimingFunction": {
                "nav-link": "cubic-bezier(0.4, 0, 0.2, 1)",   # Nav link transition
                "ease-out": "cubic-bezier(0.25, 0.46, 0.45, 0.94)",
                "button": "cubic-bezier(0.32, 2.32, 0.61, 0.27)",  # Springy for checkboxes
            },
        }
    }
}

config = rx.Config(
    app_name="rag_app_kruvx",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(),
        rx.plugins.TailwindV4Plugin(config=tailwind_config),
    ],
)