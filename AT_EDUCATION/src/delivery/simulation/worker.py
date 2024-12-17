from at_queue.core.at_component import ATComponent
from at_queue.utils.decorators import component_method

from delivery.response import SomeResponse
from delivery.simulation.models.resource import (ResourceRequest,
                                                 ResourceTypeRequest)
from delivery.simulation.models.responses import (EditorResponse,
                                                  TranslatorResponse)
from delivery.simulation.models.template import (IrregularEventRequest,
                                                 OperationRequest, RuleRequest,
                                                 TemplateUsageRequest)


class SimulationWorker(ATComponent):
    @component_method
    def handle_resource_type(
        self,
        in_params: ResourceTypeRequest,
        out_params: EditorResponse,
    ) -> SomeResponse:
        pass

    @component_method
    def handle_resource(
        self,
        in_params: ResourceRequest,
        out_params: EditorResponse,
    ) -> SomeResponse:
        pass

    @component_method
    def handle_operation_template(
        self,
        in_params: OperationRequest,
        out_params: EditorResponse,
    ) -> SomeResponse:
        pass

    @component_method
    def handle_rule_template(
        self,
        in_params: RuleRequest,
        out_params: EditorResponse,
    ) -> SomeResponse:
        pass

    @component_method
    def handle_irregular_event_template(
        self,
        in_params: IrregularEventRequest,
        out_params: EditorResponse,
    ) -> SomeResponse:
        pass

    @component_method
    def handle_template_usage(
        self,
        in_params: TemplateUsageRequest,
        out_params: EditorResponse,
    ) -> SomeResponse:
        pass

    @component_method
    def handle_translate(
        self,
        in_params: Something,  # еще не знаю
        out_params: TranslatorResponse,
    ) -> SomeResponse:
        pass
