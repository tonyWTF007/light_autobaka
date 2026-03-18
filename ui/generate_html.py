import logging

from jinja2 import Template
from config import appconfig

logger = logging.getLogger(__name__)

def create_html(context: dict["str", float]) -> None:
    """Generate HTML file with the results"""
    if not context:
        return

    with open(appconfig.path.html_template, "r", encoding="utf-8") as f:
        template_html = f.read()

    template = Template(template_html)

    with open(appconfig.path.html_output, "w", encoding="utf-8") as f:
        f.write(template.render(data=context))

    logger.debug("HTML file with results successfully generated")