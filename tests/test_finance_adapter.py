import unittest
from unittest import mock

from runner_windows.actions import finance_adapter, secrets_adapter


class TestFinanceAdapter(unittest.TestCase):
    def test_missing_keys_returns_parked(self):
        """When API keys are missing, broker and data functions should park."""
        with mock.patch.object(secrets_adapter, "get", return_value={"status": "parked", "reason": "missing_secret", "note": "Not configured"}):
            res_cash = finance_adapter.cash()
            self.assertEqual(res_cash["status"], "parked")
            self.assertEqual(res_cash["reason"], "missing_secret")
            res_pos = finance_adapter.positions()
            self.assertEqual(res_pos["status"], "parked")
            res_order = finance_adapter.place_order("AAPL", "buy", 1, "market")
            self.assertEqual(res_order["status"], "parked")
            res_quote = finance_adapter.quote("AAPL")
            self.assertEqual(res_quote["status"], "parked")

    def test_paper_order_and_data(self):
        """With API keys, broker functions simulate orders and data functions return values."""
        # Patch secrets.get to return dummy strings for both keys
        def fake_get(alias):
            return "dummy"

        with mock.patch.object(secrets_adapter, "get", side_effect=fake_get):
            # Cash and positions
            res_cash = finance_adapter.cash()
            self.assertIn("cash", res_cash)
            res_pos = finance_adapter.positions()
            self.assertIn("positions", res_pos)
            # Place an order within cap
            order = finance_adapter.place_order("AAPL", "buy", 5, "market")
            self.assertIn("order_id", order)
            self.assertEqual(order["status"], "accepted")
            order_id = order["order_id"]
            # Order status should return filled
            status = finance_adapter.order_status(order_id)
            self.assertEqual(status["status"], "filled")
            # Cancel should return canceled
            cancel = finance_adapter.cancel(order_id)
            self.assertEqual(cancel["status"], "canceled")
            # Place an order exceeding cap should park
            over = finance_adapter.place_order("AAPL", "buy", 11, "market")  # 11*100 > 1000
            self.assertEqual(over["status"], "parked")
            self.assertEqual(over["reason"], "trade_cap_exceeded")
            # Invalid symbol should park
            invalid = finance_adapter.place_order("1234", "buy", 1, "market")
            self.assertEqual(invalid["status"], "parked")
            self.assertEqual(invalid["reason"], "invalid_order")
            # Data adapter returns price
            quote = finance_adapter.quote("AAPL")
            self.assertIn("price", quote)
            self.assertEqual(quote["price"], 100.0)
            # Rate limit triggers on subsequent call
            rate_limited = finance_adapter.quote("AAPL")
            if rate_limited.get("status") == "parked":
                self.assertEqual(rate_limited["reason"], "rate_limit")
            # Bars returns list of bars
            bars = finance_adapter.bars("AAPL", "1d", 3)
            if bars.get("status") == "parked":
                self.assertEqual(bars["reason"], "rate_limit")
            else:
                self.assertEqual(len(bars.get("bars", [])), 3)


if __name__ == "__main__":
    unittest.main()