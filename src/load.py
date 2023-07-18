import os
import sys
import tarfile

from pandas import (
    DataFrame
    ,concat
    ,read_csv)

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
        print(f'Items extracted...')

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
    
    # Move files and build data catalogue
    print('Building data catalogue...')
    catalogue = DataFrame(columns=['file', 'variable', 'type'])

    for file in os.listdir(os.path.join(DATA_DIR, 'data')):
        
        # Build file full path
        file = os.path.join(DATA_DIR, 'data', file)
        
        # Filter csv files for catalogue
        if file.endswith('.csv'):
            _df = (
                # Convert catalogue to dataframe
                DataFrame(
                    # Open csv file and get dtypes
                    read_csv(file, nrows=10)
                    .dtypes)
                # Reset index for column manipulation
                .reset_index()
                # Rename columns
                .rename(columns={'index':'variable', 0:'type'})
                # Assign file source as column
                .assign(file = os.path.basename(file)))
            
            # Append file data to global catalogue
            catalogue = concat([catalogue, _df])
            
            # Realease system memory
            del _df

        # Move file to new directory
        move(file, DST_DIR)

    # Save data catalogue as csv
    catalogue.to_csv(
        os.path.join(DST_DIR, '00_data_catalogue.csv')
        ,index=False)

    # Delete empty directory
    os.rmdir(os.path.join(DATA_DIR, 'data'))
