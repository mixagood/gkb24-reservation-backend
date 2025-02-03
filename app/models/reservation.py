# app/models/reservation.py
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.core.db import Base
from sqlalchemy.orm import relationship

class Reservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    # Столбец с внешним ключом: ссылка на таблицу meetingroom
    meetingroom_id = Column(Integer, ForeignKey("meetingroom.id"))
    # Поле с указанием внешнего ключа пользователей
    user_id = Column(Integer, ForeignKey("user.id"))

    meeting_room = relationship("MeetingRoom", back_populates="reservations")
    comment = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"Уже забронировано с {self.from_reserve} по {self.to_reserve}"

