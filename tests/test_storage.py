import tempfile
import unittest
from pathlib import Path

from storage import ReviewStore


class ReviewStoreTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tempdir.name) / "contractguard.db"
        self.store = ReviewStore(f"sqlite:///{self.db_path}")

    def tearDown(self):
        self.store.engine.dispose()
        self.tempdir.cleanup()

    def _review(self, review_id="review-1", retain=False):
        return {
            "id": review_id,
            "source_name": "lease.txt",
            "contract_type": "Lease",
            "analysis": {"risk_assessment": []},
            "summary": {"high": 0},
            "review_context": {"party_role": "Tenant"},
            "document_quality": {"quality": "Readable"},
            "messages": [],
            "document_text": "confidential source text",
            "retain_source_text": retain,
            "retention_days": 30,
        }

    def test_reviews_are_scoped_to_owner(self):
        self.store.upsert_review("alice", self._review())
        self.assertEqual(len(self.store.list_reviews("alice")), 1)
        self.assertEqual(self.store.list_reviews("bob"), [])
        self.assertIsNone(self.store.get_review("bob", "review-1"))

    def test_source_text_is_opt_in(self):
        self.store.upsert_review("alice", self._review(retain=False))
        self.assertEqual(self.store.get_review("alice", "review-1")["document_text"], "")
        self.store.upsert_review("alice", self._review(retain=True))
        self.assertEqual(self.store.get_review("alice", "review-1")["document_text"], "confidential source text")

    def test_hard_delete_removes_review_and_decisions(self):
        self.store.upsert_review("alice", self._review())
        self.store.record_decision(
            "alice",
            "review-1",
            {"finding_key": "finding", "finding_title": "Termination", "status": "Escalate"},
        )
        self.assertTrue(self.store.list_decisions("alice", "review-1"))
        self.assertTrue(self.store.delete_review("alice", "review-1"))
        self.assertIsNone(self.store.get_review("alice", "review-1"))
        self.assertEqual(self.store.list_decisions("alice", "review-1"), [])


if __name__ == "__main__":
    unittest.main()
