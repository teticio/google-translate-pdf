# Use an AWS Lambda Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.9

# Install necessary packages
RUN yum update -y && \
    yum install -y wget unzip curl jq xorg-x11-server-Xvfb libXi libgbm libGConf2 nss libXScrnSaver libXtst alsa-lib liberation-mono-fonts libappindicator-gtk3 atk gtk3 u2f-hidraw-policy vulkan mesa-dri-drivers xdg-utils redhat-lsb-core && \
    yum clean all

# Install Chrome and Chromedriver
RUN LATEST_CHROME_RELEASE=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq '.channels.Stable') && \
    LATEST_CHROME_URL=$(echo "$LATEST_CHROME_RELEASE" | jq -r '.downloads.chrome[] | select(.platform == "linux64") | .url') && \
    wget -N "$LATEST_CHROME_URL" && \
    unzip chrome-linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chrome-linux64/chrome && \
    ln -s /usr/local/bin/chrome-linux64/chrome /usr/local/bin/chrome && \
    rm chrome-linux64.zip && \
    LATEST_CHROMEDRIVER_URL=$(echo "$LATEST_CHROME_RELEASE" | jq -r '.downloads.chromedriver[] | select(.platform == "linux64") | .url') && \
    wget -N "$LATEST_CHROMEDRIVER_URL" && \
    unzip chromedriver-linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver-linux64/chromedriver && \
    ln -s /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    rm chromedriver-linux64.zip

# Install Selenium
RUN pip install boto3 selenium undetected-chromedriver

# Add application code
COPY lambda.py /var/task
COPY utils.py /var/task

ENV FONTCONFIG_PATH=/opt/etc/fonts

# Set the CMD to the handler
CMD ["lambda.lambda_handler"]
