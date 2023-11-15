from aiohttp import ClientSession, ClientResponse
import asyncio

from .const import Endpoint, HEADERS, DEFAULT_HOST



# KNOWN_ENDPOINTS
#   "https://api.libreview.io"
#   "https://api-us.libreview.io"
#   "https://api-eu.libreview.io"
#   "https://api-eu2.libreview.io"



class Auth():
    """Creates an Auth object to pull data from LibreView using one set of account info"""

    def __init__(self, session: ClientSession, email: str, password: str) -> None:
        """Initialize Auth"""
        self._session = session
        self._host = DEFAULT_HOST.format("")
        self._authInfo = {"email": email, "password": password}
        self._patientID = None
        self._connectionID = None
        self._accessToken = None

    async def authenticate(self) -> bool:
        """
        Tries to acquire a valid token with the LibreView API.
        Uses username and password and raises additional errors.
        If redirect message received, will attempt to redirect manually.
        """
        try:
            response = await self.request(Endpoint.AUTH, data = self._authInfo)
        except:
            raise
        
        return True
        # match response.get("status")
        
    async def request(self, endpoint: Endpoint, **kwargs) -> ClientResponse:
        """Make a request."""
        data = kwargs.get("data")

        headers = HEADERS

        if endpoint != Endpoint.AUTH and self._accessToken is not None:
            headers["authorization"] = "Bearer " + self._accessToken          
        # need a way to call authenticate for accessToken if there isn't one
        # and then return to called function

        method = Endpoint.endpoint.method
        path = Endpoint.endpoint.path
        
        response = await self._session.request(
            method, f"{self._host}/{path}", data, headers=headers,
        )
        # return raw data with no (?) error checking
