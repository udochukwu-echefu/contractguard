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

    def test_streamlit_toolbar_has_reserved_layout_space(self):
        self.assertIn('header[data-testid="stHeader"]', APP_CSS)
        self.assertIn("padding: 5.5rem 2rem 4rem", APP_CSS)
        self.assertIn("top:4.25rem", APP_CSS)


if __name__ == "__main__":
    unittest.main()
