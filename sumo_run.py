import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd


def getdatetime():
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        currentDT = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
        DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        return DATIME

def flatten_list(_2d_list):
    flat_list = []
    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


sumoCmd = ["sumo", "-c", "osm.sumocfg"]
traci.start(sumoCmd)

packVehicleData = []
packBigData = []

while traci.simulation.getMinExpectedNumber() > 0:
       
        traci.simulationStep()

        vehicles=traci.vehicle.getIDList()

        for i in range(0,len(vehicles)):
                print(len(vehicles))
                print(vehicles)
                #Function descriptions
                #https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
                #https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-getSpeed
                vehid = vehicles[i]
                '''x, y = traci.vehicle.getPosition(vehicles[i])
                coord = [x, y]
                lon, lat = traci.simulation.convertGeo(x, y)
                gpscoord = [lon, lat]'''
                spd = round(traci.vehicle.getSpeed(vehicles[i])*3.6,2)
                '''edge = traci.vehicle.getRoadID(vehicles[i])
                lane = traci.vehicle.getLaneID(vehicles[i])
                turnAngle = round(traci.vehicle.getAngle(vehicles[i]),2)'''
                displacement = round(traci.vehicle.getDistance(vehicles[i]), 2)
                emissions = round(traci.vehicle.getCO2Emission(vehicles[i]),2)

                #Packing of all the data for export to CSV/XLSX
                vehList = [vehid, spd, displacement, emissions]

                
                print("Vehicle: ", vehicles[i], " at datetime: ", getdatetime())
                print(vehicles[i], " Speed: ", round(traci.vehicle.getSpeed(vehicles[i])*3.6,2), "km/h |", \
                                      #Returns the distance to the starting point like an odometer.
                                       " Distance: ", round(traci.vehicle.getDistance(vehicles[i]),2), "m |", \
                                      #Returns the CO2 emission in mg/s.
                                       " CO2Emission ", round(traci.vehicle.getCO2Emission(vehicles[i]),2), " mg/s"
                       )

                packBigDataLine = flatten_list([vehList])
                packBigData.append(packBigDataLine)
                print(packBigDataLine)
                print(vehList)
traci.close()

#Generate Excel file
columnnames = ['vehid', 'spd', 'displacement', 'CO2 emission']
dataset = pd.DataFrame(packBigData, index=None, columns=columnnames)
dataset.to_excel("output.xlsx", index=False)
time.sleep(5)








