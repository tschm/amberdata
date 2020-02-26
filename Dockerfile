# Set the base image to Ubuntu
FROM continuumio/miniconda3 as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

# We don't make pyserver installable. It's enough to copy it!
COPY pyamber         /amberdata/pyamber

# We don't make pyserver installable. It's enough to copy it!
#COPY requirements.txt /tmp/requirements.txt

# install all requirements...
RUN conda install -y -c conda-forge nomkl pandas=0.25.3 requests=2.22.0 flask=1.1.1 && \
    conda clean -y --all
    #&& \
    #pip install --no-cache-dir -r /tmp/requirements.txt && \
    #rm -r /tmp/requirements.txt


# ----------------------------------------------------------------------------------------------------------------------
FROM builder as production

COPY config           /amberdata/config

WORKDIR amberdata

# ----------------------------------------------------------------------------------------------------------------------
FROM builder as test

#ENV APPLICATION_SETTINGS="/amberdata/test/config/settings.cfg"

WORKDIR amberdata

RUN pip install --no-cache-dir httpretty pytest pytest-cov pytest-html requests-mock

CMD py.test --cov=pyamber  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html /amberdata/test

COPY test /amberdata/test

