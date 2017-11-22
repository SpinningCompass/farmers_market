# Use an official Python runtime as a parent image
FROM python:2.7-slim
COPY . /app
# Run app.py when the container launches
CMD ["python", "/app/farmers-market.py"]
