import pytest
from src.room_repository import RoomRepository


def test_exists_returns_true_for_existing_room():
    repo = RoomRepository()
    assert repo.exists(1) is True


def test_is_available_returns_true_for_available_room():
    repo = RoomRepository()
    assert repo.is_available(1) is True


def test_is_available_returns_false_for_unavailable_room():
    repo = RoomRepository()
    assert repo.is_available(3) is False


def test_mark_unavailable_changes_room_state():
    repo = RoomRepository()
    repo.mark_unavailable(1)
    assert repo.is_available(1) is False


def test_mark_available_changes_room_state():
    repo = RoomRepository()
    repo.mark_available(3)
    assert repo.is_available(3) is True


def test_mark_unavailable_raises_for_unknown_room():
    repo = RoomRepository()
    with pytest.raises(ValueError, match="Room not found"):
        repo.mark_unavailable(999)
