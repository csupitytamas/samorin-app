# Hivatalos Python image (könnyű, gyors)
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# WAIT-FOR-IT
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# A CMD helyett ENTRYPOINT-et írj, hogy shell-parancssorban fusson a wait-for-it
ENTRYPOINT ["/wait-for-it.sh", "jumpdepo-db:5433", "--"]

CMD ["gunicorn", "DjangoProject.wsgi:application", "--bind", "0.0.0.0:8000"]