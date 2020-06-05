# Hecho por William, si vas a ver este codigo espero que mi documentacion sea de ayuda :D
# Importancion de las librerias
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
from flask import session
from flask import make_response
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import pygal
import pdfkit

# Intancia de la app de flask 
app = Flask(__name__)
mail = Mail(app)

# Mysql conexiones
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'protesis'
mysql = MySQL(app)

# Consiguraciones de la app para los correos
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465            
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBUG'] = True 
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = ''
app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail = Mail(app)

# pruebas de correo 
@app.route("/correo")
def correo():
      msg = Message("Hello", recipients=["haseke4061@lerwfv.com"])
      msg.body = ("Hola qeu tal")
      print(msg)
      mail.send(msg)

      return 'Correo enviado'











# Opciones es la llave para la sessiones
app.secret_key = 'llaveSecreta'

# Funcion que redireciona al login
@app.route('/')
def login():
    return render_template('login.html')

# Funcion de validar el usuario en el login
@app.route('/validar', methods=['GET', 'POST'])
def validar():
    if request.method == 'POST':
        usuario = request.form['cedula']
        contraseña = request.form['pass']
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM user WHERE cedula = %s AND pass = %s', (usuario, contraseña))
        mysql.connection.commit()
        data = cur.fetchall()
        if len(data) > 0:
            cuenta = data[0]
            if (cuenta[0]) == 1:
                # Registra la sesscion para el usuario
                session['user'] = usuario
                session['pass'] = contraseña
                return redirect(url_for('inicioUser'))
            elif (cuenta[0]) == 2:
                # Registra la sesscion para el doctor
                session['user'] = usuario
                session['pass'] = contraseña
                return redirect(url_for('inicioDoc'))
            else:
                # Registra la sesscion para el doctor
                session['user'] = usuario
                session['pass'] = contraseña
                return redirect(url_for('inicioEnfermera'))
        else:
            return redirect(url_for('login'))

# Funcion de cerrar session
@app.route('/logout')
def logout():
    # Elimina la sesion
    session.pop('user', None)
    session.pop('pass', None)
    return redirect(url_for('login'))

# Inicio de seciones del paciente ----------------------------------------------

# Funcion que redireciona a agendar cita
@app.route('/agendar')
def agendar():
    if 'user' in session:
        usuario = session['user']
        return render_template('agendar.html', user=usuario)
    else:
        return render_template('login.html')

# Funcion de agregar una cita del usuario
@app.route('/agregarCita', methods=['POST'])
def agregarCita():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        email = request.form['email']
        dia = request.form['dia']
        hora = request.form['hora']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO citas (nombre, apellido, cedula, email, dia, hora) VALUES (%s, %s, %s, %s, %s, %s)',
                    (nombre, apellido, cedula, email, dia, hora))
        mysql.connection.commit()
        flash('Cita Agregada Satisfactoriamente')
    return redirect(url_for('agendar'))

# Funcion que redireciona al inicio del usuario
@app.route('/inicioUser')
def inicioUser():
    if 'user' in session:
        usuario = session['user']
        return render_template('inicioUser.html', user=usuario)
    else:
        return render_template('login.html')


# Funcion que redireciona a los servicios
@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

# Funcion que redireciona a la galeria
@app.route('/galeria')
def galeria():
    if 'user' in session:
        usuario = session['user']
        return render_template('galeria.html', user=usuario)
    else:
        return render_template('login.html')

# Final de las seciones del paciente ---------------------------------------------------------


# Inicio de Secion de enfermeras --------------------------------------------------------------

# Funcion de la pagina del inicio del doctor
@app.route('/inicioEnfermera')
def inicioEnfermera():
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM citas')
        cita = cur.fetchall()
        return render_template('inicioEnfermera.html', citas=cita)
    else:
        return render_template('login.html')

# Funcion que redireciona a registar pacientes
@app.route('/registrarPaciente')
def registrarPaciente():
    if 'user' in session:
        usuario = session['user']
        return render_template('registrarPaciente.html', user=usuario)
    else:
        return render_template('login.html')

# Funcion de registrar una cita de parte de la enfermera
@app.route('/agregarPaciente', methods=['POST'])
def agregarPaciente():
    if request.method == 'POST':
        # ---------------------------
        # General del Paciente
        # ---------------------------
        # ---------------------------
        # Datos de identificacion
        # ---------------------------
        cedula = request.form['cedula']
        numeroSS = request.form['numeroSS']
        nacionalidad = request.form['nacionalidad']
        # ---------------------------
        # Datos personal del paciente
        # ---------------------------
        primerNombre = request.form['primerNombre']
        segundoNombre = request.form['segundoNombre']
        primerApellido = request.form['primerApellido']
        segundoApellido = request.form['segundoApellido']
        sexo = request.form['sexo']
        estadoCivil = request.form['estadoCivil']
        tipodeSangre = request.form['tipodeSangre']
        temperatura = request.form['temperatura']
        edad = request.form['edad']
        estatura = request.form['estatura']
        peso = request.form['peso']
        fechadeNacimiento = request.form['fechadeNacimiento']
        # ---------------------------
        # Contacto / Dirección del paciente
        # ---------------------------
        provincia = request.form['provincia']
        distrito = request.form['distrito']
        corregimiento = request.form['corregimiento']
        direcionDetallada = request.form['direcionDetallada']
        telefonodeCasa = request.form['telefonodeCasa']
        telefonoCelular = request.form['telefonoCelular']
        telefonodeTrabajo = request.form['telefonodeTrabajo']
        email = request.form['email']
        # ---------------------------
        # Datos universitarios
        # ---------------------------
        tipodePaciente = request.form['tipodePaciente']
        facultad = request.form['facultad']
        centro = request.form['centro']
        instancia = request.form['instancia']
        # ---------------------------
        # Antecedentes
        # ---------------------------
        # ---------------------------
        # Patologicos
        # ---------------------------
        enfermedades = request.form['enfermedades']
        medicamentos = request.form['medicamentos']
        alergias = request.form['alergias']
        cirugiaPrevia = request.form['cirugiaPrevia']
        hospitalPrevia = request.form['hospitalPrevia']
        accidentes = request.form['accidentes']
        transfucion = request.form['transfucion']
        # ---------------------------
        # No patologicos
        # ---------------------------
        tabaco = request.form['tabaco']
        cantidadTabaco = request.form['cantidadTabaco']
        alcohol = request.form['alcohol']
        cantidadAlcohol = request.form['cantidadAlcohol']
        droga = request.form['droga']
        cantidadDroga = request.form['cantidadDroga']
        # ---------------------------
        # Familiares
        # ---------------------------
        antecedentePadre = request.form['antecedentePadre']
        antecedenteMadre = request.form['antecedenteMadre']
        antecedenteHermano = request.form['antecedenteHermano']
        abuelosMaternos = request.form['abuelosMaternos']
        abuelosPaternos = request.form['abuelosPaternos']
        tiosMaternos = request.form['tiosMaternos']
        tiosPaternos = request.form['tiosPaternos']
        # ---------------------------
        # Gineco-obstétricos
        # ---------------------------
        menarcaEdad = request.form['menarcaEdad']
        fechaMestruacion = request.form['fechaMestruacion']
        fechaUltimoParto = request.form['fechaUltimoParto']
        gestas = request.form['gestas']
        partos = request.form['partos']
        abortos = request.form['abortos']
        cesarea = request.form['cesarea']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO generalpaciente (cedula, numeroSS, nacionalidad, primerNombre, segundoNombre, primerApellido, segundoApellido, sexo, estadoCivil, tipodeSangre, temperatura, edad, estatura, peso, fechadeNacimiento, provincia, distrito, corregimiento, direcionDetallada, telefonodeCasa, telefonoCelular, telefonodeTrabajo, email, tipodePaciente, facultad, centro, instancia, enfermedades, medicamentos, alergias, cirugiaPrevia, hospitalPrevia, accidentes, transfucion, tabaco, cantidadTabaco, alcohol, cantidadAlcohol, droga, cantidadDroga, antecedentePadre, antecedenteMadre, antecedenteHermano, abuelosMaternos, abuelosPaternos, tiosMaternos, tiosPaternos, menarcaEdad, fechaMestruacion, fechaUltimoParto, gestas, partos, abortos, cesarea) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (cedula, numeroSS, nacionalidad, primerNombre, segundoNombre, primerApellido, segundoApellido, sexo, estadoCivil, tipodeSangre, temperatura, edad, estatura, peso, fechadeNacimiento, provincia, distrito, corregimiento, direcionDetallada, telefonodeCasa, telefonoCelular, telefonodeTrabajo, email, tipodePaciente, facultad, centro, instancia, enfermedades, medicamentos, alergias, cirugiaPrevia, hospitalPrevia, accidentes, transfucion, tabaco, cantidadTabaco, alcohol, cantidadAlcohol, droga, cantidadDroga, antecedentePadre, antecedenteMadre, antecedenteHermano, abuelosMaternos, abuelosPaternos, tiosMaternos, tiosPaternos, menarcaEdad, fechaMestruacion, fechaUltimoParto, gestas, partos, abortos, cesarea))
        mysql.connection.commit()
        flash('Paciente Registrado Satisfactoriamente')
    return redirect(url_for('registrarPaciente'))


# Funcion de aceptar una cita de parte de la enfermera
@app.route('/aceptarCita/<id>')
def aceptarCita(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM citas WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Cita Aceptada Satisfactoriamente')
    return redirect(url_for('inicioEnfermera'))


# Funcion para elimnar una cita de parte de la enfermera
@app.route('/eliminarCita/<string:id>')
def eliminarCita(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM citas WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Cita Eliminada Satisfactoriamente')
    return redirect(url_for('inicioEnfermera'))

# Final de seciones de la enfermera -------------------------------




# Sesion de los Doctores ------------------------------------------

# Funcion del inicio del doctor
@app.route('/inicioDoc')
def inicioDoc():
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM generalpaciente')
        paciente = cur.fetchall()
        return render_template('inicioDoc.html', pacientes=paciente)
    else:
        return render_template('login.html')

# Funcion del inicio del doctor para poder ver los pacientes
@app.route('/inicioDocVer/<id>')
def inicioDocVer(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM generalpaciente where id = {0}'.format(id))
        paciente = cur.fetchall()
        return render_template('inicioDocVer.html', pacientes=paciente)
    else:
        return render_template('login.html')

# Funcion del inicio del doctor para editar los pacientes ingresar la modificacion
@app.route('/inicioDocEdit/<id>')
def inicioDocEdit(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM generalpaciente where id = {0}'.format(id))
        paciente = cur.fetchall()
        return render_template('inicioDocEdit.html', pacientes=paciente)
    else:
        return render_template('login.html')

# Funcion del inicio del doctor para editar los pacientes realizar la modificacion esta es la funcion del uptade
@app.route('/inicioDocEditModi/<id>', methods=['POST'])
def inicioDocEditModi(id):
    if 'user' in session:
        if request.method == 'POST':
            # ---------------------------
            # General del Paciente
            # ---------------------------
            # ---------------------------
            # Datos de identificacion
            # ---------------------------
            cedula = request.form['cedula']
            numeroSS = request.form['numeroSS']
            nacionalidad = request.form['nacionalidad']
            # ---------------------------
            # Datos personal del paciente
            # ---------------------------
            primerNombre = request.form['primerNombre']
            segundoNombre = request.form['segundoNombre']
            primerApellido = request.form['primerApellido']
            segundoApellido = request.form['segundoApellido']
            sexo = request.form['sexo']
            estadoCivil = request.form['estadoCivil']
            tipodeSangre = request.form['tipodeSangre']
            temperatura = request.form['temperatura']
            edad = request.form['edad']
            estatura = request.form['estatura']
            peso = request.form['peso']
            fechadeNacimiento = request.form['fechadeNacimiento']
            # ---------------------------
            # Contacto / Dirección del paciente
            # ---------------------------
            provincia = request.form['provincia']
            distrito = request.form['distrito']
            corregimiento = request.form['corregimiento']
            direcionDetallada = request.form['direcionDetallada']
            telefonodeCasa = request.form['telefonodeCasa']
            telefonoCelular = request.form['telefonoCelular']
            telefonodeTrabajo = request.form['telefonodeTrabajo']
            email = request.form['email']
            # ---------------------------
            # Datos universitarios
            # ---------------------------
            tipodePaciente = request.form['tipodePaciente']
            facultad = request.form['facultad']
            centro = request.form['centro']
            instancia = request.form['instancia']
            # ---------------------------
            # Antecedentes
            # ---------------------------
            # ---------------------------
            # Patologicos
            # ---------------------------
            enfermedades = request.form['enfermedades']
            medicamentos = request.form['medicamentos']
            alergias = request.form['alergias']
            cirugiaPrevia = request.form['cirugiaPrevia']
            hospitalPrevia = request.form['hospitalPrevia']
            accidentes = request.form['accidentes']
            transfucion = request.form['transfucion']
            # ---------------------------
            # No patologicos
            # ---------------------------
            tabaco = request.form['tabaco']
            cantidadTabaco = request.form['cantidadTabaco']
            alcohol = request.form['alcohol']
            cantidadAlcohol = request.form['cantidadAlcohol']
            droga = request.form['droga']
            cantidadDroga = request.form['cantidadDroga']
            # ---------------------------
            # Familiares
            # ---------------------------
            antecedentePadre = request.form['antecedentePadre']
            antecedenteMadre = request.form['antecedenteMadre']
            antecedenteHermano = request.form['antecedenteHermano']
            abuelosMaternos = request.form['abuelosMaternos']
            abuelosPaternos = request.form['abuelosPaternos']
            tiosMaternos = request.form['tiosMaternos']
            tiosPaternos = request.form['tiosPaternos']
            # ---------------------------
            # Gineco-obstétricos
            # ---------------------------
            menarcaEdad = request.form['menarcaEdad']
            fechaMestruacion = request.form['fechaMestruacion']
            fechaUltimoParto = request.form['fechaUltimoParto']
            gestas = request.form['gestas']
            partos = request.form['partos']
            abortos = request.form['abortos']
            cesarea = request.form['cesarea']
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE generalpaciente
                SET cedula = %s,
                    numeroSS = %s,
                    nacionalidad = %s,
                    primerNombre = %s,
                    segundoNombre = %s,
                    primerApellido = %s,
                    segundoApellido = %s,
                    sexo = %s,
                    estadoCivil = %s,
                    tipodeSangre = %s,
                    temperatura = %s,
                    edad = %s,
                    estatura = %s,
                    peso = %s,
                    fechadeNacimiento = %s,
                    provincia = %s,
                    distrito = %s,
                    corregimiento = %s,
                    direcionDetallada = %s,
                    telefonodeCasa = %s,
                    telefonoCelular = %s,
                    telefonodeTrabajo = %s,
                    email = %s,
                    tipodePaciente = %s,
                    facultad = %s,
                    centro = %s,
                    instancia = %s,
                    enfermedades = %s,
                    medicamentos = %s,
                    alergias = %s,
                    cirugiaPrevia = %s,
                    hospitalPrevia = %s,
                    accidentes = %s,
                    transfucion = %s,
                    tabaco = %s,
                    cantidadTabaco = %s,
                    alcohol = %s,
                    cantidadAlcohol = %s,
                    droga = %s,
                    cantidadDroga = %s,
                    antecedentePadre = %s,
                    antecedenteMadre = %s,
                    antecedenteHermano = %s,
                    abuelosMaternos = %s,
                    abuelosPaternos = %s,
                    tiosMaternos = %s,
                    tiosPaternos = %s,
                    menarcaEdad = %s,
                    fechaMestruacion = %s,
                    fechaUltimoParto = %s,
                    gestas = %s,
                    partos = %s,
                    abortos = %s,
                    cesarea = %s
                WHERE id = %s
            """, (cedula, numeroSS, nacionalidad, primerNombre, segundoNombre, primerApellido,
            segundoApellido, sexo, estadoCivil, tipodeSangre, temperatura, edad, 
            estatura, peso, fechadeNacimiento, provincia, distrito, corregimiento,
            direcionDetallada, telefonodeCasa, telefonoCelular, telefonodeTrabajo, email, tipodePaciente,
            facultad, centro, instancia, enfermedades, medicamentos, alergias,
            cirugiaPrevia, hospitalPrevia, accidentes, transfucion, tabaco, cantidadTabaco,
            alcohol, cantidadAlcohol, droga, cantidadDroga, antecedentePadre, antecedenteMadre,
            antecedenteHermano, abuelosMaternos, abuelosPaternos, tiosMaternos, tiosPaternos, menarcaEdad,
            fechaMestruacion, fechaUltimoParto, gestas, partos, abortos, cesarea, id))
            mysql.connection.commit()
            flash('Paciente Editado Satisfactoriamente')
            return redirect(url_for('inicioDoc'))
    else:
        return render_template('login.html')

# Funcion para eliminar paciente de parte de la doctora
@app.route('/eliminarPaciente/<string:id>')
def eliminarPaciente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM generalpaciente WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Paciente Eliminado Satisfactoriamente')
    return redirect(url_for('inicioDoc'))



# Funcion de archivo clinico
@app.route('/archivoClinico')
def archivoClinico():
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM citas')
        cita = cur.fetchall()
        return render_template('archivoClinico.html', citas=cita)
    else:
        return render_template('login.html')


# Funcion regitrar un archivo clinico
@app.route('/agregarArchivo', methods=['POST'])
def agregarArchivo():
    if 'user' in session:
        if request.method == 'POST':
            paciente = request.form['paciente']
            cedula = request.form['cedula']
            numeross = request.form['numeroSS']
            fecha = request.form['fecha']
            afeccion = request.form['afeccion']
            cie = request.form['cie']
            diagnostico = request.form['diagnostico']
            tratamiento = request.form['tratamiento']
            procedimiento = request.form['procedimiento']
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO archivoclinico (paciente, cedula, numeross, fecha, afeccion, cie, diagnostico, tratamiento, procedimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (paciente, cedula, numeross, fecha, afeccion, cie, diagnostico, tratamiento, procedimiento))
            mysql.connection.commit()
            flash('Archivo Clínico Agregada Satisfactoriamente')
            return redirect(url_for('archivoClinico'))   
    else:
        return render_template('login.html')


# Funcion de mostra el menu de los archivos clinicos
@app.route('/archivoClinicoMenu')
def archivoClinicoMenu():
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM archivoclinico')
        paciente = cur.fetchall()
        return render_template('archivoClinicoMenu.html', pacientes=paciente)
    else:
        return render_template('login.html')

# Funcion de ver los archivos clinicos
@app.route('/archivoClinicoVer/<id>')
def archivoClinicoVer(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM archivoclinico where id = {0}'.format(id))
        archi = cur.fetchall()
        return render_template('archivoClinicoVer.html', archivos=archi)
    else:
        return render_template('login.html')


# Funcion de ver las fererencias con el id
@app.route('/archivoClinicoEdit/<id>')
def archivoClinicoEdit(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM archivoclinico where id = {0}'.format(id))
        archi = cur.fetchall()
        return render_template('archivoClinicoEdit.html', archivos=archi)
    else:
        return render_template('login.html')

# Funcion de ver las fererencias con el id
@app.route('/archivoClinicoEditModi/<id>', methods=['POST'])
def archivoClinicoEditModi(id):
    if 'user' in session:
        if request.method == 'POST':
            paciente = request.form['paciente']
            cedula = request.form['cedula']
            numeross = request.form['numeroSS']
            fecha = request.form['fecha']
            afeccion = request.form['afeccion']
            cie = request.form['cie']
            diagnostico = request.form['diagnostico']
            tratamiento = request.form['tratamiento']
            procedimiento = request.form['procedimiento']
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE archivoclinico
                SET paciente = %s,
                    cedula = %s,
                    numeross = %s,
                    fecha = %s,
                    afeccion = %s,
                    cie = %s,
                    diagnostico = %s,
                    tratamiento = %s,
                    procedimiento = %s
                WHERE id = %s
            """, (paciente, cedula, numeross, fecha, afeccion, cie, diagnostico, tratamiento, procedimiento, id))
            mysql.connection.commit()
            flash('Archivo Clínico Editada Satisfactoriamente')
            return redirect(url_for('archivoClinicoMenu'))
    else:
        return render_template('login.html')

# Funcion para eliminar referencias
@app.route('/archivoClinicoEli/<string:id>')
def archivoClinicoEli(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM archivoclinico WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Archivo Clínico Eliminada Satisfactoriamente')
    return redirect(url_for('archivoClinicoMenu'))


# Funcion de las hoja de referencias
@app.route('/referencia')
def referencia():
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM citas')
        cita = cur.fetchall()
        return render_template('referencia.html', citas=cita)
    else:
        return render_template('login.html')


# Funcion de agregar una referencia de parte del doctor al paciente
@app.route('/agregarRefe', methods=['POST'])
def agregarRefe():
    if request.method == 'POST':
        paciente = request.form['paciente']
        doctor = request.form['doctor']
        referir = request.form['referir']
        fecha = request.form['fecha']
        sintomas = request.form['sintomas']
        tratamiento = request.form['tratamiento']
        examenfisico = request.form['examenfisico']
        diagnostico = request.form['diagnostico']
        laboratorio = request.form['laboratorio']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO referencia (paciente, doctor, refiere, fecha, sintomas, tratamiento, examenfisico, diagnostico, laboratorios) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (paciente, doctor, referir, fecha, sintomas, tratamiento, examenfisico, diagnostico, laboratorio))
        mysql.connection.commit()
        flash('Referencia Agregada Satisfactoriamente')
    return redirect(url_for('referencia'))


# Funcion de mostra el menu de las referencias
@app.route('/referenciaMenu')
def referenciaMenu():
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM referencia')
        paciente = cur.fetchall()
        return render_template('referenciaMenu.html', pacientes=paciente)
    else:
        return render_template('login.html')

# Funcion de ver las fererencias con el id
@app.route('/referenciaVer/<id>')
def referenciaVer(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM referencia where id = {0}'.format(id))
        refe = cur.fetchall()
        return render_template('referenciaVer.html', referencia=refe)
    else:
        return render_template('login.html')



# Funcion de ver las fererencias con el id
@app.route('/referenciaEdit/<id>')
def referenciaEdit(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM referencia where id = {0}'.format(id))
        refe = cur.fetchall()
        return render_template('referenciaEdit.html', referencia=refe)
    else:
        return render_template('login.html')

# Funcion de ver las fererencias con el id
@app.route('/referenciaEditModi/<id>', methods=['POST'])
def referenciaEditModi(id):
    if 'user' in session:
        if request.method == 'POST':
            paciente = request.form['paciente']
            doctor = request.form['doctor']
            referir = request.form['referir']
            fecha = request.form['fecha']
            sintomas = request.form['sintomas']
            tratamiento = request.form['tratamiento']
            examenfisico = request.form['examenfisico']
            diagnostico = request.form['diagnostico']
            laboratorio = request.form['laboratorio']
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE referencia
                SET paciente = %s,
                    doctor = %s,
                    refiere = %s,
                    fecha = %s,
                    sintomas = %s,
                    tratamiento = %s,
                    examenfisico = %s,
                    diagnostico = %s,
                    laboratorios = %s
                WHERE id = %s
            """, (paciente, doctor, referir, fecha, sintomas, tratamiento, examenfisico, diagnostico, laboratorio, id))
            mysql.connection.commit()
            flash('Referencia Editada Satisfactoriamente')
            return redirect(url_for('referenciaMenu'))
    else:
        return render_template('login.html')

# Funcion para eliminar referencias
@app.route('/referenciaEli/<string:id>')
def referenciaEli(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM referencia WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Referencia Eliminada Satisfactoriamente')
    return redirect(url_for('referenciaMenu'))


# Funcion de recetar los laboratorios
@app.route('/recetarLab')
def recetarLab():
    if 'user' in session:
        return render_template('recetarLab.html')
    else:
        return render_template('login.html')


# Funcion de agregar una receta de laboratorio
@app.route('/agregarLab', methods=['POST'])
def agregarLab():
    if request.method == 'POST':
        paciente = request.form['paciente']
        cedula = request.form['cedula']
        numeroSS = request.form['numeroSS']
        fecha = request.form['fecha']
        parasitologia = request.form['parasitologia']
        urinalisis = request.form['urinalisis']
        bacteriologia = request.form['bacteriologia']
        hematologia = request.form['hematologia']
        serologia = request.form['serologia']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO laboratorios (paciente, cedula, numeroSS, fecha, parasitologia, urinalisis, bacteriologia, hematologia, serologia) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    ( paciente, cedula, numeroSS, fecha, parasitologia, urinalisis, bacteriologia, hematologia, serologia))
        mysql.connection.commit()
        flash('Receta de Laboratorio Agregada Satisfactoriamente')
    return redirect(url_for('recetarLab'))

# Funcion de mostra el menu de las recetas de los laboratorios
@app.route('/recetarLabMenu')
def recetarLabMenu():
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM laboratorios')
        laboratorios = cur.fetchall()
        return render_template('recetarLabMenu.html', laboratorios=laboratorios)
    else:
        return render_template('login.html')


# Funcion de ver las recetas del laboratorio conel id
@app.route('/recetarLabVer/<id>')
def recetarLabVer(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM laboratorios where id = {0}'.format(id))
        laboratorios = cur.fetchall()
        return render_template('recetarLabVer.html', laboratorios=laboratorios)
    else:
        return render_template('login.html')


# Funcion de editar las recetas de los laboratorios
@app.route('/recetarLabEdit/<id>')
def recetarLabEdit(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM laboratorios where id = {0}'.format(id))
        laboratorios = cur.fetchall()
        return render_template('recetarLabEdit.html', laboratorios=laboratorios)
    else:
        return render_template('login.html')

# Funcion de ejecutar la modificaciones de la recetas 
@app.route('/recetarLabEditModi/<id>', methods=['POST'])
def recetarLabEditModi(id):
    if 'user' in session:
        if request.method == 'POST':
            paciente = request.form['paciente']
            cedula = request.form['cedula']
            numeroSS = request.form['numeroSS']
            fecha = request.form['fecha']
            parasitologia = request.form['parasitologia']
            urinalisis = request.form['urinalisis']
            bacteriologia = request.form['bacteriologia']
            hematologia = request.form['hematologia']
            serologia = request.form['serologia']
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE laboratorios
                SET paciente = %s,
                    cedula = %s,
                    numeroSS = %s,
                    fecha = %s,
                    parasitologia = %s,
                    urinalisis = %s,
                    bacteriologia = %s,
                    hematologia = %s,
                    serologia = %s
                WHERE id = %s
            """, (paciente, cedula, numeroSS, fecha, parasitologia, urinalisis, bacteriologia, hematologia, serologia, id))
            mysql.connection.commit()
            flash('Laboratorio Editada Satisfactoriamente')
            return redirect(url_for('recetarLabMenu'))
    else:
        return render_template('login.html')


# Funcion para eliminar recetas de laboratorios
@app.route('/recetarLabEli/<string:id>')
def recetarLabEli(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM laboratorios WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Receta Eliminada Satisfactoriamente')
    return redirect(url_for('recetarLabMenu'))


# Funcion del documentos clinicos
@app.route('/docuClinico')
def docuClinico():
    if 'user' in session:
        return render_template('docuClinico.html')
    else:
        return render_template('login.html')


# Funcion de las estadisticas
@app.route('/estadis')
def estadis():
    if 'user' in session:
        # Lineal
        line_chart = pygal.Line()
        line_chart.title = 'No. Pacientes'
        line_chart.x_labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        line_chart.add('Sistemas', [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6])
        line_chart.add('Civil',  [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8])
        line_chart.add('Mecanica',      [9.0, 5.2, 7.7, 9.5, 1.9, 25.2, 18.0, 16.6, 14.2, 11.3, 7.6, 9.8])
        line_chart.add('Industrial',      [7.0, 6.0, 9.7, 6.5, 4.9, 10.2, 1.0, 9.6, 12.2, 9.3, 10.6, 8.8])
        line_chart.add('Ciencia y Tec.',      [2.0, 5.0, 3.7, 2.5, 2.9, 7.0, 3.0, 7.6, 9.2, 7.0, 8.6, 6.8])
        line_chart.add('Electrica',  [5.0, 3.0, 2.7, 7.3, 2.0, 7.0, 5.3, 2.1, 2.2, 3.1, 4.6, 4.0]) 
        line_chart = line_chart.render_data_uri()
        # Barra
        bar = pygal.Bar()
        bar.title = 'Estudiantes Por Facultad'
        bar.x_labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        bar.add('Sistemas', [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6])
        bar.add('Civil',  [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8])
        bar.add('Mecanica',      [9.0, 5.2, 7.7, 9.5, 1.9, 25.2, 18.0, 16.6, 14.2, 11.3, 7.6, 9.8])
        bar.add('Industrial',      [7.0, 6.0, 9.7, 6.5, 4.9, 10.2, 1.0, 9.6, 12.2, 9.3, 10.6, 8.8])
        bar.add('Ciencia y Tec.',      [2.0, 5.0, 3.7, 2.5, 2.9, 7.0, 3.0, 7.6, 9.2, 7.0, 8.6, 6.8])
        bar.add('Electrica',  [5.0, 3.0, 2.7, 7.3, 2.0, 7.0, 5.3, 2.1, 2.2, 3.1, 4.6, 4.0]) 
        bar = bar.render_data_uri()
        # Pie
        pie_chart = pygal.Pie()
        pie_chart.title = 'Afecciones Mas Comunes'
        pie_chart.add('Resfriados', 45.0)
        pie_chart.add('Alergias', 26.8)
        pie_chart.add('Diabetes', 8.5)
        pie_chart.add('Virus', 12.8)
        pie_chart.add('Heridas y moretones', 6.2)
        pie_chart.add('Otras', 0.8)
        pie_chart = pie_chart.render_data_uri()
        return render_template('estadis.html', line_chart=line_chart, bar=bar, pie_chart=pie_chart)
    else:
        return render_template('login.html')


# Cosa que aun no he tocado de aqui hacia abajo --------------------------

# Funcion de los certificados de buena salud
@app.route('/certificado')
def certificado():
    if 'user' in session:
        return render_template('certificado.html')
    else:
        return render_template('login.html')

# Funcion de generar el pdf para el certificado de buena salud
@app.route('/certificadoPDF/<name>/<ubi>')
def certificadoPDF(name, ubi):
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    rendered = render_template('certificadoAsisPDF.html', name=name, ubi=ubi)
    #pdf = pdfkit.from_string(rendered, False)
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=salida.pdf'
    flash('Certificado Generada Satisfactoriamente')
    return rendered    
  

# Funcion de menu de las constancia
@app.route('/constancia')
def constancia():
    if 'user' in session:
        return render_template('constancia.html')
    else:
        return render_template('login.html')

# Funcion de mostra la forma de generar la costancia de asistencia
@app.route('/constanciaAsis')
def constanciaAsis():
    if 'user' in session:
        return render_template('constanciaAsis.html')
    else:
        return render_template('login.html')
        
# Funcion de mostra la forma de generar la costancia de incapacidad
@app.route('/constanciaInca')
def constanciaInca():
    if 'user' in session:
        return render_template('constanciaInca.html')
    else:
        return render_template('login.html')

# Final de la seccion de los doctores ------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
