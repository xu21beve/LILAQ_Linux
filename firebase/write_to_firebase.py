import os
import pandas as pd
from google.cloud import firestore
from datetime import datetime

# Make sure authentication is set
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\acsm.ACSMC-087\\Documents\\GitHub\\firebase\\serviceAccountKey.json"

# Firestore project and database
project_id = "lilaqmetdata"
database_id = "lilaq-data"

# Initialize Firestore client (supports custom database IDs)
db = firestore.Client(project=project_id, database=database_id)

def update_firestore_from_csv(collection_name, local_file_name, upload_log_file_name, key_field):
    """
    Reads local CSV, then updates the Firestore collection so that each row becomes
    a document keyed by the `key_field` (e.g., date_id). Existing docs are merged.
    """
    # Load local TSV into pandas
    df = pd.read_csv(local_file_name, sep="\t")
    # print(f"Loaded {len(df)} rows from {local_file_name}")

    # Iterate through rows and update Firestore
    for _, row in df.iterrows():
        key_value = str(row[key_field])
        doc_ref = db.collection(collection_name).document(key_value)

        # Drop the second column of timestamps
        key_indices = [i for i, c in enumerate(df.columns) if c == key_field]

        # Convert row to dictionary and write
        data = row.drop(df.columns[key_indices[-1]]).to_dict()
        doc_ref.set(data, merge=True)
        # print(f"Updated {collection_name}/{key_value}")

    with open(upload_log_file_name, 'a') as out:
    	print(datetime.now().strftime("%Y%m%d%T") + f"Finished updating {collection_name} collection.", file=out)

# Upload met data:
collection_name = "acsm"
local_file_name = "C:\\Users\\acsm.ACSMC-087\\Documents\\GitHub\\data\\buffer.txt"
error_file_name = "C:\\Users\\acsm.ACSMC-087\\Documents\\GitHub\\error_log.txt"
upload_log_file_name = "C:\\Users\\acsm.ACSMC-087\\Documents\\GitHub\\upload_log.txt"

try:
	update_firestore_from_csv(collection_name, local_file_name, upload_log_file_name, "time_text")
except Exception as e:
	with open(error_file_name, 'a') as out:
		print(datetime.now().strftime("%Y%m%d%T") + str(e), file=out)
else: 
	# Wipe buffer file if upload was successful
	with open(local_file_name, 'w'):
		pass