import os
import xml.etree.ElementTree as ET
import psycopg2
from Member import Member

basePath = os.path.dirname(os.path.realpath(__file__))
familyFile = os.path.join(basePath, 'familyWriteFile.xml')

tree = ET.parse(familyFile)
root = tree.getroot()


def updateLocation(name, city, state):
    '''Update the location of a family member in the database and familyWriteFile.xml'''
    checkForChangesInFile()


def checkForChangesInFile():
    '''Check for any mismatches between the database and familyWriteFile.xml
    For every mismatch found, update the database to match familyWriteFile.xml
    '''
    for member in root:
        memberObject = createMemberObject(member)
        if memberObject.isInDatabase():
            synchronizeMemberToDatabase(memberObject, memberObject.getDatabaseRow())


def createMemberObject(member):
    name = member.find('name').text
    memberType = member.find('type').text
    birthday = member.find('birthday').text
    city = member.find('city').text
    state = member.find('state').text
    return Member(name, memberType, birthday, city, state)


def synchronizeMemberToDatabase(memberObject, row):
    '''Checks if each attribute of memberObject matches the corresponding
    attribute in row. For any mismatch, the database is updated to match
    memberObject. '''
    for i, attributeValue in enumerate(row):
        if str(row[i]) != str(memberObject.attributes[i]):
            updateDB(memberObject, row, i)


def updateDB(memberObject, row, rowIndex):
    '''Set the database entry at rowIndex of row to newValue'''
    cur.execute('SELECT * from members')
    cur.execute("UPDATE members SET %s = '%s' WHERE name='%s'" %
                (memberObject.attributeNames[rowIndex], memberObject.attributes[rowIndex], memberObject.name))


conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
cur = conn.cursor()
checkForChangesInFile()
conn.commit()
cur.close()
conn.close()
