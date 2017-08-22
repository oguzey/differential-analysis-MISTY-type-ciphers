from multiprocessing import Value, Lock


class Counter(object):
    def __init__(self, initval: int = 0) -> None:
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self) -> int:
        with self.lock:
            self.val.value += 1
            return self.val.value

    def value(self) -> int:
        with self.lock:
            return self.val.value

    def reset(self) -> None:
        with self.lock:
            self.val.value = 0
