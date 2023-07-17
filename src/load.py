import os
import sys
import tarfile

def get_tar(name:str, path='.'):
    """
    Gets contents of a <file>.tar.gz compressed file and renames
    directory if applicable.

    Parameters:
        name: <type:str> Name or path to compressed file
        path: <type:str, default:'.'> Destiny directory
    """

    # Validate file extension
    if name.endswith('.tar.gz'):

        # Tar content extraction
        tar = tarfile.open(name)
        tar.extractall(path=path)
        tar.close()

        # Extraction confirmation message
        print(f'Items extracted in {os.path.abspath(path)}')

    else:
        print('Invalid file, verify <name>.tar.gz extension...')


if __name__ == '__main__':
    
    # Imports for main execution
    from settings import ROOT
    from shutil import move

    # Process resources and variables
    NAME = 'datos-produccion-maiz'
    DATA_DIR = os.path.join(ROOT, 'data')
    DST_DIR = os.path.join(DATA_DIR, NAME)

    # Break process if directory already exists
    if os.path.exists(DST_DIR):
        print(f'{DST_DIR} already exists')
        sys.exit(1)

    # Make directory
    else:
        os.mkdir(DST_DIR)
    
    # Extract files from tar
    get_tar(
        name=os.path.join(DATA_DIR, NAME + '.tar.gz')
        ,path=DATA_DIR)
    
    # Move files
    for file in os.listdir(os.path.join(DATA_DIR, 'data')):
        move(
            os.path.join(DATA_DIR, 'data', file)
            ,DST_DIR)

    # Delete empty directory
    os.rmdir(os.path.join(DATA_DIR, 'data'))
