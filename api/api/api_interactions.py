# API interactions module
import aiohttp


async def send_request_to_openrouter(api_url, headers, payload):
    """Send a request to the OpenRouter API."""
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise ValueError(
                    f"API request failed with status {response.status}: {await response.text()}"
                )
