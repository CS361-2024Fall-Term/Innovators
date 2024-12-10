from datetime import datetime, timedelta
import logging


def parse_date(date_input, formats=None):
    if isinstance(date_input, datetime):
        return date_input  # Already a datetime object
    elif isinstance(date_input, str):
        try:
            return datetime.strptime(date_input, "%Y-%m-%d %H:%M")
        except ValueError as e:
            logging.error(f"Invalid date format: {date_input}")
            return None
    else:
        logging.error(f"Unsupported date type: {type(date_input)}")
        return None


class NotificationService:
    def __init__(self, alert, feedback):
        self.alert = alert
        self.feedback = feedback
