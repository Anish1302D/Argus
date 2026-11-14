"""Regression checks for static Argus frontend interaction and branding."""

from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = PROJECT_ROOT / "apps" / "api" / "src" / "api" / "static" / "index.html"


def test_inactive_navigation_scrim_does_not_intercept_desktop_pointer_events():
    html = INDEX_HTML.read_text(encoding="utf-8")

    scrim_rule = re.search(r"\.scrim\s*\{([^}]*)\}", html)
    active_rule = re.search(r"\.scrim\.is-on\s*\{([^}]*)\}", html)

    assert scrim_rule is not None, "Base navigation scrim CSS rule must exist"
    assert active_rule is not None, "Active navigation scrim CSS rule must exist"
    assert re.search(r"pointer-events\s*:\s*none", scrim_rule.group(1), re.IGNORECASE)
    assert re.search(r"pointer-events\s*:\s*auto", active_rule.group(1), re.IGNORECASE)


def test_static_frontend_uses_argus_product_identity():
    html = INDEX_HTML.read_text(encoding="utf-8")

    assert re.search(r"<title>\s*Argus\b", html, re.IGNORECASE)
    assert "argus.theme" in html
    assert "TRL Debate Engine" not in html
