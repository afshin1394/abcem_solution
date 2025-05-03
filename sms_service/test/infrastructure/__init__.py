import asyncio
import aio_pika

async def test_rabbitmq_connection():
    try:
        connection = await aio_pika.connect_robust(
            host="localhost",
            port=5672,
            login="admin",
            password="admin",
            heartbeat=60
        )
        print("Connection successful!")
        await connection.close()
    except Exception as e:
        print(f"Connection failed: {e}")

def main():
    """
    Entry point for the script.
    """
    asyncio.run(test_rabbitmq_connection())

if __name__ == "__main__":
    main()