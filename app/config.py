class BaseConfig:
    DEBUG = False
    TESTING = False
    MAX_WORKERS = 2

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    TESTING = True