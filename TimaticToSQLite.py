
from os import listdir
import re
from bs4 import BeautifulSoup
import sqlite3

### Set path to the Timatic files 
Timatic_files_folder_path = "/tmp/"

### Set path to output SQLite database file
db_path = "/tmp/Timatic.db"
conn = sqlite3.connect(db_path)

### Obtain HTML file names ###
data = []
file_names = [ s for s in listdir(Timatic_files_folder_path) if s.endswith(".html") ]
for file_name in file_names:
    nat_dest = file_name.replace(".html","").split("_")
    page = open(Timatic_files_folder_path+file_name,"r").read()
    soup = BeautifulSoup(page)
    text = ' '.join(soup.get_text().split())
    data.append([nat_dest[0],nat_dest[1],text])
    
    
### Function to allow data to be split into chucks for faster SQL query
### Got this from stackoverflow somewhere...
def chunks(data, rows=10000):
    for i in range(0, len(data), rows):
        yield data[i:i+rows]
        
### Batch process Timatic files and insert to SQLite database
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Timatic_Raw;")
cur.execute('CREATE TABLE IF NOT EXISTS Timatic_Raw (National text, Destination text, Text text, UNIQUE(National,Destination));')

divData = chunks(data)

for chunk in divData:
    cur.execute('BEGIN TRANSACTION')
    for nat, dest, text in chunk:
        cur.execute('INSERT OR IGNORE INTO Timatic_Raw (National, Destination, Text) VALUES (?,?,?)', (nat, dest, text))
    conn.commit()