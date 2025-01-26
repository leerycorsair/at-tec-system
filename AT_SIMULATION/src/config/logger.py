import json
import logging

from pythonjsonlogger import jsonlogger


def setup_logger(logger_name: str = "application_logger") -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()

    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def format(self, record):
            log_record = super().format(record)
            try:
                return json.dumps(json.loads(log_record), indent=4)
            except Exception:
                return log_record

    formatter = CustomJsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s %(details)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logging.getLogger("uvicorn").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)

application_logger = setup_logger()
