from aiohttp import ClientSession, ClientResponse
import asyncio

from .const import Endpoint, HEADERS, DEFAULT_HOST
from .exceptions import TOUNotAcceptedError, BadCredentialsError


# KNOWN_ENDPOINTS
#   "https://api.libreview.io"
#   "https://api-us.libreview.io"
#   "https://api-eu.libreview.io"
#   "https://api-eu2.libreview.io"



class Auth():
    """Creates an Auth object to pull data from LibreView using one set of account info"""

    def __init__(self, email: str, password: str) -> None:
        """Initialize Auth"""
        self._session = ClientSession()
        # self._create_session()
        self._host = DEFAULT_HOST.format("")
        self._authInfo = {"email": email, "password": password}
        self._accessToken = None

    def __del__(self) -> None:
        try:
            loop = asyncio.get_event_loop()
            asyncio.create_task(self._close_session())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._close_session())

    async def _close_session(self):
        if not self._session.closed:
            await self._session.close()

    async def _create_session(self):
        self._session = ClientSession()


    async def authenticate(self) -> ClientResponse:
        """
        Tries to acquire a valid token with the LibreView API.
        Uses username and password and raises additional errors.
        If redirect message received, will attempt to redirect manually.
        """
        try:
            response = await self.request(Endpoint.AUTH, data = self._authInfo)
        except:
            raise
        
        return response
        # match response.get("status")
        
    async def request(self, endpoint: Endpoint, **kwargs) -> ClientResponse:
        """Make a request."""
        data = kwargs.get("data")

        headers = HEADERS

        if endpoint != Endpoint.AUTH and self._accessToken is not None:
            headers["authorization"] = "Bearer " + self._accessToken          
        # need a way to call authenticate for accessToken if there isn't one
        # and then return to called function

        method = endpoint.method
        path = endpoint.path
        
        try:
            response = await self._session.request(
                method, f"{self._host}/{path}", json=data, headers=headers,
            )
            json_body = await response.json()
        except:
            raise
        
        status = json_body.get("status")
        
        #Error checking
        match status:
            case None:
                raise KeyError("There is no status in the response JSON")
            case 0: #good status
                pass
            case 2: #bad credentials
                raise BadCredentialsError("Double check your email address and password")
            case 4: #TOU needs to be accepted
                raise TOUNotAcceptedError("You need to manually accept the TOU on the LibreLinkUp app.")
            case _: # Other status issue, need to see the json to determine issue
                pass
        
        #Wants a redirect, gives status 0 anyway
        if json_body.get("data").get("redirect") is not None:
            redirect = json_body.get("data").get("region")
            self._host = DEFAULT_HOST.format("-"+redirect)
            return await self.request(endpoint, data=data)

        return json_body
        # return raw data with common (as in shared) error checking


