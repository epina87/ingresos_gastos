
from flask import render_template,request,redirect
import csv
from registro_ig import app
from datetime import date
from operator import itemgetter


@app.route("/")
def index():
    fichero = open("data/movimientos.txt")
    csvReader = csv.reader(fichero, delimiter=",",quotechar='"')
    

    #movimientos = [movimiento for movimiento in csvReader]
    # list comprehension. igual a= 

    movimientos = []
    total = 0
    for movimiento in csvReader:
        movimientos.append(movimiento)

        total += float(movimiento[3])

    fichero.close()
    #mov_ordenados = sorted(movimientos,key=lambda movimiento: movimiento[1])
    mov_ordenados = sorted(movimientos,key=itemgetter(2))

    return render_template("index.html", pageTitle="Lista", moviments=mov_ordenados,totalReg=total)

@app.route("/nuevo",methods=["GET","POST"])
def alta():
    if request.method == 'GET':
    
        return render_template("insert.html", pageTitle="Alta",msgErrors={},dataForm={"date":date.today().isoformat()},)
    else:
        errores = validaFormulario(request.form)
        if not errores:

            fichero = open("data/movimientos.txt","a",newline="")
            csvWriter= csv.writer(fichero,delimiter=",",quotechar='"')
            numreg = numeroRegistro()

            csvWriter.writerow([numreg,request.form['date'],request.form['concept'],request.form['quantity']])  
            fichero.close()
            return redirect("/") 
                       

        else:
            return render_template("insert.html",pageTitle = "Modificación",msgErrors=errores,dataForm=dict(request.form)) 
            

def validaFormulario(camposFormulario):
    #errores = []
    errores={}
    hoy = date.today().isoformat()
    if camposFormulario['date'] > hoy:
        #errores.append("La fecha introducida es el futuro.")
        errores['date'] = "La fecha introducida es el futuro."
    if camposFormulario['concept']=="":
        #errores.append("Introduce un concepto para la transacción")
        errores['concept'] = "Introduce un concepto para la transacción."
    if camposFormulario['quantity']=="" or float(camposFormulario['quantity'])==0.0:
       # errores.append("Introduce cantidad positiva o negativa.")  
        errores['quantity'] = "Introduce cantidad positiva o negativa."

    return errores  

def numeroRegistro():
    fichero = open("data/movimientos.txt")
    csvReader = csv.reader(fichero, delimiter=",",quotechar='"')
    numreg = 0
    for movimiento in csvReader:
        numreg += 1

    return numreg




@app.route("/modificar/<int:id>", methods=["GET","POST"])
def modificar(id):
  
    if request.method == "GET":
        
        '''
        1.Consultar en movimientos.txt y recuperar el registro 3
        2.Devolver el formulario html con los datos de mi registro
        '''
        
        fichero = open("data/movimientos.txt")
        csvReader = csv.reader(fichero, delimiter=",",quotechar='"')

  
        for movimiento in csvReader:
            if int(movimiento[0]) == id:
                movimientos = movimiento
 
        fichero.close()

        return render_template("modify.html", msgErrors={},movModify=movimientos)
    else:

        """
        1. validar registro de entrada
        2. Si el registro es correcto lo sustituyo en movimientos.txt. La mejor manera es copiar registro a registro e fichero nuevo y dar el cambiazo
        3. redirect 
        4. Si el registro es incorrecto la gestion de errores que conocemos
        """

        errores = validaFormulario(request.form)
        if not errores:

            fichero = open("data/movimientos.txt")
            csvReader = csv.reader(fichero, delimiter=",",quotechar='"')

            movimiento_Modificado =[id,request.form['date'],request.form['concept'],request.form['quantity']]
        
            movimientos = []
       
            for movimiento in csvReader:
                movimientos.append(movimiento)

            fichero.close()    

            vaciarFichero()  
            cargarFicheroModificado(movimientos,movimiento_Modificado)

            return redirect("/")

        else:
            movimientos=[id,request.form['date'],request.form['concept'],request.form['quantity']]

            return render_template("modify.html",msgErrors=errores,movModify=movimientos) 


         
def cargarFicheroModificado(movimientos,movimiento_Modificado):      
    fichero = open("data/movimientos.txt","a",newline="")
    csvWriter= csv.writer(fichero,delimiter=",",quotechar='"')

    for registro in movimientos:
        if registro[0] != str(movimiento_Modificado[0]):           
            csvWriter.writerow([registro[0],registro[1],registro[2],registro[3]]) 
        else:
            csvWriter.writerow([movimiento_Modificado[0],movimiento_Modificado[1],movimiento_Modificado[2],movimiento_Modificado[3]])      
    fichero.close()    
    
             
        
    

@app.route("/borrar/<int:id>", methods=["GET","POST"])
def borrar(id):
   #return f"Debería borrar el registro{id}"
   
    if request.method == "GET":
        
        """
        1. Consultar en movimientos.txt y recueperar el registro con id al de la petición
        2. Devolver el formulario html con los datos de mi registro, no modificables 
        3. Tendrá un boton que diga confirmar.
        """
        
        fichero = open("data/movimientos.txt")
        csvReader = csv.reader(fichero, delimiter=",",quotechar='"')

  
        for movimiento in csvReader:
            if int(movimiento[0]) == id:
                movimientos = movimiento
 
        fichero.close()

        return render_template("remove.html", movRemove=movimientos)
    else:
        """
            Borrar el registro
        """
         
        fichero = open("data/movimientos.txt")
        csvReader = csv.reader(fichero, delimiter=",",quotechar='"')
    
        movimientos = []
 
    
        for movimiento in csvReader:
            movimientos.append(movimiento)

        fichero.close()    

        vaciarFichero()  
        cargarFicheroBorrado(movimientos,id)

        return redirect("/")
     

def vaciarFichero():
    fichero = open("data/movimientos.txt","w")
    csvWriter= csv.writer(fichero,delimiter=",",quotechar='"')     
    fichero.close()

def cargarFicheroBorrado(movimientos,id):
      
    fichero = open("data/movimientos.txt","a",newline="")
    csvWriter= csv.writer(fichero,delimiter=",",quotechar='"')
    numreg = 0

    for registro in movimientos:
        
        if registro[0] != str(id):
            numreg += 1
            csvWriter.writerow([str(numreg),registro[1],registro[2],registro[3]])  
    fichero.close()    
    
        
 