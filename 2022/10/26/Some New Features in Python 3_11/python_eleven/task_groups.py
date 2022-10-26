import asyncio

async def example(i):
    print(f"Start {i}")
    await asyncio.sleep(i)
    print(f"End {i}")

    return f"Finished {i}"

async def run_with_gather():
    tasks = []
    for num in range(1, 5):
        task = asyncio.create_task(example(num))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    print(results)

async def run_with_groups():
    results = []
    async with asyncio.TaskGroup() as tg:
        for num in range(1, 5):
            task = tg.create_task(example(num))
            results.append(task)

    print([task.result() for task in results])

asyncio.run(run_with_groups())