import logging

from core.bootstrap import initialize
initialize()

logger = logging.getLogger(__name__)

# === Non-CI environment === #
# Rich handler
# DEBUG, INFO - hidden

# === CI environment === #
# everything should be displayed
# no rich handler, basic prompt

logger.debug("Debug test log")
logger.info("Info test log")
logger.warning("Warning test log")
logger.error("Error test log")
logger.critical("Critical test log")
