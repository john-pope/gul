FROM python:3.10

ENV ENVIRONMENT=production

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g ${GROUP_ID} user && \
  useradd -ms /bin/bash -l -u ${USER_ID} -g user user

RUN mkdir /ssl
RUN apt-get update && apt-get upgrade -y && apt-get install ssl-cert
RUN make-ssl-cert /usr/share/ssl-cert/ssleay.cnf /ssl/self-signed-cert

RUN mkdir /app
RUN chown -R user:user /app /ssl
USER user

RUN python -m pip install --upgrade pip

WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY --chown=user:user pyproject.toml /app

RUN $HOME/.poetry/bin/poetry config virtualenvs.create false \
  && $HOME/.poetry/bin/poetry install $(test "$ENVIRONMENT" == production && echo "--no-dev") --no-interaction --no-ansi

WORKDIR /app/api

COPY --chown=user:user ./api /app/api
COPY --chown=user:user ./docker/entrypoint.sh /app/docker/entrypoint.sh

ENTRYPOINT [ "/bin/bash", "/app/docker/entrypoint.sh" ]
CMD [ "/app/docker/run-app" ]
