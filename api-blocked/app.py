import json
from flask import Flask, jsonify, request
from db.config import Config
from threading import Event
from aiokafka import AIOKafkaConsumer
import asyncio
import datetime
async def consume(topic):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers='kafka:9092',
        group_id=None)
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            with open('data.txt', 'a') as f:
                timestamp = msg.timestamp
                date = datetime.datetime.fromtimestamp(timestamp / 1e3)
                msg = msg.value.decode('utf-8')+','+str(date)+'\n'
                f.write(msg)
                f.close()
                
             
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/blocked', methods=['GET'])
def blocked():
    with open('data.txt', 'r') as f:
        data = f.read()
        f.close()
    data = data.split('\n')
    data = list(filter(None, data))
    
    return jsonify({'data': data})
@app.route('/consume', methods=['GET'])
def consumir():
    asyncio.run(consume('login'))

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
