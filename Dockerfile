FROM python:3.6-alpine

ENV APP_BASE /opt/instability
ENV PYTHONPATH $APP_BASE

RUN mkdir -p $APP_BASE
COPY ./ $APP_BASE/
WORKDIR $APP_BASE

RUN pip install -e .

EXPOSE 8000
ENTRYPOINT ["python", "instability"]
