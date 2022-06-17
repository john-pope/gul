FROM python:3.10

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g ${GROUP_ID} user && \
    useradd -ms /bin/bash -l -u ${USER_ID} -g user user

RUN mkdir /app
RUN chown -R user:user /app
USER user

ENV ENVIRONMENT=production
RUN python -m pip install --upgrade pip

WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY --chown=user:user pyproject.toml /app

RUN $HOME/.poetry/bin/poetry config virtualenvs.create false \
  && $HOME/.poetry/bin/poetry install $(test "$ENVIRONMENT" == production && echo "--no-dev") --no-interaction --no-ansi

COPY ./api /app/api

CMD ["/home/user/.poetry/bin/poetry", "run", "/home/user/.local/bin/uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]