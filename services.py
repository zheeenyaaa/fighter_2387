from itertools import count
from models import FighterInput, FighterModel, FighterUpdate


fighters: dict[int, FighterModel] = {
    1: FighterModel(
        id=1,
        name="F-16 Fighting Falcon",
        engine_count=1,
        mass_kg=9295.44, 
        wingspan_m=9.144,
        wing_area_m2=27.87,
        mean_aerodynamic_chord_m=3.45,
    ),
    2: FighterModel(
        id=2,
        name="F-15 Eagle",
        engine_count=2,
        mass_kg=18355.0, 
        wingspan_m=13.05,
        wing_area_m2=56.61,
        mean_aerodynamic_chord_m=4.86,
    ),
    3: FighterModel(
        id=3,
        name="F/A-18A Hornet",
        engine_count=2,
        mass_kg=14506.0,
        wingspan_m=11.40,  
        wing_area_m2=37.16,
        mean_aerodynamic_chord_m=3.51,
    ),
}

next_id = count(max(fighters, default=0) + 1)


class FighterService:
    def create(self, fighter: FighterInput) -> FighterModel:
        new_fighter = FighterModel(
            id=next(next_id),
            **fighter.model_dump(),
        )
        fighters[new_fighter.id] = new_fighter
        return new_fighter

    def read(
        self,
        fighter_id: int | None = None,
    ) -> list[FighterModel] | FighterModel | None:
        if fighter_id is None:
            return list(fighters.values())

        return fighters.get(fighter_id)

    def update(
        self,
        fighter_id: int,
        fighter: FighterUpdate,
    ) -> FighterModel | None:
        if fighter_id not in fighters:
            return None

        updated_fighter = FighterModel(
            id=fighter_id,
            **fighter.model_dump(),
        )
        fighters[fighter_id] = updated_fighter
        return updated_fighter

    def delete(self, fighter_id: int) -> FighterModel | None:
        return fighters.pop(fighter_id, None)