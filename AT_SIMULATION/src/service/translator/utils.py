import re
from typing import List


def preprocess_template_code(code: str, params: List[str]) -> str:
    sorted_params = sorted(params, key=len, reverse=True)

    param_pattern = (
        r"(?<![\w.\"\'])("
        + "|".join(re.escape(param) for param in sorted_params)
        + r")(?![\w])"
    )

    def replace_param(match):
        param_name = match.group(1)
        return f"t.{param_name}"

    new_code = re.sub(param_pattern, replace_param, code)
    return new_code
