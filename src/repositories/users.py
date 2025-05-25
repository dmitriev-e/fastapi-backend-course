from src.schemas.users import UserResponse
from src.repositories.base import BaseRepository
from src.models.users import UsersORM

class UsersRepository(BaseRepository):
    model = UsersORM
    schema = UserResponse