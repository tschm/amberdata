FROM python:3.7.7-slim-stretch as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

# We don't make pyamber installable. It's enough to copy it!
COPY pyamber         /amberdata/pyamber

# install all requirements...
RUN pip install --no-cache-dir pandas==0.25.3 requests==2.23.0 flask==1.1.1

WORKDIR amberdata
# ----------------------------------------------------------------------------------------------------------------------
FROM builder as production

COPY config           /amberdata/config

# ----------------------------------------------------------------------------------------------------------------------
FROM builder as test

# install a bunch of test tools
RUN pip install --no-cache-dir httpretty pytest pytest-cov pytest-html requests-mock

CMD py.test --cov=pyamber  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html /amberdata/test

# copy over the tests
COPY test /amberdata/test

