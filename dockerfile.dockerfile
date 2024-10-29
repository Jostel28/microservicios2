# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requisitos y los archivos de la aplicación al contenedor
COPY requirements.txt ./
COPY usuarios.py ./
COPY pedidos.py ./
COPY .env ./

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer los puertos
EXPOSE 5000 5001

# Comando para ejecutar el servicio de usuarios y pedidos
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
