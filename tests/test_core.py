import tempfile
import unittest
from pathlib import Path

from analyzer import parse_document, review_context_text, safe_filename
from export_utils import build_csv, build_json_report, build_markdown_report
from styles import APP_CSS


class ContractGuardCoreTests(unittest.TestCase):
    def test_txt_parser_adds_line_markers_and_quality(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
            handle.write("Agreement\nThe tenant must pay rent monthly.\nTermination requires 30 days notice.")
            path = handle.name
        try:
            text, chunks, quality = parse_document(path)
        finally:
            Path(path).unlink(missing_ok=True)
        self.assertIn("[L1] Agreement", text)
        self.assertTrue(chunks)
        self.assertEqual(quality["file_type"], "TXT")

    def test_review_context_is_explicit(self):
        context = review_context_text(
            {"party_role": "Tenant", "jurisdiction": "Lagos", "goal": "Negotiate"}
        )
        self.assertIn("Tenant", context)
        self.assertIn("Lagos", context)

    def test_export_contains_evidence(self):
        analysis = {
            "title": "Lease",
            "contract_type": "Lease",
            "executive_summary": "Summary",
            "risk_assessment": [
                {
                    "title": "Termination",
                    "risk_level": "High",
                    "explanation": "Risk",
                    "recommendation": "Ask for notice",
                    "citation": "Section 7",
                    "quote": "terminate immediately",
                }
            ],
            "negotiation_priorities": [],
            "missing_protections": [],
            "obligations": [],
            "uncertainties": [],
        }
        report = build_markdown_report(
            analysis, "lease.txt", {"party_role": "Tenant", "goal": "Negotiate"}
        )
        self.assertIn("Section 7", report)
        self.assertIn("terminate immediately", report)
        self.assertIn('"analysis"', build_json_report(analysis, {}, {}))

    def test_csv_and_filename_helpers(self):
        csv_text = build_csv([{"party": "Tenant", "obligation": "Pay rent"}])
        self.assertIn("party,obligation", csv_text)
        self.assertEqual(safe_filename("My lease (final)"), "My-lease-final")

    def test_streamlit_toolbar_keeps_sidebar_controls_visible(self):
        self.assertIn('header[data-testid="stHeader"]', APP_CSS)
        self.assertIn('header[data-testid="stHeader"] [data-testid="stToolbar"]', APP_CSS)
        self.assertIn('[data-testid="stToolbarActions"]', APP_CSS)
        self.assertIn('[data-testid="stMainMenu"]', APP_CSS)
        self.assertIn('[data-testid="stExpandSidebarButton"]', APP_CSS)
        self.assertIn('[data-testid="stSidebarCollapseButton"]', APP_CSS)
        self.assertIn('[data-testid="stSidebarCollapsedControl"]', APP_CSS)
        self.assertNotIn("height: 0;", APP_CSS)
        self.assertIn("pointer-events: auto", APP_CSS)

    def test_review_setup_is_styled_as_a_primary_main_page_workflow(self):
        self.assertIn(".st-key-review_setup", APP_CSS)
        self.assertIn('[data-testid="stFileUploaderDropzone"]', APP_CSS)
        app_source = Path(__file__).resolve().parents[1].joinpath("app.py").read_text()
        self.assertIn("def render_review_setup", app_source)
        self.assertIn('st.button("Review contract"', app_source)
        self.assertIn("disabled=not uploaded_file or not consent", app_source)
        self.assertIn('initial_sidebar_state="auto"', app_source)

    def test_repository_scope_is_contract_review_only(self):
        root = Path(__file__).resolve().parents[1]
        scoped_text = "\n".join(
            root.joinpath(name).read_text()
            for name in ("app.py", "README.md", "PRODUCT.md", "DESIGN.md")
        ).lower()
        self.assertNotIn("verify onboarding", scoped_text)
        self.assertNotIn("identity reconciliation", scoped_text)
        self.assertFalse(root.joinpath("kyc.py").exists())
        self.assertFalse(root.joinpath("kyc_ui.py").exists())


if __name__ == "__main__":
    unittest.main()
