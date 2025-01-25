from typing import List

from jinja2 import Environment, FileSystemLoader, Template

from src.repository.editor.resource.models.models import ResourceDB
from src.repository.editor.template.models.models import (RelevantResourceDB,
                                                          TemplateMetaDB,
                                                          TemplateUsageDB)

TEMPLATE_DIR = "./src/service/translator/templates/"
TEMPLATE_NAME = "template_usage.jinja"

current_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)
template: Template = current_env.get_template(TEMPLATE_NAME)


def trnsl_template_usages(
    template_usages: List[TemplateUsageDB],
    templates: List[TemplateMetaDB],
    resources: List[ResourceDB],
) -> List[str]:
    def find_resource(resource_id: int) -> ResourceDB:
        return next((r for r in resources if r.id == resource_id), None)

    def find_template(template_id: int) -> TemplateMetaDB:
        return next((t for t in templates if t.id == template_id), None)

    def find_relevant_resource(
        relevant_resource_id: int, rel_resources: List[RelevantResourceDB]
    ) -> RelevantResourceDB:
        return next((r for r in rel_resources if r.id == relevant_resource_id), None)

    rendered_templates = []

    for template_usage in template_usages:
        tmpl = find_template(template_usage.template_id)

        args_info = {}
        for arg in template_usage.arguments:
            resource = find_resource(arg.resource_id)
            relevant_resource = find_relevant_resource(
                arg.relevant_resource_id,
                tmpl.rel_resources,
            )
            if resource:
                args_info[arg.id] = {
                    "resource": resource,
                    "relevant_resource": relevant_resource,
                }

        rendered_template = template.render(
            to_template_usage_tr(template_usage, tmpl, args_info)
        )
        rendered_templates.append(rendered_template)

    return rendered_templates


def to_template_usage_tr(
    template_usage: TemplateUsageDB,
    tmpl: TemplateMetaDB,
    args_info: dict,
) -> dict:
    args = [
        {
            "resource_name": args_info[arg.id]["resource"].name,
            "relevant_resource_name": args_info[arg.id]["relevant_resource"].name,
        }
        for arg in template_usage.arguments
        if arg.id in args_info
    ]

    return {
        "template_name": tmpl.name,
        "usage_name": template_usage.name,
        "args": args,
    }
