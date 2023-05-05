# pull official base image
FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# set path
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/home/mpharma/app

## SETTING UP THE APP ##
RUN mkdir -p  $APP_HOME
WORKDIR $APP_HOME

# Copy in the application code and Chown all the files to the app user.
COPY . $APP_HOME

RUN ls -l $APP_HOME

RUN pip install --upgrade pip install  --upgrade pip
RUN pip install --upgrade pip install  --no-cache-dir -r requirements.txt

VOLUME ["/app"]

# Add executable permissions to the file
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/home/mpharma/app/entrypoint.sh"]

