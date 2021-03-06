from flask import *
from busroute import BusRoute
import pandas as pd


#flask app
app = Flask(__name__,template_folder="templates",static_url_path="/static")
app.secret_key = "soukyapsg"

#Bus route object
cbe_transport = BusRoute()


@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
       
        src = request.form['source']
        des = request.form['destination']
       
        if src!="" and des!="":
            minShifts = cbe_transport.numBusesToDestination(src,des)
            print(minShifts)
            if minShifts>0:
                busesToTake = cbe_transport.takeBuses(src,des,minShifts)
                shiftBusLocations = cbe_transport.shiftsAt(busesToTake)
                shiftBusLocations = [src]+shiftBusLocations+[des]
                print(shiftBusLocations,busesToTake)
                bsd = []
                i,j = 0,1
                while i<len(busesToTake):
                    bsd.append((busesToTake[i],shiftBusLocations[i],shiftBusLocations[j]))
                    i+=1
                    j+=1

                print(bsd)
                travelDetails = {'bsd':bsd,'minShifts':minShifts,'busesToTake':busesToTake,'shiftBusLocations':shiftBusLocations}
                return render_template('myTravel.html',travelDetails = travelDetails)
            else:
                flash("Your travel is not possible")
                return redirect(url_for('home'))
    places = set()
    for route in cbe_transport.busRoutes:
        for place in route:
            place = place.strip()
            place = place.lower()
            places.add(place)

    places = sorted(list(places))
    return render_template('index.html',places = places)

@app.route('/addBus')
def addBus():
    return render_template('addbus.html')

if __name__ == "__main__":
    df = pd.read_csv('static/dataset/buses.csv')
    for index, row in df.iterrows():
        if index == 10:
            break
        #print(row['Bus No'], row['Via'])
        busName = row['Bus No']
        busRoute = row['Via'].split(',')
        cbe_transport.addBus(busName,busRoute)
    app.run(debug=True)