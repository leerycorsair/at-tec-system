from src.dto.db.user import DTOUserDB


class UserRepositoryInterface:
    def create_user(self, user: DTOUserDB) -> int:
        pass

    def get_user(self, login: str) -> DTOUserDB:
        pass
