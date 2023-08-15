import os

class Settings:
    def __init__(self):
        self.SRC_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT = os.path.dirname(self.SRC_DIR)

if __name__ == '__main__':
    settings = Settings()
    print(settings.ROOT)
    