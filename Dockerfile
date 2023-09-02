# Use an AWS Lambda Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.9

# Install necessary packages (detemined with check_deps.sh script)
RUN yum update -y && \
    yum install -y alsa-lib atk at-spi2-atk at-spi2-core bash ca-certificates cairo chkconfig curl expat glib2 glibc gtk3 jq libcurl libdrm libgcc libX11 libxcb libXcomposite libXdamage libXext libXfixes libxkbcommon libXrandr mesa-libgbm nspr nss nss-util pango unzip vulkan wget xdg-utils && \
    yum clean all

# Install Chrome
RUN LATEST_CHROME_RELEASE=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq '.channels.Stable') && \
    LATEST_CHROME_URL=$(echo "$LATEST_CHROME_RELEASE" | jq -r '.downloads.chrome[] | select(.platform == "linux64") | .url') && \
    wget -N "$LATEST_CHROME_URL" && \
    unzip chrome-linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chrome-linux64/chrome && \
    ln -s /usr/local/bin/chrome-linux64/chrome /usr/local/bin/chrome && \
    rm chrome-linux64.zip

# Install Selenium
RUN pip install boto3 selenium undetected-chromedriver

# Add application code
COPY lambda.py /var/task
COPY utils.py /var/task

ENV FONTCONFIG_PATH=/tmp

# Set the CMD to the handler
CMD ["lambda.lambda_handler"]
