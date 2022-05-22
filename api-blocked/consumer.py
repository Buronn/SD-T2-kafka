from aiokafka import AIOKafkaConsumer
import asyncio
import datetime

async def consume():
    await asyncio.sleep(10)
    consumer = AIOKafkaConsumer(
        'login',
        bootstrap_servers='kafka:9092')
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

asyncio.run(consume())