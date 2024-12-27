# Użyj oficjalnego obrazu Python 3.11.11 jako bazowego
FROM python:3.11.11-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj wymagania aplikacji (jeśli istnieje plik requirements.txt)
COPY req.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r req.txt

# Skopiuj resztę plików projektu do kontenera
COPY src/ src/
COPY static/ static/
COPY templates/ templates/

# Ustaw zmienną środowiskową dla Pythona
ENV PYTHONUNBUFFERED=1

# Otwórz port 5000 (lub inny używany przez Twoją aplikację)
EXPOSE 5000

# Ustaw polecenie startowe (dostosuj do swojej aplikacji)
CMD ["python", "src/main.py"]
