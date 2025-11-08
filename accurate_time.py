import ntplib
from datetime import datetime
    

def get_ntp_time() -> datetime:
    """
    Establish a connection with time.google.com (Google's NTP Server).

    @return a datetime object of the time returned by Google.
    """
    
    client = ntplib.NTPClient()
    response = client.request('time.google.com', version=3)

    return datetime.fromtimestamp(response.tx_time)

