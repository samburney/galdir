FROM lsiobase/alpine:3.9

LABEL maintainer 'Sam Burney <sam@burney.io>'

ENV GALDIR_LISTEN=0.0.0.0:6543 \
    GALDIR_SITENAME=GalDir \
    GALDIR_ALBUMS=albums \
    GALDIR_CACHE=cache \
    GALDIR_ITEMS_PERPAGE=8

RUN apk add --update \
    git \
    python3 \
    libjpeg zlib \
    gcc musl-dev python3-dev zlib-dev jpeg-dev \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install Pillow \
    && apk del gcc musl-dev python3-dev zlib-dev jpeg-dev \
    && rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /var/cache/distfiles/* /root/.cache/pip

RUN git clone https://github.com/samburney/galdir.git /usr/local/share/galdir \
    && python3 -m pip install -e /usr/local/share/galdir

ADD ./docker/root/ /

EXPOSE 6543/tcp

ENTRYPOINT [ "/init" ]
