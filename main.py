from core.bootstrap import initialize
initialize()

import logging

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

from utils.constants import IS_GITHUB_ACTIONS
from core.fetch import  fetch_data
from core.calc import calc_marks

logger = logging.getLogger(__name__)

if not IS_GITHUB_ACTIONS:
    from utils.output import display_results
    from utils.models.progress_config import ProgressConfig
    from utils.models.export import Export

    # TODO: make progress bar updatable global
    # TODO: possible to add more than few checkpoints (a lot of is happening in the background)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        transient=True
    ) as progress:

        STEPS = ["Load Credentials", "Fetch Data", "Calculate Marks", "Export Results"]
        progress_config = ProgressConfig(len(STEPS), progress)

        progress_config.update_progress() # temporary represents loading configuration

        marks = fetch_data()
        progress_config.update_progress()

        average = calc_marks(marks)
        progress_config.update_progress()

        Export(average).results()
        progress_config.update_progress()

    display_results(average)
else:
    from ui.generate_html import create_html

    marks = fetch_data()

    average = calc_marks(marks)

    create_html(average)




