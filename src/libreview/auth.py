from aiohttp import ClientSession, ClientResponse, TCPConnector
import asyncio

from .const import Endpoint, HEADERS, DEFAULT_HOST
from .exceptions import TOUNotAcceptedError, BadCredentialsError, UnexpectedResponseError


# KNOWN_ENDPOINTS
#   "https://api.libreview.io"
#   "https://api-us.libreview.io"
#   "https://api-eu.libreview.io"
#   "https://api-eu2.libreview.io"



class Auth():
    """
    Creates an Auth object to pull data from LibreView using one set of account info.
    Only returns raw data, to be used by other programs as desired
    """

    def __init__(self, email: str, password: str) -> None:
        """Initialize Auth"""
        connector = TCPConnector(limit=5)
        self._session = ClientSession(connector=connector)
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


    async def authenticate(self) -> bool:
        """
        Tries to acquire a valid token with the LibreView API.
        Uses username and password and raises additional errors.
        If redirect message received, will attempt to redirect manually.
        """
        try:
            response = await self._request(Endpoint.AUTH, data = self._authInfo)
        except:
            raise

        try:
            isAuth = await self._setAuthFromTicket(response)
        except BadCredentialsError:
            raise

        return isAuth


    async def acceptTOU(self) -> bool:
        """
        To define, need testing capability (unaccepted tou)
        """
        return False

    async def getUser(self) -> dict:
        try:
            response = await self._request(Endpoint.GET_USER)
        except:
            raise

        return response.get("data") #dict 

    async def getAccount(self) -> dict:
        try:
            response = await self._request(Endpoint.GET_ACCOUNT)
        except:
            raise

        return response.get("data") #dict
    
    async def getConnections(self) -> list:
        try:
            response = await self._request(Endpoint.GET_CONNECTIONS)
        except:
            raise
        
        return response.get("data") #list of connections
    
    async def getGraph(self) -> dict:
        try:
            response = await self._request(Endpoint.GET_GRAPH)
        except:
            raise

        return response.get("data")
    
    async def getLogbook(self) -> list:
        try:
            response = await self._request(Endpoint.GET_LOGBOOK)
        except:
            raise

        return response.get("data") #list of logbook entries
    
    async def getNotiSettings(self) -> dict:
        try:
            response = await self._request(Endpoint.GET_NOTI_SETTINGS)
        except:
            raise

        return response.get("data")
    
    async def getConfig(self) -> dict:
        try:
            response = await self._request(Endpoint.GET_CONFIG)
        except:
            raise

        return response.get("data")
    

    async def _setAuthFromTicket(self, response: ClientResponse) -> bool:
        token = None
        try:
            token = response.get("ticket").get('token')
        except AttributeError: #no ticket in response
            try:
                token = response.get("data").get('authTicket').get('token')
            except AttributeError:
                raise BadCredentialsError("No ticket found")

        if token is not None:
            self._accessToken = token
            return True
        else:
            raise BadCredentialsError("No token found")


    async def _request(self, endpoint: Endpoint, **kwargs) -> dict:
        """
        Make a request.
        Does status checking
        Does auto-redirect
        Checks for data
        """
        data = kwargs.get("data")

        headers = HEADERS

        if endpoint != Endpoint.AUTH:
            if self._accessToken is not None:
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
                if json_body.get("message") == "missing or malformed jwt":
                    isAuthenticated = await self.authenticate()
                    if isAuthenticated == True:
                        return await self._request(endpoint,data=data)
                else:
                    raise KeyError("There is no status in the response JSON")
            case 0: #good status
                pass
            case 2: #bad credentials
                raise BadCredentialsError("Double check your email address and password")
            case 4: #TOU needs to be accepted
                raise TOUNotAcceptedError("You need to manually accept the TOU on the LibreLinkUp app.")
            case _: # Other status issue, need to see the json to determine issue
                pass
        
        if json_body.get("data") is not None:
            #Wants a redirect, gives status 0 anyway
            try:
                if json_body.get("data").get("redirect") is not None:
                    redirect = json_body.get("data").get("region")
                    self._host = DEFAULT_HOST.format("-"+redirect)
                    return await self._request(endpoint, data=data)
            except AttributeError: #returns list, not dict, no redirect here
                pass
            return json_body
        else:
            raise UnexpectedResponseError("No data in response body")
        # return raw data with common (as in shared) error checking



    # async def requestExact(self, endpoint: Endpoint, **kwargs) -> ClientResponse:
    #     """
    #     For testing only
    #     """
    #     data = kwargs.get("data")

    #     headers = HEADERS

    #     if endpoint != Endpoint.AUTH:
    #         if self._accessToken is not None:
    #             headers["authorization"] = "Bearer " + self._accessToken
    #     # need a way to call authenticate for accessToken if there isn't one
    #     # and then return to called function

    #     method = endpoint.method
    #     path = endpoint.path
        
    #     try:
    #         response = await self._session.request(
    #             method, f"{self._host}/{path}", json=data, headers=headers,
    #         )
    #         # json_body = await response.json()
    #     except:
    #         raise

    #     return response