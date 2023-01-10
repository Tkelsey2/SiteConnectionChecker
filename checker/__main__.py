#entry point script

import sys
import pathlib
import asyncio

from checker.checker import site_online, site_online_async
from checker.cli import cli_args, display_result

def main():
    """Run Checker."""
    user_args = cli_args()
    urls = _get_site_urls(user_args)

    #check if input is empty
    if not urls:
        print("Error: no URLs to chcek", file=sys.stderr)
        sys.exit(1)

    if user_args.asynchronous:
        asyncio.run(_asynchronous_check(urls))
    else:
        _synchronous_check(urls)

def _get_site_urls(user_args):

    #stores initial list of URLs provided at command line
    urls = user_args.urls

    #checks if URL file has been provided and checks results of _read_urls_from_file and adds to list
    if user_args.input_file:
        urls += _read_urls_from_file(user_args.input_file)

    #returns resulting list of URLs
    return urls

def _read_urls_from_file(file):

    #sets to pathlib.Path object to facilitate processing
    file_path = pathlib.Path(file)

    #checks if file is an actual file in local file system, it then opens file and reads its content using a list comprehension.
    #Comprehension strips any possible leading/ending whitespace from every line to prevent processing errors
    if file_path.is_file():
        with file_path.open() as urls_file:
            urls = [url.strip() for url in urls_file]

            #Nested conditional to check if any URL has been gathered
            if urls:
                return urls
            print(f"Error: empty input file, {file}", file=sys.stderr)

    else:
        print("Error: input file not found", file=sys.stderr)
    return []

async def _asynchronous_check(urls):
    async def _check(url):
        error = ""
        try:
            result = await site_online_async(url)
        except Exception as e:
            result = False
            error = str(e)
        display_result(result, url, error)
        
    await asyncio.gather(*(_check(url) for url in urls))

def _synchronous_check(urls):

    #loop interates over the target URLs
    for url in urls:

        #initialises and defines error
        error = ""

        #catches any exception that may occur during the checks
        try:
            result = site_online(url)
        except Exception as e:
            result = False
            error = str(e)

        #displays the connectivity check result
        display_result(result, url, error)

if __name__ == "__main__":
    main()