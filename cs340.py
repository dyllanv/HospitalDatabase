from flask import Flask, render_template, request
import mysql.connector as mariadb

app = Flask(__name__)


def connect_to_database(query, request, values=None):
    cnx = mariadb.connect(user='cs340_vangemed', password='PASSWORD',
                                  host='classmysql.engr.oregonstate.edu',
                                  database='cs340_vangemed')
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query, values)
    if request == "GET":
        data = cursor.fetchall()
        cnx.close()
        return data
    else:
        cnx.commit()
        cnx.close()


@app.route('/')
def homepage():
    return render_template('index.html')


# DOCTOR PAGE FUNCTIONS

@app.route('/doctors', methods=['GET', 'POST'])
def doctors_page(dr_search=None):
    if request.method == 'POST':
        post = request.form.to_dict()
        if post["_method"] == "DELETE":
            delete_doctor(post["dr_code"])
        elif post["_method"] == "ADD":
            add_doctor(post)
        elif post["_method"] == "RELATION":
            insert_doctors_units(post["dr_code"], post["unit_id"])
    doctors = get_all_doctors()
    units = get_all_units()
    data = {"doctors": doctors, "units": units, "search": dr_search}
    return render_template('doctors.html', data=data)


def get_all_doctors():
    query = "SELECT * FROM Doctors ORDER BY last_name ASC;"
    data = connect_to_database(query, "GET")
    convert_bools(data)

    return data


def insert_doctors_units(dr_code, unit_id):
    values = (dr_code, unit_id)
    query = "SELECT * FROM DoctorsUnits WHERE dr_code = %s AND unit_id = %s ;"
    data = connect_to_database(query, "GET", values)
    if data:
        print("Doctor already assigned to unit")
    else:
        query = "INSERT INTO DoctorsUnits (`dr_code`, `unit_id`) VALUES (%s, %s);"
        connect_to_database(query, "POST", values)



def remove_doctors_units(dr_code, unit_id):
    query = "DELETE FROM DoctorsUnits WHERE dr_code = %s AND unit_id = %s;"
    values = (dr_code, unit_id)
    connect_to_database(query, "POST", values)


def add_doctor(data):
    first_name = data["fname"]
    last_name = data["lname"]
    sex = data["sex"]
    on_duty = data["duty"]
    in_house = data["house"]
    attending = data["att_res"]
    phone = data["phone"]

    query = "INSERT INTO Doctors (`first_name`, `last_name`, `sex`, `on_duty`, `in_house`, `attending`, `phone`) " \
            "VALUES (%s,%s,%s,%s,%s,%s,%s);"
    values = (first_name, last_name, sex, on_duty, in_house, attending, phone)
    connect_to_database(query, "POST", values)


def delete_doctor(dr_code):
    query = "DELETE FROM Doctors WHERE dr_code = " + dr_code + ";"
    connect_to_database(query, "POST")


@app.route('/doctors/<dr_code>', methods=['GET', 'POST'])
def dr_pat_page(dr_code):
    if request.method == "POST":
        post = request.form.to_dict()
        print(post)
        update_doctor(post)
    doctor = get_doctor(dr_code)
    patients = get_doctor_patients(dr_code)
    data = {"doctor": doctor[0], "patients": patients}

    return render_template('dr_pats.html', data=data)


def get_doctor(dr_code):
    query = "SELECT dr_code, first_name AS dr_first, last_name AS dr_last, sex AS dr_sex, on_duty, in_house, " \
            "attending, phone FROM Doctors WHERE dr_code = " + dr_code + ";"
    data = connect_to_database(query, "GET")

    return data


def update_doctor(data):
    dr_code = data["dr_code"]
    first_name = data["fname"]
    last_name = data["lname"]
    sex = data["sex"]
    on_duty = data["duty"]
    in_house = data["house"]
    attending = data["att_res"]
    phone = data["phone"]

    query = "UPDATE Doctors SET first_name = %s, last_name = %s, sex = %s, on_duty = %s, " \
            " in_house = %s, attending = %s, phone = %s WHERE dr_code = %s;"
    values = (first_name, last_name, sex, on_duty, in_house, attending, phone, dr_code)
    connect_to_database(query, "POST", values)


def get_doctor_patients(dr_code):
    query = "SELECT p.*, n.first_name AS rn_first, n.last_name AS rn_last, u.name FROM Patients p " \
            "JOIN Doctors d ON p.dr_code = d.dr_code AND d.dr_code = " + str(dr_code) + \
            " JOIN Units u ON p.unit_id = u.unit_id " \
            "JOIN Nurses n ON p.rn_code = n.rn_code ORDER BY p.last_name;"
    data = connect_to_database(query, "GET")
    convert_bools(data)

    return data


@app.route('/doctors/results', methods=['POST'])
def doctor_results():
    if request.method == 'POST':
        post = request.form.to_dict()
        last_name = post["search"]
        query = "SELECT * FROM Doctors WHERE last_name = '" + str(last_name) + "';"
        data = connect_to_database(query, "GET")
        convert_bools(data)

        return doctors_page(data)



# NURSE PAGE FUNCTIONS

@app.route('/nurses', methods=['GET', 'POST'])
def nurses_page(rn_search=None):
    if request.method == 'POST':
        post = request.form.to_dict()
        if post["_method"] == "DELETE":
            delete_nurse(post["rn_code"])
        elif post["_method"] == "ADD":
            add_nurse(post)
        elif post["_method"] == "RELATION":
            insert_nurses_units(post["rn_code"], post["unit_id"])
    nurses = get_all_nurses()
    units = get_all_units()
    data = {"nurses": nurses, "units": units, "search": rn_search}
    return render_template('nurses.html', data=data)


def get_all_nurses():
    query = "SELECT * FROM Nurses ORDER BY last_name ASC;"
    data = connect_to_database(query, "GET")
    convert_bools(data)

    return data


def insert_nurses_units(rn_code, unit_id):
    values = (rn_code, unit_id)
    query = "SELECT * FROM NursesUnits WHERE rn_code = %s AND unit_id = %s ;"
    data = connect_to_database(query, "GET", values)
    if data:
        print("Nurse already assigned to unit")
    else:
        query = "INSERT INTO NursesUnits (`rn_code`, `unit_id`) VALUES (%s, %s);"
        connect_to_database(query, "POST")


def remove_nurses_units(rn_code, unit_id):
    query = "DELETE FROM NursesUnits WHERE rn_code = %s AND unit_id = %s;"
    values = (rn_code, unit_id)
    connect_to_database(query, "POST", values)


def add_nurse(data):
    first_name = data["fname"]
    last_name = data["lname"]
    sex = data["sex"]
    on_duty = data["duty"]
    phone = data["phone"]

    query = "INSERT INTO Nurses (`first_name`, `last_name`, `sex`, `on_duty`, `phone`) " \
            "VALUES (%s,%s,%s,%s,%s);"
    values = (first_name, last_name, sex, on_duty, phone)
    connect_to_database(query, "POST", values)


def delete_nurse(rn_code):
    query = "DELETE FROM Nurses WHERE rn_code = " + rn_code + ";"
    connect_to_database(query, "POST")


@app.route('/nurses/<rn_code>', methods=["GET", "POST"])
def rn_pat_page(rn_code):
    if request.method == "POST":
        post = request.form.to_dict()
        update_nurse(post)
    nurse = get_nurse(rn_code)
    patients = get_nurse_patients(rn_code)
    data = {"nurse": nurse[0], "patients": patients}

    return render_template('rn_pats.html', data=data)


def get_nurse(rn_code):
    query = "SELECT rn_code, first_name AS rn_first, last_name AS rn_last, sex AS rn_sex, on_duty, phone " \
            "FROM Nurses WHERE rn_code = " + rn_code + ";"
    data = connect_to_database(query, "GET")

    return data


def update_nurse(data):
    rn_code = data["rn_code"]
    first_name = data["fname"]
    last_name = data["lname"]
    sex = data["sex"]
    on_duty = data["duty"]
    phone = data["phone"]
    query = "UPDATE Nurses SET first_name = %s, last_name = %s, sex = %s, on_duty = %s, phone = %s " \
            "WHERE rn_code = %s;"
    values = (first_name, last_name, sex, on_duty, phone, rn_code)
    connect_to_database(query, "POST", values)


def get_nurse_patients(rn_code):
    query = "SELECT p.*, d.first_name AS dr_first, d.last_name AS dr_last, u.name FROM Patients p " \
            "JOIN Doctors d ON p.dr_code = d.dr_code " \
            "JOIN Units u ON p.unit_id = u.unit_id " \
            "JOIN Nurses n ON p.rn_code = n.rn_code WHERE n.rn_code = " + str(rn_code) + \
            " ORDER BY p.last_name;"
    data = connect_to_database(query, "GET")
    convert_bools(data)

    return data


@app.route('/nurses/results', methods=['POST'])
def nurse_results():
    if request.method == 'POST':
        post = request.form.to_dict()
        last_name = post["search"]
        query = "SELECT * FROM Nurses WHERE last_name = '" + str(last_name) + "';"
        data = connect_to_database(query, "GET")
        convert_bools(data)
        return nurses_page(data)



# UNIT PAGE FUNCTIONS

@app.route('/units', methods=['GET', 'POST'])
def units_page():
    if request.method == 'POST':
        post = request.form.to_dict()
        if len(post) == 1:
            delete_unit(post["unit_id"])
        else:
            add_unit(post)
    units = get_all_units()
    doctors = get_all_doctors()
    data = {"units": units, "doctors": doctors}
    return render_template('units.html', data=data)


def get_all_units():
    query = "SELECT * FROM Units ORDER BY name ASC;"
    data = connect_to_database(query, "GET")
    doctors = get_all_doctors()
    for u in data:
        for dr in doctors:
            if dr["dr_code"] == u["dept_head"]:
                u["head_name"] = dr["last_name"] + ", " + dr["first_name"]

    return data


def add_unit(data):
    name = data["name"]
    dept_head = data["dept_head"]
    phone = data["phone"]

    query = "INSERT INTO Units (`name`, `dept_head`, `phone`) " \
            "VALUES (%s,%s,%s);"
    values = (name, dept_head, phone)
    connect_to_database(query, "POST", values)


def delete_unit(unit_id):
    query = "DELETE FROM Units WHERE unit_id = " + unit_id + ";"
    connect_to_database(query, "POST")


@app.route('/units/<unit_id>', methods=['GET', 'POST'])
def unit_page(unit_id):
    search = 0
    if request.method == "POST":
        post = request.form.to_dict()
        if post["_method"] == "UPDATE":
            update_unit(post)
        elif post["_method"] == "ADD":
            add_patient(post)
        elif post["_method"] == "DELETE":
            delete_patient(post["pat_id"])
        elif post["_method"] == "REMOVE DR":
            remove_doctors_units(post["dr_code"], post["unit_id"])
        elif post["_method"] == "REMOVE RN":
            remove_nurses_units(post["rn_code"], post["unit_id"])
        elif post["_method"] == "FILTER":
            if len(post) == 2:
                search = 1
    unit = get_unit(unit_id)
    patients = get_unit_patients(unit_id)
    doctors = get_unit_doctors(unit_id)
    nurses = get_unit_nurses(unit_id)
    data = {"unit": unit, "patients": patients, "doctors": doctors, "nurses": nurses, "search": search}

    return render_template('unit_pats.html', data=data)


def update_unit(data):
    unit_id = data["unit_id"]
    name = data["name"]
    dept_head = data["dept_head"]
    phone = data["phone"]
    query = "UPDATE Units SET name = %s, dept_head = %s, phone = %s " \
            "WHERE unit_id = %s;"
    values = (name, dept_head, phone, unit_id)
    connect_to_database(query, "POST", values)


def get_unit(unit_id):
    query = "SELECT u.*, d.first_name, d.last_name FROM Units u " \
            "JOIN Doctors d ON u.dept_head = d.dr_code " \
            "WHERE unit_id = " + unit_id + ";"
    data = connect_to_database(query, "GET")

    return data[0]


def get_unit_patients(unit_id):
    query = "SELECT p.*, d.first_name AS dr_first, d.last_name AS dr_last, n.first_name AS rn_first, " \
            "n.last_name AS rn_last, u.name FROM Patients p " \
            "JOIN Units u ON p.unit_id = u.unit_id AND u.unit_id = " + unit_id + \
            " JOIN Doctors d ON p.dr_code = d.dr_code " \
            "JOIN Nurses n ON p.rn_code = n.rn_code " \
            "ORDER BY p.last_name;"
    data = connect_to_database(query, "GET")

    return data


def get_unit_nurses(unit_id):
    query = "SELECT n.*, u.unit_id FROM Nurses n " \
            "JOIN NursesUnits nu ON n.rn_code = nu.rn_code " \
            "JOIN Units u on nu.unit_id = u.unit_id " \
            "WHERE u.unit_id = " + unit_id + \
            " ORDER BY n.last_name ASC;"
    data = connect_to_database(query, "GET")

    return data


def get_unit_doctors(unit_id):
    query = "SELECT d.*, u.unit_id FROM Doctors d " \
            "JOIN DoctorsUnits du ON d.dr_code = du.dr_code " \
            "JOIN Units u on du.unit_id = u.unit_id " \
            "WHERE u.unit_id = " + unit_id + \
            " ORDER BY d.last_name ASC;"
    data = connect_to_database(query, "GET")

    return data



# PATIENT PAGE FUNCTIONS

@app.route('/patients', methods=['GET', 'POST'])
def patients_page(pat_search=None):
    patients = get_all_patients()
    data = {"patients": patients, "search": pat_search}

    return render_template('patients.html', data=data)


def get_all_patients():
    query = "SELECT p.*, n.first_name AS rn_first, n.last_name AS rn_last, d.first_name AS dr_first, " \
            "d.last_name AS dr_last, u.name AS unit_name FROM Patients p " \
            "JOIN Doctors d ON p.dr_code = d.dr_code " \
            "JOIN Nurses n ON p.rn_code = n.rn_code " \
            "JOIN Units u ON p.unit_id = u.unit_id " \
            "ORDER BY p.last_name ASC;"
    data = connect_to_database(query, "GET")
    convert_bools(data)

    return data


def add_patient(data):
    first_name = data["fname"]
    last_name = data["lname"]
    sex = data["sex"]
    dob = data["dob"]
    admit_date = data["admit"]
    anticipated_discharge = data["ant_dis"]
    code_status = data["code"]
    diagnosis = data["diagnosis"]
    room = data["room"]
    rn_code = data["nurse"]
    dr_code = data["doctor"]
    unit_id = data["unit_id"]

    query = "INSERT INTO Patients (`first_name`, `last_name`, `sex`, `dob`, `admit_date`, `anticipated_discharge`, " \
            "`code_status`, `diagnosis`, `room`, `rn_code`, `dr_code`, `unit_id`) " \
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    values = (first_name, last_name, sex, dob, admit_date, anticipated_discharge, code_status,
              diagnosis, room, rn_code, dr_code, unit_id)
    connect_to_database(query, "POST", values)


def delete_patient(pat_id):
    query = "DELETE FROM Patients WHERE pat_id = " + pat_id + ";"
    connect_to_database(query, "POST")


@app.route('/patients/<pat_id>', methods=['GET', 'POST'])
def pat_page(pat_id):
    if request.method == "POST":
        post = request.form.to_dict()
        update_patient(post)
    patient = get_patient(pat_id)
    doctors = get_all_doctors()
    nurses = get_all_nurses()
    units = get_all_units()
    data = {"patient": patient[0], "doctors": doctors, "nurses": nurses, "units": units}
    return render_template('pat_page.html', data=data)


def get_patient(pat_id):
    query = "SELECT p.*, d.first_name AS dr_first, d.last_name AS dr_last, n.first_name AS rn_first, " \
            "n.last_name AS rn_last, n.sex AS rn_sex, n.on_duty, u.name AS unit_name FROM Patients p " \
            "JOIN Doctors d ON p.dr_code = d.dr_code " \
            "JOIN Nurses n ON p.rn_code = n.rn_code " \
            "JOIN Units u ON p.unit_id = u.unit_id " \
            "WHERE p.pat_id = " + pat_id + ";"
    data = connect_to_database(query, "GET")
    convert_bools(data)

    return data


def update_patient(data):
    pat_id = data["pat_id"]
    first_name = data["fname"]
    last_name = data["lname"]
    sex = data["sex"]
    dob = data["dob"]
    admit_date = data["admit"]
    anticipated_discharge = data["ant_dis"]
    diagnosis = data["diagnosis"]
    code_status = data["code"]
    room = data["room"]
    rn_code = data["rn_code"]
    dr_code = data["dr_code"]
    unit_id = data["unit_id"]

    query = "UPDATE Patients SET first_name = %s, last_name = %s, sex = %s, dob = %s, admit_date = %s, " \
            "anticipated_discharge = %s, diagnosis = %s, code_status = %s, room = %s, rn_code = %s, " \
            "dr_code = %s, unit_id = %s WHERE pat_id = %s;"
    values = (first_name, last_name, sex, dob, admit_date, anticipated_discharge,
              diagnosis, code_status, room, rn_code, dr_code, unit_id, pat_id)
    connect_to_database(query, "POST", values)


@app.route('/patients/results', methods=['GET','POST'])
def patient_results():
    if request.method == 'POST':
        post = request.form.to_dict()
        last_name = post["search"]
        query = "SELECT p.*, d.first_name AS dr_first, d.last_name AS dr_last, n.first_name AS rn_first, " \
                "n.last_name AS rn_last, u.name FROM Patients p " \
                "JOIN Doctors d ON p.dr_code = d.dr_code " \
                "JOIN Nurses n ON p.rn_code = n.rn_code " \
                "JOIN Units u ON p.unit_id = u.unit_id " \
                "WHERE p.last_name = '" + str(last_name) + "';"
        data = connect_to_database(query, "GET")
        convert_bools(data)
        return patients_page(data)



def convert_bools(data):
    for item in data:
        if item["sex"] == 0:
            item["sex"] = "Female"
        elif item["sex"] == 1:
            item["sex"] = "Male"
        try:
            if item["on_duty"] == 0:
                item["on_duty"] = "Off"
            elif item["on_duty"] == 1:
                item["on_duty"] = "On"
            if item["in_house"] == 0:
                item["in_house"] = "Out"
            elif item["in_house"] == 1:
                item["in_house"] = "In house"
            if item["attending"] == 0:
                item["attending"] = "Resident"
            elif item["attending"] == 1:
                item["attending"] = "Attending"
        except:
            continue


if __name__ == '__main__':
    app.run(debug=True)

