from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask import flash

## Clase de usuario para poder heredar en las otras tablas
class User:
    data_name = "medcenter"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.mail = data['mail']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, mail, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(mail)s, %(password)s, NOW(), NOW());"
        user = connectToMySQL(cls.data_name).query_db(query, data)
        return user

##clase de citas para info recibida de form
class Session: 
    data_name = "medcenter"
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.hour = data['hour']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.doctor_id = data['doctor_id']
        self.patient_id = data['patient_id']
        self.area_id = data['area_id']
        self.note_id = data['note_id']
        self.first_name = data.get('first_name', "")
        self.last_name = data.get('last_name', "")
        self.area_name = data.get('area_name', "")
        self.dx = data.get('dx', "")
        self.description = data.get('description', "")
        self.mail = data.get('mail', "")

    @classmethod
    def make_appointment(cls,data):
        query = "INSERT INTO sessions (date, hour, created_at, updated_at, doctor_id, patient_id, area_id, note_id) VALUES (%(date)s, %(hour)s, NOW(), NOW(), %(doctor_id)s, %(patient_id)s, %(area_id)s, %(note_id)s);"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        return result 

    @classmethod
    def show_appointments(cls, data):  ##muestra datos de cita para tabla de paciente con citas
        query = """SELECT * FROM sessions 
            JOIN doctors ON doctors.id = sessions.doctor_id
            JOIN areas ON areas.id = sessions.area_id
            JOIN users ON users.id = doctors.user_id
            WHERE patient_id = %(id)s"""
        results = connectToMySQL(cls.data_name).query_db(query, data)
        sessions = []
        for session in results:
            print(session)
            sessions.append(cls(session))
        return sessions
    
    @classmethod
    def get_appointment_id(cls, data):
        query = "SELECT * FROM sessions WHERE sessions.id = %(id)s;"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def patients_with_areas(cls, data):  ##LA CONSULTA FUNCIONA PERO NO PERMITE RECORRERLO, la tengo para mostrar que areas atienden a un solo usuario
        query = """SELECT * FROM sessions 
                JOIN patients ON patients.id = sessions.patient_id
                LEFT JOIN areas ON areas.id = sessions.area_id
                WHERE patients.id = %(id)s
                LIMIT 4
                """
        result = connectToMySQL(cls.data_name).query_db(query, data)
        sessions = []
        for session in result:
            print(session)
            sessions.append(cls(session))
        return sessions
    
    @classmethod
    def sessions_with_patients(cls, data):
        query = """SELECT * FROM sessions 
                JOIN patients ON patients.id = sessions.patient_id
                JOIN users ON users.id = patients.user_id
                WHERE doctor_id = %(id)s"""
        results = connectToMySQL(cls.data_name).query_db(query, data)
        sessions = []
        for session in results:
            print(session)
            sessions.append(cls(session))
        return sessions

    ##Muestra datos de sesion y une id de notas
    @classmethod
    def session_with_notes(cls, data):
        query = """SELECT * FROM sessions
            JOIN patients on patients.id = sessions.patient_id
            JOIN users on users.id = patients.user_id
            LEFT JOIN notes on notes.id = sessions.note_id
            WHERE sessions.id = %(id)s"""
        result = connectToMySQL(cls.data_name).query_db(query, data)
        return cls(result[0])
    
    ##Contador de citas totales hechas en el centro medico 
    @classmethod
    def count_sessions(cls):
        query = "SELECT COUNT(sessions.id) AS total FROM sessions;"
        result = connectToMySQL(cls.data_name).query_db(query)
        print(result)
        return result
    
    ##Contador de sesiones x paciente para restarlas con el amount
    @classmethod
    def sessions_left(cls, data):
        query = """SELECT COUNT(sessions.id) AS taken FROM sessions 
            JOIN patients ON patients.id = sessions.patient_id 
            WHERE patients.id = %(id)s"""
        result = connectToMySQL(cls.data_name).query_db(query,data)
        return result

    @classmethod
    def update_appointment(cls,data):
        query = "UPDATE sessions SET date=%(date)s, hour=%(hour)s, doctor_id=%(doctor_id)s, patient_id=%(patient_id)s, area_id=%(area_id)s, updated_at = NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.data_name).query_db(query,data)
    
    @classmethod
    def delete_appointment(cls,data):
        query = "DELETE FROM sessions WHERE id=%(id)s;"
        return connectToMySQL(cls.data_name).query_db(query,data)
    
    @staticmethod
    def validate_appointment(appointment):
        is_valid = True
        today_date = datetime.today().strftime('%Y-%m-%d')
        if appointment["date"] == "":
            flash("Debes seleccionar una fecha", "register")
            is_valid = False
        if appointment["date"] < today_date:
            flash("Selecciona una fecha valida", "register")
            is_valid = False
        if appointment["hour"] == "":
            flash("Debes seleccionar una hora", "register")
            is_valid = False
        # if appointment["hour"] > 15:   ARREGLA ESTO, COMO PONER LIMITE DE HORA
        #     flash("Recuerda que la ultima cita programable es hasta las 3pm", "register")
        #     is_valid = False
        if appointment["doctor_id"] == "":
            flash("Debes seleccionar un doctor", "register")
            is_valid = False
        if appointment["area_id"] == "":
            flash("Debes seleccionar un servicio", "register")
        ##Valida si doctor SI pertenece al área seleccionada: ARREGLA ESO, CONSULTA VA BIEN PERO ACÁ NO  FUNCIONA
        # query = "SELECT COUNT(%(doctor_id)s) AS area_doctors FROM doctors LEFT JOIN areas ON areas.id = doctors.area_id WHERE areas.id =%(area_id)s)"
        # coincidence = connectToMySQL("medcenter").query_db(query, appointment)
        # if len(coincidence) >= 1:
        #     flash ("El doctor no pertenece a esa area", "register")
        #     is_valid = False
        #     return is_valid
        return is_valid