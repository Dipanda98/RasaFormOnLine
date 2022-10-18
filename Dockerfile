# NB! when updating make sure the version is in sync with:
# * rasa version in requirements.txt
# * RASA_VERSION and RASA_X_VERSION  in .github/workflows/continuous-deployment.yml
# Pull SDK image as base image
FROM rasa/rasa:3.2.10-full

#ENTRYPOINT []
# Use subdirectory as working directory
WORKDIR /app
USER root
COPY . /app
#ADD . /app

# Change to root user to install dependencies
#USER 1001
RUN rasa train
USER 1001
VOLUME /app/models

#RUN apt-get update -qq
#RUN apt-get install software-properties-common
#RUN apt-get install -y --no-install-recommends
  # required by psycopg2 at build and runtime
#RUN apt-get install -y libpq-dev
  # required for health check
#RUN apt-get install -y curl
#RUN apt-get install -y git
#RUN apt-get autoremove -y

# Make sure that all security updates are installed
#RUN apt-get update && apt-get dist-upgrade -y --no-install-recommends
# Install extra requirements for actions code
CMD ["run", "-m", "/app/models", "--enable-api", "--cors","*", "--debug", "--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]


EXPOSE 5005