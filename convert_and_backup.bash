# !/bin/bash

/home/HawkinsPi/venv/bin/python3 /home/HawkinsPi/text_to_csv.py # Convert all temp metData files to CSV
/home/HawkinsPi/venv/bin/python3 /home/HawkinsPi/firebase/write_to_firebase.py # Upload new metData values from metData.csv to Firestore
/home/HawkinsPi/clear_buffer.bash # Clear metData buffer files