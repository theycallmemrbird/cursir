import unittest

from app import app, load_deck


class CardDrawTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.client = app.test_client()

    def test_draws_each_card_once_until_reset(self):
        total_cards = len(load_deck())
        drawn_ids = set()

        for expected_remaining in range(total_cards - 1, -1, -1):
            response = self.client.post("/draw")
            self.assertEqual(response.status_code, 200)

            payload = response.get_json()
            self.assertIsNotNone(payload["card"])
            self.assertEqual(payload["remaining"], expected_remaining)
            drawn_ids.add(payload["card"]["id"])

        self.assertEqual(len(drawn_ids), total_cards)

        empty_response = self.client.post("/draw")
        empty_payload = empty_response.get_json()
        self.assertIsNone(empty_payload["card"])
        self.assertEqual(empty_payload["remaining"], 0)

    def test_reset_restores_full_deck(self):
        self.client.post("/draw")

        response = self.client.post("/reset")
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["remaining"], len(load_deck()))


if __name__ == "__main__":
    unittest.main()
