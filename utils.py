import base64
import json
import os
import unittest.mock as mock
from tempfile import NamedTemporaryFile, TemporaryDirectory
from time import sleep

import boto3

with mock.patch("multiprocessing.Lock", return_value=object()):
    import undetected_chromedriver as uc

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 1000000


def translate_pdf(pdf: bytearray) -> bytearray:
    with NamedTemporaryFile(suffix=".pdf") as tmp_file, TemporaryDirectory() as tmp_dir:
        tmp_file.write(pdf)

        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--single-process")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        options.add_argument("--v=0")
        options.add_argument(f"--homedir={tmp_dir}")
        options.add_argument(f"--disk-cache-dir={tmp_dir}/cache-dir")
        options.add_argument(f"--user-data-dir={tmp_dir}/user-data")
        options.add_argument(f"--data-path={tmp_dir}/data-path")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        )
        options.add_experimental_option(
            "prefs", {"download.default_directory": tmp_dir}
        )
        driver = uc.Chrome(options=options)

        driver.get("https://translate.google.com/?sl=auto&tl=en&op=docs")

        WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Accept all')]")
            )
        ).click()

        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        ).send_keys(tmp_file.name)

        WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(), 'Translate')]]")
            )
        ).click()

        paths = [
            "//button[.//span[contains(text(), 'Download translation')]]",
            "//button[.//span[contains(text(), 'Got it')]]",
        ]

        def check_elements_clickable(driver):
            for xpath in paths:
                try:
                    element = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    if element:
                        return element
                except WebDriverException:
                    continue
            return None

        element = WebDriverWait(driver, TIMEOUT).until(check_elements_clickable)
        if element.text == "Got it":
            # Google is telling us to try again later
            return b""
        element.click()

        output_filename = os.path.join(tmp_dir, os.path.basename(tmp_file.name))
        while not (
            os.path.exists(output_filename)
            or os.path.exists(output_filename + ".crdownload")
        ):
            sleep(0.1)
        while os.path.exists(output_filename + ".crdownload"):
            sleep(0.1)

        driver.close()

        with open(output_filename, "rb") as file:
            translated_pdf = file.read()

    return translated_pdf


def translate_pdf_proxy(pdf):  ##
    lambda_client = boto3.client("lambda")
    response = lambda_client.invoke(
        FunctionName="google-translate-pdf",
        InvocationType="RequestResponse",
        Payload=bytes(
            json.dumps({"pdf": base64.b64encode(pdf).decode("utf-8")}), encoding="utf-8"
        ),
    )
    response = json.loads(response["Payload"].read())
    return base64.b64decode(response["translated_pdf"])
