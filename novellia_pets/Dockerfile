FROM python:3.10.16
ENV PYTHONUNBUFFERED=1
RUN mkdir /api
WORKDIR /api
COPY requirements.txt /api
RUN pip install -r requirements.txt
COPY . /api/

# copy from the current directory of the Dockerfile to /api in the image
EXPOSE 8000