from pydantic import BaseModel

from config.models.path_config import PathConfig
from config.models.server_config import ServerConfig
from utils.constants import DEFAULT_PATH_CONFIG

class AppConfig(BaseModel):
    server: ServerConfig
    path: PathConfig = PathConfig(**DEFAULT_PATH_CONFIG)
