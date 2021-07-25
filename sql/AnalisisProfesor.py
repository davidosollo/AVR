#######################################
# Universidad Autónoma de Guadalara (UAG)
#
# Materia:  Tópicos avanzados de computación
# Proyecto: Perfiles de Profesores
# Autor:    David Osollo
######################################

# Packages

import pickle
import os
import re
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
import sqlite3
import sqlite3 as sql
import shutil as shu
import glob as myGlob
from chefboost import Chefboost as chef

CVS_FOLDER = './sql/CVS/'

#Covert the data to Numeric
def handle_non_numerical_data(df):
    columns = df.columns.values
    for column in columns:
        text_digit_vals = {}
        def convert_to_int(val):
            return text_digit_vals[val]

        if df[column].dtype != np.int64 and df[column].dtype != np.float64:
            column_contents = df[column].values.tolist()
            unique_elements = set(column_contents)
            x = 0
            for unique in unique_elements:
                if unique not in text_digit_vals:
                    text_digit_vals[unique] = x
                    x+=1
            df[column] = list(map(convert_to_int,df[column]))
    return df

#Construcción del Modelo
def build_model(xSize):

  model = keras.Sequential()
  model.add(keras.layers.Dense(5, kernel_initializer='glorot_uniform',
                               activation='relu', input_shape=xSize))
  model.add(keras.layers.Dropout(0.2))
  model.add(keras.layers.Dense(64, activation='tanh'))
  model.add(keras.layers.Dense(1, activation='sigmoid'))


  #model.compile(loss='mean_squared_error',
  #              optimizer=keras.optimizers.Adam())

  model.compile(loss='binary_crossentropy',
                 optimizer=keras.optimizers.Adam())
  return  model


#Plot the History Error
def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch
  plt.figure()
  plt.title('Loss vs Iterations')
  plt.xlabel('Epoch')
  plt.ylabel('Loss')
  plt.plot(hist['epoch'], hist['loss'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_loss'],
           label = 'Val Error')
  plt.ylim([-1,5])
  plt.legend()
  plt.show()


def load_table(base_file_CVS,table, fullPathDBProy):
    status = 0
    conn = None
    try:
        conn = sqlite3.connect(fullPathDBProy)
        c = conn.cursor()

        # Execute the DROP Table SQL statement
        print("Cargando tabla:"+table)
        truncateTableStatement="DELETE FROM "+table
        c.execute(truncateTableStatement)
        base_cvs = pd.read_csv(base_file_CVS)  # load to DataFrame
        base_cvs.to_sql(table, conn, if_exists='append', index=False)  # write to sqlite table
        conn.commit()
        conn.close()
        status = 0
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        status = 1
    finally:
        if (conn):
            conn.close()
            #print("The SQLite connection is closed")
    return status

#DSOO
def FindProfesion(sqlLiteDB ,BuscaProf):

    conn = None
    valor = None

    try:
        conn = sql.connect(sqlLiteDB)
        cur = conn.cursor()
        cur.execute("SELECT VALOR FROM val_fam_profesion where PROFESION = ?", (BuscaProf,))

        results = cur.fetchall()
        found = len(results)
        if found > 0:
            valor = int(results[0][0])
        else:
            valor = 0

    except sql.Error as error:
        print("Failed To Read avr_users.sqlite", error)
        valor = 0
    finally:
        if conn:
            conn.close()
            #print("The SQLite connection is closed")

    return valor


def generar_modelos_prof(file_to_process, base_proyecto):
    # Open sheets

    fullPathDirProy = "mkdir ./sql/ProyDB/" + base_proyecto + "/"
    os.system("mkdir " + fullPathDirProy)
    fullPathDBProy = "./sql/ProyDB/" + base_proyecto + "/" + base_proyecto + ".sqlite"
    os.system("sqlite3 " + fullPathDBProy + " < ./sql/create_tables.sql")

    try:
        print("Abriendo Archivo de Entrenamiento")
        df_train = pd.read_csv(file_to_process)


    except:
        print("Error Abriendo CSV de Entrenamiento")
        return 1

    #try:
    # Generar modelo
    try:
        df_train.drop(['nomina'], axis='columns', inplace=True)
        config = {'algorithm': 'C4.5'}
        model = chef.fit(df_train, config=config)
        chef.save_model(model, base_proyecto + ".pkl")

    except:
        print("Error Creando Modelo")
        return 2

    try:
        shu.copyfile("outputs/rules/" + base_proyecto + ".pkl", "outputs/rules/modelos/"+ base_proyecto + ".pkl")
        fileDelete = myGlob.glob("outputs/rules/*.pkl", recursive=False)
        # Iterate over the list of filepaths & remove each file.
        for file in fileDelete:
            try:
                os.remove(file)
            except OSError:
                print("Error while deleting file")

    except:
        print("Error limpiando directorios")
        return 3

    print("Se Genero el modelo exitosamente")


    return 0

def proc_candis(file_to_process, base_proyecto, values):
    # this will load outputs/rules/rules.py

    try:
        print("Cargando Modelo")
        moduleName = "modelos/" + base_proyecto
        model = chef.load_model(moduleName)
    except:
        print("Error Cargando Modelo")
        return 4

    try:
        print("Cargando Dataset")
        df_test = pd.read_csv(file_to_process)
    except:
        print("Error Cargando Dataset")
        return 5

    #try:
    for i in df_test.index:
        row = df_test.loc[
            i, ['experiencia', 'disciplina', 'empatia', 'liderazgo', 'seguridad', 'habilidad_tecnologica',
                'habilidad_pedagogica', 'vocacion',
                'relaciones_inter', 'curiosidad', 'paciencia', 'normal_D', 'normal_I', 'normal_S', 'normal_C',
                'motivacion_D', 'motivacion_I', 'motivacion_S', 'motivacion_C',
                'presion_D', 'presion_I', 'presion_S', 'presion_C']].to_numpy()
        prediction2 = chef.predict(model , row)
        df_test.at[i, 'Decision'] = prediction2
        if prediction2 == "No":
            values[0] = values[0] + 1
        else:
            values[1] = values[1] + 1
    #except:
    #    print("Error Procesando Candidatos Dataset")
    #    return 6

    try:
        fileDelete = myGlob.glob("resultados/*.csv", recursive=False)
        # Iterate over the list of filepaths & remove each file.
        for file in fileDelete:
            try:
                os.remove(file)
            except OSError:
                print("Error while deleting file")

    except:
        print("Error limpiando directorios")
        return 7

    file_to_process = file_to_process.replace('./uploads', '')
    file_to_process = file_to_process.replace('.csv', '')
    df_test.to_csv("./resultados/" + file_to_process + "_procesado.csv")

    return 0


def generar_modelos_prof_viejo(file_to_process, base_proyecto):
    #Open sheets

    fullPathDirProy = "mkdir ./sql/ProyDB/" + base_proyecto + "/"
    os.system("mkdir " + fullPathDirProy )
    fullPathDBProy = "./sql/ProyDB/" + base_proyecto + "/" + base_proyecto + ".sqlite"
    os.system("sqlite3 " + fullPathDBProy + " < ./sql/create_tables.sql")

    try:
        print("Abriendo pestañas")
        df_ciudad = pd.read_csv("./sql/CVS/localidad.csv")
        df_fam_prof = pd.read_csv("./sql/CVS/val_fam_profesion.csv")
        df_base = pd.read_excel(file_to_process, sheet_name="BASE")
        df_fam = pd.read_excel(file_to_process, sheet_name="FAMILIARES")
        df_exp_lab = pd.read_excel(file_to_process, sheet_name="EXPERIENCIA_LABORAL")
        df_exp_doc = pd.read_excel(file_to_process, sheet_name="EXPERIENCIA_DOCENTE")
        df_idiomas = pd.read_excel(file_to_process, sheet_name="IDIOMAS")

        """
        df_bene = pd.read_excel(file_to_process, sheet_name="BENEFICIARIOS")

        
        """
        df_esc = pd.read_excel(file_to_process, sheet_name="ESCOLARIDAD")

    except:
        print("Error Abriendo Pestañas de CSV")
        return 1

    try:
        # Elminar registros Duplicados
        print("Eliminando Duplicados")
        df_base = df_base.drop_duplicates()
        df_fam = df_fam.drop_duplicates()
        """
        df_bene = df_bene.drop_duplicates()
        df_exp_lab = df_exp_lab.drop_duplicates()
        df_exp_doc = df_exp_doc.drop_duplicates()
        df_idiomas = df_idiomas.drop_duplicates()
        """
        df_esc = df_esc.drop_duplicates()

    except:
        print("Error Eliminando duplicados")
        return 2


    try:
        # Convertir las pestañas en archivos CSV
        print("Convertir pestañas a CSV")
        df_base.to_csv(CVS_FOLDER +'base.csv', index=None, header=True)
        df_fam.to_csv(CVS_FOLDER +'familiares.csv', index=None, header=True)
        df_exp_lab.to_csv(CVS_FOLDER +'experiencia_laboral.csv', index=None, header=True)
        df_exp_doc.to_csv(CVS_FOLDER +'experiencia_docente.csv', index=None, header=True)
        df_idiomas.to_csv(CVS_FOLDER +'idiomas.csv', index=None, header=True)

        """
        df_bene.to_csv(CVS_FOLDER +'beneficiarios.csv', index=None, header=True)
        df_idiomas.to_csv(CVS_FOLDER +'idiomas.csv', index=None, header=True)
        """
        df_esc.to_csv(CVS_FOLDER +'escolaridad.csv', index=None, header=True)
        #df_loc.to_csv(CVS_FOLDER + 'locales.csv', index=None, header=True)

    except:
        print("Error En Convertir las pestañas en archivos CSV")
        return 3

    """.separator,
    .import./ sql / csv / locales.csv
    localidad"""

    # Cargar las pestañas a tablas
    print("Cargar los CSV a las Tablas")

    status_CSV = load_table(CVS_FOLDER + "base.csv", "base", fullPathDBProy)
    status_CSV += load_table(CVS_FOLDER + "familiares.csv", "familiares", fullPathDBProy)
    status_CSV += load_table(CVS_FOLDER + "localidad.csv", "localidad", fullPathDBProy)
    status_CSV += load_table(CVS_FOLDER + "val_fam_profesion.csv", "val_fam_profesion", fullPathDBProy)
    status_CSV += load_table(CVS_FOLDER + "experiencia_docente.csv", "experiencia_docente", fullPathDBProy)
    status_CSV += load_table(CVS_FOLDER + "idiomas.csv", "idiomas", fullPathDBProy)

    """
    status_CSV += load_table(CVS_FOLDER + "beneficiarios.csv", "beneficiarios", fullPathDBProy)
    status_CSV += load_table(CVS_FOLDER + "experiencia_laboral.csv", "experiencia_laboral", fullPathDBProy)
    status_CSV += load_table(CVS_FOLDER + "escolaridad.csv", "escolaridad", fullPathDBProy)

    """

    #BASE TAB
    if status_CSV != 0:
        print("Error en Cargar los archivos CSV a tablas de sqlite")
        return 4

    try:
        #Seleccionar Columnas para procesar
        df_base_cols = df_base[["NÓMINA", "FECHA_ALTA", "FECHA_BAJA", "MOTIVO_BAJA",
                                "GRADO", "SEXO", "ESTADOCIVIL", "CP", "CIUDAD", "RELIGION",
                                "PSICOMETRIA", "RHVCODDEP", "PUESTO", "CODIGO_PUESTO_GENERICO"]]

        #df_base_cols = df_base_cols[df_base_cols['PUESTO'].str.match('PROFE*|ASIGNATURA', na=False)]
        df_base_cols = df_base_cols[df_base_cols['PUESTO'].str.match('PROFE*', na=False)]
        #df_base_cols['FECHA_BAJA'].replace([pd.to_datetime('1900-01-01 00:00:00')], value=pd.to_datetime('2020-01-01 00:00:00'))

        df_base_cols['LOCALIDAD'] = 6

        for i in df_base_cols.index:
            fecha_baja = df_base_cols.at[i ,'FECHA_BAJA']
            if fecha_baja == pd.to_datetime('1900-01-01 00:00:00'):
                df_base_cols.at[i, 'FECHA_BAJA'] = datetime.now()

            loc_prof = df_base_cols.at[i, 'CIUDAD']
            if type(loc_prof) == str:
                for j in df_ciudad.index:
                    if loc_prof.find(df_ciudad.at[j, 'CIUDAD']) != -1:
                        df_base_cols.at[i, 'LOCALIDAD'] = df_ciudad.at[j, 'VALOR']
                        break

        df_base_cols['DATE_DIFF'] = (df_base_cols['FECHA_BAJA'] - df_base_cols['FECHA_ALTA']).dt.days
        #df_base_cols = df_base_cols[df_base_cols.DATE_DIFF > 0]
        df_base_cols['EVAL'] = np.where(df_base_cols['DATE_DIFF'] >= 365, 1, 0)

        #Generar las Columnas de One Hot Encoding
        #Para datos de clasificacion
        GRADOS = pd.get_dummies(df_base_cols.GRADO, prefix='GRADO')
        df_base_cols = pd.concat([df_base_cols, GRADOS], axis=1)

        SEXO = pd.get_dummies(df_base_cols.SEXO, prefix='SEXO')
        df_base_cols = pd.concat([df_base_cols, SEXO], axis=1)

        ESTADO_CIVIL = pd.get_dummies(df_base_cols.ESTADOCIVIL, prefix='ESTADO_CIVIL')
        df_base_cols = pd.concat([df_base_cols, ESTADO_CIVIL], axis=1)

        RELIGION = pd.get_dummies(df_base_cols.RELIGION, prefix='RELIGION')
        df_base_cols = pd.concat([df_base_cols, RELIGION], axis=1)


        #Eliminar Columnas de Clasificacion ya
        #Que se generaron las columnas de One Hot Encoding
        df_base_cols.drop(['GRADO', 'SEXO', 'ESTADOCIVIL', 'RELIGION', 'PUESTO', 'CODIGO_PUESTO_GENERICO', 'CIUDAD'], axis='columns', inplace=True)

        #Parsear el dato de Psicometría
        df_base_cols.dropna(subset=["PSICOMETRIA"], inplace=True)
        df_Psicometric = df_base_cols["PSICOMETRIA"]

        psicoArr = np.array([])

        for i in df_base_cols.index:

            value = df_base_cols.loc[i][5]
            print("-----------------")
            sNumVal = re.sub('[^\d.]+','', str(value))
            print(sNumVal)
            sNumVal = re.sub('[.]$', '', str(sNumVal))
            print(sNumVal)
            sNumVal = sNumVal[0:5]

            try:
                numVal = float(sNumVal)
            except ValueError:
                numVal = 0

            if numVal > 170:
                numVal = 0
            elif numVal <= 1 and numVal > 0:
                numVal = numVal * 100

            psicoArr = np.append(psicoArr, numVal)
            df_base_cols.at[i,'PSICOMETRIA'] = numVal
            print(numVal)

        #df_base_cols = df_base_cols[df_base_cols.PSICOMETRIA != 0]

        #Definir como Exito Profesor que Trabajo mas de
        # de un año

    except:

        print("Error en seleccionar columnas")
        return 5


    try:

        df_base_cols['FAM_FACT'] = 0
        df_base_cols['FAM_PROF'] = 0

        dic_fam = {'HERMANO(A)': 1, 'ABUELO(A)': 2, 'PAPAS': 3, 'ESPOSO(A)': 4, 'HIJO(A)': 5}
        #Cargar Datos Familiares
        for i in df_base_cols.index:
            nomina = df_base_cols.at[i, 'NÓMINA']
            valor_fam = 0
            valor_fam_prof = 0

            for j in df_fam.index:
                if nomina == df_fam.at[j, 'NÓMINA']:
                    valor_fam += dic_fam.get(df_fam.at[j, 'ApvDescFam'])
                    profesion = df_fam.at[j, 'apvProfesion']
                    valor_fam_prof+=FindProfesion(fullPathDBProy, profesion)

            df_base_cols.at[i, 'FAM_FACT'] = valor_fam
            df_base_cols.at[i, 'FAM_FACT_PROF'] = valor_fam_prof

    except:

        print("Error en Datos Familiares")
        return 6

    try:
        df_base_cols['DIAS_EXP'] = 0
        df_exp_lab['DATE_DIFF'] = (df_exp_lab['apvTermino'] - df_exp_lab['apvInicio']).dt.days
        #Cargar Datos Exp_Lab
        for i in df_base_cols.index:
            nomina = df_base_cols.at[i, 'NÓMINA']
            days_exp = 0.0
            for j in df_exp_lab.index:
                if nomina == df_exp_lab.at[j, 'NÓMINA']:
                    days_exp += df_exp_lab.at[j,'DATE_DIFF']

            df_base_cols.at[i, 'DIAS_EXP'] = days_exp

    except:
        print("Error datos experiencia Laboral")
        return 7

        # Cargar Datos Exp_Docente


    #Experiencia Docente
    dic_numero = {'UN': 1, 'DOS': 2, 'TRES': 3, 'CUATRO': 4, 'CINCO': 5,
                  'SEIS': 6, 'SIETE': 7, 'OCHO': 8, 'NUEVE': 9, 'DIEZ': 10,
                  'ONCE': 11, 'DOCE': 12}
    df_base_cols['MONTH_EXP'] = 0

    try:

        for i in df_base_cols.index:
            nomina = df_base_cols.at[i, 'NÓMINA']
            month_exp = 0.0
            cant_num = 0.0
            for j in df_exp_doc.index:
                if nomina == df_exp_doc.at[j, 'NÓMINA']:

                    try:

                        sTimeExp = df_exp_doc.at[j,'apvAntiguedad']
                        #cantidad, tiempo = sTimeExp.split()
                        listExp = sTimeExp.split()

                        if listExp[0].isnumeric():
                            cant_num = float(listExp[0])
                        else:
                            cant_num = dic_numero.get(listExp[0])

                        if listExp[1] == "AÑO" or listExp[1] == "AÑOS":
                            cant_num = cant_num * 12

                        if len(listExp) == 4:

                            if listExp[2].isnumeric():
                                cant_num += float(listExp[2])
                            else:
                                cant_num += dic_numero.get(listExp[2])

                            if listExp[3] == "AÑO" or listExp[3] == "AÑOS":
                                cant_num += cant_num * 12


                    except:
                        print(sTimeExp)

                    finally:
                        try:
                           month_exp += cant_num
                        except:
                            print(cant_num)
            df_base_cols.at[i, 'MONTH_EXP'] = month_exp

    except:
        print("Error datos experiencia Docente")
        return 8

    #IDIOMAS

    try:

        df_base_cols['INGLES'] = 0
        df_base_cols['OTROS_IDIOMAS'] = 0
        iOtrosIdiomas = 0
        iIngles = 0
        for i in df_base_cols.index:
            nomina = df_base_cols.at[i, 'NÓMINA']
            for j in df_idiomas.index:
                if nomina == df_idiomas.at[j, 'NÓMINA']:

                    iIdiomaID = df_idiomas.at[j,'ApvIdidi']
                    ApvNivConver = df_idiomas.at[j,'ApvNivConver']

                    if iIdiomaID == 10: #Ingles
                        iIngles = ApvNivConver
                    else:
                        iOtrosIdiomas += ApvNivConver

            df_base_cols.at[i,'OTROS_IDIOMAS'] = iOtrosIdiomas
            df_base_cols.at[i, 'INGLES'] = iIngles


    except:
        print("Error datos Idiomas")
        return 9

    Y = np.asanyarray(df_base_cols[['EVAL']])
    df_base_cols.drop(['EVAL'], axis='columns', inplace=True)
    X = df_base_cols[df_base_cols.columns[5:]].to_numpy()

    print(X.shape)
    print(Y.shape)

    df_base_cols.drop(['FECHA_ALTA'], axis='columns', inplace=True)
    df_base_cols.drop(['FECHA_BAJA'], axis='columns', inplace=True)
    df_base_cols.drop(['MOTIVO_BAJA'], axis='columns', inplace=True)
    df_base_cols.drop(['CP'], axis='columns', inplace=True)

    #f_base_cols.to_csv("AVR_datos.csv", encoding="utf-8")
    df_base_cols.to_csv(CVS_FOLDER + 'AVR_datos.csv', index=None, header=True)
    df_base_cols.to_json(CVS_FOLDER + 'AVR_datos.json')

    try:
        #Seleccionar los datos de Prueba y Test
        xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.2,random_state=0)

        #Construir el Modelo
        model = build_model([X.shape[1]])
        model.summary()

        callback = keras.callbacks.EarlyStopping(monitor='loss', patience=15)

        X = np.asarray(X).astype(np.float32)
        Y = np.asarray(Y).astype(np.float32)
        xtrain = np.asarray(xtrain).astype(np.float32)
        ytrain = np.asarray(ytrain).astype(np.float32)
        xtest = np.asarray(xtest).astype(np.float32)
        ytest = np.asarray(ytest).astype(np.float32)

        #Entrenar el Modelo
        history = model.fit(xtrain, ytrain,
                            batch_size=150, epochs=300,
                            validation_split=0.2, verbose=1)#, callbacks=[callback])

        #Imprimir el Error
        #plot_history(history)


        print("\n-----------------------------------------------\n")
        results = model.evaluate(xtest, ytest)

        print("Evaluete Test", results)
        print("\n-----------------------------------------------\n")

        #Hacer la prueba
        results = model.predict(xtest)


        #Generación de Resultados y Matriz de Confusion

        yPred = np.array([])
        yPred = np.where(results >= .5, 1, 0)

        #Resultados de la Prueba
        print("Predicción Prob - Esperado")
        i = 0
        for resultado in results:
            print(resultado, yPred[i],"\t - ",ytest[i])
            i = i + 1

        #Imprimir estadisticas de la Prueba
        print("-----------------------------------------------")
        print('Accuracy: ', accuracy_score(y_true=ytest, y_pred=yPred))
        print('Matriz de confusión:\n', confusion_matrix(y_true=ytest, y_pred=yPred))

    except:
        print("Error en generar modelos")
        return 100

    return 0

#generar_modelos_prof("../uploads/BASE_DATOS_TESIS.xlsx", "test")



