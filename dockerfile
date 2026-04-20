# Используем официальный легкий образ Python 3.11
FROM python

# Рабочая папка внутри контейнера
WORKDIR /app

# Копируем зависимости сначала (для кэширования слоёв)
COPY requirements.txt .

# Устанавливаем пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт (по умолчанию 8000 для Uvicorn)
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
