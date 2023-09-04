import base64

# import debugpy
# debugpy.listen(5678)
# debugpy.wait_for_client()
# debugpy.breakpoint()

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
    # import logging
    # import subprocess
    # import selectors

    # logging.basicConfig(level=logging.INFO)
    # logger = logging.getLogger(__name__)
    # browser = subprocess.Popen(
    #     [
    #         "/bin/google-chrome",
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
    #         "--log-level=0",
    #     ],
    #     stdin=subprocess.PIPE,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    #     close_fds=True,
    # )
    # selector = selectors.DefaultSelector()

    # def read_from_fileno(fileno):
    #     if fileno == browser.stdout.fileno():
    #         line = browser.stdout.readline()
    #         if line:
    #             logger.info(line.decode("utf-8").strip())
    #     elif fileno == browser.stderr.fileno():
    #         line = browser.stderr.readline()
    #         if line:
    #             logger.error(line.decode("utf-8").strip())

    # # Register the stdout and stderr streams for read events
    # selector.register(browser.stdout, selectors.EVENT_READ)
    # selector.register(browser.stderr, selectors.EVENT_READ)

    # # Monitor the streams for any data to read
    # while True:
    #     for key, _ in selector.select():
    #         read_from_fileno(key.fileobj.fileno())

    #     # Check if the process has terminated
    #     if browser.poll() is not None:
    #         break

    # # Close the selector to free up resources
    # selector.close()

    pdf = base64.b64decode(event["pdf"])
    translated_pdf = translate_pdf(pdf)
    return {"translated_pdf": base64.b64encode(translated_pdf).decode("utf-8")}
