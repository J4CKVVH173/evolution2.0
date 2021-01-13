import logging
import logging.config as logging_config
from typing import List

from cells.live.base import BaseLive

from .config import LOGGING

logging_config.dictConfig(LOGGING)

INFO_LOGGER = logging.getLogger("info_logger")
GENOME_LOGGER = logging.getLogger("genome_logger")


class Log:
    @classmethod
    def log_genome(cls, cells: List[BaseLive], epoch: int) -> None:
        for_logs = dict()
        for cell in cells:
            for_logs[cell.get_clan_name] = cell.save_genome()
        GENOME_LOGGER.info(f'{"-"*20}\n{epoch}\n{for_logs}\n{"-"*20}')

    @classmethod
    def log_info(cls, epoch: int, cells_count: int) -> None:
        INFO_LOGGER.info(f"{epoch}  {cells_count}")
