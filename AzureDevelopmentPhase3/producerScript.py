from azure.eventhub import EventData, TransportType
from azure.eventhub.aio import EventHubProducerClient
import asyncio

async def send_event_to_eventhub():
    producer = EventHubProducerClient.from_connection_string(
        conn_str = "Endpoint=sb://sepsisstreamingeventhubnamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=HmtoeA1c8SpIls4m6VV55l79cIj/+AIAa+AEhPX1xDA=",
        eventhub_name = "eventhubsepsisstreaming",
        transport_type=TransportType.AmqpOverWebsocket
    )

    async with producer:
        event_data_batch = await producer.create_batch()
        event_data_batch.add(EventData("Sample message to Event Hub"))
        await producer.send_batch(event_data_batch)
        print("Message sent to Event Hub")

asyncio.run(send_event_to_eventhub())
