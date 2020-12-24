# Import modules
import time
import argparse
from enum import Enum
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Prefix variable added before each URL
HTTPS_PREFIX = "https://"

# Amount of time to wait and allow for JavaScript to execute
WAIT_FOR_JAVASCRIPT_EXECUTION_SECS = 5

# This yields a list of the all the names of JavaScript requests that have been executed on the
# website
WEBSITE_JAVASCRIPT_REQUEST_NAMES = """return window.performance.getEntriesByType("resource")
.filter(e => e.initiatorType === 'script').map(e => e.name.match(/.+\/([^?]+)/)[1]); """

# Variables corresponding to analytics tracking code names
GOOGLE_ANALYTICS_TRACKING_CODE_NAME = 'Google Analytics'
CHARTBEAT_TRACKING_CODE_NAME = 'Chartbeat'
FACEBOOK_PIXEL_TRACKING_CODE_NAME = 'Facebook Pixel'

# Variable corresponding to the names of JavaScript requests
# Documentation for each JavaScript request is found in the README.md
GOOGLE_ANALYTICS_JS_REQUEST_NAME = 'analytics.js'
CHARTBEAT_JS_REQUEST_NAME = 'chartbeat'
FACEBOOK_PIXEL_JS_REQUEST_NAME = 'fbevents.js'


# Enumerate analytics code names to their JavaScript requests
class AnalyticsTrackingCode(Enum):
    GOOGLE_ANALYTICS_TRACKING_CODE_NAME = GOOGLE_ANALYTICS_JS_REQUEST_NAME
    CHARTBEAT_TRACKING_CODE_NAME = CHARTBEAT_JS_REQUEST_NAME
    FACEBOOK_PIXEL_TRACKING_CODE_NAME = FACEBOOK_PIXEL_JS_REQUEST_NAME


def open_website_return_javascript_requests(url):
    """
    Function takes a URL and opens it via the ChromeDriver. The driver waits for a set JavaScript
    execution time beforescraping for JavaScript requests and returning them in list form. The
    website and driver are closed.

    Parameters:
    url (string): The domain that will be opened, loaded and scraped for JavaScript (www.XYZ.com)

    Returns:
    website_javascript_request_list (list): A list of JavaScript requests from the scraped domain
    """

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(HTTPS_PREFIX + url)
    time.sleep(WAIT_FOR_JAVASCRIPT_EXECUTION_SECS)
    website_javascript_request_list = driver.execute_script(WEBSITE_JAVASCRIPT_REQUEST_NAMES)
    driver.close()

    return website_javascript_request_list


def is_js_request_in_list(website_js_request_list, js_request_name):
    """
    Function takes a dictionary, a list of JavaScript requests, a tracking code name (key) and
    specific JavaScriptrequest name. The function will search through the JavaScript request list to
    see if a specific instance of JavaScript exists in it. The function will populate the
    dictionary with a key/value pair consisting of the name (key) and a True/False (value).

    Parameters:
    dictionary (dictionary): A dictionary to be populated by function
    website_js_list (list): A list of JavaScript requests
    tracking_code_name (string): A string which will be used as the dictionary key (name of
    JavaScript request)
    javascript_name (string): A string which will be searched for in the website_js list (
    JavaScript request)

    Returns:
    dictionary (dictionary): Dictionary containing the name of the JavaScript request and a
    boolean (True/False) value for the existence of the JavaScript request.
    """

    return any(js_request_name in js for js in website_js_request_list)


def check_website_for_analytics_javascript(url):
    """
    Function takes a URL ('www.XYZ.com') and accesses it using selenium. The webpage is loaded
    and all JavaScript requests are returned to a list. The list is used to check if the webpage
    has Google Analytics, Chartbeat and a Facebook Pixel. The results are returned in a dictionary.

    Parameters:
    url (string): URL of website ('www.XYZ.com') to be checked

    Returns:
    dict_js (dictionary): Dictionary containing website and a boolean (True/False) value for
    Google Analytics,
    Chartbeat and Facebook Pixel JavaScript request.
    """

    # Open and scrape url for JavaScript requests
    website_javascript_request_list = open_website_return_javascript_requests(url)

    website_js_dictionary = dict()
    website_js_dictionary['URL'] = domain

    # Check for a Google Analytics, Chartbeat and Facebook Pixel
    website_js_dictionary[GOOGLE_ANALYTICS_TRACKING_CODE_NAME] = is_js_request_in_list(
        website_javascript_request_list,
        AnalyticsTrackingCode.GOOGLE_ANALYTICS_TRACKING_CODE_NAME.value)
    website_js_dictionary[CHARTBEAT_TRACKING_CODE_NAME] = is_js_request_in_list(
        website_javascript_request_list, AnalyticsTrackingCode.CHARTBEAT_TRACKING_CODE_NAME.value)
    website_js_dictionary[FACEBOOK_PIXEL_TRACKING_CODE_NAME] = is_js_request_in_list(
        website_javascript_request_list,
        AnalyticsTrackingCode.FACEBOOK_PIXEL_TRACKING_CODE_NAME.value)

    return website_js_dictionary


# To run from the terminal provide the websites for which the scraper should check by using the
# ```--domains``` argument. Example: python check_javascript.py --domains www.echobox.com
if __name__ == "__main__":
    CLI = argparse.ArgumentParser()
    CLI.add_argument(
        "--domains",
        nargs="*",
        type=str,
        default="",
    )

    # Parse the command line
    ARGS = CLI.parse_args()
    for domain in ARGS.domains:
        print(check_website_for_analytics_javascript(domain))
