from __future__ import annotations
from collections import deque
from datetime import datetime 
import itertools
from textwrap import dedent

from .auth import Auth
from .const import Endpoint
from .exceptions import CalledEarlyUpdateError, UnexpectedResponseError


class LibreViewAPI():
    """
    This API provides an async Python interface to the LibreView REST API

    In order to maintain accurate reading history, I recommend selecting
    one connection { listConenctions() then selectConnection(int) } and
    sticking with it. Changing connections at this time will result in
    having history of both. May make this compatible with multiple
    connections in the future.

    LibreView API details from this source:
      https://libreview-unofficial.stoplight.io/'
    
    Thank you, FokkeZB! #WeAreNotWaiting

    This API also provides QoL functions, including:
    - Modeled Data
        - Classes for each kind of response section
    - Deltas
        - Minute-by-minute: delta between readings
        - Set interval: delta over a number of minutes up to x minutes (tbd)
    - Customized data
        - Receive only the latest reading instead of a long list of readings
        - Receive only readings relevant to the chosen connection
        - Receive only data in the desired units (mg/dl or libreview-configured)
    """

    def __init__(self, auth: Auth, maxReadings: int=10) -> None:
        """Initialize the API and store the auth so we can make requests."""
        self._auth = auth
        if maxReadings < 1:
            maxReadings = 1
        self._recentReadings: deque[GlucoseReading] = deque(maxlen=maxReadings)
        self._currentConnection = 0
        self._lastUpdateReadings = datetime.now()


    async def authenticate(self) -> bool:
        try:
            return await self._auth.authenticate()
        except:
            raise

    async def updateReadings(self) -> bool:
        deltaSinceLast = datetime.now() - self._lastUpdateReadings

        # Only grab readings at most once per minute, since that's how often
        # the device will auto-send glucose levels
        if deltaSinceLast.total_seconds() > 55:  
            raise CalledEarlyUpdateError("Update called within 1 min of last update")
        self._lastUpdateReadings = datetime.now()
        try:
            data = await self._auth.getConnections()
        except:
            raise

        reading = data[self._currentConnection].get("glucoseMeasurement")
        if reading is not None:
            self._recentReadings.appendleft(GlucoseReading(**reading))
            return True
        return False

    async def getLatestReading(self) -> GlucoseReading:

        try:
            await self.updateReadings()
        except:
            raise

        try:
            result = self._recentReadings[0]
        except IndexError:
            raise IndexError("Not enough readings available")

        return result

    async def getLastXReadings(self, numReadings: int=1) -> list[GlucoseReading]:
        if numReadings < 1 or numReadings > len(self._recentReadings):
            raise IndexError("Provide a number greater than 0 and less than the maximum number of saved readings (" + len(self._recentReadings) + ")")

        return list(itertools.islice(self._recentReadings,numReadings))

    async def listConnections(self) -> list[Connection]:
        try:
            data = await self._auth.getConnections()
        except:
            raise
        
        if data is not None:
            result = []
            for connection in data:
                result.append(Connection(**connection))
            return result
        raise UnexpectedResponseError("No data received from auth")


class GlucoseReading():
    """
    This class represents a single glucose reading interpreted from raw data.
    """

    # can be init with GlucoseReading(**response["data"]["glucoseMeasurement"])
    def __init__(self, Timestamp: str, ValueInMgPerDl: float, GlucoseUnits: int, Value: float, TrendArrow: int, **kwargs) -> None:
        self._timestamp = Timestamp
        self._mgdlValue = ValueInMgPerDl
        self._units = "mmol/l" if GlucoseUnits == 0 else "mg/dl"
        self._value = Value
        self._trendArrow = TrendArrow
        self._otherData = kwargs

    def __str__(self) -> str:
        result = """\
                 Timestamp: {timestamp}
                 Value: {value} {units}
                 Trend: {trend}\
                 """
        return dedent(result).format(timestamp=self._timestamp,
                                     value=self._value,
                                     units=self._units,
                                     trend=self._trendArrow
                                    )
    
    async def getAbsoluteValue(self) -> int:
        return self._mgdlValue

class Connection():
    def __init__(self, patientId: str, lastName: str, firstName: str, targetLow: int, targetHigh: int, **kwargs) -> None:
        self._patientID = patientId
        self._name = firstName + " " + lastName
        self._targets = {"low": targetLow, "high": targetHigh} #targets are always in mg/dl

    def __str__(self) -> str:
        result = """\
                 Name: {name}
                 ID: {id}
                 Range: {low} - {high}
                 """
        return dedent(result).format(name=self._name,
                                     id=self._patientID,
                                     low=self._targets.get("low"),
                                     high=self._targets.get("high")
                                    )

    async def isWithinTarget(self, reading: GlucoseReading) -> bool:
        value = await reading.getAbsoluteValue()
        if value >= self._targets["low"] and value <= self._targets["high"]:
            return True
        return False


# class Sensor():


# class AlarmRules():



# class GraphData():



# class LogbookData():



# class PatientDevice():



# class UserData():

# class AdditionalUserData():

# class AccountData():








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