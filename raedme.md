### Bot Telegram PDF efecto escaneado
- Este bot permite recibir un documento en formato pdf y devolverlo con un efecto de escaneo



# Docker
Establece la maquina virtual a trabajar y el espacio de trabajo
```
FROM python:3.6-buster
WORKDIR /app
```

Instala las aplicaciones utilizadas para el efecto
```
RUN apt-get update && apt-get install -y ghostscript imagemagick 
```
Desactiva la politica de seguridad ImageMagick
```
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml
```
Copia he instala los requirimientos del app
```
COPY requirements.txt .
RUN pip install -r requirements.txt
```
Copia todos los archivos a la maquina virtual y los ejecuta
```
COPY . .
CMD ["python", "app.py"]
```



# Instalación Heroku
Vamos a crear la imagen de Docker localmente y ejecutarla para asegurarnos de que el servicio se está ejecutando localmente.

```
docker image build -t my-app .
```
La probamos localmente

```
docker run -p 5000:5000 -d my-app
```

Nos logueamos en heroku 
```
heroku login -i
```
Logueamos heroku containers
```
heroku container:login
```
Creamos una app en heroku
```
heroku create <nombre-de-su-aplicación>
```
Ahora, recibirás un enlace como,
```
https://<nombre-de-su-aplicación>.herokuapp.com/
```
Ahora, ejecute el siguiente comando para insertar el contenedor en Heroku (el siguiente comando puede tardar hasta horas dependiendo de su velocidad de Internet)
```
heroku container:push web --app <nombre-de-su-aplicación>
```
En este punto, el contenedor docker se envía a Heroku, pero no se implementa ni se libera. El siguiente comando desplegaría el contenedor.
```
heroku container:release web --app <nombre-de-su-aplicación>
```
Ahora, la aplicación se lanza y se ejecuta en Heroku y puede verla en el sitio a continuación
```
https://< nombre de su aplicación>.herokuapp.com/
```

[![](https://i.ibb.co/99hRXrJ/avatar-81774fad4428cbfbcf64.png)](https://i.ibb.co/99hRXrJ/avatar-81774fad4428cbfbcf64.png)
Autor: Edilson Laverde Molina
Correo: edilsonlaverde_182@hotmail.com