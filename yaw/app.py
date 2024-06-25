import redis
from flask import Flask, render_template
from flask_sock import Sock

r = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def index():
    return render_template('index.html')


@sock.route('/deviceorientation')
def handle_deviceorientation(ws):
    print('connected to ws!')
    while True:
        data = ws.receive()

        if data:
            print(data)
            r.publish('orientation', data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, ssl_context=('cert.pem', 'key.pem'))
