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


if __name__ == "__main__":
    oxblue()