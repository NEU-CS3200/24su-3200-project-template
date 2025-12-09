FROM python:3.11-slim

WORKDIR /appcode

# downloads 
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  git \
  libfreetype6-dev \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*

# RUN mkdir /requirements
# COPY ./src/requirements.txt /requirements/requirements.txt

COPY ./src/requirements.txt .

RUN pip3 install -r requirements.txt

# lists all the packages
RUN ls 

EXPOSE 8501

# docker container runs streamlit
CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]