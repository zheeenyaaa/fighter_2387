from fastapi import APIRouter, HTTPException, status
from models import FighterInput, FighterModel, FighterUpdate
from services import FighterService

router = APIRouter(prefix = "/api/v1/fighters", tags=["fighters"])
service = FighterService()

@router.get("/")
def get_fighters() -> list[FighterModel]:
  return service.read()


@router.get("/{fighter_id}")
def get_fighter(fighter_id: int) -> FighterModel:
    fighter = service.read(fighter_id)

    if fighter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Истребитель не найден",
        )

    return fighter

@router.post("/", status_code = status.HTTP_201_CREATED)
def create_fighter(fighter: FighterInput) -> FighterModel:
	return service.create(fighter)


@router.put("/{fighter_id}")
def update_fighter(fighter_id: int, fighter: FighterUpdate) -> FighterModel:
    updated_fighter = service.update(fighter_id, fighter)

    if updated_fighter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Истребитель не найден",
        )

    return updated_fighter
      

@router.delete("/{fighter_id}")
def delete_fighter(fighter_id: int) -> FighterModel:
    fighter = service.delete(fighter_id)

    if fighter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Истребитель не найден",
        )

    return fighter


