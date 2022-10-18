FROM rasa/rasa-sdk:3.1.1
WORKDIR /app
#COPY ./actions/ /app/actions/
COPY requirements.txt requirement.txt
USER root
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt
#CMD ["start","--actions","actions"]
EXPOSE 5055
USER 1001