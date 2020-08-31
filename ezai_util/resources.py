import time
import tracemalloc
import gc

class ResourceCounter:
    __slots__ = ['start_time','stop_time','clean']
    def __init__(self, clean=True):
        # in fractional seconds
        self.start_time = 0
        self.stop_time = 0
        self.clean = clean

    def _check_and_raise_start(self):
        if self.start_time <= 0:
            raise ValueError('TimeCounter in invalid state. Did you forget to start the counter?')

    def _check_and_raise_stop(self):
        if self.stop_time < self.start_time:
            raise ValueError('TimeCounter in invalid state. Did you forget to stop the counter?')

    def start(self):
        if self.clean:
            gc.collect()
        self.start_time = time.process_time()
        tracemalloc.start()

    def snapshot(self):
        self._check_and_raise_start()
        snapshot_time = time.process_time() - self.start_time
        self.current_memory, self.peak_memory = tracemalloc.get_traced_memory()
        return snapshot_time, self.current_memory, self.peak_memory   # in seconds


    def stop(self,clean=True):
        self._check_and_raise_start()
        self.stop_time = time.process_time()
        self.current_memory, self.peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        if self.clean:
            gc.collect()
        return self.elapsed_time, self.current_memory, self.peak_memory   # in seconds

    @property
    def elapsed_time(self):
        self._check_and_raise_start()
        self._check_and_raise_stop()
        if self.stop_time < self.start_time:
            raise ValueError('TimeCounter in invalid state. Did you forgot to stop the counter?')
        else:
            return self.stop_time - self.start_time
