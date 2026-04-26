import pytest
from unittest.mock import Mock
from src.coworking_service import CoworkingService


def make_service():
    room_repository = Mock()
    member_repository = Mock()
    booking_repository = Mock()
    waitlist_repository = Mock()
    service = CoworkingService(
        room_repository,
        member_repository,
        booking_repository,
        waitlist_repository,
    )
    return service, room_repository, member_repository, booking_repository, waitlist_repository


def test_book_room_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Member ID and room ID are required"):
        service.book_room(None, 1)


def test_book_room_returns_false_when_member_does_not_exist():
    service, _, member_repository, _, _ = make_service()
    member_repository.exists.return_value = False
    assert service.book_room(999, 1) is False


def test_book_room_creates_booking_when_all_rules_are_satisfied():
    service, room_repository, member_repository, booking_repository, waitlist_repository = make_service()

    member_repository.exists.return_value = True
    room_repository.exists.return_value = True
    member_repository.is_blocked.return_value = False
    member_repository.has_overdue_fee.return_value = False
    room_repository.is_available.return_value = True
    booking_repository.count_active_bookings.return_value = 0
    waitlist_repository.next_member.return_value = None
    waitlist_repository.has_waitlist.return_value = False

    result = service.book_room(10, 1)

    assert result is True
    room_repository.mark_unavailable.assert_called_once_with(1)
    booking_repository.create_booking.assert_called_once_with(10, 1)


def test_release_room_returns_false_when_booking_does_not_exist():
    service, _, _, booking_repository, _ = make_service()
    booking_repository.is_room_with_member.return_value = False
    assert service.release_room(10, 1) is False


def test_join_waitlist_adds_member_when_rules_are_satisfied():
    service, room_repository, member_repository, booking_repository, waitlist_repository = make_service()

    member_repository.exists.return_value = True
    room_repository.exists.return_value = True
    member_repository.is_blocked.return_value = False
    member_repository.has_overdue_fee.return_value = False
    room_repository.is_available.return_value = False
    waitlist_repository.has_waitlist.return_value = False
    booking_repository.is_room_with_member.return_value = False

    result = service.join_waitlist(10, 1)

    assert result is True
    waitlist_repository.add_to_waitlist.assert_called_once_with(10, 1)


def test_join_waitlist_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Member ID and room ID are required"):
        service.join_waitlist(None, 1)
