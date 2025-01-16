from typing import List

from jinja2 import Environment, FileSystemLoader, Template

from src.repository.editor.resource.models.models import ResourceDB
from src.repository.editor.template.models.models import (
    TemplateUsageDB,
)


TEMPLATE_DIR = "./src/service/translator/templates/"
TEMPLATE_NAME = "template_usage.jinja"

current_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)
template: Template = current_env.get_template(TEMPLATE_NAME)


def trnsl_template_usages(
    template_usages: List[TemplateUsageDB], resources: List[ResourceDB]
) -> List[str]:
    def find_resource(resource_id: int) -> ResourceDB:
        return next((r for r in resources if r.id == resource_id), None)

    rendered_templates = []

    for template_usage in template_usages:
        args_info = {}
        for arg in template_usage.arguments:
            resource = find_resource(arg.resource_id)
            if resource:
                args_info[arg.id] = resource

        rendered_template = template.render(
            to_template_usage_tr(template_usage, args_info)
        )
        rendered_templates.append(rendered_template)

    return rendered_templates


def to_template_usage_tr(template_usage: TemplateUsageDB, args_info: dict) -> dict:
    args = [
        {"resource_name": args_info[arg.id].name}
        for arg in template_usage.arguments
        if arg.id in args_info
    ]

    return {
        "usage_name": template_usage.name,
        "args": args,
    }
