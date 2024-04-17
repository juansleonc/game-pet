FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade Flask


COPY . .
# CMD ["gunicorn", "-w 4", "-b 0.0.0.0:5000", "wsgi:app"]
CMD ["flask", "run", "--host=0.0.0.0"]


