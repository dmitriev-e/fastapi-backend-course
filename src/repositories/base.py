from fastapi import HTTPException
from sqlalchemy import delete, select, insert, update
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session
    
    # Repository Template for getting all records from database
    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(res, from_attributes=True) for res in result.scalars().all()]
 
    # Repository Template for getting one record from database
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        return self.schema.model_validate(res, from_attributes=True)
    
    # Repository Template for adding new record to database
    async def add(self, data: BaseModel):
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_stmt)
            res = result.scalars().one()
            return self.schema.model_validate(res, from_attributes=True)
        except IntegrityError as e:
            raise e

    # Repository Template for editing record in database
    async def edit(self, data: BaseModel, partial_update: bool = False, **filter_by):
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
                res = result.scalars().one()
                return self.schema.model_validate(res, from_attributes=True)
            case _:
                raise HTTPException(status_code=400, detail="Multiple records found")


    # Repository Template for deleting record from database
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
            