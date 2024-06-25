import redis
from flask import Flask, render_template
from flask_sock import Sock

r = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/orientation', methods=['POST'])
# def orientation():
#     data = request.json

#     if data:
#         roll = data['roll']
#         pitch = data['pitch']
#         yaw = data['yaw']
#         # print(f"Roll: {roll:.3f}, Pitch: {pitch:.3f}, Yaw: {yaw:.3f}")
#         print(f"{roll}, {pitch}, {yaw}")

#         # Add new signal, dump old data
#         prev_roll.append(roll)
#         prev_roll.pop(0)
#         prev_pitch.append(pitch)
#         prev_pitch.pop(0)
#         prev_yaw.append(yaw)
#         prev_yaw.pop(0)

#         # Smooth the signal
#         smooth_roll = np.average(prev_roll)
#         smooth_pitch = np.average(prev_pitch)
#         smooth_yaw = np.average(prev_yaw)
#         # smooth_roll = simple_moving_average(prev_roll, window_size)
#         # smooth_pitch = simple_moving_average(prev_pitch, window_size)
#         # smooth_yaw = simple_moving_average(prev_yaw, window_size)

#         angles = {
#             'roll': smooth_roll,
#             'pitch': smooth_pitch,
#             'yaw': smooth_yaw,
#         }

#         # r.set('latest_orientation', jsonify(angles).data)
#         # r.set('latest_orientation', jsonify(data).data)
#         # r.publish('orientation', jsonify(angles).data)
#         # r.publish('orientation', jsonify(data).data)

#     return jsonify({'status': 'success', 'data': data})


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
