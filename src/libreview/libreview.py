from __future__ import annotations
from .auth import Auth
from collections import deque

from .const import Endpoint


class LibreViewAPI():
    """
    This API provides an async Python interface to the LibreView REST API

    This API also provides QoL functions, including:
    - Modeled Data
        - Classes for each kind of response section
    - Deltas
        - Minute-by-minute: delta between readings
        - Set interval: delta over a number of minutes up to x minutes (tbd)
    - Customized data
        - Receive only the latest reading instead of a long list of readings
        - Receive only data in the desired units (mg/dl or libreview-configured)
    """

    def __init__(self, auth: Auth, maxReadings: int=10) -> None:
        """Initialize the API and store the auth so we can make requests."""
        self._auth = auth
        self._recentReadings = deque(maxlen=maxReadings)


    async def authenticate(self) -> bool:
        self._auth.authenticate()
    
    async def getLatestReading(self,connection: int) -> GlucoseReading:
        
        return GlucoseReading();

    # async def _whatDoYouEvenCallThis(self) -> None:
        




class GlucoseReading():
    """
    This class represents a single glucose reading interpreted from raw data.
    """

    # can be init with GlucoseReading(**response["data"]["glucoseMeasurement"])
    def __init__(self, Timestamp: str, ValueInMgPerDl: float, GlucoseUnits: int, Value: float, TrendArrow: int) -> None:
        self._timestamp = Timestamp
        self._mgdlValue = ValueInMgPerDl
        self._units = "mmol/l" if GlucoseUnits == 0 else "mg/dl"
        self._value = Value
        self._trendArrow = TrendArrow

"""    
getconnections
.get("data").get("connection").get("glucoseMeasurement") latest data

getgraph 

.get("data").get("graphData")[0] = oldest (approx. 12 hours)
.get("data").get("graphData")[1] = newest (approx 30 min delay)
getlogbook

.get("data")[0] = latest, but may have been hours ago
.get("data")[last#] = oldest, up to 2 weeks ago
"""