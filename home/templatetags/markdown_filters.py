import re
from django import template
import markdown2

register = template.Library()


@register.filter
def custom_markdown(value):
    html_content = markdown2.markdown(value)

    def format_code(match):
        code = match.group(1)
        return f"<pre>{code}</pre>"

    html_content = re.sub(
        r"```.*?\n(.*?)\n```", format_code, html_content, flags=re.DOTALL
    )

    return html_content
