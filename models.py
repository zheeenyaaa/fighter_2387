from pydantic import BaseModel, ConfigDict, Field


class FighterInput(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        allow_inf_nan=False,
    )

    name: str = Field(min_length=1)
    engine_count: int = Field(gt=0)
    mass_kg: float = Field(gt=0)
    wingspan_m: float = Field(gt=0)
    wing_area_m2: float = Field(gt=0)
    mean_aerodynamic_chord_m: float = Field(gt=0)

class FighterModel(FighterInput):
   id: int = Field(gt=0)


class FighterUpdate(FighterInput):
   pass