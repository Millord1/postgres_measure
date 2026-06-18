import tracemalloc

class MemoryTracker:
    def __enter__(self):
        tracemalloc.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.peak_mo = peak / (1024 * 1024)