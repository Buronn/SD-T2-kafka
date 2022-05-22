from flask import Flask, jsonify, request
from db.config import Config
from threading import Event
import signal
import json
import time 

from flask_kafka.consumer import FlaskKafka
app = Flask(__name__)

INTERRUPT_EVENT = Event()

bus = FlaskKafka(INTERRUPT_EVENT,
                 bootstrap_servers=",".join(["kafka:9092"]),
                 group_id="consumer-grp-id"
                 )

# Register termination listener
def listen_kill_server():
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGINT, bus.interrupted_process)
    signal.signal(signal.SIGQUIT, bus.interrupted_process)
    signal.signal(signal.SIGHUP, bus.interrupted_process)

counter = {}
banned = set()

# Handle message received from a Kafka topic
@bus.handle('login')
def process_real_time(msg):

    #print("consumed {} from test-topic".format(msg))
    val = msg.value.decode("ascii")
    temp = {"user": val, "date": msg.timestamp}
    
    if val in counter:
        current = int(time.time() * 1000)
        for item in counter[val]:
            print(item, current, current - item)
        x = [a for a in counter[val] if current - a < 60*1000]
        x.append(msg.timestamp)
        counter[val] = x
        if len(x) >=5:
            banned.add(val)
    else:
        counter[val] = [msg.timestamp]
    """
    with open("sample.json", "w") as outfile:
        json.dump(counter, outfile)
    """



@app.route('/blocked', methods=['GET'])
def blocked():
    print(counter)
    #data = json.dump(counter, indent = 4)
    
    return jsonify({"users-blocked": list(banned), "logins": counter})   

if __name__ == '__main__':
    # Start consuming from the Kafka server
    bus.run()
    # Termination listener
    listen_kill_server()
    # Start Flask server
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)
