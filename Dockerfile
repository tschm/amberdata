# Set the base image to Ubuntu
FROM continuumio/miniconda3 as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

# We don't make pyserver installable. It's enough to copy it!
COPY pyamber         /amberdata/pyamber

# We don't make pyserver installable. It's enough to copy it!
COPY requirements.txt /tmp/requirements.txt

# install all requirements...
RUN conda install -y -c conda-forge nomkl pandas=1.0.1 requests=2.22.0 && \
    conda clean -y --all && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -r /tmp/requirements.txt


# ----------------------------------------------------------------------------------------------------------------------
FROM builder as production
# or shall I do copy?
# COPY --from=builder / /

ENV APPLICATION_SETTINGS="/amberdata/config/settings.cfg"

COPY config           /amberdata/config

# copy files such as build_whoosh, etc.
# COPY *.py             /amberdata/

# Expose Jupyter port & cmd
# EXPOSE 8000
WORKDIR amberdata

#CMD python start.py

# ----------------------------------------------------------------------------------------------------------------------
FROM builder as test

ENV APPLICATION_SETTINGS="/amberdata/test/config/settings.cfg"

WORKDIR amberdata

RUN pip install --no-cache-dir httpretty pytest pytest-cov pytest-html requests-mock
#pytest-mock requests-mock

CMD py.test --cov=pyamber  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html /amberdata/test

COPY test /amberdata/test

