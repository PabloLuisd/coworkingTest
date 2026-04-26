class WaitlistRepository:
    def __init__(self):
        self._waitlist = []

    def add_to_waitlist(self, member_id: int, room_id: int) -> None:
        self._waitlist.append({"member_id": member_id, "room_id": room_id})

    def has_waitlist(self, member_id: int, room_id: int) -> bool:
        return any(
            entry["member_id"] == member_id and entry["room_id"] == room_id
            for entry in self._waitlist
        )

    def has_any_waitlist(self, room_id: int) -> bool:
        return any(entry["room_id"] == room_id for entry in self._waitlist)

    def next_member(self, room_id: int):
        for entry in self._waitlist:
            if entry["room_id"] == room_id:
                return entry["member_id"]
        return None

    def remove_from_waitlist(self, member_id: int, room_id: int) -> None:
        for entry in list(self._waitlist):
            if entry["member_id"] == member_id and entry["room_id"] == room_id:
                self._waitlist.remove(entry)
                return
        raise ValueError("Waitlist entry not found")
