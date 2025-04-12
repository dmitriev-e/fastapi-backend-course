# Just for test async function
# Use * to unpack iterable object to pass to asyncio.gather
# ------------- Additional Info -------------
# https://www.youtube.com/watch?v=h-EFkclgCc8 more about asyncio in Russian


import asyncio


async def waitNSecond(n: int):
    print(f"Starting wait {n} seconds")
    await asyncio.sleep(n)
    print(f"Finished wait {n} second")


async def main():
    await asyncio.gather(*(waitNSecond(_) for _ in range(1, 4)))


if __name__ == "__main__":
    asyncio.run(main())