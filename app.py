import os
import pandas as pd
import re
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import time

nombre_archivo = None
columna = None

app = Flask(__name__)

# Carpeta de subida

app.config['UPLOAD_FOLDER'] = './Archivos Excel'

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
        global columna
        columna = request.form.get('columna')
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retornamos una respuesta satisfactoria
        return render_template('cargando.html')

    

@app.route("/transformar", methods=['GET', "POST"])

def transformar():

    time.sleep(2)
    df = pd.read_excel(f"./Archivos Excel/{nombre_archivo}")
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
    df.to_excel(f"{nombre_archivo}'_TRANSFORMADO'.xlsx")
    
    return render_template('exito.html')
    

if __name__ == '__main__':
    # Iniciamos la aplicacion 
    app.run(debug=True)
