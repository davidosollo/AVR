import sqlite3
import os

if os.path.exists('review.sqlite'):
    os.remove('review.sqlite')

conn = sqlite3.connect('review.sqlite')
c = conn.cursor()
c.execute('CREATE TABLE review_db (review TEXT , sentiment INTEGER, date TEXT)')

example1 = 'I love this movie'
c.execute("INSERT INTO review_db (review , sentiment , date) VALUES"
          "(?, ?, DATETIME('now'))", (example1, 1))

example2 = 'I Dislike this movie'
c.execute("INSERT INTO review_db (review , sentiment , date) VALUES"
          "(?, ?, DATETIME('now'))", (example2, 5))

conn.commit()

c.execute("SELECT * FROM review_db")
results = c.fetchall()
conn.close()

print(results)
