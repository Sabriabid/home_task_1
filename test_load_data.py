import pandas as pd
import os
from etl import load_data
from etl import insert_into_db
import sqlite3
from etl import ensure_table_exists

def test_load_data():
    # Préparez un chemin de fichier pour le test
    path = 'temp_test.csv'  # Utilisez un nom de fichier temporaire pour éviter les conflits
    try:
        # Créez un petit fichier CSV pour le test
        df_expected = pd.DataFrame({'col1': [1, 2], 'col2': ['Alice', 'Bob']})
        df_expected.to_csv(path, index=False)
        
        # Exécutez la fonction
        df_result = load_data(path)
        
        # Vérifiez si le résultat est correct (ici on vérifie si les DataFrame sont égaux)
        pd.testing.assert_frame_equal(df_result, df_expected)
    finally:
        # Assurez-vous de supprimer le fichier CSV après le test pour éviter les effets de bord
        if os.path.exists(path):
            os.remove(path)

def test_load_data_with_incorrect_path():
    # Tenter de charger un fichier qui n'existe pas
    df_result = load_data('non_existent_file.csv')
    assert df_result is None, "La fonction devrait retourner None pour un chemin incorrect"



def test_insert_into_db():
    df = pd.DataFrame({'col1': [1, 2], 'col2': ['Alice', 'Bob']})
    db_path = 'file:memdb1?mode=memory&cache=shared'
    
    # Créer une connexion initiale pour créer la table et maintenir la base de données en vie
    conn = sqlite3.connect(db_path, uri=True)
    try:
        ensure_table_exists(db_path)
        insert_into_db(df, db_path)

        # Utiliser la même connexion pour interroger les données
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM data')
        results = cursor.fetchall()
        assert len(results) == 2, "Deux lignes doivent être insérées"
    finally:
        conn.close()



def test_insert_into_db_with_invalid_data():
    db_path = 'file:memdb1?mode=memory&cache=shared'
    ensure_table_exists(db_path)
    df_invalid = pd.DataFrame({'col1': ['invalid', 'data'], 'col2': ['Test', 'Data']})
    
    insert_into_db(df_invalid, db_path)
    conn = sqlite3.connect(db_path, uri=True)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data')
    results = cursor.fetchall()
    assert len(results) == 2, "Les lignes ont été insérées malgré des types incompatibles (SQLite behaviour)"
    conn.close()




def test_load_data_with_missing_values():
    path = 'temp_test_with_missing.csv'
    df_expected = pd.DataFrame({'col1': [1, None], 'col2': ['Alice', None]})
    df_expected.to_csv(path, index=False)
    
    try:
        df_result = load_data(path)
        pd.testing.assert_frame_equal(df_result.fillna('Missing'), df_expected.fillna('Missing'))
    finally:
        if os.path.exists(path):
            os.remove(path)
