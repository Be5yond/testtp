from loguru import logger

send = logger.level("SEND", no=38, color="<yellow>", icon="⬆")
recv = logger.level("RECV", no=38, color="<green>", icon="⬇")

