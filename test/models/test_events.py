from datetime import datetime, timedelta
from src.models.event import Event

def test_get_location():
    start_time = datetime.now() - timedelta(hours =1)
    end_time = datetime.now() + timedelta(hours =1)
    event = Event("CS class", "Software engineering", start_time, end_time, location="LINC")

    assert event.get_location() == "LINC"