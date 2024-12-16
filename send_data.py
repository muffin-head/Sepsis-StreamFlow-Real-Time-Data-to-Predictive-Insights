import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json
from azure.eventhub import TransportType
from azure.eventhub.aio import EventHubProducerClient

async def run():

    producer = EventHubProducerClient.from_connection_string(
    conn_str="Endpoint=sb://streamingdatasepsis.servicebus.windows.net/;SharedAccessKeyName=eventhub;SharedAccessKey=g7fCnBi4CfJOKCpxjLrFY7nVdAUa8DUmM+AEhBcv+4M=;EntityPath=streamingeventhub",
    eventhub_name="streamingeventhub",
    transport_type=TransportType.AmqpOverWebsocket
    )   
    
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()
        f = open("test.json")
        json_temp = json.load(f)
        # Add events to the batch.
        event_data_batch.add(EventData(str(json_temp)))

        await producer.send_batch(event_data_batch)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())