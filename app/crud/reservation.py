# app/crud/reservation.py
from typing import Optional
from datetime import datetime
from sqlalchemy import and_, between, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import User, Reservation
from sqlalchemy.orm import joinedload

from app.schemas.reservation import ReservationWithRoomName

class CRUDReservation(CRUDBase):
    async def get_reservations_at_the_same_time(
        self,
        # Через * обозначим что все дальнейшие параметры должны передаваться по
        # ключу. И расположим  параметры со значением по-умолчанию перед
        # значениями без параметра по-умолчанию
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        # Опциональный параметр - id объекта бронирования
        reservation_id: Optional[int] = None,
        comment: Optional[str] = None,
        session: AsyncSession,
    ) -> list[Reservation]:

        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            or_(
                between(
                    from_reserve,
                    Reservation.from_reserve,
                    Reservation.to_reserve,
                ),
                between(
                    to_reserve,
                    Reservation.from_reserve,
                    Reservation.to_reserve,
                ),
                and_(
                    from_reserve <= Reservation.from_reserve,
                    to_reserve >= Reservation.to_reserve,
                ),
            ),
        )
        # Если передан id бронирования, то проверим условие
        if reservation_id is not None:
            select_stmt = select_stmt.where(Reservation.id != reservation_id)
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
        self, room_id: int, session: AsyncSession
    ):
        reservations = await session.execute(
            # Получим все объекты Reservation
            select(Reservation).where(
                # где id равен запрашиваему room_id
                Reservation.meetingroom_id == room_id,
                #  И время окончания бронирования больше текущего времени
                Reservation.to_reserve > datetime.now(),
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_by_user(
        self, session: AsyncSession, user: User
    ) -> list[ReservationWithRoomName]:
        reservations = await session.execute(
            select(Reservation)
            # Добавил тут join
            .options(joinedload(Reservation.meeting_room))
            .where(Reservation.user_id == user.id)
        )
        reservations = reservations.scalars().all()

        return [
            ReservationWithRoomName(
                id=reservation.id,
                meetingroom_id=reservation.meetingroom_id,
                user_id=reservation.user_id,
                from_reserve=reservation.from_reserve,
                to_reserve=reservation.to_reserve,
                meeting_room_name=reservation.meeting_room.name, # Добавляем имя комнаты
                comment=reservation.comment
            )
            for reservation in reservations
        ]


reservation_crud = CRUDReservation(Reservation)



#     async def get_by_user(
#         self, session: AsyncSession, user: User
#     ) -> list[Reservation]:
#         reservations = await session.execute(
#             select(Reservation).where(Reservation.user_id == user.id)
#         )
#         return reservations.scalars().all()


# reservation_crud = CRUDReservation(Reservation)
