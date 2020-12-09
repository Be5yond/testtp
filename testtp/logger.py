from loguru import logger
import logging

class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logger.add(PropogateHandler(), format="{time:YYYY-MM-DD at HH:mm:ss} | {message}")
send = logger.level("SEND", no=38, color="<yellow>", icon="⬆")
recv = logger.level("RECV", no=38, color="<green>", icon="⬇")


