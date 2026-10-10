from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from relay_agent.demo import bootstrap
from relay_agent.data import read_historical
from relay_agent.models import SupportMessage
from relay_agent.pipeline import SupportAgent


class PipelineTests(unittest.TestCase):
    def make_agent(self) -> SupportAgent:
        self.temp = TemporaryDirectory()
        root = Path(self.temp.name)
        bootstrap(root)
        return SupportAgent(read_historical(root / "data/demo/historical_resolutions.csv", "AmazonHelp"))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_legal_language_is_escalated(self):
        agent = self.make_agent()
        output = agent.handle(SupportMessage("1", "My damaged item is unsafe and I will sue", "AmazonHelp"))
        self.assertEqual(output.decision, "escalate")
        self.assertIn("High-risk", output.decision_reason)

    def test_delivery_message_returns_auditable_result(self):
        agent = self.make_agent()
        output = agent.handle(SupportMessage("2", "My delivery is late. Please help", "AmazonHelp"))
        self.assertEqual(output.intent, "delivery_delay")
        self.assertTrue(output.retrieved)
        self.assertIn("DM", output.reply)
