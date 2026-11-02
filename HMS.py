import mysql.connector
from mysql.connector import Error

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="crud_app"
)

cursor = conn.cursor()


def create_patient(name, age, gender, phone, address, disease):
    query = ("INSERT INTO patients (name, age, gender, phone, address, disease) "
             "VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (name, age, gender, phone, address, disease))
    conn.commit()
    print("Patient added successfully.")
 
 
def read_patients():
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    if not rows:
        print("No patients found.")
    for (id, name, age, gender, phone, address, disease) in rows:
        print(f"ID: {id}, Name: {name}, Age: {age}, Gender: {gender}, "
              f"Phone: {phone}, Address: {address}, Disease: {disease}")
 
 
def update_patient(patient_id, name, age, gender, phone, address, disease):
    query = ("UPDATE patients SET name=%s, age=%s, gender=%s, phone=%s, "
             "address=%s, disease=%s WHERE id=%s")
    cursor.execute(query, (name, age, gender, phone, address, disease, patient_id))
    conn.commit()
    if cursor.rowcount == 0:
        print("No patient found with that ID.")
    else:
        print("Patient updated successfully.")
 
 
def delete_patient(patient_id):
    cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
    conn.commit()
    if cursor.rowcount == 0:
        print("No patient found with that ID.")
    else:
        print("patient deleted successfully.")

def create_doctor(name, specialization, phone, email):
    query = ("INSERT INTO doctors (name, specialization, phone, email) "
             "VALUES (%s, %s, %s, %s)")
    cursor.execute(query, (name, specialization, phone, email))
    conn.commit()
    print("Doctor added successfully.")


def read_doctors():
    cursor.execute("SELECT * FROM doctors")
    rows = cursor.fetchall()
    if not rows:
        print("No doctors found.")
    for (id, name, specialization, phone, email) in rows:
        print(f"ID: {id}, Name: {name}, Specialization: {specialization}, "
              f"Phone: {phone}, Email: {email}")


def update_doctor(doctor_id, name, specialization, phone, email):
    query = ("UPDATE doctors SET name=%s, specialization=%s, phone=%s, email=%s "
             "WHERE id=%s")
    cursor.execute(query, (name, specialization, phone, email, doctor_id))
    conn.commit()
    if cursor.rowcount == 0:
        print("No doctor found with that ID.")
    else:
        print("Doctor updated successfully.")


def delete_doctor(doctor_id):
    cursor.execute("DELETE FROM doctors WHERE id=%s", (doctor_id,))
    conn.commit()
    if cursor.rowcount == 0:
        print("No doctor found with that ID.")
    else:
        print("Doctor deleted successfully.")


def create_appointment(patient_id, doctor_id, date, time):
    # check that the patient and doctor exist
    cursor.execute("SELECT id FROM patients WHERE id=%s", (patient_id,))
    if cursor.fetchone() is None:
        print("No patient found with that ID. Add the patient first.")
        return
    cursor.execute("SELECT id FROM doctors WHERE id=%s", (doctor_id,))
    if cursor.fetchone() is None:
        print("No doctor found with that ID. Add the doctor first.")
        return

    # check that the doctor is free at that date and time
    cursor.execute("SELECT id FROM appointments WHERE doctor_id=%s "
                   "AND appointment_date=%s AND appointment_time=%s "
                   "AND status <> 'Cancelled'", (doctor_id, date, time))
    if cursor.fetchone() is not None:
        print("That doctor already has an appointment at this date and time.")
        return

    query = ("INSERT INTO appointments (patient_id, doctor_id, appointment_date, "
             "appointment_time) VALUES (%s, %s, %s, %s)")
    cursor.execute(query, (patient_id, doctor_id, date, time))
    conn.commit()
    print("Appointment booked successfully.")


def read_appointments():
    query = """
        SELECT a.id, p.name, d.name, d.specialization,
               a.appointment_date, a.appointment_time, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.appointment_date, a.appointment_time
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        print("No appointments found.")
    for (id, patient, doctor, specialization, date, time, status) in rows:
        print(f"ID: {id}, Patient: {patient}, Doctor: {doctor} ({specialization}), "
              f"Date: {date}, Time: {time}, Status: {status}")


def update_appointment(appointment_id, date, time, status):
    query = ("UPDATE appointments SET appointment_date=%s, appointment_time=%s, "
             "status=%s WHERE id=%s")
    cursor.execute(query, (date, time, status, appointment_id))
    conn.commit()
    if cursor.rowcount == 0:
        print("No appointment found with that ID.")
    else:
        print("Appointment updated successfully.")


def delete_appointment(appointment_id):
    cursor.execute("DELETE FROM appointments WHERE id=%s", (appointment_id,))
    conn.commit()
    if cursor.rowcount == 0:
        print("No appointment found with that ID.")
    else:
        print("Appointment deleted successfully.")


def patient_menu():
    while True:
        print("\n--- Patient Menu ---")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Update Patient")
        print("4. Delete Patient")
        print("5. Back")

        choice = input("Enter choice: ")

        try:
            if choice == '1':
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                gender = input("Enter gender: ")
                phone = input("Enter phone: ")
                address = input("Enter address: ")
                disease = input("Enter disease: ")
                create_patient(name, age, gender, phone, address, disease)
            elif choice == '2':
                read_patients()
            elif choice == '3':
                patient_id = int(input("Enter patient ID to update: "))
                name = input("Enter new name: ")
                age = int(input("Enter new age: "))
                gender = input("Enter new gender: ")
                phone = input("Enter new phone: ")
                address = input("Enter new address: ")
                disease = input("Enter new disease: ")
                update_patient(patient_id, name, age, gender, phone, address, disease)
            elif choice == '4':
                patient_id = int(input("Enter patient ID to delete: "))
                delete_patient(patient_id)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number for age and ID.")
        except Error as e:
            conn.rollback()
            print(f"Database error: {e}")


def doctor_menu():
    while True:
        print("\n--- Doctor Menu ---")
        print("1. Add Doctor")
        print("2. View Doctors")
        print("3. Update Doctor")
        print("4. Delete Doctor")
        print("5. Back")

        choice = input("Enter choice: ")

        try:
            if choice == '1':
                name = input("Enter name: ")
                specialization = input("Enter specialization: ")
                phone = input("Enter phone: ")
                email = input("Enter email: ")
                create_doctor(name, specialization, phone, email)
            elif choice == '2':
                read_doctors()
            elif choice == '3':
                doctor_id = int(input("Enter doctor ID to update: "))
                name = input("Enter new name: ")
                specialization = input("Enter new specialization: ")
                phone = input("Enter new phone: ")
                email = input("Enter new email: ")
                update_doctor(doctor_id, name, specialization, phone, email)
            elif choice == '4':
                doctor_id = int(input("Enter doctor ID to delete: "))
                delete_doctor(doctor_id)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number for the ID.")
        except Error as e:
            conn.rollback()
            print(f"Database error: {e}")


def appointment_menu():
    while True:
        print("\n--- Appointment Menu ---")
        print("1. Book Appointment")
        print("2. View Appointments")
        print("3. Update Appointment")
        print("4. Delete Appointment")
        print("5. Back")

        choice = input("Enter choice: ")

        try:
            if choice == '1':
                patient_id = int(input("Enter patient ID: "))
                doctor_id = int(input("Enter doctor ID: "))
                date = input("Enter date (YYYY-MM-DD): ")
                time = input("Enter time (HH:MM): ")
                create_appointment(patient_id, doctor_id, date, time)
            elif choice == '2':
                read_appointments()
            elif choice == '3':
                appointment_id = int(input("Enter appointment ID to update: "))
                date = input("Enter new date (YYYY-MM-DD): ")
                time = input("Enter new time (HH:MM): ")
                status = input("Enter status (Scheduled/Completed/Cancelled): ").capitalize()
                if status not in ("Scheduled", "Completed", "Cancelled"):
                    print("Status must be Scheduled, Completed or Cancelled.")
                else:
                    update_appointment(appointment_id, date, time, status)
            elif choice == '4':
                appointment_id = int(input("Enter appointment ID to delete: "))
                delete_appointment(appointment_id)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number for the IDs.")
        except Error as e:
            conn.rollback()
            print(f"Database error: {e}")


def main():
    while True:
        print("\n===== Hospital Management System =====")
        print("1. Manage Patients")
        print("2. Manage Doctors")
        print("3. Manage Appointments")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            patient_menu()
        elif choice == '2':
            doctor_menu()
        elif choice == '3':
            appointment_menu()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

    cursor.close()
    conn.close()
    print("Goodbye!")


if __name__ == "__main__":
    main()
