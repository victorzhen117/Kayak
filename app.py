from flask import Flask, request
from flask.ext.mysql import MySQL
import uuid
app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'fishrcool'
app.config['MYSQL_DATABASE_DB'] = 'kayak'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/addPassenger', methods=['POST'])
def addPassenger():
    #name, age, gender
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    passengerId = str(uuid.uuidv4())
    #mysql
    cursor.execute(''' INSERT INTO Passengers(PassengerId, Gender, Age, PassengerName) VALUES (passengerId, gender, age, name) ''');
    return jsonify({'status':'OK'})

@app.route('/createGroup', methods=['POST'])
def createGroup():
    #source, destination, modeoftransportation, groupsize, purpose
    source = request.form['source']
    destination = request.form['destination']
    modeOfTransportation = request.form['modeOfTransportation']
    groupSize = request.form['groupSize']
    purpose = request.form['purpose']
    groupId = str(uuid.uuidv4())
    cursor.execute(''' INSERT INTO Groups (GroupId, SourceLocation, DestinationLocation, ModeOfTransportation, GroupSize, Purpose) VALUES (groupId, source, destination, modeOfTranspportation, groupSize, purpose) ''')
    return jsonify({'status':'OK'})

@app.route('/transportation', methods=['POST'])
def transportation():
    #type, along with the appropriate information for each
    typeOfTransport = request.form['type']
    classOfTransport = request.form['class']
    transportId = str(uuid.uuidv4())
    if(typeOfTransport == 'Flight'):
        cursor.execute(''' INSERT INTO Transportation (TransportationId, Class, TransportType) VALUES (transportId, classOfTransport, typeOfTransport) ''')
        #add also into flight database
        flightNumber = request.form['flightNumber']
        source = request.form['source']
        destination = request.form['destination']
        classOfFlight = request.form['classOfFlight']
        fare = request.form['fare']
        flightCarrier = request.form['flightCarrier']
        cursor.execute(''' INSERT INTO Flight(FlightNumber, SourceLocation, DestinationLocation, Class, Fare, FlightCarrier) VALUES (flightNumber, source, destination, classOfFlight, fare, flightCarrier) ''')
        return jsonify({'status':'OK'})
    elif (typeOfTransport == 'Cruise'):
        return jsonify({'status':'OK'})
    else:
        return jsonify({'status':'OK'})


if __name__ == "__main__":
    app.run(host="0.0.0.0")

