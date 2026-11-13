from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Fighter
from schemas import FighterInput, FighterModel, FighterUpdate


async def list_fighters(db: AsyncSession) -> list[FighterModel]:
    rows = await db.scalars(select(Fighter).order_by(Fighter.id))
    return [
        FighterModel.model_validate(row, from_attributes=True)
        for row in rows
    ]


async def get_fighter(db: AsyncSession, fighter_id: int) -> FighterModel | None:
    row = await db.get(Fighter, fighter_id)
    if row is None:
        return None
    return FighterModel.model_validate(row, from_attributes=True)


async def create_fighter(db: AsyncSession, data: FighterInput) -> FighterModel:
    async with db.begin():
        row = Fighter(**data.model_dump())
        db.add(row)
        await db.flush()
        return FighterModel.model_validate(row, from_attributes=True)


async def update_fighter(
    db: AsyncSession, fighter_id: int, data: FighterUpdate
) -> FighterModel | None:
    statement = (
        update(Fighter)
        .where(Fighter.id == fighter_id)
        .values(**data.model_dump())
        .returning(Fighter)
    )
    async with db.begin():
        row = (await db.scalars(statement)).one_or_none()
        if row is None:
            return None
        return FighterModel.model_validate(row, from_attributes=True)


async def delete_fighter(db: AsyncSession, fighter_id: int) -> FighterModel | None:
    statement = (
        delete(Fighter)
        .where(Fighter.id == fighter_id)
        .returning(Fighter)
    )
    async with db.begin():
        row = (await db.scalars(statement)).one_or_none()
        if row is None:
            return None
        return FighterModel.model_validate(row, from_attributes=True)