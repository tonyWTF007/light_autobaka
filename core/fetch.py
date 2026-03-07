import logging
import re
import json
from typing import Any

import requests
from bs4 import BeautifulSoup

from config import appconfig
from utils import Mark, Export

logger = logging.getLogger(__name__)

def _extract_data(soup: BeautifulSoup) -> Any:
    regex_script = re.compile(r"model\.items\s*=\s*")
    raw_script = soup.find("script", string=regex_script) # pyright: ignore[reportArgumentType, reportCallIssue]
    if raw_script is None:
        logger.error("Marks not found")

    raw_data = re.search(r"\[\{.*?\}\]", raw_script.text, re.DOTALL)
    if raw_data is None:
        logger.error("Marks not found")

    logger.info("Data successfully extracted")
    return json.loads(raw_data.group()) # pyright: ignore[reportOptionalMemberAccess]

def fetch_data(username: str, password: str) -> list["Mark"]:
    """
    Fetch data from bakalari website
    You receive entire html source code and there's one script where u can find
    everything what you need. Than javascript is converted to json style

    Args:
        username (str):
        password (str):

    Returns:
        List[Mark]: List of parsed marks
    """
    payload = {
        "username": username,
        "password": password
    }

    with requests.session() as s:
        if s.post(str(appconfig.server.login_url), data=payload).status_code != 200:
            logger.critical("Login failed")
            exit()

        r = s.get(str(appconfig.server.marks_url))
        if r.status_code != 200:
            logger.critical("Error with interacting on mark's page")
            exit()

    soup = BeautifulSoup(r.content, "html.parser")
    logger.info("Data fetched sucessfully")

    data = _extract_data(soup)

    Export(data).fetched_data()
    
    return [Mark(**raw_mark) for raw_mark in data]