#core functionality

import asyncio

#uses HTTPConnection class to establish connection with target site and handle the HTTP requests
from http.client import HTTPConnection

#urlparse() used to help parse target URL's
from urllib.parse import urlparse

import aiohttp

#url takes input url, timeout will hold the number of seconds before time out connection attempts
def site_online(url, timeout=2):
    #immutable string below
    """Return True if the target URL is online.
    
    Raise an exception otherwise.
    """
    #defines a generic exception as a placeholder
    error = Exception("unknown error")

    #parser variable containing results of using urlparse()
    parser = urlparse(url)

    #uses or to extract the hostname from the url
    host = parser.netloc or parser.path.split("/")[0]

    #loops over HTTP and HTTPS ports to check availability on both ports
    for port in (80, 443):
        #creates a HTTPConnection instance using host, port and timeout arguments
        connection = HTTPConnection(host=host, port=port, timeout=timeout)

        #try attempts to make a HEAD request to the target website, returns true if successful, exception refers to the exception in error, 
        #finally then closes the connection
        try:
            connection.request("HEAD", "/")
            return True

        except Exception as e:
            error = e

        finally:
            connection.close()
    #raises the exception stored in error if finished without a successful request
    raise error


async def site_online_async(url, timeout=2):
    """Return True if the target URL is online.
    
    Raise an exception otherwise.
    """

    error = Exception("unknown error")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]
    for scheme in ("http", "https"):

        #builds a URL using the current scheme and hostname
        target_url = scheme + "://" + host

        #ClientSession class to handle HTTP requests with aiohttp
        async with aiohttp.ClientSession() as session:

            #try awaits a HEAD request to the target site by calling .head(), returns true if succeeds
            try:
                await session.head(target_url, timeout=timeout)
                return True
            
            #catches TimeoutError exceptions and sets error to a new instance
            except asyncio.exceptions.TimeoutError:
                error = Exception("timed out")

            #catches any other exception
            except Exception as e:
                error = e
    raise error