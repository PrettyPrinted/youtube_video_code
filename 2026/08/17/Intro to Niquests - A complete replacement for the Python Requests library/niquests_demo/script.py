import asyncio
import requests
import niquests
from time import time

# async def main():
#     # r = await niquests.aget("https://prettyprinted.com")
#     # print(r.text)
#     async with niquests.AsyncSession() as session:
#         request_list = [session.get("https://prettyprinted.com") for _ in range(10)]
#         response_list = await asyncio.gather(*request_list)
#         print([response.status_code for response in response_list])

# asyncio.run(main())

start = time()
with niquests.Session(multiplexed=True) as session:
    response_list = [session.get("https://prettyprinted.com") for _ in range(10)]
    session.gather(*response_list)
    print([response.status_code for response in response_list])

print(f"Time spent: {time() - start}")