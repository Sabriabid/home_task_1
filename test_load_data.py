import pandas as pd
import os
from etl import load_data
from etl import insert_into_db
import sqlite3
from etl import ensure_table_exists

def test_load_data():
    # Prepare a file path for the test
    path = 'temp_test.csv'  # Use a temporary file name to avoid conflicts
    try:
        # Create a small CSV file for the test
        df_expected = pd.DataFrame({'col1': [1, 2], 'col2': ['Alice', 'Bob']})
        df_expected.to_csv(path, index=False)
        
        # Execute the function
        df_result = load_data(path)
        
        # Check that the result is correct (here we're checking that the DataFrames are equal)
        pd.testing.assert_frame_equal(df_result, df_expected)
    finally:
        # Be sure to delete the CSV file after testing to avoid side effects.
        if os.path.exists(path):
            os.remove(path)

def test_load_data_with_incorrect_path():
    # Attempt to load a file that doesn't exist
    df_result = load_data('non_existent_file.csv')
    assert df_result is None, "La fonction devrait retourner None pour un chemin incorrect"



def test_insert_into_db():
    df = pd.DataFrame({'col1': [1, 2], 'col2': ['Alice', 'Bob']})
    db_path = 'file:memdb1?mode=memory&cache=shared'
    
    # Create an initial connection to create the table and keep the database alive
    conn = sqlite3.connect(db_path, uri=True)
    try:
        ensure_table_exists(db_path)
        insert_into_db(df, db_path)

        # Use the same connection to query data
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM data')
        results = cursor.fetchall()
        assert len(results) == 2, "Deux lignes doivent être insérées"
    finally:
        conn.close()

def test_insert_into_db_with_invalid_data():
    # Define the in-memory SQLite DB path
    db_path = 'file:memdb1?mode=memory&cache=shared'
    # Ensure the table exists in the DB
    ensure_table_exists(db_path)

    # Create a DataFrame with invalid data types for the 'data' table
    df_invalid = pd.DataFrame({'col1': ['invalid', 'data'], 'col2': ['Test', 'Data']})
    
    # Attempt to insert invalid data into the DB
    insert_into_db(df_invalid, db_path)

    # Connect to the in-memory SQLite DB to verify the results
    conn = sqlite3.connect(db_path, uri=True)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data')
    results = cursor.fetchall()

    # Assert that two rows are inserted despite incompatible data types (due to SQLite's dynamic type system)
    assert len(results) == 2, "Rows were inserted despite incompatible data types (SQLite behaviour)"
    conn.close()


def test_load_data_with_missing_values():

    # Define the path for a temporary CSV file with missing values
    path = 'temp_test_with_missing.csv'

    # Create a DataFrame that includes missing values
    df_expected = pd.DataFrame({'col1': [1, None], 'col2': ['Alice', None]})
    # Write the DataFrame with missing values to a CSV file
    df_expected.to_csv(path, index=False)
    
    try:
        df_result = load_data(path)

        # Assert that the loaded DataFrame matches the expected DataFrame, treating None as 'Missing'
        pd.testing.assert_frame_equal(df_result.fillna('Missing'), df_expected.fillna('Missing'))
    finally:
        # Clean up: remove the temporary CSV file if it exists
        if os.path.exists(path):
            os.remove(path)
