FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY model.py .
COPY student_model.pkl .

EXPOSE 9000

CMD ["seldon-core-microservice", "StudentPerformanceModel", "REST"]