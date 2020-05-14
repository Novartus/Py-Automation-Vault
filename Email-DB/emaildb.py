import re
import sqlite3

con = sqlite3.connect('email.sqlite')
cur = con.cursor()

cur.execute('CREATE TABLE Counts(org TEXT, count INTEGER)')

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'mbox.txt'

fl = open(fname)

for line in fl:
    if not line.startswith('From: '):
        continue
    line = line.strip()
    temp = re.findall('@([\w.]+)', line)  #temp will be stored as list
    #print(temp)

    if len(temp) > 0:
        domain = temp[0]  #1st element of list OR domain 
        cur.execute('SELECT count FROM Counts WHERE org = ?', (domain,))
        row = cur.fetchone()

        if row is None:
            cur.execute('INSERT INTO Counts(org, count) VALUES(?, 1)', (domain,))
        else:
            cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (domain,))
        con.commit()

cur.close()