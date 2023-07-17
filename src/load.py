import os
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