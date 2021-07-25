#new AVR
#David Osollo
#Universidad Autonoma de Guadalajara (UAG)

import sys, os
import re
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_file


labels = [
    'N0', 'Si'
]

values = [
    0, 0
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


sys.path.append('./sql')
import users_avr as dbHandler
import AnalisisProfesor as ModelGen

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx',  'xlsm',  'xlsb', 'xltx'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
filename=""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def home():
	return render_template('index.html')
	
@app.route('/login', methods=['POST'])
def login():
    error = "Usuario Invalido"
    username = request.form['username']
    password = request.form['password']
    validate = dbHandler.validateUsers(username, password)
    print(username)
    if validate == 0:
        return render_template('index.html', error=error)
    else:
    	return render_template('avr_home.html')
        
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   global filename
   if request.method == 'POST':

        AccionToDO = request.form['opcion']
        # check if the post request has the file part
        if 'choose_file' not in request.files:
            error_load = "Tipo de archivo no soprtado"
            if AccionToDO == "cargar_datos":
                return render_template('avr_cargar_datos.html',error_load=error_load)
            elif AccionToDO == "process_candi":
                return render_template('avr_proces_candi.html', error_load=error_load)
        file_to_proces  = request.files['choose_file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file_to_proces.filename == '':
            error_load = "Archivo no seleccionado"
            if AccionToDO == "cargar_datos":
                return render_template('avr_cargar_datos.html', error_load=error_load,
                                        generar_modelo="no_generar_modelo")

            elif AccionToDO == "process_candi":
                return render_template('avr_proces_candi.html', error_load=error_load,
                                        generar_modelo="no_generar_modelo")
            
        if allowed_file(file_to_proces.filename) and file_to_proces:
            #filename = secure_filename(file.filename)
            filename = file_to_proces.filename
            file_to_proces.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            status_load = "El archivo se cargo correctamente: " + file_to_proces.filename
            #resultado de SELECT id, nombre FROM usuarios ORDER BY nombre
            res = [{'id': 1, 'nombre': 'Fulano'}, {'id': 2, 'nombre': 'Fulanito'}]
            usuarios = [(di['id'], di['nombre']) for di in res]

            if AccionToDO == "cargar_datos":
                return render_template('avr_cargar_datos.html',status_load=status_load,
                                   generar_modelo="generar_modelo",archivo_procesar=filename)
            elif AccionToDO == "process_candi":
                list_mod = []
                file_list = os.listdir('./outputs/rules/modelos')
                for modelo in file_list:
                    if modelo.endswith(".pkl"):
                        list_mod.append(modelo)


                return render_template('avr_proces_candi.html',status_load=status_load,
                                   generar_modelo="generar_modelo",archivo_procesar=filename, proy_list=list_mod)


        else:
            #filename = secure_filename(file.filename)
            error_load = "Tipo de Archivo no valido: " + file_to_proces.filename
            if AccionToDO == "cargar_datos":
                return render_template('avr_cargar_datos.html',error_load=error_load,
                                       generar_modelo="no_generar_modelo")
            elif AccionToDO == "process_candi":
                return render_template('avr_proces_candi.html',error_load=error_load,
                                       generar_modelo="no_generar_modelo")

   if request.method == 'GET':
        return render_template('avr_home.html', generar_modelo="no_generar_modelo")

@app.route('/')
def upload_form():
	return render_template('download.html')

@app.route('/download_file')
def download_file():
    list_mod = []
    list_mod = os.listdir('./resultados')
    file_down = list_mod [0]

    return send_file('resultados/' + file_down, as_attachment=True)

@app.route('/GenModelos', methods = ['POST'])
def generar_modelos():
    global filename

    if request.method == 'POST':
        ProyectName = request.form['proyec_name']
        ProyectName = ProyectName.strip()
        if ProyectName == "":
            error_modelo = "Nombre de Proyecto vacio"
            return render_template('avr_cargar_datos.html', error_modelo=error_modelo, generar_modelo="generar_modelo",
                                   archivo_procesar= filename, go_home="no_go_home")
        if not re.match("^[\w-]+$", ProyectName):
            error_modelo = "Solo se aceptan Letras y Números"
            return render_template('avr_cargar_datos.html', error_modelo=error_modelo, generar_modelo="generar_modelo",
                                   archivo_procesar=filename , go_home="no_go_home")
        
        status_mod = ModelGen.generar_modelos_prof(UPLOAD_FOLDER + '/' + filename, ProyectName)
        if status_mod == 0:
            status_procesado = "El modelo se generó corretamente para el proyecto: " + ProyectName
            return render_template('avr_cargar_datos.html', generar_modelo="generar_modelo", archivo_procesar=filename,
                                   status_procesado=status_procesado , go_home="go_home")
        else:
            error_modelo = "Error " + str(status_mod) + " en genracion de modelos"
            return render_template('avr_cargar_datos.html', error_modelo=error_modelo, generar_modelo="generar_modelo",
                                   archivo_procesar=filename , go_home="go_home")


@app.route('/ProcModelos', methods=['POST'])
def proc_Modelos():
    global filename

    if request.method == 'POST':
        ProyectName = request.form['proyec_name']
        ProyectName = ProyectName.strip()
        if ProyectName == "":
            error_modelo = "Nombre de Proyecto vacio"
            return render_template('avr_proces_candi.html', error_modelo=error_modelo, generar_modelo="generar_modelo",
                                   archivo_procesar=filename)

        values[0] = 0
        values[1] = 0

        status_mod = ModelGen.proc_candis(UPLOAD_FOLDER + '/' + filename, ProyectName, values)
        if status_mod == 0:
            status_procesado = "Los candidatos se procesaron correctamente con el modelo: " + ProyectName
            return render_template('avr_proces_candi.html', proc_modelo="proc_modelo", archivo_procesar=filename,
                                   status_procesado=status_procesado,  generar_modelo="generar_modelo")
        else:
            error_modelo = "Error " + str(status_mod) + " en genracion de modelos"
            return render_template('avr_proces_candi.html', error_modelo=error_modelo, proc_modelo="error",
                                   archivo_procesar=filename,  generar_modelo="generar_modelo")

@app.route('/cargar_datos')
def cargar_datos():
    return render_template('avr_cargar_datos.html', generar_modelo="no_generar_modelo")

@app.route('/proces_candi')
def proces_candi():
    return render_template('avr_proces_candi.html', generar_modelo="no_generar_modelo")

@app.route('/analisis_candi')
def analisis_candi():
    return render_template('avr_analisis_candi.html', generar_modelo="no_generar_modelo")


@app.route('/home_page')
def home_page():
    return render_template('avr_home.html', generar_modelo="no_generar_modelo")

@app.route('/back_home')
def back_home():
    return render_template('avr_home.html', generar_modelo="no_generar_modelo")

@app.route('/bar')
def bar():
    bar_labels=labels
    bar_values=values
    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)

@app.route('/line')
def line():
    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels, values=line_values)

@app.route('/pie')
def pie():
    pie_labels = labels
    pie_values = values
    if values[0] == 0 and values[1] == 0:
        values[0] = 1
        values[1] = 1

    return render_template('pie_chart.html', title='Bitcoin Monthly Price in USD', max=17000, set=zip(values, labels, colors) , no_valid_per=values[0], valid_per=values[1])



if __name__ == '__main__':
    app.run(debug=True)