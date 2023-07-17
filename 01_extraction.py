import os
import src.load as load
import src.settings as settings


DATA_DIR = os.path.join(settings.ROOT, 'data')
FILE_PATH = os.path.join(DATA_DIR, 'datos-produccion-maiz.tar.gz')

load.get_tar(name=FILE_PATH, path=DATA_DIR)


if __name__ == '__main__':
    print('Job done...')
