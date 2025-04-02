import logging
import time

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pandas as pd
import threading
from services.telemetry_data_class import telemetry_data_class
from typing import Type
from flask_socketio import SocketIO, emit
from threading import Lock
from services.live_telemetry_class import SerialRead
from datetime import datetime
import csv
import json
from custom_exceptions.serial_connection_exception import SerialConnectionException

#Εδώ φτιάχουμε ενα Object τύπου Flask που επιτρέπει την διαχείριση του server και των http request που θα γινονται
#από το front end
app = Flask(__name__)

#To cors είναι ένα μέτρο προστασίας των browser που δεν αφήνει άλλα domains (άλλες διευθύνσεις, ports) να κάνουν
#access τον server, με το * αφήνουμε κάθε άλλο domain να μας κάνει requests, δηλαδή το front-end εφόσον τρέχει σε άλλο port
#μπορουμε να το πεταξουμε αν περασουμε το front end στο ίδιο port, ίσως άχρηστο
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

#Φορτώνουμε μεταβλητές που βρίσκονται στο .env file
load_dotenv()

#Φτιάχνουμε ένα Python dictionary για να κρατάμε το όνομα των αρχείων που κάνουμε log δεδομένα
files = {}
#Αποθηκεύουμε το dict που φτιάξαμε ως μεταβλητή του config της Flask εφαρμογής που φτιάξαμε, το config δουλευει σαν dict
app.config['uploaded_files'] = files
#Δεν κρύβουμε κάτι so who cares, ίσως άχρηστο
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

#Με αυτόν τον τρόπο παίρνουμε το port που θα χρησιμοποιήσουμε για τον server απο το .env
FLASK_CONTAINER_PORT = os.getenv('FLASK_CONTAINER_PORT')

#Αντίστοιχα για το αν θέλουμε DEBUG ή όχι, με το DEBUG η Flask δίνει καλύτερες περιγραφές για όταν προκύπτουν
#προβλήματα
DEBUG = os.getenv('DEBUG')

#Χρειαζόμαστε sockets έτσι ώστε να έχουμε μπρος πίσω επικοινωνία μεταξύ front και back end
#Εδώ φτιάχνουμε ενα socket object το οποίο να δουλεύει μαζί με την εφαρμογή app, πάλο βάζουμε cors κατάλληλο
socketio = SocketIO(app, cors_allowed_origins="*")

"""
    Prom-Telemetry Data analysis VD, API server
    ~~~~
"""


#Για να κάνουμε request από το browser μας, μπαίνουμε σε αυτό το path, δλδ http://localhost:8081/api/v1/data_analysis
#Τα app.route κάνουν αυτό που λέει η από κάτω συνάρτηση όταν ζητείται κάνεις access το αντίστοιχο url και χρησιμοποιείς
#την αντίστοιχη μέθοδο, by default η μέθοδος είναι GET (παίρνω δεδομένα από τον server), μετά είναι η POST(δίνω στον server)
@app.route('/api/v1/data_analysis', methods=['GET'])
def data_analysis_health_check():
    #Το request object διαχειρίζεται τα http requests Και τα δεδομενα που δινονται στον server
    #με το args.get παίρνουμε από το http request ενα argument με όνομα test, δεν έχουμε τέτοιο
    #argument άρα περιμένουμε None, μπορούμε να το αλλάξουμε αν βάζαμε στο link ?test=kati
    test = request.args.get('test')
    return jsonify(
        status=200,
        data=f"Data analysis alive!! {test}"
    )

#Όταν μπαίνουμε στο από κάτω url ανεβάζουμε ένα αρχείο και τα δεδομενα του στο back end από το front end
#και γράφουμε τα δεδομένα σε ένα object τύπου telemetry_data_class
@app.route('/api/v1/data_analysis/file_upload', methods=['POST'])
def upload_data_file():
    #Το request object εδώ μας δίνει το αρχείο που ανεβάζει το front end στο συγκεκριμένο site
    uploaded_file = request.files['file']

    #Κοιτάμε αν το όνομα του αρχείου υπάρχει ήδη και ενημερώνουμε το front end με 400 αν υπάρχει
    #(αλλιώς ίσως το νέο αρχείο κάνει overwrite το παλιό?)
    if f"data_{uploaded_file.filename}" in list(dict(app.config['uploaded_files']).keys()):
        return {
            'status': 400,
            'data': {
                'message': f'The file with filename: data_{uploaded_file.filename} already exists in the server'
            }
        }

    #Διαβάζουμε το αρχείο με το pandas στην αντίστοιχη μορφή που δίνει η βιβλιοθήκη
    df = pd.read_csv(request.files['file'])

    try:

        #Μετατρέπουμε τα δεδομένα σε class που ορίζουμε εμείς σε άλλο αρχείο
        df_telem_data_class = telemetry_data_class(df)

        #Εδώ αποθηκεύουμε το αρχείο ως ενα object μεσα στην flask
        app.config['uploaded_files'][f'data_{uploaded_file.filename}'] = df_telem_data_class

        # ONLY FOR DEBUG, άμα θέλουμε να τυπώσουμε τα uploaded files
        #print(app.config['uploaded_files'])

        #Άμα δεν έχουμε θέμα τότε ενημερώνουμε το front end
        return jsonify(
            {
                'status': 200,
                'data': {
                    'message': f'File uploaded successfully with name: data_{uploaded_file.filename}'
                }
            }
        )
    
    #Αν έχουμε θέμα ενημερώνουμε το front end
    except Exception as e:
        return jsonify(
            {
                'status': 500,
                'data': {
                    'error': f'could not load the file{e}'
                }
            }

        )

#Εδώ κάνουμε παίρνουμε JSON δεδομένα και τα επιστρέφουμε μετά από κατάλληλη επεξεργασία του telemetry_data_class
@app.route('/api/v1/data_analysis/get_collumns/<file_name>', methods=['GET'])
def fetch_two_columns(file_name: str):
    #Ορίζουμε την μεταβλητή να είναι τύπου telemetry_data_class
    telemetry_data: Type[telemetry_data_class]

    #Παίρνουμε τα json δεδομένα
    data = request.get_json()

    #Από το json file παίρνουμε τα col_1, col_2, το json μοιάζει με python dict
    col_1 = data.get('col_1')
    col_2 = data.get('col_2')

    try:
        #Βλέπουμε αν το αρχείο το οποίο θέλουμε, το <file_name>, υπάρχει στο flask object
        telemetry_data = app.config['uploaded_files'][file_name]

    #Αν όχι κάνουμε error handling
    except KeyError as keyErr:
        return jsonify({
            'status': 500,
            "msg": "There is no file with this name in the database"
        })

    return {
        'status': 200,
        'data': {
            #Στέλνουμε τα δεδομένα αφότου τα έχει επεξεργαστεί η get_two_cols
            'data': telemetry_data.get_two_cols(col_1, col_2)
        }
    }

#Εδώ απλά δίνουμε τα ονόματα των αρχείων στο flask object
@app.route('/api/v1/data_analysis/get_file_ids', methods=['GET'])
def fetch_file_names():
    try:

        file_names = list(dict(app.config['uploaded_files']).keys())

        print(file_names)

    except Exception as e:
        return {
            'status': 500,
            'data': {
                'message': 'There was an error while fetching the names'
            }
        }

    return {
        'status': 200,
        'data': {
            'data': file_names
        }
    }


@app.route('/api/v1/data_analysis/get_all_cols/<file_name>', methods=['GET'])
def get_all_cols_in_file(file_name: str):
    # Definition of a type
    telemetry_data: Type[telemetry_data_class]

    try:
        # Fetching the telemetry object by file name
        telemetry_data = app.config['uploaded_files'][file_name]

        return jsonify({
            "status": 200,
            "data": telemetry_data.get_cols_all()
        })

    except KeyError as keyErr:
        return jsonify({
            'status': 500,
            "msg": f"There is no file with this name in the database {keyErr}"
        })


"""
    Prom-Telemetry Live Telemetry, API server
    ~~~~
"""

#Βασικός έλεγχος ότι τα requests δουλεύουν
@app.route('/api/v1/live_telemetry/', methods=['GET'])
def telemetry_health_check():
    return jsonify(
        status=200,
        data="Telemetry is alive!!"
    )

#Όταν λάβει το event disconnect από το socket τότε κάνει print ότι ο client αποσυνδέθηκε
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')


#Χρησιμοποιούμε threading έτσι ώστε να μην μπλοκάρει η ακόλουθη διαδικασία το υπόλοιπο πρόγραμμα
#και να γίνεται παράλληλα
#Ορίζουμε το thread που θα χρησιμοποιήσουμε μετά
thread = None
#Φροντίζουμε μόνο ένα background thread να μπορεί να τρέχει κάθε φορά για να απούγουμε race conditions
thread_lock = Lock()


# Essentialy what we are doing here is to emit an event, but instead of doing it once we are enabling a backstage process with threading
# so we will have a concurrent procedure emiting event, in this case our procudure is the infinite while from the telemetry module.
#Η ακόλουθη συνάρτηση καλείται όταν ένας client συνδέεται
@socketio.event
def connect():
    try:

        #Φροντίζουμε η προηγούμενη μεταβλητή να είναι global
        global thread

        #Με το thread lock φροντίζουμε να μην μπορεί κάποιος άλλος να πειράξει την μεταβλητή
        #όπως αν είχαμε πολλούς clients(??)
        with thread_lock:
            #Άμα το background thread δεν τρέχει ήδη
            if thread is None:

                #Φτιάχνουμε ένα object τύπου SerialRead που ορίζεται σε άλλο αρχείο
                #Με το που δημιουργείται κοιτάει να βρει και να ανοίξει την κατάλληλη σύνδεση
                telemetry_serial_obj = SerialRead()

                #Με αυτήν την συνάρτηση προσπαθούμε να αρχίσουμε Serial επικοινωνία με το usb
                if telemetry_serial_obj.serialInst is None:
                    raise SerialConnectionException(
                        "Could not establish connection with usb serial, connect usb device")

                #Εδώ κάνουμε assign στο thread να μπορεί την συνάρτηση read_from_serial_thread για να τρέχει αυτήν
                #παράλληλα με το υπόλοιπο πρόγραμμα και να μην το μπλοκάρει και το telemetry_serial_obj χρειάζεται επίσης
                thread = socketio.start_background_task(read_from_serial_thread, telemetry_serial_obj)

        emit('connection_response', {'status': 'Success'})

    except Exception as e:
        emit('connection_response', {'status': 'Failed', 'msg': str(e)})


#Με αυτές τις μεταβλητές κοιτάμε αν το thread για το data logging τρέχει ή οχι
is_thread_running = 0
logging_thread = None

#Μπαίνοντας σε αυτό το site ξεκινάμε ένα thread για το logging process
@app.route('/api/v1/live_telemetry/start_logging', methods=['POST'])
def start_telemetry_logging():

    #Κάνουμε τις προηγούμενες μεταβλητές global
    global is_thread_running
    global logging_thread

    #Αν δεν τρέχει ήδη το thread
    if not is_thread_running:
        try:
            #Φτιάχνουμε ένα νέο thread για να τρέξει to logging process παρακάτω
            logging_thread = threading.Thread(target=logging_process)

            #Και ορίζουμε ότι θα τρέχει
            is_thread_running = 1

            #Αρχίζουμε το thread
            logging_thread.start()

            #Ενημερώνουμε
            return jsonify(
                status=200,
                data="Thread Started"
            )

        except Exception as e:
            return jsonify(
                status=500,
                data="Thread could not start"
            )
    #Αλλιώς σταματάμε το thread
    else:
        is_thread_running = 0

        return jsonify(
            status=200,
            data="Thread Successfully stoped"
        )

#Η παρακάτω συνάρτηση ελέγχει για το αν έχει αρχίσει το logging με βάση την παράπανω is_thread_running global μεταβλητή
@app.route('/api/v1/live_telemetry/logging_status', methods=['GET'])
def logging_status():
    """
    Endpoint to check the current status of the logging process.

    This endpoint allows clients to check whether the logging process is actively running
    or has been stopped. It's designed to give a quick status check on the logging process
    through a simple GET request.

    Global Variables:
    - is_thread_running (bool): A flag indicating whether the logging thread is currently running.

    Responses:
    - When the logging process is running:
        - status: 200 (int) - HTTP success status code indicating the request was successful.
        - data: 1 (int) - Indicator that the logging process is active.
        - msg: "The logging process is running" (str) - Descriptive message about the current state.

    - When the logging process is not running:
        - status: 200 (int) - HTTP success status code.
        - data: 0 (int) - Indicator that the logging process is inactive.
        - msg: "The logging process is stopped" (str) - Descriptive message about the current state.

    Returns:
    JSON object containing the status code, data, and a message indicating the logging status.
    """
    global is_thread_running

    if is_thread_running:
        return jsonify(
            status=200,
            data=1,
            msg="The logging process is running"
        )
    else:
        return jsonify(
            status=200,
            data=0,
            msg="The logging process is stopped"
        )


temp_packages = []

#Αυτή είναι η συνάρτηση που είναι υπεύθυνη για το logging με τη χρήση του thread από πριν
def logging_process():
    global is_thread_running
    global temp_packages

    #Φτιάχνουμε ένα αρχείο με την τωρινή μέρα και ώρα για να είναι unique και το ορίζουμε σαν csv
    date_time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"logging_data_{date_time_now}.csv"

    #Παίρνουμε την τοποθεσία στην οποία αποθηκεύουμε το αρχείο
    directory_path = os.getenv('LOGS_LOCATION')

    #Έλεγχοι για το αν υπάρχει και αν χρειάζεται να το φτιάξουμε
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print("Directory created:", directory_path)
    else:
        print("Directory already exists.")

    #Φτιάχνουμε ένα object τύπου pandas dataframe και του βάζουμε ως columns τα headers που καθορίζουμε στο .env file
    #που τα ξεχωρίζουμε με τα ","
    packages_df = pd.DataFrame(columns=os.getenv('CSV_HEADERS').split(','))

    #Φτιάχνουμε ένα header για το csv μετά που να έχουμε και το timestamp
    headers = ['timestamp'] + os.getenv('CSV_HEADERS').split(',')

    #Από κάτω έχουμε ένα dict που θα αποθηκεύουμε τις τελευταίες τιμές για κάθε τιμή στο header
    last_known_values = {key: '' for key in os.getenv('CSV_HEADERS').split(',')}

    #Ανοίγουμε το αρχείο file_name από πριν στο ορισμένο directory_path ως write
    with open(os.path.join(directory_path, file_name), mode='w', newline='') as file:
        #Εδώ ορίζουμε το writer για να μπορούμε να γράφουμε dicts σε csv files χρησιμοποιώντας τα headers από πριν
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  #Γράφουμε τα CSV headers
        #Καθαρίζουμε ότι είχε πριν το temp_packages
        #Τα temp_packages είναι global μεταβλητή πάνω στην οποία κάνουμε μετά serial_read
        temp_packages.clear()
        #Όταν τρέχουμε το logging
        while is_thread_running:
            try:
                #Αν έχουμε πάνω από 10000 (μάλλον) φοβόμαστε μην είναι υπερβολικά πολλά και χαλάσει
                if len(temp_packages) <= 10000:
                    print("ALL OKAY: temp packages indeed <= 10000")
                    #Επεξεργαζόμαστε κάθε package
                    for package in temp_packages:
                        #Προσθέτουμε timestamp ως πρώτο key to value
                        package_with_time = {'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        #Για κάθε key που έχουμε από το header του .env αν έχουμε μη '' τιμή την γράφουμε
                        #στην last_known_values από πριν
                        for key in os.getenv('CSV_HEADERS').split(','):
                            if key in package and package[key] != '':
                                last_known_values[key] = package[key]
                            #Προσθέτουμε αντιστοιχίες key και των τιμών στο package_with_time
                            package_with_time[key] = last_known_values[key]
                        #γράφουμε νέο row στο αρχείο
                        writer.writerow(package_with_time)
                    # Flush the file to ensure data is written
                    file.flush()
                    # Clear temp_packages after writing
                    temp_packages.clear()
                    print("temp_packages has been cleared.")
            except Exception as e:
                print("There was an error while trying to write:", e)

            time.sleep(0.1)  # Sleep for a short while to avoid overloading the system


#Εδώ κάνουμε, επιτέλους, serial read, το telemetry είναι τύπου SerialRead()
def read_from_serial_thread(telemetry):
    # Φτιάχνουμε ένα DataFrame με τιμές αυτές από το .env
    packages_df = pd.DataFrame(columns=os.getenv('CSV_HEADERS').split(','))

    #Εδώ έχουμε τα temp_packages που είναί global και χρησιμοποιούνται και πάνω
    #είναι temp γιατί όπως φάνηκε και από πριν θα κάνουμε και άλλη επεξεργασία
    global temp_packages
    """Editing event to the connected clients every time we receive data from the telemetry module"""
    #Διαβάζουμε συνέχεια από το serial
    while True:
        #Αρχίζουμε με κενό αρχείο
        package = None
        try:
            #Διαβάζουμε από το SerialRead object μέσω του COM του μέχρι να βρούμε \n (readline)
            package = telemetry.serialInst.readline().decode('utf-8').strip()
            #package = '{"vcu_water_temp_in_right":444,"vcu_water_temp_out_right":57,"vcu_pc_flag":1,"vcu_r2d_flag":0,"vcu_watchdog_status":2,"vcu_bspdState":89,"vcu_fan_right":34,"vcu_fan_left":76,"vcu_pump_right":23,"vcu_pump_left":45,"vcu_gearbox_ntc_left":67,"vcu_apps1":56,"vcu_apps2":92,"vcu_brake_front":38,"vcu_brake_rear":14,"vcu_hall_fr":63,"vcu_hall_fl":88,"vcu_Vx":0,"vcu_Vy":0,"vcu_yaw_rate":0,"vcu_accel_x":0,"vcu_accel_y":0,"vcu_accel_z":0,"vcu_gyro_x":0,"vcu_gyro_y":0,"vcu_gyro_z":0,"vcu_TVtrqLeft":0,"vcu_TVtrqRight":0,"vcu_antiw":0,"vcu_error":0,"vcu_integral":0,"vcu_integral_error":0,"vcu_m_z_nonsat":0,"vcu_m_z_sat":0,"vcu_prevError":0,"vcu_SteeringLinear_mm":0,"vcu_proportional":0,"vcu_yaw_rate_ref":0,"vcu_Vx1":0,"vcu_Vy1":0,"radio_rssi":0,"radio_packet_loss":0,"radio_wrong_crc":0,"radio_kbps":0}'

            #για debug
            # print(package)

            #Άμα πήραμε package τότε
            if package:
                pass

                #Κάνουμε τα JSON δεδομένα που πήραμε από το Serial σε python dictionary
                package_dict = json.loads(package)

                #Το προσθέτει στα packages τα οποία θα στείλουμε μαζί
                temp_packages.append(package_dict)

        except Exception as e:
            print("False, Json reading")

        if package != None:
            # print(package)

            #Το κάνουμε transmit ως socket event
            socketio.emit('telemetry_data',
                      {'data': package})


if __name__ == '__main__':
    socketio.run(app, debug=DEBUG, host='0.0.0.0', port=FLASK_CONTAINER_PORT, allow_unsafe_werkzeug=True)
