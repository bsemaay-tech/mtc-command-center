from __future__ import annotations

import re
import unittest
from pathlib import Path


MCC_ROOT = Path(__file__).resolve().parents[4]
WEB_ROOT = MCC_ROOT / "08_DASHBOARD_APP" / "apps" / "web"


class StrategyDetailA11yStaticTests(unittest.TestCase):
    def test_workflow_cards_are_native_buttons(self) -> None:
        app_js = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn('type="button"', app_js)
        self.assertRegex(app_js, r'<button\s+type="button"\s+class="workflow-card')
        self.assertNotRegex(app_js, r'<div\s+class="workflow-card[^"]*"\s+onclick=')

    def test_focus_visible_and_reduced_motion_css_exist(self) -> None:
        css = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

        self.assertRegex(css, r":focus-visible\s*\{")
        self.assertIn(".workflow-card:focus-visible", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertRegex(
            css,
            re.compile(r"\.dot\.amber\s*\{[^}]*animation:\s*none", re.MULTILINE | re.DOTALL),
        )


if __name__ == "__main__":
    unittest.main()
