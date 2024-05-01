# Import necessary modules
import re
from django import template
import markdown2

register = template.Library()


@register.filter
def custom_markdown(value):
    # Convert markdown content to HTML
    html_content = markdown2.markdown(value)

    # Define a function to format all code blocks uniformly
    def format_code(match):
        code = match.group(1)
        # Wrap code block with <pre> tag for formatting
        return f"<pre>{code}</pre>"

    # Use regular expression to find all code blocks and apply formatting
    html_content = re.sub(
        r"```.*?\n(.*?)\n```", format_code, html_content, flags=re.DOTALL
    )

    return html_content
