from flask import Flask, request
from threading import Lock
from cellService.send_sms import send_sms
from cellService.group import send_group
from cellService.android_sms import android_sms
from cellService.call import call

app = Flask(__name__)
app.register_blueprint(send_sms)
app.register_blueprint(send_group)
app.register_blueprint(android_sms)
app.register_blueprint(call)

# Create locks for each function
send_sms_lock = Lock()
send_group_lock = Lock()
android_sms_lock = Lock()
call_lock = Lock()

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        return 'Hello, World! (GET Request)'
    elif request.method == 'POST':
        return 'Hello, World! (POST Request)'

# Apply locks to functions in blueprints
@app.before_request
def before_request():
    if request.blueprint == 'send_sms':
        send_sms_lock.acquire()
    elif request.blueprint == 'send_group':
        send_group_lock.acquire()
    elif request.blueprint == 'android_sms':
        android_sms_lock.acquire()
    elif request.blueprint == 'call':
        call_lock.acquire()

@app.after_request
def after_request(response):
    if request.blueprint == 'send_sms':
        send_sms_lock.release()
    elif request.blueprint == 'send_group':
        send_group_lock.release()
    elif request.blueprint == 'android_sms':
        android_sms_lock.release()
    elif request.blueprint == 'call':
        call_lock.release()
    return response

if __name__ == '__main__':
    app.run(host='10.190.7.69', port=5000, debug=True)
