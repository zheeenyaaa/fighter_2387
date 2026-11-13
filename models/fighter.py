from sqlalchemy import CheckConstraint, Double, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Fighter(Base):
    __tablename__ = "fighters"
    __table_args__ = (
        CheckConstraint(
            "name ~ '[^[:space:]]'",
            name="ck_fighters_name_nonblank",
        ),
        CheckConstraint(
            "engine_count > 0",
            name="ck_fighters_engine_count_positive",
        ),
        CheckConstraint(
            "mass_kg > 0 AND mass_kg < 'Infinity'::double precision",
            name="ck_fighters_mass_kg_positive_finite",
        ),
        CheckConstraint(
            "wingspan_m > 0 AND wingspan_m < 'Infinity'::double precision",
            name="ck_fighters_wingspan_m_positive_finite",
        ),
        CheckConstraint(
            "wing_area_m2 > 0 AND wing_area_m2 < 'Infinity'::double precision",
            name="ck_fighters_wing_area_m2_positive_finite",
        ),
        CheckConstraint(
            "mean_aerodynamic_chord_m > 0 "
            "AND mean_aerodynamic_chord_m < 'Infinity'::double precision",
            name="ck_fighters_mean_aerodynamic_chord_m_positive_finite",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    engine_count: Mapped[int] = mapped_column(Integer, nullable=False)
    mass_kg: Mapped[float] = mapped_column(Double, nullable=False)
    wingspan_m: Mapped[float] = mapped_column(Double, nullable=False)
    wing_area_m2: Mapped[float] = mapped_column(Double, nullable=False)
    mean_aerodynamic_chord_m: Mapped[float] = mapped_column(Double, nullable=False)