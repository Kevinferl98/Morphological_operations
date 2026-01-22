import os

def pytest_configure():
    os.environ["MINIO_ROOT_USER"] = "user"
    os.environ["MINIO_ROOT_PASSWORD"] = "password"