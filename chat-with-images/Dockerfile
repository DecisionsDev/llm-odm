FROM python:3.9 as builder
WORKDIR /code

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

COPY requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt && chmod a+x /code/serverStart.sh
COPY . /code

EXPOSE $GRADIO_SERVER_PORT


CMD ["/code/serverStart.sh"]

