FROM python:3.11.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/
COPY requirements.txt /app/

RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . /app/

# Use python's builtin webserver for now for simplicity
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
