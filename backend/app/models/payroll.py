from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Payroll(Base):
    __tablename__ = "payroll"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    pay_period: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    pay_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    basic_salary: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    allowances: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    deductions: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    bonus: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    gross_salary: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    net_salary: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    employee = relationship("Employee")