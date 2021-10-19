from flask import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from busroute import BusRoute


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

#firestore client
db = firestore.client()

#flask app
app = Flask(__name__,template_folder="templates",static_url_path="/static")
app.secret_key = "soukyapsg"

#Bus route object
cbe_transport = BusRoute()


@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'GET':
        """
        src = request.form['source']
        des = request.form['destination']
        """
        src,des = "sulur","ramakrishna"
        minShifts = cbe_transport.numBusesToDestination(src,des)

        if minShifts>0:
            busesToTake = cbe_transport.takeBuses(src,des)
            shiftBusLocations = cbe_transport.shiftsAt(busesToTake)
            shiftBusLocations = [src]+shiftBusLocations+[des]
            bsd = []
            i,j = 0,1
            while i<minShifts:
                bsd.append((busesToTake[i],shiftBusLocations[i],shiftBusLocations[j]))
                i+=1
                j+=1

            travelDetails = {'bsd':bsd,'minShifts':minShifts,'busesToTake':busesToTake,'shiftBusLocations':shiftBusLocations}
            return redirect(url_for('myTravel',travelDetails = travelDetails))
        else:
            flash("Your travel is not possible")
            return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/addBus')
def addBus():
    return render_template('addbus.html')

@app.route('/myTravel')
def myTravel():
    travelDetails = request.args.get('travelDetails', None)
    print(travelDetails)
    return render_template('myTravel.html',travelDetails = travelDetails)

if __name__ == "__main__":
    buses = db.collection('buses').get()
    for doc in buses:
        bus = doc.to_dict()
        cbe_transport.addBus(bus['busName'],bus['busRoute'])
    app.run(debug=True)