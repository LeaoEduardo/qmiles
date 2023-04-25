FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR service

RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       firefox-esr

ENV FIREFOX_VERSION 112.0
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VERSION}/linux-x86_64/en-US/firefox-${FIREFOX_VERSION}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

ENV GECKODRIVER_VERSION 0.33.0
RUN wget -O driver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz 
RUN tar -xf driver.tar.gz && mkdir drivers && mv geckodriver drivers/geckodriver

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

ENTRYPOINT ["python", "-m", "src.web_scraper"]
CMD ["-k", "shared/kwargs.json"]