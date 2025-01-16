from typing import Dict, List

from jinja2 import Environment, FileSystemLoader, Template
from src.repository.editor.resource.models.models import ResourceTypeDB


TEMPLATE_DIR = "./src/service/translator/templates/"
TEMPLATE_NAME = "resource_type.jinja"

current_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)
template: Template = current_env.get_template(TEMPLATE_NAME)

TYPE_MAPPING: Dict[str, str] = {
    "INT": "int",
    "BOOL": "bool",
    "FLOAT": "float64",
}


def trnsl_resource_types(resource_types: List[ResourceTypeDB]) -> List[str]:
    rendered_templates = [
        template.render(
            resource_type=to_resource_type_tr(resource_type),
            enums=_collect_enums(resource_type),
        )
        for resource_type in resource_types
    ]
    return rendered_templates


def to_resource_type_tr(resource_type: ResourceTypeDB) -> dict:
    attrs = [
        {
            "name": attr.name,
            "go_type": (
                f"{resource_type.name.capitalize()}{attr.name.capitalize()}Enum"
                if attr.type == "ENUM"
                else TYPE_MAPPING.get(attr.type, "interface{}")
            ),
        }
        for attr in resource_type.attributes
    ]

    return {
        "name": resource_type.name,
        "attributes": attrs,
    }


def to_enum_tr(resource_type_name: str, attr_name: str, enum_values_set: List[str]) -> dict:
    enum_name = f"{resource_type_name.capitalize()}{attr_name.capitalize()}Enum"
    return {
        "name": enum_name,
        "values": enum_values_set,
    }


def _collect_enums(resource_type: ResourceTypeDB) -> List[dict]:
    enums = [
        to_enum_tr(resource_type.name, attr.name, attr.enum_values_set)
        for attr in resource_type.attributes
        if attr.type == "ENUM"
    ]
    return enums
