import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER , mount Text)''')

fname = raw_input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From '): continue
    pieces = line.split()
    email = pieces[1]
    mount = pieces[3]

    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (email,mount, count)
                VALUES ( ?,?, 1 )''', (email, mount,))
    else:
        cur.execute('UPDATE Counts SET count=count+1 WHERE email = ?',
                    (email,))
        cur.execute("UPDATE Counts SET mount=? WHERE email = ?",
                    (mount, email,))
    conn.commit()

sqlstr = 'SELECT email,count,mount FROM Counts Order BY mount,count DESC LIMIT 10'

print
print "E-mail:"
for row in cur.execute(sqlstr):
    print str(row[0]), str(row[1]), str(row[2])

cur.close()
