import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-waf-project-default-rtdb.firebaseio.com/'
})


def log_attack(username, attack_type, ip):

    ref = db.reference("attack_logs")

    data = {
        "username": username,
        "attack": attack_type,
        "ip": ip,
        "time": str(datetime.now())
    }

    ref.push(data)


def get_logs():

    ref = db.reference("attack_logs")

    logs = ref.get()

    if logs is None:
        return []

    return logs