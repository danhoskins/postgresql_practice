import os
import xml.etree.ElementTree as ET
import psycopg2

basePath = os.path.dirname(os.path.realpath(__file__))
familyFile = os.path.join(basePath, 'familyReadFile.xml')
tree = ET.parse(familyFile)
root = tree.getroot()


def createMembersTable():
    '''Upload data from familyReadFile.xml to database.'''
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE members (name text, type text, birthday date, city text, state text);")
    # Read data from familyReadFile.xml file:
    for member in root:
        name = member.find('name').text
        memberType = member.find('type').text
        birthday = member.find('birthday').text
        city = member.find('city').text
        state = member.find('state').text
        cur.execute("""
			INSERT INTO members
			VALUES (%s, %s, %s, %s, %s);
			""",
                    (name, memberType, birthday, city, state))
    conn.commit()
    cur.close()
    conn.close()


createMembersTable()
