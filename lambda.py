import base64
import os

import debugpy

if "LOCAL_LAMBDA" in os.environ:
    debugpy.listen(5678)
    debugpy.wait_for_client()
    debugpy.breakpoint()

from utils import translate_pdf


def lambda_handler(event, context):  # pylint: disable=unused-argument
    """
    AWS Lambda function handler to translate a PDF file.

    Args:
        event (dict): AWS Lambda function event data.
                       It should contain a key "pdf" with base64 encoded PDF data as the value.
        context (obj): AWS Lambda function context object.

    Returns:
        dict: A dictionary containing the key "translated_pdf" with the translated PDF data
              (base64 encoded) as the value.
    """
    # import http
    # import json
    # import logging
    # import subprocess
    # import tempfile
    # from time import sleep

    # logging.basicConfig(level=logging.INFO)
    # logger = logging.getLogger(__name__)

    # with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
    #     binary = "/usr/bin/google-chrome"
    #     args = [
    #         "--disable-gpu",
    #         "--disable-dev-shm-usage",
    #         "--hide-scrollbars",
    #         "--single-process",
    #         "--ignore-certificate-errors",
    #         "--homedir=/tmp",
    #         "--disk-cache-dir=/tmp/cache-dir",
    #         "--data-path=/tmp/data-path",
    #         "--remote-debugging-host=127.0.0.1",
    #         "--remote-debugging-port=43631",
    #         "--headless",
    #         "--user-data-dir=/tmp",
    #         "--lang=en-US",
    #         "--no-default-browser-check",
    #         "--no-first-run",
    #         "--no-sandbox",
    #         "--test-type",
    #         "--headless=new",
    #         "--window-size=1920,1080",
    #         "--start-maximized",
    #         "--no-sandbox",
    #         "--log-level=10",
    #         "--log-file=/tmp/chrome.log",
    #         "--enable-logging",
    #         "--v=1",
    #     ]

    #     logger.debug("Start browser")
    #     browser = subprocess.Popen(
    #         [
    #             binary,
    #             *args,
    #         ],
    #         stdin=subprocess.PIPE,
    #         stdout=stdout,
    #         stderr=stderr,
    #         close_fds=True,
    #     )
    #     logger.debug("Browser PID: " + str(browser.pid))

    #     while True:
    #         try:
    #             conn = http.client.HTTPConnection(host="127.0.0.1", port=43631)
    #             conn.request("GET", "/json/version")
    #             response = conn.getresponse()
    #             if response.status == 200:
    #                 break
    #         except Exception as e:
    #             logger.error(f"GET request failed due to {str(e)}")
    #             sleep(5)
    #     logger.debug("Browser response: " + response.read().decode("ascii"))

    #     logger.debug("Start chromedriver")
    #     process = subprocess.Popen(
    #         [
    #             "/opt/bin/chromedriver",
    #             "--port=51957",
    #             "--verbose",
    #         ],
    #         env=os.environ,
    #         stdout=stdout,
    #         stderr=stderr,
    #         stdin=subprocess.DEVNULL,
    #         creationflags=0,
    #     )
    #     sleep(5)
    #     logger.debug("Chromedriver PID: " + str(process.pid))

    #     logger.debug("Make request to chromedriver")
    #     conn = http.client.HTTPConnection(host="127.0.0.1", port=51957, timeout=60)
    #     try:
    #         conn.request(
    #             "POST",
    #             "/session",
    #             body=json.dumps(
    #                 {
    #                     "capabilities": {
    #                         "firstMatch": [{}],
    #                         "alwaysMatch": {
    #                             "browserName": "chrome",
    #                             "pageLoadStrategy": "normal",
    #                             "goog:chromeOptions": {
    #                                 "extensions": [],
    #                                 "binary": binary,
    #                                 "args": args,
    #                                 "debuggerAddress": "127.0.0.1:43631",
    #                             },
    #                         },
    #                     }
    #                 }
    #             ),
    #             headers={
    #                 "Accept": "application/json",
    #                 "Content-Type": "application/json;charset=UTF-8",
    #                 "User-Agent": "selenium/4.12.0 (python linux)",
    #                 "Connection": "keep-alive",
    #             },
    #         )
    #         response = conn.getresponse()
    #         logger.debug("Chromedriver response: " + response.read().decode("ascii"))
    #     except Exception as e:
    #         logger.error(f"POST request failed due to {str(e)}")

    #     stderr.seek(0)
    #     logger.error("STDERR: " + str(stderr.read().decode("utf-8")))
    #     stdout.seek(0)
    #     logger.error("STDOUT: " + str(stdout.read().decode("utf-8")))
    #     with open("/tmp/chrome.log", "r") as file:
    #         logger.debug("Chrome log: " + str(file.read()))

    # return {"translated_pdf": base64.b64encode(b"").decode("utf-8")}

    pdf = base64.b64decode(event["pdf"])
    translated_pdf = translate_pdf(pdf)
    return {"translated_pdf": base64.b64encode(translated_pdf).decode("utf-8")}
