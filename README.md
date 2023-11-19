# libreview
A python wrapper for the LibreLinkUp API, with additional helper functions for interpreting CGM data

LibreView API details from this source:
      
      https://libreview-unofficial.stoplight.io/
    
    
Thank you, FokkeZB! #WeAreNotWaiting

LibreView API uses Semantic Versioning 2.0 (to the best of my ability as a new programmer)

https://semver.org/

Quickstart (probably not working yet, just draft):

in file.py:

import asyncio

from libreview import auth, libreview

async def main():
  
  myAuth = auth.Auth("emailaddress","password")
  
  myApi = libreview.LibreViewAPI(myAuth)

  response = await myApi.getLatestReading()

  print(response)
