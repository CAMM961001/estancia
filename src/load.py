import os
import tarfile

from numpy import arange
from pandas import DataFrame, concat, read_csv
from h3 import latlng_to_cell

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
        print(f'Items extracted')

    else:
        print('Invalid file, verify <name>.tar.gz extension')


def build_data_catalogue(file:str):
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
        
        return _df
    
    else:
        print(f'Skippping invalid file: {os.path.basename(file)}')


def build_h3_catalogue(file:str, id:str, lng:str, lat:str):
    # Build referenc latlon catalogue
    _df = (
        # Convert path to dataframe object
        read_csv(file)
        # Filter h3 reference columns in dataframe
        .filter(items=[id, lng, lat])
        # Drop duplicate columns in data and reset index
        .drop_duplicates()
        .reset_index(drop=True))
    
    # Compute h3 cells in different resolutions
    for mesh_resolution in arange(0, 16):
        # Build resolution column name
        hex_cell = 'hex_' + str(int(mesh_resolution))

        # Hexagonal cells identifiers
        _df[hex_cell] = _df.apply(
            func=lambda row: latlng_to_cell(
                lat=row[lat]
                ,lng=row[lng]
                ,res=mesh_resolution)
            ,axis=1)

        print(f'\t{hex_cell} mesh computed')
    
    return _df


if __name__ == '__main__':
    # ----------------------------------------------------------------- Imports
    from settings import ROOT
    from shutil import move


    # ----------------------------------------- Process resources and constants
    NAME = 'datos-produccion-maiz'
    DATA_DIR = os.path.join(ROOT, 'data')
    DST_DIR = os.path.join(DATA_DIR, NAME)

    # Break process if directory already exists
    if os.path.exists(DST_DIR):
        print(f'{DST_DIR} already exists')
        #sys.exit(1)

    # Make directory
    else:
        os.mkdir(DST_DIR)
    

        # ------------------------------------------------- Files decompression
        get_tar(
            name=os.path.join(DATA_DIR, NAME + '.tar.gz')
            ,path=DATA_DIR)
        
        # Build data catalogue
        print('Building data catalogue')
        catalogue = DataFrame(columns=['file', 'variable', 'type'])

        for file in os.listdir(os.path.join(DATA_DIR, 'data')):
            
            # Build file catalogue as dataframe
            file = os.path.join(DATA_DIR, 'data', file)
            _df = build_data_catalogue(file=file)
            
            # Append to global catalogue and release memory
            catalogue = concat([catalogue, _df])
            del _df

            # Move raw file to new directory
            move(file, DST_DIR)

        # Save data catalogue as csv in dir
        catalogue.to_csv(
            os.path.join(DST_DIR, '00_data_catalogue.csv')
            ,index=False)

        # Delete empty directory
        os.rmdir(os.path.join(DATA_DIR, 'data'))


    # --------------------------------------------- Build h3-py cells catalogue
    print('Building h3 cells catalogue')

    # List files with historical data
    LIST_OF_HISTORICAL_FILES = [
        file for file in os.listdir(DST_DIR)
        if file.startswith('hist')]
    
    # Reference file for h3 cells compute
    # Expects for all historical files to have the same data structure
    file = os.path.join(DST_DIR, LIST_OF_HISTORICAL_FILES[0])
    
    # Compute h3 cells in different resolutions
    _df = build_h3_catalogue(file=file, id='id', lng='lon', lat='lat')
    
    # Store catalogue
    _df.to_csv(
        os.path.join(DST_DIR, '01_h3_cells_catalogue.csv')
        ,index=False)
