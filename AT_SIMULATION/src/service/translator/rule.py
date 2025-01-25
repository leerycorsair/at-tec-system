from typing import List

from jinja2 import Environment, FileSystemLoader, Template

from src.repository.editor.resource.models.models import ResourceTypeDB
from src.repository.editor.template.models.models import RuleDB
from src.service.translator.utils import preprocess_template_code

TEMPLATE_DIR = "./src/service/translator/templates/"
TEMPLATE_NAME = "rule.jinja"

current_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)
template: Template = current_env.get_template(TEMPLATE_NAME)


def trnsl_rules(rules: List[RuleDB], resource_types: List[ResourceTypeDB]) -> List[str]:
    def find_resource_type(resource_type_id: int) -> ResourceTypeDB:
        return next((rt for rt in resource_types if rt.id == resource_type_id), None)

    rendered_templates = []

    for rule in rules:
        rel_resources_info = {}
        for rel_resource in rule.meta.rel_resources:
            resource_type = find_resource_type(rel_resource.resource_type_id)
            if resource_type:
                rel_resources_info[rel_resource.id] = resource_type

        rendered_template = template.render(to_rule_tr(rule, rel_resources_info))
        rendered_templates.append(rendered_template)

    return rendered_templates


def to_rule_tr(rule: RuleDB, rel_resources_info: dict) -> dict:
    params = [
        {
            "name": rel_resource.name,
            "type": rel_resources_info[rel_resource.id].name,
        }
        for rel_resource in rule.meta.rel_resources
        if rel_resource.id in rel_resources_info
    ]

    param_names = [param["name"] for param in params]
    new_condition = preprocess_template_code(rule.body.condition, param_names)
    new_body = preprocess_template_code(rule.body.body, param_names)

    return {
        "template_name": rule.meta.name,
        "params": params,
        "condition": new_condition,
        "body": new_body,
    }
