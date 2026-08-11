import unittest

from analyzer import harden_report


class TrustTests(unittest.TestCase):
    def test_unknown_jurisdiction_forces_general_guardrail(self):
        report = {
            "overall_attention": "High attention",
            "risk_assessment": [
                {
                    "title": "Broad access",
                    "risk_level": "High",
                    "recommendation": "Request reasonable notice.",
                    "confidence": "High",
                }
            ],
            "missing_protections": [],
        }
        result = harden_report(
            report,
            {"contract_category": "Residential lease", "confidence": "High"},
            {"jurisdiction": ""},
        )
        finding = result["risk_assessment"][0]
        self.assertEqual(result["contract_type"], "Residential lease")
        self.assertEqual(finding["recommendation_scope"], "General")
        self.assertFalse(finding["jurisdiction_supplied"])
        self.assertIn("Confirm enforceability under the applicable jurisdiction", finding["recommendation"])
        self.assertEqual(result["overall_attention"], "Needs verification")

    def test_jurisdiction_specific_scope_requires_a_basis(self):
        report = {
            "risk_assessment": [
                {
                    "risk_level": "Medium",
                    "confidence": "Medium",
                    "recommendation": "Check the statutory notice period.",
                    "jurisdiction_specific_basis": "Supplied Lagos State tenancy rules",
                }
            ],
            "missing_protections": [],
        }
        result = harden_report(
            report,
            {"contract_category": "Residential lease", "confidence": "Medium"},
            {"jurisdiction": "Lagos State, Nigeria"},
        )
        self.assertEqual(result["risk_assessment"][0]["recommendation_scope"], "Jurisdiction-specific")


if __name__ == "__main__":
    unittest.main()
