import grequests
import requests
import json
def alberta():
    js = json.load(open('config/America/511.alberta.json'))
    c = 1
    for i in js['correct']:

        a = requests.get(i)
        asd = open(f'511.alberta/{c}.png', 'wb+')
        asd.write(a.content)
        c+=1


def trafikverket():
    counter = 39635000 
    l = []
    for i in range(2300):
        l.append(grequests.get(f'https://api.trafikinfo.trafikverket.se/v2/Images/TrafficFlowCamera_{counter+i}.Jpeg?type=fullsize&maxage=140'))
        #print(f'https://api.trafikinfo.trafikverket.se/v2/Images/TrafficFlowCamera_{counter+i}.Jpeg?type=fullsize&maxage=140')
        print(i)
    res = grequests.map(l)
    for i in range(2300):
        print(res[i].status_code)
        if (res[i].status_code==200):
            asd = open(f'trafikinfo/{counter+i}.png', 'wb+')
            asd.write(res[i].content)

def oxblue():
    counter = 39635000 
    l = []
    for i in range(1, 1500):
        l.append(grequests.get(f'https://infocar.dgt.es/etraffic/data/camaras/{i}.jpg?t=1695814051472'))
        #print(f'https://api.trafikinfo.trafikverket.se/v2/Images/TrafficFlowCamera_{counter+i}.Jpeg?type=fullsize&maxage=140')
        print(i)
    res = grequests.map(l)
    for i in range(2300):
        print(res[i].status_code)
        if (res[i].status_code==200):
            asd = open(f'../infocar/{i}.png', 'wb+')
            asd.write(res[i].content)


def dgt():

    for i in range(1, 1601):
        a = requests.get(f'https://cameras.trafikinfo.trafikverket.se/image/39635199.jpeg?t=1696601818559')
        #print(f'https://api.trafikinfo.trafikverket.se/v2/Images/TrafficFlowCamera_{counter+i}.Jpeg?type=fullsize&maxage=140')
        print(a.status_code)
        if (a.status_code==200):
            asd = open(f'dgt/{i}.png', 'wb+')
            asd.write(a.content)

def trafikkort():
    counter = 39635190
    for i in range(1, 800):
        a = requests.get(f'https://cameras.trafikinfo.trafikverket.se/image/{counter+i}.jpeg?t=1696602487183')
        print(f'https://cameras.trafikinfo.trafikverket.se/image/{counter+i}.jpg?t=1696602487183')
        print(a.status_code)
        if (a.status_code==200):
            asd = open(f'trafikkort/{i}.png', 'wb+')
            asd.write(a.content)

def roadi_pref():
    for i in range(1, 12):
        high = str(i).zfill(2)
        for j in range(1, 100):
            low = str(j).zfill(2)
            num = high+low
            path = f'https://www.roadi.pref.shimane.jp/data/snapshot/{num}.jpg'
            a = requests.get(path)
            if (a.status_code==200):
                asd = open(f'roadi_pref/{num}.png', 'wb+')
                asd.write(a.content)
            else:
                print(path)

def images_drivebc():
    counter = 5
    for i in range(1050):
        a = requests.get(f'https://images.drivebc.ca/bchighwaycam/pub/cameras/{counter + i}.jpg')
        #print(f'https://cameras.trafikinfo.trafikverket.se/image/{counter+i}.jpg?t=1696602487183')
        print(a.status_code)
        if (a.status_code==200):
            asd = open(f'images_drivebc/{i}.png', 'wb+')
            asd.write(a.content)


def liikennetilanne():
    for i in range(15, 155, 10):
        high = str(i).zfill(3)
        for j in range(4, 100):
            low = str(j).zfill(2)
            res_url = f'https://weathercam.digitraffic.fi/C{high}{low}01.jpg?versionId='
            a = requests.get(res_url)
            print(a.status_code)
            print(res_url)
            if (a.status_code==200):
                asd = open(f'liikennetilanne/{i}_{j}.png', 'wb+')
                asd.write(a.content)

def vegvesen():
    js = json.load(open('config/Norway/vegvesen.json'))
    c = 1
    for i in js['correct']:
        path = f'https://webkamera.atlas.vegvesen.no/public/kamera?id={i}'
        a = requests.get(path)
        asd = open(f'vegvesen/{c}.png', 'wb+')
        asd.write(a.content)
        c+=1

def on511():
    js = json.load(open('config/Kanada/511on.json'))
    c = 1
    for i in js['correct']:
        path = f'https://511on.ca/map/Cctv/{i}'
        a = requests.get(path)
        if a.status_code == 200:
            asd = open(f'511on/{i}.png', 'wb+')
            asd.write(a.content)
            c+=1

if __name__ == "__main__":
    on511()