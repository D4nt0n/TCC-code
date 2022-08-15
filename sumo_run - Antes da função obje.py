import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd
import xml.dom.minidom as ET
from scipy.optimize import minimize

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

def danton(x):

    packSimulationsData = []
    packBigData = []
    packOutputData = []
    dataset = []
    emissions_total = 0
    j = 0
    for j in range(5):
        # Initialize total_simulation as zero
        total_simulation = 0

        # Access route xml file
        tree = ET.parse("osm_pt.rou.xml")

        # Get the list of vehicles in route xml file
        vehicles = tree.getElementsByTagName("vehicle")
        # print(vehicles)
        vehicle_depart = 0 + j * 10

        # For each vehicle in route xml file determine its depart
        for vehicle in vehicles:
            vehicle_depart_coefficient = j * 20
            # print(vehicle.getAttribute("id"))
            vehicle.setAttribute("depart", str(vehicle_depart))
            # print(vehicle.getAttribute("depart"))
            vehicle_depart = vehicle_depart + vehicle_depart_coefficient + 300

        with open("osm_pt.rou.xml", "w") as fs:
            fs.write(tree.toxml())
            fs.close()

        # Open sumo and start traci
        sumoCmd = ["sumo", "-c", "osm.sumocfg"]
        traci.start(sumoCmd)

        # Run every step time until the simulation is over
        while traci.simulation.getMinExpectedNumber() > 0:

                traci.simulationStep()
                vehicles = traci.vehicle.getIDList()

                for i in range(0,len(vehicles)):

                        # Get differents values of each vehicle at every steptime
                        vehid = vehicles[i]
                        spd = round(traci.vehicle.getSpeed(vehicles[i])*3.6,2)
                        displacement = round(traci.vehicle.getDistance(vehicles[i]), 2)
                        emissions = round(traci.vehicle.getCO2Emission(vehicles[i]),2)
                        capacity = 0
                        occupation = 0
                        percentage = 0
                        stopstate = traci.vehicle.getStopState(vehicles[i])
                        stop = []
                        '''
                            print(stop)'''
                        bus_stopped = traci.busstop.getVehicleIDs("P3_Padre_Cacique")
                        if bus_stopped != ():
                        # print(stop)
                            print(bus_stopped)
                            for vehicle in bus_stopped:
                                occupation = round(traci.vehicle.getPersonNumber(vehicles[i]), 2)
                                capacity = round(traci.vehicle.getPersonCapacity(vehicles[i]), 2)
                                if capacity != 0:
                                    percentage = occupation / capacity
                                    print(percentage)
                                else:
                                    percentage = 'nan'
                        # Depart time and later get with unique from list
                        vehicle_depart = traci.simulation.getDepartedIDList()
                        k = 0
                        departure_time = 0
                        for k in range(0, len(vehicle_depart)):
                            if vehicle_depart[k] == vehid:
                                departure_time = traci.simulation.getTime()
                            else:
                                departure_time = 'nan'
                        # Packing of all the data for export to CSV/XLSX
                        vehList = [j, vehid, spd, displacement, emissions, departure_time, capacity, occupation, percentage]
                        packBigDataLine = flatten_list([vehList])
                        packBigData.append(packBigDataLine)
        traci.close()

        columnnames = ['simu', 'vehid', 'spd', 'displacement', 'CO2 emission', 'Time', 'Capacity', 'Occupation', 'percentage']
        dataset = pd.DataFrame(packBigData, index=None, columns=columnnames)
    dataset.to_excel("output.xlsx", index=False)
    # displacement = dataset.groupby(['simu', 'vehid'])['displacement'].last()
    '''displacement.to_excel("output2.xlsx", index=False)'''
    occupation_veh = dataset.groupby(['simu', 'vehid'], as_index=False)['percentage'].max()
    occupation_veh.to_excel("output2.xlsx", index=False)
    total_occupation = occupation_veh.groupby('simu', as_index=False)['percentage'].mean()
    print(total_occupation)
    total_simulation = dataset.groupby('simu', as_index=False)['CO2 emission'].sum()
    total = pd.merge(total_simulation, total_occupation, on='simu', how='inner')
    total.to_excel("output3.xlsx", index=False)
    # Solve problem of columns percentage
    time.sleep(5)
return

'''total_distance = jow['displacement'].sum()
print(total_distance)'''
# SimulationsList = [j, total_simulation, displacement, total_occupation]

# packSimulationsDataLine = flatten_list([SimulationsList])
# packSimulationsData.append(packSimulationsDataLine)

'''columnnames2 = ['Number of Buses', ' Total CO2 emission (kgCO2e)', 'total displacement (m)', 'total occupation']
dataset2 = pd.DataFrame(packSimulationsData, index=None, columns=columnnames2)
dataset2.to_excel("output.xlsx", index=False)'''






'''oldpack = dataset['vehid'].unique()
newpack = dataset[['vehid', 'CO2 emission']].copy()
for i in oldpack:
    total = newpack.loc[newpack['vehid'] == i, 'CO2 emission'].sum()
    vehList2 = [i, total]
    packBigDataLine = flatten_list([vehList2])
    packVehicleData.append(packBigDataLine)
columnnames2 = ['vehid', 'CO2 emission']

dataset2 = pd.DataFrame(packVehicleData, index=None, columns=columnnames2)
total_simulation2 = dataset2['CO2 emission'].sum()'''













