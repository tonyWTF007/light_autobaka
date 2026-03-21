import os
from pathlib import Path

IS_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

USERNAME_ENV_TAG = "BAKA_USERNAME"
PASSWORD_ENV_TAG = "BAKA_PASSWORD"

if not IS_GITHUB_ACTIONS:
    CONFIG_PATH = PROJECT_ROOT / "config.toml"
else:
    SCHOOL_DATA_TAG = "SCHOOL_DATA"

DEFAULT_PATH_CONFIG = {
    "raw_marks": "./output/marks.json",
    "results": "./output/results.txt",
    "log": "./output/logs.log",
    "html_template": "./ui/template_index.html",
    "html_output": "./index.html"
}
