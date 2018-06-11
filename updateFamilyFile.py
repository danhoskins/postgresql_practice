import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import xml.etree.ElementTree
from xml.dom import minidom
import psycopg2
from datetime import date
import Member
from Member import Member

basePath = os.path.dirname(os.path.realpath(__file__))
familyFile = os.path.join(basePath, 'familyWriteFile.xml')


def getFamilyData():
    '''Download family data from database and create list of member objects.'''
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
    cur = conn.cursor()
    cur.execute("Select * from members")
    row = cur.fetchone()
    members = []
    '''Create member objects from the table data.'''
    while(row is not None):
        members.append(Member(row[0], row[1], row[2], row[3], row[4]))
        row = cur.fetchone()
    cur.close
    conn.close
    return members


def writeToFile(members):
    '''Write the data from the database to familyWriteFile.xml.'''
    familyElement = Element('Family')
    for member in members:
        newMember = SubElement(familyElement, 'member')
        name = SubElement(newMember, 'name')
        name.text = member.name
        memberType = SubElement(newMember, 'type')
        memberType.text = member.memberType
        birthday = SubElement(newMember, 'birthday')
        birthday.text = str(member.birthday)
        age = SubElement(newMember, 'age')
        age.text = str(member.age)
        city = SubElement(newMember, 'city')
        city.text = member.city
        state = SubElement(newMember, 'state')
        state.text = member.state
    '''Write the ElementTree to familyWriteFile.xml'''
    xmlstr = minidom.parseString(xml.etree.ElementTree.tostring(
        familyElement)).toprettyxml(indent="    ")
    with open("familyWriteFile.xml", "w") as f:
        f.write(xmlstr)


# Get the data from the database and write it to familyWriteFile.xml
members = getFamilyData()
writeToFile(members)
