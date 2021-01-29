#! python3
# notas.py - Encuentra los nombres y las notas del portapapeles
# Autor: Álvaro Moreno
# Entrar en notas en la intranet. Seleccionar la nota de la que se quieren ver las
# estadísticas y presionar Ctrol+a para seleccionar la página entera. Tras esto, pulsar
# Ctrol+c y ejecutar el script. Si todo ha ido bien aparecerán las estadísticas.
from tkinter import messagebox

import pyperclip, operator
import numpy as np
from tkinter import * # ok
import sys


def media(diccionario):
    notaMedia = 0
    for nota in diccionario.values():
        notaMedia += nota
    return notaMedia / len(diccionario)


def notaMax(diccionario):
    max = 0
    for nombre, nota in diccionario.items():
        if max < nota:
            max = nota
    return max


def notaMin(diccionario):
    min = 10
    for nombre, nota in diccionario.items():
        if min > nota:
            min = nota
    return min


def numAprobados(diccionario):
    aprobados = 0
    for nombre, nota in diccionario.items():
        if nota >= 5:
            aprobados += 1
    suspensos = len(diccionario) - aprobados
    porcentajeAprobados = 100 * aprobados / len(diccionario)
    propertySuspendidos = 100 * suspensos / len(diccionario)
    return aprobados, suspensos, porcentajeAprobados, propertySuspendidos


def ordenarPorNota(diccionario):
    diccionario_sort = sorted(diccionario.items(), key=operator.itemgetter(1),
                              reverse=True)  # devuelve una lista de tuplas
    listaNombreNota = []
    for nombre in enumerate(diccionario_sort):
        listaNombreNota.append(nombre[1][0]+':  '+str(diccionario[nombre[1][0]]))
    for i in range(len(listaNombreNota)):
        listBox.insert(END , str(i+1)+'º.   '+str(listaNombreNota[i]))


def percentil(perc, diccionario):
    diccionario_sort = sorted(diccionario.items(), key=operator.itemgetter(1),
                              reverse=False)  # devuelve una lista de tuplas
    listaNotas = []
    for i in enumerate(diccionario_sort):
        listaNotas.append(i[1][1])  # lista con notas de menor a mayor según índice
    a = np.array(listaNotas)
    p = np.percentile(a, perc)
    return p


texto = str(pyperclip.paste())


# Interfaz
ventana = Tk()
ventana.title('UPV Notas')
#ventana.iconbitmap('logoUPV.ico')
ventana.geometry('500x600')
ventana.resizable(0,1)
# scrollbar = Scrollbar(ventana)
# scrollbar.pack(side = RIGHT, fill = Y)

titulo = Label(ventana, text = 'Notas UPV', font = 'Helvetica 30 bold').pack()

try:
    inicioNota = texto.find('Nombre	Nota') + len('Nombre	Nota') + 2
    finNota = texto.find('R-1') - 1

    alumNotasDic = {}

    alumNotasList = texto[inicioNota:finNota].split('\n')

    for nombreYnota in alumNotasList:
        nombre, nota = nombreYnota.rstrip().split('\t')
        alumNotasDic[nombre] = float(nota.replace(",", "."))
except Exception as e:
    print(e)
    messagebox.showerror('Atención', 'Presiona Ctrol + A en la pantalla de las notas y después Ctrol + C. Tras esto ejecuta el programa')
    sys.exit() # El programa terminó por algún error

inicio = Frame(ventana)
inicio.pack(fill = BOTH, expand = True)
inicio.config(bd = 20)
var_strMedia = 'La media es: ' + str(media(alumNotasDic))
lab_media = Label(inicio, text = var_strMedia, anchor = W)
lab_media.pack(fill = X, expand = True)

var_strPercentilBajo = 'El percentil 25 es: ' + str(percentil(25, alumNotasDic))
labPercentilBajo = Label(inicio, text = var_strPercentilBajo, anchor = W)
labPercentilBajo.pack(fill = X, expand = True)

var_strPercentilMedio = 'El percentil 50 es: ' + str(percentil(50, alumNotasDic))
lab_percentilMedio = Label(inicio, text = var_strPercentilMedio, anchor = W)
lab_percentilMedio.pack(fill = X, expand = True)

var_strPercentilAlto = 'El percentil 75 es: ' + str(percentil(75, alumNotasDic))
lab_percentilAlto = Label(inicio, text = var_strPercentilAlto, anchor = W)
lab_percentilAlto.pack(fill = X, expand = True)

var_strNotaMax = 'La nota máxima es: ' + str(notaMax(alumNotasDic))
lab_notaMax = Label(inicio, text = var_strNotaMax, anchor = W)
lab_notaMax.pack(fill = X, expand = True)

var_srtNotaMin = 'La nota mínima es: ' + str(notaMin(alumNotasDic))
lab_notaMin = Label(inicio, text = var_srtNotaMin, anchor = W)
lab_notaMin.pack(fill = X, expand = True)

aprobados, suspensos, porAprobados, porSuspensos = numAprobados(alumNotasDic)
var_strNumAlumnos = 'Número de alumnos de la asignatura: ' + str(len(alumNotasDic))
lab_numAlumnos = Label(inicio, text = var_strNumAlumnos, anchor = W)
lab_numAlumnos.pack(fill = X, expand = True)

var_strNumAprobados = 'El número de aprobados es: ' + str(aprobados)
lab_numAprobados = Label(inicio, text = var_strNumAprobados, anchor = W)
lab_numAprobados.pack(fill = X, expand = True)

var_strNumSuspensos = 'El número de suspensos es: ' + str(suspensos)
lab_numSuspensos = Label(inicio, text = var_strNumSuspensos, anchor = W)
lab_numSuspensos.pack(fill = X, expand = True)

var_strPorAprobados = 'El porcentaje de aprobados es: ' + str(porAprobados)
lab_porAprobados = Label(inicio, text = var_strPorAprobados, anchor = W)
lab_porAprobados.pack(fill = X, expand = True)

var_strPorSuspensos = 'El porcentaje de suspensos es: ' + str(porSuspensos)
lab_porSuspensos = Label(inicio, text = var_strPorSuspensos, anchor = W)
lab_porSuspensos.pack(fill = X, expand = True)

varOrdenados = 'Ordenados de mayor a menor nota:'
lab_Ordenados = Label(ventana, text = varOrdenados, font = 'Helvetica 18 bold')
lab_Ordenados.pack()

# Frame
frame = Frame(ventana)
frame.pack(fill = BOTH, expand = True)
scrollbar = Scrollbar(frame)
scrollbar.pack(side = RIGHT, fill = Y)

# Creo una lista para introducir el nombre y la nota de cada alumno
listBox = Listbox(frame, yscrollcommand = scrollbar.set, bd = '20', relief = FLAT, width = 200)

ordenarPorNota(alumNotasDic)
listBox.pack(fill = Y, expand = True, anchor = CENTER)
scrollbar.config(command = listBox.yview)

ventana.mainloop()