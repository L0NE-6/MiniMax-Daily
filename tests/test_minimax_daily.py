import importlib.util
import unittest
from pathlib import Path
from unittest import mock


SOURCE = Path(__file__).resolve().parents[1] / "minimax_daily.py"
SPEC = importlib.util.spec_from_file_location("minimax_daily_test", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


STATUS_PENDING = {
    "base_resp": {"status_code": 0},
    "data": {"days": [{"is_today": True, "day_no": 4, "status": 2, "points": 1000}]},
}
STATUS_ALREADY = {
    "base_resp": {"status_code": 0},
    "data": {"days": [{"is_today": True, "day_no": 4, "status": 3, "points": 1000}]},
}


class MiniMaxDailyTests(unittest.TestCase):
    def test_no_auth_is_not_success(self):
        with mock.patch.object(MODULE, "get_bearer_token", return_value=(None, None)):
            code, out = MODULE.checkin(claim=True)
        self.assertEqual(2, code)
        self.assertEqual("NO_AUTH", out["result"])

    def test_already_checked_in_skips_claim(self):
        calls = []

        def fake_request(path, *args, **kwargs):
            calls.append(path)
            return 200, STATUS_ALREADY

        with mock.patch.object(MODULE, "get_bearer_token", return_value=("token", "oauth")), \
                mock.patch.object(MODULE, "real_user_id", return_value="1"), \
                mock.patch.object(MODULE, "signed_request", side_effect=fake_request):
            code, out = MODULE.checkin(claim=True)

        self.assertEqual(0, code)
        self.assertEqual("ALREADY", out["result"])
        self.assertEqual(["/minimax-cloud/api/v1/signin/status"], calls)

    def test_status_mode_never_claims(self):
        calls = []

        def fake_request(path, *args, **kwargs):
            calls.append(path)
            return 200, STATUS_PENDING

        with mock.patch.object(MODULE, "get_bearer_token", return_value=("token", "oauth")), \
                mock.patch.object(MODULE, "real_user_id", return_value="1"), \
                mock.patch.object(MODULE, "signed_request", side_effect=fake_request):
            code, out = MODULE.checkin(claim=False)

        self.assertEqual(0, code)
        self.assertEqual("PENDING", out["result"])
        self.assertNotIn("/minimax-cloud/api/v1/signin/claim", calls)

    def test_claim_success(self):
        responses = [
            (200, STATUS_PENDING),
            (200, {
                "base_resp": {"status_code": 0},
                "data": {"claim_result": 1, "points": 1000, "day_no": 4},
            }),
        ]
        calls = []

        def fake_request(path, *args, **kwargs):
            calls.append(path)
            return responses.pop(0)

        with mock.patch.object(MODULE, "get_bearer_token", return_value=("token", "oauth")), \
                mock.patch.object(MODULE, "real_user_id", return_value="1"), \
                mock.patch.object(MODULE, "signed_request", side_effect=fake_request):
            code, out = MODULE.checkin(claim=True)

        self.assertEqual(0, code)
        self.assertEqual("CLAIMED", out["result"])
        self.assertEqual(1000, out["points"])
        self.assertEqual("/minimax-cloud/api/v1/signin/claim", calls[-1])

    def test_claim_idempotent_result_is_already(self):
        responses = [
            (200, STATUS_PENDING),
            (200, {
                "base_resp": {"status_code": 0},
                "data": {"claim_result": 2, "points": 400, "day_no": 2},
            }),
        ]
        with mock.patch.object(MODULE, "get_bearer_token", return_value=("token", "oauth")), \
                mock.patch.object(MODULE, "real_user_id", return_value="1"), \
                mock.patch.object(MODULE, "signed_request", side_effect=responses):
            code, out = MODULE.checkin(claim=True)
        self.assertEqual(0, code)
        self.assertEqual("ALREADY", out["result"])

    def test_expired_session_is_visible(self):
        with mock.patch.object(MODULE, "get_bearer_token", return_value=("token", "oauth")), \
                mock.patch.object(MODULE, "real_user_id", return_value="1"), \
                mock.patch.object(MODULE, "signed_request", return_value=(
                    401, {"base_resp": {"status_code": 1022100011}})):
            code, out = MODULE.checkin(claim=True)
        self.assertEqual(1, code)
        self.assertEqual("NO_SESSION", out["result"])


if __name__ == "__main__":
    unittest.main()
