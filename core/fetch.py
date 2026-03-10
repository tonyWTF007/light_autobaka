import logging
import re
import json
from typing import Any

import requests
from bs4 import BeautifulSoup

from config import appconfig
from utils import Mark, Export
from core.exceptions import LoginError, FetchError, DataExtractionError

logger = logging.getLogger(__name__)

def _extract_data(soup: BeautifulSoup) -> Any:
    regex_script = re.compile(r"model\.items\s*=\s*\[\{.*?}]")
    raw_script = soup.find("script", text=regex_script)

    if raw_script is None:
        error_script_not_found = "Script which contains data not found"
        logger.error(error_script_not_found)
        raise DataExtractionError(error_script_not_found)

    if (mark_data := re.search(r"\[\{.*?}]", raw_script.text, re.DOTALL)) is None:
        error_something_different = "Script doesn't contain what we expect"
        logger.error(error_something_different)
        raise DataExtractionError(error_something_different)

    if not (match := mark_data.group()):
        logger.warning("It seems that there aren't any marks")

    logger.info("Data successfully extracted")
    return json.loads(match)

def fetch_data(username: str, password: str) -> list["Mark"]:
    """
    Extracts mark data from a JSON object embedded in a script tag within the Bakalari HTML source.

    Returns:
        List[Mark]: List of parsed marks
    """
    payload = {
        "username": username,
        "password": password
    }

    with requests.session() as s:
        if s.post(str(appconfig.server.login_url), data=payload).status_code != 200:
            logging.critical("Login failed")
            raise LoginError("Login failed")

        r = s.get(str(appconfig.server.marks_url))
        if r.status_code != 200:
            logging.critical("Fetching data fails")
            raise FetchError("Fetching data fails")

    soup = BeautifulSoup(r.content, "lxml")
    logger.info("Data fetched successfully")

    data = _extract_data(soup)
    Export(data).fetched_data()
    
    return [Mark(**raw_mark) for raw_mark in data]
