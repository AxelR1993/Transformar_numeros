import os
import pandas as pd
import re
from flask import Blueprint, Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import time
from os import getcwd

nombre_archivo = None
columna = None
routes_files = Blueprint("routes_files", __name__)
PATH_FILE = getcwd()

app = Flask(__name__)

# Carpeta de subida

app.config['UPLOAD_FOLDER'] = '/'

@app.route('/')
def upload_file():
    return render_template('formulario.html')

@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # Obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        global nombre_archivo
        nombre_archivo = filename
        if filename == '' :
            return render_template('archivo.html')
        global columna
        columna = request.form.get('columna')
        if columna == '' :
            return render_template('nombre.html')
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(filename)
        # Retornamos una respuesta satisfactoria
        return (render_template('cargando.html'), nombre_archivo)
    

    

@app.route("/transformar", methods=['GET', "POST"])

def transformar():

    time.sleep(2)
    df = pd.read_excel(nombre_archivo)
    df.applymap(str)

    def validar_telefono(telefono_celular):

        tel_limpio = re.sub(r"[^0-9]","",str(telefono_celular))

        if len(tel_limpio) < 10 :
            return ""
    
        if len(tel_limpio) > 13 :
            tel_limpio = tel_limpio[-10:]

        if len(tel_limpio) == 13:
            tel_limpio = tel_limpio[3:]

        if len(tel_limpio) == 12:
            tel_limpio = tel_limpio[2:]
    
        if len(tel_limpio) == 11:
            tel_limpio = tel_limpio[1:]

        iguales = 0

        for i in range(len(tel_limpio)-1):
            if tel_limpio[i] == tel_limpio[i+1]:
                iguales += 1
            if iguales > 4:
                return ""

        return tel_limpio

    def eliminar_vacios(numero):
        if numero == '54' or numero == '549':
            return ""
        else:
            return numero

    
    df["Numero sin 54 ni 9"] = df[columna].apply(validar_telefono)
    df["Numero con 54"] = '54' +  df["Numero sin 54 ni 9"]
    df["Numero con 54 9"] = '549' +  df["Numero sin 54 ni 9"]
    df["Numero con 54"] = df["Numero con 54"].apply(eliminar_vacios)
    df["Numero con 54 9"] = df["Numero con 54 9"].apply(eliminar_vacios)
    
    df.to_excel(nombre_archivo)
    
   
    return (render_template('exito.html'))

@app.route("/descargar", methods=['GET', "POST"])

def descargar():
    
    return send_from_directory(PATH_FILE, path=nombre_archivo, as_attachment=True)
    

if __name__ == '__main__':
    # Iniciamos la aplicacion 
    app.run(debug=True)
