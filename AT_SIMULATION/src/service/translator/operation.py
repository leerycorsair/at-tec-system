from typing import List

from jinja2 import Environment, FileSystemLoader, Template

from src.repository.editor.resource.models.models import ResourceTypeDB
from src.repository.editor.template.models.models import OperationDB
from src.service.translator.utils import preprocess_template_code


TEMPLATE_DIR = "./src/service/translator/templates/"
TEMPLATE_NAME = "operation.jinja"

current_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)
template: Template = current_env.get_template(TEMPLATE_NAME)


def trnsl_operations(
    operations: List[OperationDB], resource_types: List[ResourceTypeDB]
) -> List[str]:
    def find_resource_type(resource_type_id: int) -> ResourceTypeDB:
        return next((rt for rt in resource_types if rt.id == resource_type_id), None)

    rendered_templates = []

    for operation in operations:
        rel_resources_info = {}
        for rel_resource in operation.meta.rel_resources:
            resource_type = find_resource_type(rel_resource.resource_type_id)
            if resource_type:
                rel_resources_info[rel_resource.id] = resource_type

        rendered_template = template.render(
            to_operation_tr(operation, rel_resources_info)
        )
        rendered_templates.append(rendered_template)

    return rendered_templates


def to_operation_tr(operation: OperationDB, rel_resources_info: dict) -> dict:
    params = [
        {"name": rel_resource.name, "type": rel_resources_info[rel_resource.id].name}
        for rel_resource in operation.meta.rel_resources
        if rel_resource.id in rel_resources_info
    ]

    param_names = [param["name"] for param in params]
    new_condition = preprocess_template_code(operation.body.condition, param_names)
    new_body_before = preprocess_template_code(operation.body.body_before, param_names)
    new_body_after = preprocess_template_code(operation.body.body_after, param_names)

    return {
        "template_name": operation.meta.name,
        "params": params,
        "condition": new_condition,
        "body_before": new_body_before,
        "body_after": new_body_after,
    }
