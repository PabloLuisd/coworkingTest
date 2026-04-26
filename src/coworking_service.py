class CoworkingService:
    def __init__(self, room_repository, member_repository, booking_repository, waitlist_repository):
        self.room_repository = room_repository
        self.member_repository = member_repository
        self.booking_repository = booking_repository
        self.waitlist_repository = waitlist_repository

    def book_room(self, member_id: int, room_id: int) -> bool:
        if not member_id or not room_id:
            raise ValueError("Member ID and room ID are required")

        if not self.member_repository.exists(member_id):
            return False

        if not self.room_repository.exists(room_id):
            return False

        if self.member_repository.is_blocked(member_id):
            return False

        if self.member_repository.has_overdue_fee(member_id):
            return False

        if not self.room_repository.is_available(room_id):
            return False

        if self.booking_repository.count_active_bookings(member_id) >= 2:
            return False

        next_member = self.waitlist_repository.next_member(room_id)
        if next_member is not None and next_member != member_id:
            return False

        self.room_repository.mark_unavailable(room_id)
        self.booking_repository.create_booking(member_id, room_id)

        if self.waitlist_repository.has_waitlist(member_id, room_id):
            self.waitlist_repository.remove_from_waitlist(member_id, room_id)

        return True

    def release_room(self, member_id: int, room_id: int) -> bool:
        if not member_id or not room_id:
            raise ValueError("Member ID and room ID are required")

        if not self.booking_repository.is_room_with_member(member_id, room_id):
            return False

        self.booking_repository.close_booking(member_id, room_id)

        if not self.waitlist_repository.has_any_waitlist(room_id):
            self.room_repository.mark_available(room_id)

        return True

    def join_waitlist(self, member_id: int, room_id: int) -> bool:
        if not member_id or not room_id:
            raise ValueError("Member ID and room ID are required")

        if not self.member_repository.exists(member_id):
            return False

        if not self.room_repository.exists(room_id):
            return False

        if self.member_repository.is_blocked(member_id):
            return False

        if self.member_repository.has_overdue_fee(member_id):
            return False

        if self.room_repository.is_available(room_id):
            return False

        if self.waitlist_repository.has_waitlist(member_id, room_id):
            return False

        if self.booking_repository.is_room_with_member(member_id, room_id):
            return False

        self.waitlist_repository.add_to_waitlist(member_id, room_id)
        return True
