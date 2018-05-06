from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
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
passengerId = 1
groupId = 1
transportationId = 1

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/addPassenger', methods=['POST'])
def addPassenger():
    #name, age, gender
    json = request.get_json()
    name = str(json['name'])
    age = int(json['age'])
    gender = str(json['gender'])
    #mysql
    global passengerId
    f = "INSERT INTO Passengers(PassengerId, Gender, Age, PassengerName) VALUES (%s, %s, %s, %s)"
    cursor.execute(f, (passengerId, gender, age, name))
    passengerId += 1
    conn.commit()
    return jsonify({'status':'OK'})

@app.route('/createGroup', methods=['POST'])
def createGroup():
    #source, destination, modeoftransportation, groupsize, purpose
    json = request.get_json()
    source = str(json['source'])
    destination = str(json['destination'])
    modeOfTransportation = str(json['modeOfTransportation'])
    groupSize = int(json['groupSize'])
    purpose = str(json['purpose'])
    global groupId
    f = "INSERT INTO Groups(GroupId, SourceLocation, DestinationLication, ModeOfTransportation, GroupSize, Purpose) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(f, (groupId, source, destination, modeOfTransportation, groupSize, purpose))
    groupId += 1
    conn.commit()
    return jsonify({'status':'OK'})

@app.route('/transportation', methods=['POST'])
def transportation():
    #type, along with the appropriate information for each
    json = request.get_json()
    typeOfTransport = str(json['type'])
    classOfTransport = str(json['class'])
    global transportationId
    if(typeOfTransport == 'Flight'):
        f = "INSERT INTO Transportation (TransportationId, Class, TransportType) VALUES (%s, %s, %s)"
        cursor.execute(f, (transportationId, classOfTransport, typeOfTransport))
        conn.commit()
        #add also into flight database
        flightNumber = int(json['flightNumber'])
        source = str(json['source'])
        destination = str(json['destination'])
        classOfFlight = str(json['classOfFlight'])
        fare = float(json['fare'])
        flightCarrier = str(json['flightCarrier'])
        ff = "INSERT INTO Flight VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(ff, (flightNumber, source, destination, classOfFlight, fare, flightCarrier))
        conn.commit()
    elif (typeOfTransport == 'Cruise'):
        f = "INSERT INTO Transportation (TransportationId, Class, TransportType) VALUES (%s, %s, %s)"
        cursor.execute(f, (transportationId, classOfTransport, typeOfTransport))
        conn.commit()
        cruiseNumber = int(json['cruiseNumber'])
        fare = float(json['fare'])
        source = str(json['source'])
        destination = str(json['destination'])
        ff = "INSERT INTO Cruise VALUES (%s, %s, %s, %s)"
        cursor.execute(ff, (cruiseNumber, fare, source, destination))
        conn.commit()
    else:
        f = "INSERT INTO Transportation (TransportationId, Class, TransportType) VALUES (%s, %s, %s)"
        cursor.execute(f, (transportationId, classOfTransport, typeOfTransport))
        conn.commit()
        carRentalId = int(json['carRentalId'])
        carType = str(json['carType'])
        rent = float(json['rent'])
        ff = "INSERT INTO CarRental (CarRentalConfirmationId, CarType, Rent) VALUES (%s, %s, %s)"
        cursor.execute(ff, (carRentalId, carType, rent))
        conn.commit()
    transportationId += 1
    return jsonify({'status':'OK'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

