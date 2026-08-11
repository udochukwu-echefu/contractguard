import unittest

from playbooks import DEFAULT_PLAYBOOK, classify_contract, evaluate_report, finding_key


class PlaybookTests(unittest.TestCase):
    def test_high_risk_matching_rule_escalates(self):
        report = {
            "risk_assessment": [
                {
                    "title": "Unlimited liability",
                    "clause": "The supplier has unlimited liability",
                    "risk_level": "High",
                    "citation": "Section 9",
                    "quote": "unlimited liability",
                }
            ],
            "missing_protections": [],
        }
        result = evaluate_report(report, DEFAULT_PLAYBOOK)
        liability = next(item for item in result["deviations"] if item["rule_id"] == "liability")
        self.assertEqual(liability["status"], "Escalate")
        self.assertEqual(liability["citation"], "Section 9")
        termination = next(item for item in result["deviations"] if item["rule_id"] == "termination")
        self.assertEqual(termination["status"], "Not detected")
        self.assertEqual(termination["matched_finding"], "")
        self.assertEqual(termination["quote"], "")

    def test_finding_keys_are_stable(self):
        finding = {"title": "Termination", "citation": "Line 4", "quote": "terminate"}
        self.assertEqual(finding_key(finding, 1), finding_key(finding, 1))

    def test_residential_lease_is_classified_before_playbook_selection(self):
        result = classify_contract(
            "RESIDENTIAL TENANCY AGREEMENT. The landlord lets the dwelling to the tenant. "
            "The tenant pays a security deposit before taking possession."
        )
        self.assertEqual(result["contract_category"], "Residential lease")
        self.assertFalse(result["requires_confirmation"])

    def test_ambiguous_document_requires_confirmation(self):
        result = classify_contract("Agreement between Party A and Party B. The parties agree as follows.")
        self.assertEqual(result["contract_category"], "General contract review")
        self.assertTrue(result["requires_confirmation"])

    def test_semantic_category_blocks_irrelevant_confidentiality_match(self):
        playbook = {
            "id": "test-nda",
            "name": "NDA",
            "contract_types": [],
            "rules": [
                {
                    "id": "confidentiality",
                    "title": "Confidentiality and data use",
                    "finding_categories": ["confidentiality_data"],
                    "keywords": ["entry", "use"],
                    "required": True,
                }
            ],
        }
        report = {
            "risk_assessment": [
                {
                    "title": "Unrestricted Landlord Entry",
                    "clause": "The landlord may enter at any time.",
                    "quote": "enter at any time",
                    "applicable_category": "property_access",
                    "risk_level": "High",
                }
            ],
            "missing_protections": [],
        }
        result = evaluate_report(report, playbook)
        self.assertEqual(result["deviations"][0]["status"], "Not detected")
        self.assertEqual(result["deviations"][0]["matched_finding"], "")


if __name__ == "__main__":
    unittest.main()
