#command line interface

import argparse

def cli_args():
    """Handle the CLI arguments and options"""
    parser = argparse.ArgumentParser(
        #defines the programs name and adds a suitable description
        prog="checker", description="check the availablity of websites"
    )

    #metavar: sets the name for the argument, nargs: tells argparse to accept a list of CL arguments after -u or --urls switch
    #type: sets the data type of the CL argument, in this case it is a string
    #default: setsthje CL argument to an empty list by default
    #help provides the help message for the added argument
    parser.add_argument(
        "-u",
        "--urls",
        metavar="URLs",
        nargs="+",
        type=str,
        default=[],
        help="enter one or more website URLs")

    #CL argument addition for inputting text file for checking
    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="read URLs from a file",
    )

    #CL argument addition for asynchronous checking
    parser.add_argument(
        "-a",
        "--asynchronous",
        action="store_true",
        help="run the connectivity check asynchronously"
    )

    return parser.parse_args()


#tests to see if result is true or false and prints appropriate response
def display_result(result, url, error=""):
    """Display the result of a connectivity check."""
    print(f'The status of "{url}" is: ', end=" ")
    if result:
        print('"Online!" 👍')
    else:
        print(f'"Offline?" 👎 \n Error: "{error}"')