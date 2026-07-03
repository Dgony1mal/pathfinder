FROM python:3.10-slim

# Устанавливаем Xvfb, x11vnc, novnc, websockify и зависимости для Tkinter
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаём скрипт запуска
RUN echo '#!/bin/bash\n\
    Xvfb :99 -screen 0 1024x768x24 &\n\
    x11vnc -display :99 -forever -nopw -quiet &\n\
    websockify --web /usr/share/novnc 6080 localhost:5900 &\n\
    export DISPLAY=:99\n\
    python main.py\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 6080

ENTRYPOINT ["/entrypoint.sh"]