# Utiliza la imagen oficial de Python 3.9
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Actualiza el sistema e instala tzdata para configurar la zona horaria
RUN apt-get update && apt-get install -y tzdata

# Instala FastAPI y otros paquetes requeridos
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir fastapi[all] \
    && pip install pyjwt \
    && pip install python-dotenv \
    && pip install sqlalchemy

# Copia el código de la aplicación en el contenedor
COPY . .

# Expone el puerto 8000 para acceder a la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
