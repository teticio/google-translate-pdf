# Use an AWS Lambda Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.9

# Install Chrome
RUN yum update -y && \
    yum install -y curl gcc jq tar unzip wget && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    yum install -y ./google-chrome-stable_current_x86_64.rpm && \
    rm google-chrome-stable_current_x86_64.rpm && \
    yum clean all

# # Install Chrome for testing
# RUN yum update -y &&  \
#     yum install -y alsa-lib atk at-spi2-atk at-spi2-core bash ca-certificates cairo chkconfig curl expat glib2 glibc gtk3 jq libcurl libdrm libgcc libX11 libxcb libXcomposite libXdamage libXext libXfixes libxkbcommon libXrandr mesa-libgbm nspr nss nss-util pango tar unzip vulkan wget xdg-utils && \
#     LATEST_CHROME_RELEASE=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq '.channels.Stable') && \
#     LATEST_CHROME_URL=$(echo "$LATEST_CHROME_RELEASE" | jq -r '.downloads.chrome[] | select(.platform == "linux64") | .url') && \
#     wget -N "$LATEST_CHROME_URL" && \
#     unzip chrome-linux64.zip -d /usr/local/bin/ && \
#     chmod +x /usr/local/bin/chrome-linux64/chrome && \
#     ln -s /usr/local/bin/chrome-linux64/chrome /usr/bin/google-chrome && \
#     rm chrome-linux64.zip 

# # Install Chromium
# RUN yum install -y amazon-linux-extras curl gcc jq tar unzip wget && \
#     PYTHON=python2 amazon-linux-extras install -y epel && \
#     yum install -y chromium && \
#     mv /usr/bin/chromium-browser /usr/bin/google-chrome

# Install chromedriver (note that undetected-chromedriver downloads its own version of chromedriver)
RUN LATEST_CHROME_RELEASE=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq '.channels.Stable') && \
    LATEST_CHROMEDRIVER_URL=$(echo "$LATEST_CHROME_RELEASE" | jq -r '.downloads.chromedriver[] | select(.platform == "linux64") | .url') && \
    wget -N "$LATEST_CHROMEDRIVER_URL" && \
    unzip chromedriver-linux64.zip -d /opt/bin/ && \
    chmod +x /opt/bin/chromedriver-linux64/chromedriver && \
    ln -s /opt/bin/chromedriver-linux64/chromedriver /opt/bin/chromedriver && \
    rm chromedriver-linux64.zip

# Install Selenium
RUN pip install boto3 debugpy selenium undetected-chromedriver

# Add application code
COPY lambda.py /var/task
COPY utils.py /var/task

# For debugging
COPY .vscode /var/task/.vscode

# Hack to make Chrome work in Lambda
COPY wrap_chrome_binary /opt/bin/wrap_chrome_binary
RUN /opt/bin/wrap_chrome_binary

# Set the CMD to the handler
CMD ["lambda.lambda_handler"]
