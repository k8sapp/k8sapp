FROM python:3.7
  
RUN apt-get -q update && apt-get install -y -q \
  sqlite3 vim --no-install-recommends \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG C.UTF-8

# Setup Python virtual environment
RUN pip install --upgrade pip virtualenv
RUN virtualenv /venv
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH
RUN python -m pip install --upgrade pip

# Setup app
RUN mkdir -p /opt/app/k8sapp
RUN mkdir -p /opt/app/k8sapp/pip_cache
COPY . /opt/app/k8sapp
COPY .pip_cache /opt/app/k8sapp/pip_cache/
# pip install dependencies
WORKDIR /opt/app/k8sapp
RUN pip install -r requirements.txt --cache-dir /opt/app/k8sapp/pip_cache
RUN chown -R www-data:www-data /opt/app

EXPOSE 8020
#CMD ["gunicorn", "auth.wsgi", "--bind", "0.0.0.0:8020", "--workers", "1"]
CMD ["gunicorn", "auth.wsgi", "--bind", "0.0.0.0:8020"]
# You can also include relevant commands in a shell script and run it from here
# Dockerfile can only have one CMD statement so if there is a need to include
# multiple commands, use a shell script and execute from here
#CMD ["/opt/app/start-server.sh"]

