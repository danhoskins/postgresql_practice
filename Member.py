import psycopg2
from datetime import date


class Member:
    '''Class that represents a family member object.'''

    def __init__(self, name, memberType, birthday, city, state):
        self.name = name
        self.memberType = memberType
        self.birthday = birthday
        self.city = city
        self.state = state

    @property
    def age(self):
        '''Calculate the age of the member.'''
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    @property
    def attributes(self):
        '''Create a list of all of the member's attributes.'''
        return [self.name, self.memberType, self.birthday, self.city, self.state]

    @property
    def attributeNames(self):
        '''Returns a list of the names of the attributes of the member object.'''
        return ["name", "type", "birthday", "city", "state"]

    @property
    def location(self):
        '''Return a string representation of the location of the family member.'''
        return self.city + ', ' + self.state

    def isInDatabase(self):
        '''Checks if the family member is in the database by comparing names.'''
        conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
        cur = conn.cursor()
        cur.execute("Select * from members")
        row = cur.fetchone()
        while(row is not None):
            if str(row[0]) == self.name:
                cur.close()
                conn.close()
                return True
            row = cur.fetchone()
        cur.close()
        conn.close()
        return False

    def getDatabaseRow(self):
        '''Returns the row object (from the database) corresponding to the member.'''
        conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
        cur = conn.cursor()
        cur.execute("Select * from members")
        row = cur.fetchone()
        while(row is not None):
            if str(row[0]) == self.name:
                cur.close()
                conn.close()
                return row
            row = cur.fetchone()
        return None

    def __repr__(self):
        return "{}, {}, {}, {}, {}, {}".format(self.name, self.memberType, self.birthday, self.age, self.city, self.state)
