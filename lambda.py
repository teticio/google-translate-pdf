import base64

from utils import translate_pdf


def lambda_handler(event, context):
    pdf = base64.b64decode(event["pdf"])
    translated_pdf = translate_pdf(pdf)
    return {"translated_pdf": base64.b64encode(translated_pdf).decode("utf-8")}
