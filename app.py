from flask import Flask, request, send_from_directory, render_template, Response
import os
import time

app = Flask(__name__)

# Define the working dir to a variable
WORKING_DIR = "data"

# Function to get the next available log number
def get_next_log_number():
    log_number = 1
    while os.path.exists(os.path.join(WORKING_DIR, f'log-{log_number}.txt')):
        log_number += 1
    return log_number

@app.route('/')
def handle_root():
    return render_template('fck.html')

@app.route('/testings')
def handle_testings():
    def generate():
        try:
            while True:
                yield "Hello World!\n"
                time.sleep(1)
        except GeneratorExit:
            pass

    return Response(generate(), content_type='text/plain')



# Handling POST requests to the specific endpoint
# Scrambled to make FUZZing harder
@app.route('/c2VydmVy', methods=['POST'])
def handle_webhook_post():
    # Checking if the request method is POST
    if request.method == 'POST':
        # Getting the data from the request
        data = request.data

        # Check if the data contains Mac-style line endings
        if b'\r' in data:
            # Replace Mac-style line endings with Unix-style line endings
            data = data.replace(b'\r', b'\n')

        # Getting the next available log number
        log_number = get_next_log_number()
        # Generating the log filename based on the log number
        log_filename = f'log-{log_number}.txt'

        # Writing the received data to the log file in the script's directory
        log_filepath = os.path.join(WORKING_DIR, log_filename)
        with open(log_filepath, 'wb') as file:
            file.write(data)

        # Returning a response indicating successful receipt and logging of data
        return f"Webhook data received and logged as {log_filename}", 200
    else:
        # Returning a 501 status code for unsupported methods
        return "Unsupported method", 501

# Handling GET requests to the specific endpoint
# Scrambled to make FUZZing harder
@app.route('/c2VydmVy/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Using send_from_directory to serve the file from the script's directory
        return send_from_directory(WORKING_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        # Returning a 404 status code if the file is not found
        return "File not found", 404

# Running the Flask app if this script is executed directly
if __name__ == '__main__':
    # Configuring the Flask app to run on a specific host and port
    app.run(debug=True)

