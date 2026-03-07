import json
import logging

logger = logging.getLogger(__name__)

class Export:
    def __init__(self, data) -> None:
        self.data: dict = self._isempty(data)

    def fetched_data(self) -> None:
        """Export raw fetched data converted to json"""
        if not self.data:
            return
        
        from config import appconfig

        try:
            with open(appconfig.path.raw_marks, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)

            logger.info("Export json successful")

        except Exception as e:
            logger.exception(e)

    def results(self) -> None:
        """Export subject and it's average"""
        if not self.data:
            return
        
        from config import appconfig

        try:
            with open(appconfig.path.results, "w", encoding="utf-8") as f:
                for s, a in self.data.items():
                    f.write(f"{s:30} {a}\n")
            logger.info("Export results successful")

        except Exception as e:
            logger.exception(e)

    @staticmethod
    def _isempty(data: dict) -> dict:
        if not data:
            logger.warning(f"No data to export")
            return {}
        
        return data