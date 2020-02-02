#
#
# Ref: https://github.com/pulumi/pulumi/blob/master/dist/docker/Dockerfile

FROM python:3.7.5-slim

# GIT_COMMIT should be specified on the build command line
# Example: docker build -t vollgas/python-dev --build-arg GIT_COMMIT=$(git log -1 --format=%h) ./
# ARG GIT_COMMIT=unspecified

# Label Schema http://label-schema.org/
LABEL org.label-schema.schema-version="1.0.0-rc.1"
LABEL org.label-schema.name="vollgas-config"
# LABEL org.label-schema.vcs-url="https://bitbucket.org/chriskauffman/docker-python-complexity"
# LABEL org.label-schema.vcs-ref=${GIT_COMMIT}

# Organization and Project Labels
LABEL net.vollgas.project="vollgas-config"
LABEL net.vollgas.maintainer="chriskauffman@vollgas.net"

# ToDo: More labels - follow https://github.com/projectatomic/ContainerApplicationGenericLabels ?

# ADD VERSION .

# ARG PULUMI_VERSION=1.8.1

# Install deps all in one step
RUN apt-get update -y --quiet && \
  apt-get install -y --quiet \
    curl \
    git

# Update Python with correct packages
RUN pip install \
    --upgrade \
    --quiet \
    black \
    pytest \
    pylava

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
