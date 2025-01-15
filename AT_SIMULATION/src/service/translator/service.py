from src.service.translator.dependencies import IModelService


class TranslatorService:
    def __init__(
        self,
        model_service: IModelService,
    ) -> None:
        self._model_service = model_service

    def translate_model(self, model_id: int, user_id: int): ...

    def get_translated_files(self, user_id: int): ...
