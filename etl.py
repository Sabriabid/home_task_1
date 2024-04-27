import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    try:
        logging.info("Loading data from file: %s", file_path)
        df = pd.read_csv(file_path)
        print("Données chargées avec succès :")
        print(df.head())  # Display first lines to check content
        return df
    except Exception as e:
        print("Erreur lors du chargement des données :", e)
        return None

def ensure_table_exists(db_path):
    conn = sqlite3.connect(db_path, uri=True)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                col1 INTEGER,
                col2 TEXT
            );
        ''')
        conn.commit()
    finally:
        conn.close()



def insert_into_db(df, db_path="my_database.db"):
    if df is None:
        print("Aucune donnée à insérer dans la base de données.")
        return
    try:
        ensure_table_exists(db_path)  # Make sure the table exists
        conn = sqlite3.connect(db_path)
        df.to_sql('data', conn, if_exists='replace', index=False)
        print(f"Données insérées dans {db_path} dans la table 'data'")
        conn.close()
        logging.info("Data inserted into database successfully.")
    except Exception as e:
        print("Erreur lors de l'insertion des données :", e)
        logging.error("Error inserting data into database: %s", str(e))

if __name__ == '__main__':
    logging.info("ETL Job Started.")
    df = load_data("test.csv")
    insert_into_db(df)
    logging.info("ETL Job Finished.")
