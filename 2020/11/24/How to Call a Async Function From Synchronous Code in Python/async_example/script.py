import asyncio

from databases import Database 

database = Database('sqlite:///example.db')

results = asyncio.run(database.fetch_all(query='SELECT * FROM user'))
print(results)