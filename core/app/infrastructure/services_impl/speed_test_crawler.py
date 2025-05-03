import asyncio
import aiohttp
import os
from typing import List, Iterable
from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

class SpeedTestServerCrawler:
    def __init__(self, t=None, r=None, d=1):
        self.t = t or 5  # Number of concurrent tasks
        self.r = r or 5  # Retry count
        self.d = d or 5  # Delay
        self.task_queue = asyncio.Queue()
        self.servers = []
        self.passed = set()
        self.URL = "https://www.speedtest.net/api/js/servers"
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
        }

    async def _init_tasks(self):
        # Directly add tasks for Iran
        iran_data = [
            "Iran (Islamic Republic of)",  # e_name
            "IR",  # iso_3166_1_alpha_2
            "IRN"  # iso_3166_1_alpha_3
        ]
        for search_term in iran_data:
            await self.task_queue.put((search_term, 0))

    async def fetch(self, client: aiohttp.ClientSession, search: str) -> Iterable:
        async with client.get(
            url=self.URL,
            params={
                "engine": "js",
                "search": search,
                "limit": 1000,
            },
            headers=self.HEADERS,
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    def _filter(self, server):
        server_id = server.get("id")
        if server_id not in self.passed:
            self.passed.add(server_id)
            return True
        return False

    async def process_tasks(self):
        async with aiohttp.ClientSession() as client:
            while not self.task_queue.empty():
                search, retries = await self.task_queue.get()
                if retries >= self.r:
                    continue
                try:
                    servers = await self.fetch(client=client, search=search)
                    filtered_servers = filter(self._filter, servers)
                    for filtered_server in filtered_servers:
                        filtered_server["server_id"] = filtered_server.pop("id")
                        self.servers.append(SpeedTestServerDomain(**filtered_server))
                except Exception as e:
                    print(f"Error fetching data for {search}: {e}")
                    await self.task_queue.put((search, retries + 1))

    async def run(self) -> List[SpeedTestServerDomain]:
        await self._init_tasks()
        tasks = [self.process_tasks() for _ in range(self.t)]
        await asyncio.gather(*tasks)
        return self.servers

    def start(self) -> List[SpeedTestServerDomain]:
        asyncio.run(self.run())
        return self.servers
