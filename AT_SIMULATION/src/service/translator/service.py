from typing import List

from src.service.translator.dependencies import IModelService
from src.service.translator.function import trnsl_functions
from src.service.translator.models.models import FileMeta, TranslateInfo
from src.service.translator.resource import trnsl_resources
from src.service.translator.resource_type import trnsl_resource_types


class TranslatorService:
    def __init__(
        self,
        model_service: IModelService,
    ) -> None:
        self._model_service = model_service

    def translate_model(self, model_id: int, user_id: int) -> TranslateInfo:
        model = self._model_service.get_model(model_id, user_id)

        resource_types = trnsl_resource_types(model.resource_types)
        print("\n".join(resource_types))
        
        resources = trnsl_resources(model.resources, model.resource_types)
        print("\n".join(resources))
        
        functions = trnsl_functions(model.functions)
        print("\n".join(functions))

        return TranslateInfo(
            file_id=0,
            file_content="LOL",
            translate_logs="KEK",
        )

    def get_translated_files(self, user_id: int) -> List[FileMeta]:
        return []

    # def _trnsl_resources(self) -> str: ...

    # def _trnsl_irregular_events(self) -> str: ...

    # def _trnsl_operations(self) -> str: ...

    # def _trnsl_rules(self) -> str: ...

    # def _trnsl_template_usages(self) -> str: ...

    # def _trnsl_functions(self) -> str: ...
