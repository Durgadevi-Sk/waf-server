from flask import Flask, request, redirect, jsonify
import requests

from ai_model import AIModel
from firebase_logger import log_attack, get_logs

app = Flask(__name__)

ai = AIModel()

# SERVER MACHINE IP
SERVER = "https://server2side.onrender.com"

# CLIENT MACHINE (Live Server running here)
CLIENT = "https://example.com"

ADMIN_USER = "dhana"
ADMIN_PASS = "1234"


@app.route("/")
def home():
    return "AI WAF Running"


# USER LOGIN THROUGH WAF
@app.route("/waf_login", methods=["POST"])
def waf_login():

    username = request.form.get("username")
    password = request.form.get("password")

    payload = username + " " + password

    ip = request.remote_addr

    result = ai.predict(payload)

    print("Prediction:", result)


    # NORMAL REQUEST
    if result == "NORMAL":

        try:

            res = requests.post(
                SERVER + "/login",
                data={"username": username, "password": password}
            )

            if res.text == "LOGIN_SUCCESS":
                return redirect(CLIENT + "/project.html")

            return "Login Failed"

        except:
            return "Server Not Reachable"


    # SQL ATTACK
    elif result == "SQL":

        log_attack(username, "SQL Injection", ip)

        return "Something went wrong unable to reach the server . Try again"


    # XSS ATTACK
    elif result == "XSS":

        log_attack(username, "XSS Attack", ip)

        return "Something went wrong unable to reach the server. Try again"


    # UNKNOWN ATTACK
    else:

        log_attack(username, "NEW ATTACK", ip)

        return "Blocked : Unknown Attack"


# ADMIN LOGIN
@app.route("/admin_login", methods=["POST"])
def admin_login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == ADMIN_USER and password == ADMIN_PASS:
        return redirect(CLIENT + "/admin.html")

    return "Invalid Admin Login"


# ADMIN VIEW ATTACK LOGS
@app.route("/get_logs")
def logs():

    return jsonify(get_logs())


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # default to 5000 locally
    app.run(host="0.0.0.0", port=port)