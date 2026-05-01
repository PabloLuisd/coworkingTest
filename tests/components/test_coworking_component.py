import pytest

from src.coworking_service import CoworkingService
from src.room_repository import RoomRepository
from src.member_repository import MemberRepository
from src.booking_repository import BookingRepository
from src.waitlist_repository import WaitlistRepository


@pytest.fixture
def service():
    return CoworkingService(
        RoomRepository(),
        MemberRepository(),
        BookingRepository(),
        WaitlistRepository()
    )


def test_reserva_com_sucesso_deve_marcar_sala_indisponivel(service):
    result = service.book_room(10, 1)

    assert result is True
    assert service.room_repository.is_available(1) is False


def test_reserva_falha_quando_sala_nao_existe(service):
    result = service.book_room(10, 999)

    assert result is False


def test_reserva_falha_quando_membro_nao_existe(service):
    result = service.book_room(999, 1)

    assert result is False


def test_reserva_falha_quando_membro_inadimplente(service):
    result = service.book_room(30, 1)

    assert result is False