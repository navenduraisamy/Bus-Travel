import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


db.collection('buses').add({'busName':'1','busRoute':["vadavalli","gandhipark","poomarket","gandhipuram","ramakrishna"]})
db.collection('buses').add({'busName':'145','busRoute':["singanallur","esi hospital","hope college","peelamedu","lakshmi mills","gandhipuram"]})
db.collection('buses').add({'busName':'30K','busRoute':["singanallur","ondipudur","sulur","rvs","aero","karnampettai","ichipatti"]})