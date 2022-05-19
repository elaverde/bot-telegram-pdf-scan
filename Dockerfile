FROM python:3.6-buster
WORKDIR /app
RUN apt-get update && apt-get install -y ghostscript imagemagick 
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]