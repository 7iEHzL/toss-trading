import contextlib
import importlib.machinery
import importlib.util
import io
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]


def load_source(module_name, path):
    loader = importlib.machinery.SourceFileLoader(module_name, str(path))
    spec = importlib.util.spec_from_loader(module_name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class LiveOrderSettingTests(unittest.TestCase):
    def load_settings(self, env):
        fake_dotenv = types.ModuleType("dotenv")
        fake_dotenv.load_dotenv = Mock(return_value=False)

        with patch.dict(sys.modules, {"dotenv": fake_dotenv}), patch.dict(
            os.environ, env, clear=True
        ):
            return load_source(
                "settings_under_test",
                ROOT / "config" / "settings.py",
            )

    def test_missing_environment_value_defaults_to_false(self):
        settings = self.load_settings({})
        self.assertIs(settings.ENABLE_REAL_ORDER, False)

    def test_invalid_environment_values_are_false(self):
        for value in ("yes", "1", "enabled", "invalid", ""):
            with self.subTest(value=value):
                settings = self.load_settings({"ENABLE_REAL_ORDER": value})
                self.assertIs(settings.ENABLE_REAL_ORDER, False)

    def test_false_is_case_insensitive_and_trimmed(self):
        for value in ("false", "FALSE", "  False  "):
            with self.subTest(value=value):
                settings = self.load_settings({"ENABLE_REAL_ORDER": value})
                self.assertIs(settings.ENABLE_REAL_ORDER, False)

    def test_true_is_case_insensitive_and_trimmed(self):
        settings = self.load_settings({"ENABLE_REAL_ORDER": "  TrUe  "})
        self.assertIs(settings.ENABLE_REAL_ORDER, True)


class LiveOrderGuardTests(unittest.TestCase):
    def load_entry_point(self, enabled):
        auth = types.ModuleType("api.auth")
        auth.get_access_token = Mock(name="get_access_token")

        order = types.ModuleType("api.order")
        order.buy_stock = Mock(name="buy_stock")
        order.sell_stock = Mock(name="sell_stock")
        order.get_order_status = Mock(name="get_order_status")
        order.is_order_filled = Mock(name="is_order_filled")

        settings = types.ModuleType("config.settings")
        settings.ENABLE_REAL_ORDER = enabled

        modules = {
            "api.auth": auth,
            "api.order": order,
            "config.settings": settings,
        }

        with patch.dict(sys.modules, modules):
            entry = load_source(
                "main_to_real_purchase_under_test",
                ROOT / "main_to_real_purchase",
            )

        return entry, auth, order

    def test_disabled_mode_exits_without_input_or_broker_calls(self):
        entry, auth, order = self.load_entry_point(enabled=False)

        with patch("builtins.input", side_effect=AssertionError("input called")):
            with contextlib.redirect_stdout(io.StringIO()):
                entry.main()

        auth.get_access_token.assert_not_called()
        order.buy_stock.assert_not_called()
        order.sell_stock.assert_not_called()
        order.get_order_status.assert_not_called()
        order.is_order_filled.assert_not_called()

    def test_enabled_but_rejected_confirmation_does_not_get_token_or_order(self):
        entry, auth, order = self.load_entry_point(enabled=True)

        with patch("builtins.input", return_value="n"):
            with contextlib.redirect_stdout(io.StringIO()):
                entry.main()

        auth.get_access_token.assert_not_called()
        order.buy_stock.assert_not_called()
        order.sell_stock.assert_not_called()
        order.get_order_status.assert_not_called()
        order.is_order_filled.assert_not_called()

    def test_invalid_order_is_rejected_before_input_or_token(self):
        entry, auth, order = self.load_entry_point(enabled=True)
        entry.QUANTITY = 0

        with patch("builtins.input", side_effect=AssertionError("input called")):
            with self.assertRaises(ValueError):
                with contextlib.redirect_stdout(io.StringIO()):
                    entry.main()

        auth.get_access_token.assert_not_called()
        order.buy_stock.assert_not_called()
        order.sell_stock.assert_not_called()

    def test_missing_order_result_stops_without_status_lookup(self):
        entry, auth, order = self.load_entry_point(enabled=True)
        auth.get_access_token.return_value = "fake-token"
        order.buy_stock.return_value = None

        with patch("builtins.input", return_value="y"):
            with contextlib.redirect_stdout(io.StringIO()):
                entry.main()

        auth.get_access_token.assert_called_once_with()
        order.buy_stock.assert_called_once()
        order.get_order_status.assert_not_called()
        order.is_order_filled.assert_not_called()

    def test_missing_order_id_stops_without_status_lookup(self):
        entry, auth, order = self.load_entry_point(enabled=True)
        auth.get_access_token.return_value = "fake-token"
        order.buy_stock.return_value = {"result": {}}

        with patch("builtins.input", return_value="y"):
            with contextlib.redirect_stdout(io.StringIO()):
                entry.main()

        order.get_order_status.assert_not_called()
        order.is_order_filled.assert_not_called()


class OrderRequestValidationTests(unittest.TestCase):
    def setUp(self):
        auth = types.ModuleType("api.auth")
        auth.get_access_token = Mock()
        order = types.ModuleType("api.order")
        order.buy_stock = Mock()
        order.sell_stock = Mock()
        order.get_order_status = Mock()
        order.is_order_filled = Mock()
        settings = types.ModuleType("config.settings")
        settings.ENABLE_REAL_ORDER = False

        with patch.dict(
            sys.modules,
            {
                "api.auth": auth,
                "api.order": order,
                "config.settings": settings,
            },
        ):
            self.entry = load_source(
                "main_to_real_purchase_validation_test",
                ROOT / "main_to_real_purchase",
            )

    def test_valid_market_and_limit_orders(self):
        self.entry.validate_order_request("BUY", "005930", 1, None, 1)
        self.entry.validate_order_request("SELL", "005930", 1, 1000.5, 1)

    def test_invalid_order_fields_fail_closed(self):
        invalid_cases = (
            ("HOLD", "005930", 1, None, 1),
            ([], "005930", 1, None, 1),
            ("BUY", "", 1, None, 1),
            ("BUY", "005930", 0, None, 1),
            ("BUY", "005930", 1.0, None, 1),
            ("BUY", "005930", True, None, 1),
            ("BUY", "005930", 1, 0, 1),
            ("BUY", "005930", 1, float("nan"), 1),
            ("BUY", "005930", 1, float("inf"), 1),
            ("BUY", "005930", 1, "1000", 1),
            ("BUY", "005930", 1, None, 0),
            ("BUY", "005930", 1, None, True),
        )

        for values in invalid_cases:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    self.entry.validate_order_request(*values)


class OrderApiDefenseTests(unittest.TestCase):
    def load_order_module(self, enabled):
        requests = types.ModuleType("requests")
        requests.post = Mock(name="requests.post")
        requests.get = Mock(name="requests.get")

        settings = types.ModuleType("config.settings")
        settings.ENABLE_REAL_ORDER = enabled

        with patch.dict(
            sys.modules,
            {
                "requests": requests,
                "config.settings": settings,
            },
        ):
            module = load_source(
                "api_order_defense_test",
                ROOT / "api" / "order.py",
            )

        return module, requests

    def test_disabled_setting_blocks_buy_and_sell_before_http(self):
        order, requests = self.load_order_module(enabled=False)

        with self.assertRaises(order.LiveOrderSafetyError):
            order.buy_stock(
                "fake-token",
                1,
                "005930",
                1,
                live_order_confirmed=True,
            )

        with self.assertRaises(order.LiveOrderSafetyError):
            order.sell_stock(
                "fake-token",
                1,
                "005930",
                1,
                live_order_confirmed=True,
            )

        requests.post.assert_not_called()

    def test_missing_confirmation_blocks_http_when_setting_enabled(self):
        order, requests = self.load_order_module(enabled=True)

        with self.assertRaises(order.LiveOrderSafetyError):
            order.buy_stock("fake-token", 1, "005930", 1)

        with self.assertRaises(order.LiveOrderSafetyError):
            order.sell_stock("fake-token", 1, "005930", 1)

        requests.post.assert_not_called()

    def test_enabled_and_confirmed_order_reaches_only_fake_http(self):
        order, requests = self.load_order_module(enabled=True)
        response = Mock(status_code=200)
        response.json.return_value = {"result": {"orderId": "fake-order"}}
        requests.post.return_value = response

        with contextlib.redirect_stdout(io.StringIO()):
            result = order.buy_stock(
                "fake-token",
                1,
                "005930",
                1,
                live_order_confirmed=True,
            )

        self.assertEqual(result, {"result": {"orderId": "fake-order"}})
        requests.post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
