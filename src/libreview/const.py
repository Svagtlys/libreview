from enum import Enum

class Endpoint(Enum):
    AUTH = "POST", "llu/auth/login"
    ACCEPT_TOU = "POST", "auth/continue/tou"
    GET_USER = "GET", "user"
    GET_ACCOUNT = "GET", "account"
    GET_CONNECTIONS = "GET", "llu/connections"
    GET_GRAPH = "GET", "llu/connections/{patientID}/graph"
    GET_LOGBOOK = "GET", "llu/connections/{patientID}/logbook"
    GET_NOTI_SETTINGS = "GET", "llu/notifications/settings/{connectionID}"
    GET_CONFIG = "GET", "llu/config/country"


    def __init__(self, method, path):
        self.method = method
        self.path = path
    #For GET_GRAPH, GET_LOGBOOK, GET_NOTI_SETTINGS, use .format()
    #eg Endpoint.GET_GRAPH.format(patientID="patientID")

HEADERS = {
    # required headers
    "accept-encoding": "gzip",
    "cache-control": "no-cache",
    "connection": "Keep-Alive",
    "content-type": "application/json",
    "product": "llu.android",
    "version": "4.8.0"
    # the version could change as the app is updated, might add option to change this in config
}

DEFAULT_HOST = "https://api{}.libreview.io"