from src.dto.db.user import DTOUserDB


class UserServiceInterface:
    def create_user(self, user: DTOUserDB) -> int:
        pass

    def generate_token(self, login: str, password: str) -> str:
        pass

    def verify_token(self, token: str) -> int:
        pass
