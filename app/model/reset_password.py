import arrow
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ArrowType
from app.model.base_models import ModelBase
from app.model.meta import _expiration_1h

if TYPE_CHECKING:
    from app.model.user import User


class ResetPasswordCode(ModelBase):
    __tablename__ = "reset_password_code"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

    user: Mapped["User"] = relationship(
        "User", foreign_keys="ResetPasswordCode.user_id"
    )

    expired: Mapped[arrow.Arrow] = mapped_column(
        ArrowType, nullable=False, default=_expiration_1h
    )

    def is_expired(self):
        return self.expired < arrow.now()
