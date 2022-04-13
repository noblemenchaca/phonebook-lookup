'''
Perform 'get' request with query strings and writes desired people to csv files
'''
from bs4 import BeautifulSoup
import requests, zlib, json, urllib, csv
from urllib.request import urlopen


class Person:
    def __init__(self, last,first,ptype,email,phone,unit,position,addr,bldg,rm):
        ''''''
        self.last  = last
        self.first = first
        self.ptype = ptype
        self.email = email
        self.phone = phone
        self.unit  = unit           #degree
        self.position = position    #department
        self.addr  = addr
        self.bldg  = bldg
        self.rm    = rm
    
    def from_soup(soup_object):

        f   = ""
        l   = ""
        pt  = ""
        em  = ""
        ph  = ""
        u   = "" 
        pos = "" 
        address = ""
        building = ""
        room = ""

        try:
            person_fullname = soup_object.find("div", {"class": "phonebook"}).h3.contents[0]
            person_fullname=person_fullname.strip()
            person_fullname=person_fullname.split(", ")
            f=person_fullname[1]
            l =person_fullname[0]
        except:
            pass
        
        try:
            pt = soup_object.find("span",{"class":"type"}).contents[0]
        except:
            pass
        try:
            em = soup_object.find("a",{"class":"mailto"}).contents[0]
        except:
            pass
        try:
            ph = soup_object.find("a",{"class":"phoneto"}).contents[0]
        except:
            pass
        try:
            u = soup_object.find("div",{"class":"degree"}).contents[0]
        except:
            pass
        try:
            pos = soup_object.find("div",{"class":"department"}).contents[0]
            #print(pos)
            pos = pos.replace("\t", "").replace("\r", "").replace("\n", "")
        
        except:
            pass
        try:
            address = soup_object.find_all("div")
            address=address[-3].getText()
        except:
            pass
        try:
            building=address[-2].getText()[10:] #remove "Building: " from the string
        except:
            pass
        try:
            room=address[-1].getText()
        except:
            pass
            
        f=f.strip()
        l=l.strip()
        pt=pt.strip()
        em=em.strip()
        ph=ph.strip()
        u=u.strip()
        pos=pos.strip()
        address=address.strip()
        building=building.strip()
        room=room.strip()
        
        return Person(first=f,last=l,ptype = pt, email = em, phone = ph, unit = u, position = pos, addr = address, bldg = building, rm = room)



    def generator(self):
        '''returns a stylized string with Persons'''
        return [str(self.last + ", " + self.first), self.ptype, self.email, self.phone, self.unit, self.position, self.addr, str(self.bldg +" rm "+ self.rm)]

    def __repr__(self):
        '''returns a string to print Person objects'''
        final=""
        items = [str(self.first + " " + self.last), self.email, self.position]
        for item in items:
            final += item.strip() + ", "
        return final[0:-2]

    def __eq__(self, other):
        return (self.email == other.email)

    def __lt__(self, other):
        if (self == other): return False
        elif (self.last < other.last): return True
        elif (self.first < other.first): return True
        else: return False

    def __hash__(self):
        return hash(str(self.email))

# AAAGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH


class People:
    def __init__(self, people_list=None, fname=None):
        '''initializes People objects'''
        names0 = [] #unstripped
        names = []  # last, First Names        
        if people_list == None:
            self.people = [] #list of Person instances
        else:
            self.people = people_list
        self.missing = [] #names from file but not in phonebook
        if fname: #itterate through the csv file
            with open(fname) as csvfile:
                spam = csv.reader(csvfile, delimiter = ',')
                for item in spam:
                    names0.append(item)
                for fullname in names: #strip the names
                    name = []
                    for item in fullname:
                        names.append(item.strip())
                    names.append(name)
                    
        bare_url = ['http://directory.arizona.edu/phonebook?type_2=&lastname=','&firstname=']
        urls = []
        
        for item in names: #url builder
            string = bare_url[0] + item[0] + bare_url[1] + item[1]
            urls.append(string)
            
        for url in urls:  #iterate through names
            r = requests.get(url)
            soup = BeautifulSoup(r.content) 
            soups = soup.find_all('span',{'class': "field-content"})
            for soup_object in soups:
                self.people.append(from_soup(soup_object))
            
            #self.people_list.append(Person.from_soup(soup_object))
            
#==========================================================
def main():
    '''
    Write a description of what happens when you run
    this file here.
    '''

    input('Press enter to end.') 

if __name__ == '__main__':
    main()
