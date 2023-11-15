from .auth import Auth



class LibreViewAPI():
    """
    This API provides an async Python interface to the LibreView REST API

    This API also provides QoL functions, including:
    - Deltas
        - Minute-by-minute: delta between readings
        - Set interval: delta over a number of minutes up to x minutes (tbd)
    - Customized data
        - Receive only the latest reading instead of a long list of readings
        - Receive only data in the desired units (mg/dl or libreview-configured)
    """

    def __init__(self, auth: Auth):
        """Initialize the API and store the auth so we can make requests."""
        self._auth = auth
    
    async def 


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

    

    