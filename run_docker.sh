docker build -t google-translate-pdf .
docker run --rm --cpus 1 -m 1024m -p 9000:8080 \
    --read-only --tmpfs /tmp:rw,exec,size=512m \
    google-translate-pdf
