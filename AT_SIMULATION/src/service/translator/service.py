from typing import List

from src.service.translator.dependencies import IModelService
from src.service.translator.function import trnsl_functions
from src.service.translator.irregular_event import trnsl_irregular_events
from src.service.translator.models.models import FileMeta, TranslateInfo
from src.service.translator.operation import trnsl_operations
from src.service.translator.resource import trnsl_resources
from src.service.translator.resource_type import trnsl_resource_types
from src.service.translator.rule import trnsl_rules
from src.service.translator.template_usage import trnsl_template_usages


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

        rules = trnsl_rules(model.rules, model.resource_types)
        print("\n".join(rules))

        operations = trnsl_operations(model.operations, model.resource_types)
        print("\n".join(operations))

        irregular_events = trnsl_irregular_events(
            model.irregular_events, model.resource_types
        )
        print("\n".join(irregular_events))

        metas = []
        metas.extend([template.meta for template in model.irregular_events])
        metas.extend([template.meta for template in model.operations])
        metas.extend([template.meta for template in model.rules])
        # order by meta.name
        template_usages = trnsl_template_usages(
            model.template_usages, metas, model.resources
        )
        print("\n".join(template_usages))

        return TranslateInfo(
            file_id=0,
            file_content="\n".join(resource_types)
            + "\n".join(resources)
            + "\n".join(functions)
            + "\n".join(rules)
            + "\n".join(operations)
            + "\n".join(irregular_events)
            + "\n".join(template_usages),
            translate_logs="empty",
        )

    def get_translated_files(self, user_id: int) -> List[FileMeta]:
        return []

    # def _trnsl_resources(self) -> str: ...

    # def _trnsl_irregular_events(self) -> str: ...

    # def _trnsl_operations(self) -> str: ...

    # def _trnsl_rules(self) -> str: ...

    # def _trnsl_template_usages(self) -> str: ...

    # def _trnsl_functions(self) -> str: ...
