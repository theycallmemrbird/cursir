from app import ALL_CARD_IDS, create_app


def make_client():
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret"})
    return app.test_client()


def test_draws_each_card_once_before_deck_is_empty():
    client = make_client()
    seen_ids = set()

    for _ in ALL_CARD_IDS:
        response = client.post("/api/draw")
        assert response.status_code == 200
        payload = response.get_json()

        assert payload["card"] is not None
        assert payload["card"]["id"] not in seen_ids
        seen_ids.add(payload["card"]["id"])

    response = client.post("/api/draw")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["card"] is None
    assert payload["empty"] is True
    assert payload["remaining"] == 0
    assert len(seen_ids) == len(ALL_CARD_IDS)


def test_reset_restores_full_deck_after_draw():
    client = make_client()

    draw_response = client.post("/api/draw")
    assert draw_response.status_code == 200
    assert draw_response.get_json()["remaining"] == len(ALL_CARD_IDS) - 1

    reset_response = client.post("/api/reset")
    payload = reset_response.get_json()

    assert reset_response.status_code == 200
    assert payload["drawn"] == 0
    assert payload["remaining"] == len(ALL_CARD_IDS)
    assert payload["empty"] is False


def test_status_initializes_deck_for_new_session():
    client = make_client()

    response = client.get("/api/status")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["drawn"] == 0
    assert payload["remaining"] == len(ALL_CARD_IDS)
    assert payload["total"] == len(ALL_CARD_IDS)
    assert payload["empty"] is False
