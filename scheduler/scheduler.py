# scheduler

import asyncio


class TaskScheduler:
    def __init__(self, loop):
        self.loop = loop
        self.running = False
        self._cancel_event = asyncio.Event()

    async def start(self):
        if self.running:
            print("[Scheduler] Already running")
            return
        self.running = True
        self._cancel_event = asyncio.Event()
        while not self._cancel_event.is_set():
            print("[Scheduler] Starting task cycle")
            start_time = asyncio.get_event_loop().time()
            # Simulate task execution
            await asyncio.sleep(1)  # Simulate a task taking 1 second
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining = max(0, 10 - elapsed)
            print(f"[Scheduler] Waiting {remaining:.2f} seconds before next cycle")


    async def stop(self):
        if self.running:
            print("[Scheduler] Stop requested")
            self._cancel_event.set()
    
