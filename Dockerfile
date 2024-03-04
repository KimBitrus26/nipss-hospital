FROM python:3.9

ENV APP_HOME=/home/nipss
RUN mkdir $APP_HOME

# set work directory
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt $APP_HOME
RUN pip install -r requirements.txt

# copy project
COPY . $APP_HOME

COPY ./entrypoint.sh $APP_HOME

ENTRYPOINT ["sh", "/home/nipss/entrypoint.sh"]
