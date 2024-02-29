FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python scripts
COPY cbre_ml.py /app/
COPY prediction.py /app/
COPY broker_list.py /app/

# Run your scripts in the desired order
RUN python cbre_ml.py
RUN python prediction.py
RUN python broker_list.py

COPY . .
# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]

EXPOSE 8000
