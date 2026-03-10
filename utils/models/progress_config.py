from typing import Generator

class ProgressConfig:
    """Configuration for the progress update function"""

    def __init__(self, total_steps, progress):
        self.progress = progress
        self.total_steps = total_steps

        # create task
        self.task_id = self.progress.add_task("", total=self.total_steps)

        # Init generator
        self.counter = self._step_counter()
        self.description = f"{next(self.counter)}/{self.total_steps}"

    def update_progress(self) -> None:
            """Update progress rich bar"""
            self.progress.update(
                self.task_id,
                advance=1,
                description=f"{next(self.counter)}/{self.total_steps}"
            )

    @staticmethod
    def _step_counter() -> Generator[int]:
        """Return number of current task"""
        count = 0

        while True:
            yield count
            count += 1
