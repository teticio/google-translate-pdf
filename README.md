# Google Translate PDF

Demo to run Google Translate on a PDF file using Selenium and AWS Lambda. As the limit for PDFs to be translated is 10 Mb, the script splits the PDF into documents with a selection of pages and translates them separately. AWS Lambda further restricts the size of the payload to 6 Mb, and translated documents may be twice the size of the original, so the `split_size` parameter should be set to 3 or less in this case.

## Installation

```bash
pip install -r requirements.txt
```

## Running

Run locally (Google will throttle you after a while):

```bash
python google_translate_pdf.py --input_pdf /pth/to/input/pdf --output_pdf /path/to/output/pdf --split_size 10
```

Run in AWS Lambda (currently not working see https://github.com/teticio/google-translate-pdf/issues/1):

```bash
terraform init
terraform apply --auto-approve
python google_translate_pdf.py --input_pdf /pth/to/input/pdf --output_pdf /path/to/output/pdf --split_size 3
```

## Developmemt

To run in a local AWS Lambda function, set the environment variable `LOCAL_LAMBDA` and run the Docker container with `./run_docker.sh´.

If you uncomment the following lines in `lambda.py`, you can debug the Docker container with Visual Studio Code:

```python
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()
debugpy.breakpoint()
```

In this case you should run the Docker container with `./debug_docker.sh` as Visual Studio Code requires the container file system to be writeable. The `AWS_LAMBDA_FUNCTION_TIMEOUT` is also overridden.

## Disclaimer

This is intended as a demo for web-scraping using Selenium in an AWS Lambda function. Please use it responsibly and respect Google's terms of service.
