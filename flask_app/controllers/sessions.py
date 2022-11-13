from flask import request, redirect, render_template,session, flash
from flask_app import app
from flask_app.models.area import Area, Note
from flask_app.models.doctor import Doctor
from flask_app.models.patient import Patient
from flask_app.models.session import Session

## Todo lo relacionado con la pagina de crear cita, citas y con la pagina de servicios
@app.route("/services")
def services_appointment():
    return render_template("services.html") #agrega funciones para mostrar nombre y demas de paciente

@app.route("/patient/takesession")   ##esto va en el boton de pedir cita por servicio
def program_session():
    if 'patient_id' not in session:
        return redirect("/patient/register")
    data = {
        "id" : session['patient_id']
    }
    return render_template("sessions.html", all_doctors = Doctor.get_all_doctors(), all_areas = Area.load_area(), patient = Patient.get_by_id(data)) #agrega funciones para mostrar nombre y demas de paciente


@app.route("/patient/programsession", methods = ['POST'])
def create_appointment():
    if 'patient_id' not in session:
        return redirect("/patient/register")
    if not Session.validate_appointment(request.form):
        return redirect("/patient/takesession")
    
    note_data = {
        'description': ""
    }
    note_id = Note.add_note(note_data)

    data = {
        'date': request.form['date'],
        'hour': request.form['hour'],
        'doctor_id': request.form['doctor_id'],
        'area_id' : request.form['area_id'],
        'patient_id' : session['patient_id'],
        'note_id' : note_id
    }

    Session.make_appointment(data)
    return redirect("/patient/dashboard")

##Actualizar cita 
@app.route("/patient/session/edit/<int:id>")
def edit_template(id):
    if 'patient_id' not in session:
        return redirect('/patient/register')

    data = {
        "id" : id
    }
    appointment = Session.get_appointment_id(data)
    return render_template("editsession.html", session = appointment,  all_doctors = Doctor.get_all_doctors(), all_areas = Area.load_area())

## Pagina de información específica por cita
@app.route("/doctor/session/<int:id>")
def details_appointment(id):
    if 'doctor_id' not in session: 
        return redirect('/doctor/register')
    
    data = {
        "id" : id
    }
    appointment = Session.session_with_notes(data)
    return render_template("appointment.html", session = appointment)

##edita información de citas
@app.route("/session/edit/<int:id>", methods = ['POST'])
def update_appointment(id):
    if 'patient_id' not in session:
        return redirect("/patient/register")
    updated_session = {
            'id' : id,
            'date': request.form['date'],
            'hour': request.form['hour'],
            'area_id': request.form['area_id'],
            'doctor_id': request.form['doctor_id'],
            'patient_id' : session['patient_id']
    }
    if not Session.validate_appointment(request.form):
        flash("Intenta de nuevo, no se modifico la cita", "register")
        return redirect(f"/patient/session/edit/{id}")
    Session.update_appointment(updated_session)
    return redirect("/patient/dashboard")

## Eliminar cita
@app.route("/session/delete/<int:id>")
def delete(id):
    data = {
        "id" : id
    }
    Session.delete_appointment(data)
    if 'patient_id' in session:
        return redirect ("/patient/dashboard")
    if 'doctor_id' in session:
        return redirect("/doctor/dashboard")

##Crear nota de evolución de lo hecho en sesión (hecho por doctor)
@app.route("/session/note/<int:id>", methods = ['POST'])
def create_note(id):
    if 'doctor_id' not in session:
        return redirect("/doctor/register")
    note_content = {
            'id' : id,
            'description': request.form['description']
        }

    if not Note.validate_note(request.form):
        flash("Intenta de nuevo, no se registró la evolución", "notes")
        return redirect("/doctor/dashboard")
    Note.update_note(note_content)
    return redirect("/doctor/dashboard") ##¿Como pasar el id de la cita NO de la nota para volvera a la misma pagian donde se hace la nota?

##Redirige a cualquiera de los dos perfiles
@app.route('/profile')
def redirect_profile():
    if 'patient_id' in session:
        return redirect("/patient/dashboard")
    elif 'doctor_id' in session: 
        return redirect("/doctor/dashboard")
    else:
        return redirect("/")

    ##CIERRE DE SESIÓN DE CUALQUIER TIPO DE USER
@app.route('/logout') 
def logout(): 
    session.clear()
    return redirect('/')