# Python 3.10 tabanlı bir imaj kullan
FROM python:3.10-slim

# Çalışma dizini oluştur ve ayarla
WORKDIR /app

# Gereksinim dosyasını kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Uygulamanın çalıştırılacağı portu belirt
EXPOSE 8000

# Uygulamayı başlat
CMD ["python", "manage.py", "runserver"]
