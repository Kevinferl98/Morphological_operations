from concurrent.futures import ThreadPoolExecutor

class Executor:
    def __init__(self):
        self.executor = None

    def init_app(self, app):
        self.executor = ThreadPoolExecutor(
            max_workers=app.config["MAX_WORKERS"]
        )

executor = Executor()