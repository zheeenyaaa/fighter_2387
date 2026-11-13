from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from db_depends import get_async_db
from headers import get_language
from schemas import FighterInput, FighterModel, FighterMutation, FighterResource, FighterUpdate
# from services import FighterService
from translations import TRANSLATIONS
from sqlalchemy.ext.asyncio import AsyncSession
import repository 

router = APIRouter(prefix="/api/v1/fighters", tags=["fighters"])
# service = FighterService()
Language = Annotated[str, Depends(get_language)]
DbSession = Annotated[AsyncSession, Depends(get_async_db)]

def require_fighter(fighter: FighterModel | None, language: str) -> FighterModel:
    if fighter is None:
        raise HTTPException(status_code=404, detail=TRANSLATIONS[language]["not_found"])
    return fighter


def resource(fighter: FighterModel, request: Request, language: str) -> FighterResource:
    actions = {
        "self": ("get_fighter", "GET"),
        "create": ("create_fighter", "POST"),
        "update": ("update_fighter", "PUT"),
        "delete": ("delete_fighter", "DELETE"),
    }
    return FighterResource(
        **fighter.model_dump(),
        links={
            relation: {
                "href": str(request.url_for(route, **({} if relation == "create" else {"fighter_id": fighter.id}))),
                "method": method,
                "title": TRANSLATIONS[language][relation],
            }
            for relation, (route, method) in actions.items()
        },
    )


@router.get("/")
async def get_fighters(
        request: Request, 
        language: Language, 
        db: DbSession
    ) -> list[FighterResource]:
    fighters = await repository.list_fighters(db)
    return [resource(fighter, request, language) for fighter in fighters]


@router.get("/{fighter_id}")
async def get_fighter(
    fighter_id: int, 
    request: Request, 
    language: Language,
    db: DbSession
) -> FighterResource:
    fighter = require_fighter(await repository.get_fighter(db, fighter_id), language)
    return resource(fighter, request, language)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_fighter(
    fighter: FighterInput, 
    language: Language,
    db: DbSession
) -> FighterMutation:
    created = await repository.create_fighter(db, fighter)
    return FighterMutation(
        **created.model_dump(), 
        message=TRANSLATIONS[language]["created"]
    )


@router.put("/{fighter_id}")
async def update_fighter(
    fighter_id: int, 
    fighter: FighterUpdate, 
    language: Language,
    db: DbSession
) -> FighterMutation:
    updated = require_fighter(
        await repository.update_fighter(db, fighter_id, fighter), language
    )
    return FighterMutation(
        **updated.model_dump(),
        message=TRANSLATIONS[language]["updated"],
    )

@router.delete("/{fighter_id}")
async def delete_fighter(
    fighter_id: int, 
    language: Language,
    db: DbSession
) -> FighterMutation:
    deleted = require_fighter(await repository.delete_fighter(db, fighter_id), language)
    return FighterMutation(
        **deleted.model_dump(),
        message=TRANSLATIONS[language]["deleted"],
    )