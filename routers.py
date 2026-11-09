from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from headers import get_language
from models import FighterInput, FighterModel, FighterMutation, FighterResource, FighterUpdate
from services import FighterService
from translations import TRANSLATIONS

router = APIRouter(prefix="/api/v1/fighters", tags=["fighters"])
service = FighterService()
Language = Annotated[str, Depends(get_language)]


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
def get_fighters(request: Request, language: Language) -> list[FighterResource]:
    return [resource(fighter, request, language) for fighter in service.read()]


@router.get("/{fighter_id}")
def get_fighter(fighter_id: int, request: Request, language: Language) -> FighterResource:
    return resource(require_fighter(service.read(fighter_id), language), request, language)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_fighter(fighter: FighterInput, language: Language) -> FighterMutation:
    return FighterMutation(**service.create(fighter).model_dump(), message=TRANSLATIONS[language]["created"])


@router.put("/{fighter_id}")
def update_fighter(fighter_id: int, fighter: FighterUpdate, language: Language) -> FighterMutation:
    updated = require_fighter(service.update(fighter_id, fighter), language)
    return FighterMutation(**updated.model_dump(), message=TRANSLATIONS[language]["updated"])


@router.delete("/{fighter_id}")
def delete_fighter(fighter_id: int, language: Language) -> FighterMutation:
    deleted = require_fighter(service.delete(fighter_id), language)
    return FighterMutation(**deleted.model_dump(), message=TRANSLATIONS[language]["deleted"])
