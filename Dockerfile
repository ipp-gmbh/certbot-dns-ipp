FROM certbot/certbot

COPY dist/certbot_dns_ipp-*.tar.gz /tmp/certbot_dns_ipp.tar.gz

RUN pip install --no-cache-dir /tmp/certbot_dns_ipp.tar.gz \
    && rm /tmp/certbot_dns_ipp.tar.gz

ENTRYPOINT ["/usr/bin/env"]
