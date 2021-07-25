import sqlite3
import os

if os.path.exists('avr.sqlite'):
    os.remove('avr.sqlite')

conn = sqlite3.connect('avr.sqlite')
c = conn.cursor()
conn.commit()
conn.close()

print("Data Base Created ... !")
