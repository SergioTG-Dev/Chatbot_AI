import pytest
import json

# Skip tests if rasa_sdk is not installed in the environment where tests are run.
pytest.importorskip("rasa_sdk")

# Import the actions module under test (requires PYTHONPATH that includes this src folder)
from actions import (
    ActionFetchProcedures,
    ActionBookAppointment,
)


class DummyDispatcher:
    def __init__(self):
        self.messages = []

    def utter_message(self, text=None, buttons=None, response=None):
        self.messages.append({"text": text, "buttons": buttons, "response": response})


class DummyTracker:
    def __init__(self, slots=None, latest_text="", sender_id="test-user"):
        self._slots = slots or {}
        self.latest_message = {"text": latest_text, "intent": {"name": None, "confidence": 0.0}}
        self.sender_id = sender_id

    def get_slot(self, key):
        return self._slots.get(key)


def make_mock_response(status=200, data=None):
    class Resp:
        def __init__(self, status, data):
            self.status_code = status
            self._data = data

        def json(self):
            return self._data

    return Resp(status, data)


def test_action_fetch_procedures_lists_buttons(monkeypatch):
    dispatcher = DummyDispatcher()
    tracker = DummyTracker(slots={"department_id": "42"})

    # Mock requests.get used inside ActionFetchProcedures
    def fake_get(url, timeout=5):
        assert "/departments/42/procedures" in url or "/departments/" in url
        return make_mock_response(200, [{"id": "p1", "name": "Trámite 1"}, {"id": "p2", "name": "Trámite 2"}])

    monkeypatch.setattr("actions.requests.get", fake_get)

    action = ActionFetchProcedures()
    events = action.run(dispatcher, tracker, {})

    # Expect that dispatcher received at least one message with buttons
    assert len(dispatcher.messages) >= 1
    found = any(m.get("buttons") for m in dispatcher.messages)
    assert found, "Expected buttons for procedures but none were sent"


def test_action_book_appointment_success(monkeypatch):
    dispatcher = DummyDispatcher()
    slots = {
        "user_verified": True,
        "procedure_id": "p1",
        "dni": "12345678",
        "scheduled_at": "2025-11-01T10:30:00:00.000Z",
    }
    tracker = DummyTracker(slots=slots)

    # Mock POST to create appointment
    def fake_post(url, json=None, timeout=8):
        assert "/turnos/" in url
        return make_mock_response(201, {"id": "turno-abc-123"})

    monkeypatch.setattr("actions.requests.post", fake_post)

    action = ActionBookAppointment()
    events = action.run(dispatcher, tracker, {})

    # Expect SlotSet-like event with turno_id
    found = False
    for e in events:
        if hasattr(e, "key") and getattr(e, "key") == "turno_id":
            if getattr(e, "value", None) == "turno-abc-123":
                found = True
                break
    assert found, "Expected a SlotSet event with turno_id == 'turno-abc-123'"
