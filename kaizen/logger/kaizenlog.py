import logging
import requests
import sys
import traceback


class KaizenLogHandler(logging.Handler):
    def __init__(self, service_url):
        super().__init__()
        self.service_url = service_url

    def emit(self, record):
        log_entry = self.format(record)
        try:
            response = requests.post(self.service_url, data={"log_data": log_entry})
            response.raise_for_status()
            analysis_result = response.json().get("analysis")
            if analysis_result:
                print(f"Potential issue detected: {analysis_result}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending log to KaizenLog service: {e}")


def exception_handler(exc_type, exc_value, exc_traceback, service_url):
    exception_info = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )
    try:
        response = requests.post(service_url, data={"log_data": exception_info})
        response.raise_for_status()
        analysis_result = response.json().get("analysis")
        if analysis_result:
            print(f"Potential issue detected: {analysis_result}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending log to KaizenLog service: {e}")


def init(service_url):
    handler = KaizenLogHandler(service_url)
    logger = logging.getLogger()
    logger.addHandler(handler)
    sys.excepthook = lambda exc_type, exc_value, exc_traceback: exception_handler(
        exc_type, exc_value, exc_traceback, service_url
    )
