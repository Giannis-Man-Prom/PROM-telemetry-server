import time

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import webbrowser
from dotenv import load_dotenv
import os
import pandas as pd
import threading
from flask_socketio import SocketIO, emit
from threading import Lock
from services.live_telemetry_class import SerialRead
from datetime import datetime
import csv
import json
from custom_exceptions.serial_connection_exception import SerialConnectionException

# Declaration of variables
# Name of the application module or package
app = Flask(__name__, static_folder="dist", static_url_path="/")

# This code allows requests from other dommains
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Load ENV Variables
load_dotenv()

# Initializing a dictionary in order to keep and fetch all the files the user may add.
files = {}
# Addig this dictionary to the config object of flask
app.config['uploaded_files'] = files
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# defining these variables to our current env
FLASK_CONTAINER_PORT = os.getenv('FLASK_CONTAINER_PORT')

DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes']

# Adding socket functionality to our server.
socketio = SocketIO(app, cors_allowed_origins="*")

"""
    Prom-Telemetry Live Telemetry, API server
    ~~~~
"""

@app.route('/api/v1/live_telemetry/', methods=['GET'])
def telemetry_health_check():
    return jsonify(
        status=200,
        data="Telemetry is alive!!"
    )


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

thread = None
thread_lock = Lock()

# Essentialy what we are doing here is to emit an event, but instead of doing it once we are enabling a backstage process with threading
# so we will have a concurrent procedure emiting event, in this case our procudure is the infinite while from the telemetry module.
@socketio.event
def connect():
    try:

        global thread

        with thread_lock:
            if thread is None:

                telemetry_serial_obj = SerialRead()

                if telemetry_serial_obj.serialInst is None:
                    raise SerialConnectionException(
                        "Could not establish connection with usb serial, connect usb device")

                thread = socketio.start_background_task(read_from_serial_thread, telemetry_serial_obj)

        emit('connection_response', {'status': 'Success'})

    except Exception as e:
        emit('connection_response', {'status': 'Failed', 'msg': str(e)})


# Global variable to track the thread status
is_thread_running = 0
logging_thread = None

# With this endpoint, we are starting the logging process, if there is a thread running we will stop it and return the apropriate
# message, and if there is no thread running we will start the logging process and return the apropriate message.
@app.route('/api/v1/live_telemetry/start_logging', methods=['POST'])
def start_telemetry_logging():
    # Accessing the telemetry object from the application context memmory.
    # In case of an initialisation problem with the serial input(telemetry object) we return the respective message

    global is_thread_running
    global logging_thread

    # Check if thread is already running
    if not is_thread_running:
        try:
            # Start the process in a separate thread
            logging_thread = threading.Thread(target=logging_process)

            is_thread_running = 1

            logging_thread.start()

            return jsonify(
                status=200,
                data="Thread Started"
            )

        except Exception as e:
            return jsonify(
                status=500,
                data="Thread could not start"
            )
    else:
        is_thread_running = 0

        return jsonify(
            status=200,
            data="Thread Successfully stoped"
        )


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

def logging_process():
    global is_thread_running
    global temp_packages

    # Create a unique file name with the current date and time
    date_time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"logging_data_{date_time_now}.csv"

    directory_path = os.getenv('LOGS_LOCATION')

    # Check if the directory exists
    if not os.path.exists(directory_path):
        # Create the directory if it doesn't exist
        os.makedirs(directory_path)
        print("Directory created:", directory_path)
    else:
        print("Directory already exists.")

    # Create an empty DataFrame with the specified headers
    packages_df = pd.DataFrame(columns=os.getenv('CSV_HEADERS').split(','))

    # Add "timestamp" as the first header for the CSV file
    headers = ['timestamp'] + os.getenv('CSV_HEADERS').split(',')

    last_known_values = {key: '' for key in os.getenv('CSV_HEADERS').split(',')}

    with open(os.path.join(directory_path, file_name), mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Write CSV headers
        temp_packages.clear()
        while is_thread_running:
            try:
                # If there are enough packages, process them
                if len(temp_packages) <= 10000:
                    print("ALL OKAY: temp packages indeed <= 10000")
                    for package in temp_packages:
                        # Add the current timestamp to the package
                        package_with_time = {'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        # Add the rest of the data from the package
                        for key in os.getenv('CSV_HEADERS').split(','):
                            if key in package and package[key] != '':
                                last_known_values[key] = package[key]
                            package_with_time[key] = last_known_values[key]
                        # Write the package with the timestamp to the CSV file
                        writer.writerow(package_with_time)
                    # Flush the file to ensure data is written
                    file.flush()
                    # Clear temp_packages after writing
                    temp_packages.clear()
                    print("temp_packages has been cleared.")
            except Exception as e:
                print("There was an error while trying to write:", e)

            time.sleep(0.1)  # Sleep for a short while to avoid overloading the system


def read_from_serial_thread(telemetry):
    # Create an empty DataFrame with the specified headers
    packages_df = pd.DataFrame(columns=os.getenv('CSV_HEADERS').split(','))

    global temp_packages
    """Editing event to the connected clients every time we receive data from the telemetry module"""
    while True:
        package = None
        try:
            package = telemetry.serialInst.readline().decode('utf-8').strip()

            if package:
                pass

                package_dict = json.loads(package)

                temp_packages.append(package_dict)

        except Exception as e:
            print("False, Json reading")

        if package != None:
            # print(package)

            socketio.emit('telemetry_data',
                      {'data': package})

@app.route("/")
def serve_frontend():
    return send_from_directory("dist", "index.html")


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:" + FLASK_CONTAINER_PORT)
    socketio.run(app, debug=DEBUG, host='0.0.0.0', port=int(FLASK_CONTAINER_PORT), allow_unsafe_werkzeug=True)
