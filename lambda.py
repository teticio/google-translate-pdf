import base64

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
    pdf = base64.b64decode(event["pdf"])
    translated_pdf = translate_pdf(pdf)
    return {"translated_pdf": base64.b64encode(translated_pdf).decode("utf-8")}
