from typing import List

import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd
import xml.dom.minidom as ET
from scipy.optimize import minimize
import numpy as np


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


def danton(vehi_depart):
    packBigData = []
    packPersonsData = []
    packTimeData = []
    # Initialize total_simulation as zero
    # Access route xml file
    tree = ET.parse("osm_pt.rou.xml")

    # Get the list of vehicles in route xml file
    vehicles = tree.getElementsByTagName("vehicle")
    # print(vehicles)
    i = 0
    # For each vehicle in route xml file determine its depart
    for vehicle in vehicles:
        depart = vehi_depart[i]
        vehicle.setAttribute("depart", str(depart))
        # print(vehicle.getAttribute("depart"))
        i = i + 1
    with open("osm_pt.rou.xml", "w") as fs:
        fs.write(tree.toxml())
        fs.close()

    # Open sumo and start traci
    sumoCmd = ["sumo", "-c", "osm.sumocfg"]
    traci.start(sumoCmd)
    not_attended_people = 0
    # Run every step time until the simulation is over
    while traci.simulation.getMinExpectedNumber() > 0:

        traci.simulationStep()

        # people_at_stop = traci.busstop.getPersonIDs("P1_Salgado")
        vehicles = traci.vehicle.getIDList()

        # Get people information
        """for i in range(0, len(people_at_stop)):
            personid = people_at_stop[i]
            # Get waiting time at Salgado Bus Stop
            waiting_time = traci.person.getWaitingTime(people_at_stop[i])
            # Pack people information
            personsList = [personid, waiting_time]
            packPersonsDataLine = flatten_list([personsList])
            packPersonsData.append(packPersonsDataLine)"""
        # Get vehicles information
        for i in range(0, len(vehicles)):

            # Get different values of each vehicle at every step time
            capacity = 0
            occupation = 0
            percentage = 0

            passenger_emission_factor = 1 + round(traci.vehicle.getPersonNumber(vehicles[i]), 2) * 0.15 / 100


            vehid = vehicles[i]
            spd = round(traci.vehicle.getSpeed(vehicles[i]) * 3.6, 2)
            displacement = round(traci.vehicle.getDistance(vehicles[i]), 2)
            emissions = round(traci.vehicle.getCO2Emission(vehicles[i]), 2) * passenger_emission_factor

            # Get list of vehicles stopped at Padre Cacique Bus Stop
            bus_stopped = traci.busstop.getVehicleIDs("P3_Padre_Cacique")

            # If clause that returns vehicles occupation percentage
            if bus_stopped != ():
                # print(bus_stopped)
                occupation = round(traci.vehicle.getPersonNumber(vehicles[i]), 2)
                capacity = round(traci.vehicle.getPersonCapacity(vehicles[i]), 2)
                if capacity != 0:
                    percentage = occupation / capacity
                    # print(percentage)
                else:
                    percentage = 'nan'

            # Get vehicle depart list
            vehi_depart = traci.simulation.getDepartedIDList()
            departure_time = 0
            # Loop that get departure time of each vehicle
            for k in range(0, len(vehi_depart)):
                if vehi_depart[k] == vehid:
                    departure_time = traci.simulation.getTime()
                else:
                    departure_time = 'nan'

            # Packing of all the data for export to CSV/XLSX
            vehList = [vehid, spd, displacement, emissions, departure_time, capacity, occupation, percentage]
            packBigDataLine = flatten_list([vehList])
            packBigData.append(packBigDataLine)
            # print(traci.person.getIDCount())
            # print(traci.vehicle.getIDCount())
        if traci.vehicle.getIDCount() == 1:
            not_attended_people = traci.busstop.getPersonCount("P1_Salgado")
            # print(not_attended_people)
            # print(not_attended_people)
    traci.close()

    # Vehicles information and dataframe calculations
    """column_names = ['person id', 'waiting time (s)']
    person_dataset = pd.DataFrame(packPersonsData, index=None, columns=column_names)
    # person_dataset.to_excel("output_persons.xlsx", index=False)

    waiting_time = person_dataset.groupby('person id', as_index=False)['waiting time (s)'].max()
    waiting_time_mean = waiting_time['waiting time (s)'].mean()

    print('Average Waiting Time', waiting_time_mean, 's')"""

    # Vehicles information and dataframe calculations
    column_names2 = ['vehid', 'spd', 'displacement', 'CO2 emission', 'Time', 'Capacity', 'Occupation', 'percentage']
    dataset = pd.DataFrame(packBigData, index=None, columns=column_names2)
    # dataset.to_excel("output.xlsx", index=False)
    veh_emission = dataset.groupby('vehid', as_index=False)['CO2 emission'].sum()
    occupation_veh = dataset.groupby('vehid', as_index=False)['percentage'].max()
    for index, row in occupation_veh.iterrows():
        if row['percentage'] < 0.01:
            vehid = row['vehid']
            veh_emission.loc[veh_emission.vehid == vehid, 'CO2 emission'] = 0

    total_emission = veh_emission['CO2 emission'].sum() / 1000000

    vehicles_list = dataset['vehid'].unique()

    for vehid in vehicles_list:
        trip_time = dataset['vehid'].value_counts()[vehid]
        trip_time_list = [vehid, trip_time]
        packTimeDataLine = flatten_list([trip_time_list])
        packTimeData.append(packTimeDataLine)
    column_names3 = ['vehid', 'trip_time']
    dataset_time = pd.DataFrame(packTimeData, index=None, columns=column_names3)
    print(veh_emission)
    print(dataset_time)
    print(occupation_veh)
    print('Total emissions', total_emission, 'kgCO2')
    print(not_attended_people, 'people not attended')
    print(4 * total_emission + 5 * not_attended_people)

    return 4 * total_emission + 5 * not_attended_people


vehi_depart = np.arange(600, 19800, 400)

""" vehi_depart = np.array([98.68815403,  326.80936372,  555.28335782, 769.83629291,992.83919787, 1206.32986037,
                        1454.36451855, 1699.52819085, 1927.79386396, 2138.75071305, 2341.68200896, 2546.33949949,
                        2822.34680128, 3008.04676911, 3210.22038298, 3469.73645239, 3632.09340494, 3974.2813598,
                        4081.4865374, 4444.55357189, 4585.25325641, 4887.00920157, 5198.42275124, 5470.10764572])"""

print(danton(vehi_depart))
Farenz1 = minimize(danton, vehi_depart, method='Nelder-Mead')
print(Farenz1)
