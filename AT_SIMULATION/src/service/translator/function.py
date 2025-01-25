from typing import List

from jinja2 import Environment, FileSystemLoader, Template

from src.repository.editor.function.models.models import FunctionDB

TEMPLATE_DIR = "./src/service/translator/templates/"
TEMPLATE_NAME = "function.jinja"

current_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)
template: Template = current_env.get_template(TEMPLATE_NAME)


def trnsl_functions(functions: List[FunctionDB]) -> List[str]:
    rendered_templates = [template.render(function=function) for function in functions]
    return rendered_templates
