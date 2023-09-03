# Use an AWS Lambda Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.9

# Install Chrome
RUN yum update -y && \
    yum install -y curl jq unzip wget && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    yum install -y ./google-chrome-stable_current_x86_64.rpm && \
    rm google-chrome-stable_current_x86_64.rpm && \
    yum clean all

# Install chromedriver (note that undetected-chromedriver downloads its own version of chromedriver)
RUN LATEST_CHROME_RELEASE=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq '.channels.Stable') && \
    LATEST_CHROMEDRIVER_URL=$(echo "$LATEST_CHROME_RELEASE" | jq -r '.downloads.chromedriver[] | select(.platform == "linux64") | .url') && \
    wget -N "$LATEST_CHROMEDRIVER_URL" && \
    unzip chromedriver-linux64.zip -d /opt/bin/ && \
    chmod +x /opt/bin/chromedriver-linux64/chromedriver && \
    ln -s /optbin/chromedriver-linux64/chromedriver /opt/bin/chromedriver && \
    rm chromedriver-linux64.zip

# Install Selenium
RUN pip install boto3 selenium undetected-chromedriver

# Add application code
COPY lambda.py /var/task
COPY utils.py /var/task

# Set the CMD to the handler
CMD ["lambda.lambda_handler"]
