#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Importar el módulo subprocess
import subprocess

# Crear una lista con las librerías a instalar
librerias = ["requests", "img2pdf", "datetime"]

# Recorrer la lista e instalar cada librería
for libreria in librerias:
    # Ejecutar el comando pip install libreria
    resultado = subprocess.run(["pip", "install", libreria], capture_output=True)

    # Verificar si hubo algún error al instalar la librería
    if resultado.returncode != 0:
        # Mostrar el mensaje de error
        print(f"Ocurrió un error al instalar la librería {libreria}:")
        print(resultado.stderr.decode())
    else:
        # Mostrar el mensaje de éxito
        print(f"La librería {libreria} se instaló correctamente.")

# Importar las librerías instaladas
import requests
import img2pdf
import datetime

# Importar los módulos smtplib y email
import smtplib
from email.message import EmailMessage

# Definir la URL base de la imagen
url_base = "https://foservices.prensalibre.com/viewer/get_protected_source?protected={}%2Fnormal%2FPL_{}_001_"

# Obtener el timestamp actual como un objeto datetime
ahora = datetime.datetime.now()

# Formatear el timestamp en el formato yyyymmdd
fecha_formato = ahora.strftime("%Y%m%d")

# Formato para fecha de correo
fecha_correo = ahora.strftime("%m/%d/%Y")

# Reemplazar la fecha en la url_base con el timestamp
url_base = url_base.format(fecha_formato, fecha_formato)

# Definir el rango de números a recorrer
numeros = range(1, 51)

# Definir una variable para indicar si se encontró una imagen
encontrada = True

# Definir una lista vacía para guardar los bytes de las imágenes
lista_imagenes = []

# Recorrer los números
for numero in numeros:
    # Verificar si se encontró una imagen anteriormente
    if encontrada:
        # Formatear el número con dos dígitos y agregar la extensión .jpg
        numero_str = f"{numero:02d}.jpg"

        # Completar la URL con el número
        url = url_base + numero_str + "&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2lkLnBpYW5vLmlvIiwic3ViIjoiMzM0NjY5IiwiYXVkIjoiTldyU1FhUWpGZCIsImxvZ2luX3RpbWVzdGFtcCI6IjE2ODgxODA2MTQ0NjEiLCJlbWFpbCI6ImhhcGFsbWFjQGdtYWlsLmNvbSIsImVtYWlsX2NvbmZpcm1hdGlvbl9yZXF1aXJlZCI6ZmFsc2UsImV4cCI6MTY5MDgwODYxNCwiaWF0IjoxNjg4MTgwNjE0LCJqdGkiOiJUSWY0Mko3aHk5cngza2h5IiwicGFzc3dvcmRUeXBlIjoicGFzc3dvcmQiLCJyIjp0cnVlLCJscyI6IklEIiwidmFsaWQiOnRydWUsInVpZCI6IjMzNDY2OSIsImNvbmZpcm1lZCI6dHJ1ZSwia2V5UGwiOiJTcGRUbWhrblJEdFAyYkdnY284eCJ9._1QTRz5q6Is32OqNL7glvZFtoaybPVFclyHvMv67PxA"

        # Mostrar la URL de la imagen
        # print(f"La URL de la imagen {numero_str} es: {url}")

        # Obtener la respuesta de la solicitud
        response = requests.get(url)

        # Verificar que la respuesta sea exitosa
        if response.status_code == 200:
            # Obtener el contenido de la respuesta como bytes
            image_bytes = response.content

            # Agregar los bytes de la imagen a la lista
            lista_imagenes.append(image_bytes)

            # Mostrar un mensaje de éxito
            print(f"Se ha obtenido la imagen {numero_str} con éxito.")
        else:
            # Mostrar un mensaje de error
            print(f"Ha ocurrido un error al obtener la imagen {numero_str}. Código de estado: {response.status_code}.")

            # Cambiar el valor de la variable encontrada a False para detener el bucle
            encontrada = False
    else:
        # Salir del bucle
        break

# Verificar que la lista de imágenes no esté vacía
if lista_imagenes:
    # Definir el nombre del archivo PDF de salida concatenando los valores PL_ + el timestamp de la fecha en el formato yyyymmdd
    pdf_file = f"PL_{fecha_formato}.pdf"

    # Verificar que el nombre del archivo PDF no coincida con el nombre de alguna de las imágenes
    if pdf_file not in [f"{n:02d}.pdf" for n in numeros]:
        # Verificar que la ruta del archivo PDF no contenga caracteres especiales, espacios, o barras normales
        if not any(c in pdf_file for c in "?*:<>\n|\"/") and " " not in pdf_file:
            # Crear el archivo PDF a partir de la lista de bytes de las imágenes
            with open(pdf_file, "wb") as f:
                f.write(img2pdf.convert(lista_imagenes))

            # Mostrar un mensaje de éxito
            print(f"Se ha creado el archivo {pdf_file} con éxito.")

            # Crear un objeto EmailMessage y asignarle los campos de asunto, remitente y destinatario
            msg = EmailMessage()
            msg["Subject"] = f"Prensa Libre del día {fecha_correo}"
            msg["From"] = "hapalmac@gmail.com"
            msg["Bcc"] = ["hpalma@tigo.com.gt", "sekitamorales@gmail.com", "hapalmac@gmail.com", "ctcatalan@tigo.com.gt"]

            # Establecer el contenido del mensaje como texto plano
            msg.set_content(f"Hola!,\n\nAdjunto encontraras la prensa libre del dia de hoy.\n\nSaludos cordiales.")

            # Abrir el archivo pdf en modo binario y agregarlo como un adjunto al mensaje
            with open(pdf_file, "rb") as f:
                msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_file)

             # Crear una conexión segura con el servidor SMTP usando SSL
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                # Iniciar sesión con tu usuario y contraseña de tu cuenta de correo electrónico
                server.login("hapalmac@gmail.com", "xqljkrvifsketiob")

                # Enviar el mensaje usando el método send_message()
                server.send_message(msg)

                # Mostrar un mensaje de éxito
                print(f"Se ha enviado el correo electrónico con el archivo {pdf_file} adjunto.")
        else:
            # Mostrar un mensaje de error
            print(f"La ruta del archivo PDF contiene caracteres no válidos. Por favor, cambia la ruta del archivo PDF.")
    else:
        # Mostrar un mensaje de error
        print(f"El nombre del archivo PDF coincide con el nombre de una de las imágenes. Por favor, cambia el nombre del archivo PDF.")
else:
    # Mostrar un mensaje de error
    print(f"No se pudo obtener ninguna imagen. Por favor, verifica la URL y el token.")


# In[ ]:




