FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN dvc repro
EXPOSE 8501
ENTRYPOINT ["chainlit","run"]
CMD ["app.py"]