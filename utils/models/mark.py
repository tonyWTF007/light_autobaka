import logging
from typing import Annotated, Any
from datetime import datetime

from pydantic import Field, BeforeValidator, BaseModel

logger = logging.getLogger(__name__)

def _clean_mark(m: str) -> float:
    """
    Convert str to int & from '1-' (which is not number) make '-1'

    Args:
        m (str): mark to check
    Returns:
        int | str: correct mark
    """

    m = m.strip()

    if len(m) > 1:
        return float(m[0]) + 0.5
    
    if m.isnumeric():
        return float(m)
    else:
        return 0.0

def _is_empty(s: Any) -> str:
    """Tell me if there is missing value"""
    
    if s is None:
        logger.warning("Field is empty")
    
    return s

MissingDescription = Annotated[
    str | None,
    BeforeValidator(_is_empty),
    Field(default="Missing")
]

MarkValue = Annotated[
    float,
    BeforeValidator(_clean_mark),
    Field(alias="MarkText")
]

class Mark(BaseModel):
    """Represent one mark fetched from bakalari website"""

    caption: Annotated[MissingDescription, Field(description="description of mark")] = None
    subject: str = Field(alias="nazev", description="name of the subject")
    date: Annotated[str | None | datetime, MissingDescription, Field(alias="datum", description="date when mark was added to baka system")] = None
    weight: int = Field(ge=1, le=10, alias="vaha", description="Weight of the mark")
    mark: MarkValue