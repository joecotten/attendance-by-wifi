from flask import Flask, render_template, request
import uuid
import csv

app = Flask(__name__)

# Function to get the MAC address of the local machine
def get_mac_address():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = ':'.join(mac_num[i: i + 2] for i in range(0, 12, 2))
    return mac

# CSV file path
csv_file = 'user_mac_association.csv'

# Initialize CSV file with headers if it doesn't exist
def init_csv():
    try:
        with open(csv_file, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Full Name', 'Address', 'Email', 'Phone Number', 'MAC Address'])
    except FileExistsError:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    full_name = request.form['full_name']
    address = request.form['address']
    email = request.form['email']
    phone_number = request.form['phone_number']
    mac_address = get_mac_address()

    # Write the user details to the CSV file
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([full_name, address, email, phone_number, mac_address])

    return render_template('success.html', full_name=full_name, address=address, email=email, phone_number=phone_number, mac_address=mac_address)

@app.route('/users')
def users():
    users = []
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            users = list(reader)
    except FileNotFoundError:
        pass

    return render_template('users.html', users=users)

if __name__ == '__main__':
    init_csv()
    app.run(debug=True)
