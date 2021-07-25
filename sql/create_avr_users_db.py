import sqlite3
import os

if os.path.exists('avr_users.sqlite'):
    os.remove('avr_users.sqlite')

conn = sqlite3.connect('avr_users.sqlite')
c = conn.cursor()
conn.commit()
conn.close()

print("avr_users.sqlite Data Base Created ... !")
