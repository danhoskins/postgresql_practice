# postgresql_practice
Practice with postgreSQL databases using psycopg2 library in python.

createTable.py creates a table in a PostgreSQL database and writes data from a previously created xml file
(familyReadFile.xml) to the table. updateFamilyFile.py retrieves the data from the database and writes it 
to another xml file, familyWriteFile.xml. synchronize.py, compares the data in familyWriteFile.py to the data in 
the database, and, if there are any differences, updates the data in the database to match familyWriteFile.py. Member.py is a class 
used to crepresent family member objects. I used the xml.etree.ElementTree and psycopg2 libraries to interface with the xml 
files and PostgreSQL database, respectively. 
