# Usa una imagen oficial de Python ligera
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente al contenedor
COPY . .

# Crea la carpeta instance si no existe (para SQLite)
RUN mkdir -p instance

# Expone el puerto 5000 (Flask por defecto)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]