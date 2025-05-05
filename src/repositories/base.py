from fastapi import HTTPException
from sqlalchemy import delete, select, insert, update
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session
    
    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
 
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    # Template for adding new record to database
    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        return result.scalars().one()

    # Template for editing record in database
    async def edit(self, data: BaseModel, partial_update: bool = False, **filter_by) -> BaseModel:
        # If record exists, update it and the only one
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        len_result = len(result.scalars().all())
        match len_result:
            case 0:
                raise HTTPException(status_code=404, detail="Record not found")
            case 1:
                update_stmt = update(self.model).values(**data.model_dump(exclude_unset=partial_update)).filter_by(**filter_by).returning(self.model)
                result = await self.session.execute(update_stmt)
                return result.scalars().one()
            case _:
                raise HTTPException(status_code=400, detail="Multiple records found")


    # Template for deleting record from database
    async def delete(self, **filter_by) -> None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        len_result = len(result.scalars().all())
        match len_result:
            case 0:
                raise HTTPException(status_code=404, detail="Record not found")
            case 1:
                delete_stmt = delete(self.model).filter_by(**filter_by)
                await self.session.execute(delete_stmt)
            case _:
                raise HTTPException(status_code=400, detail="Multiple records found")
            