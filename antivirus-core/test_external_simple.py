import asyncio
import logging
from app.external_apis.manager import external_api_manager

# Set up logging
logging.basicConfig(level=logging.INFO)

async def test_external_simple():
    print("Testing external API manager...")
    try:
        result = await external_api_manager.check_url_multiple_apis('http://malware.wicar.org/data/eicar.com')
        print('External API result:', result)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_external_simple())

