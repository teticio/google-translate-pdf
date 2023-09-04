docker build -t google-translate-pdf . && \
docker run --rm --cpus 1 -m 1024m -p 9000:8080 \
    --tmpfs /tmp:rw,exec,size=512m \
    -e AWS_LAMBDA_FUNCTION_TIMEOUT=1000000 \
    google-translate-pdf
