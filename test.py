import xml.dom.minidom as ET
'''
tree = ET.parse("osm_pt.rou.xml")
flows = tree.getElementsByTagName("flow")

for flow in flows:
    print(flow.getAttribute("number"))
    flow.setAttribute("number", "50")
    print(flow.getAttribute("number"))

with open("osm_pt.rou.xml", "w") as fs:
    fs.write(tree.toxml())
    fs.close() '''
'''tree = ET.parse("osm_pt.rou.xml")
flows = tree.getElementsByTagName("flow")

for flow in flows:
    vehicle_flow_add = 15
    vehicle_number = int(flow.getAttribute("number")) + vehicle_flow_add
    print(flow.getAttribute("number"))
    flow.setAttribute("number", str(vehicle_number))
    print(flow.getAttribute("number"))

with open("osm_pt.rou.xml", "w") as fs:
    fs.write(tree.toxml())
    fs.close()'''

tree = ET.parse("osm_pt.rou.xml")
vehicles = tree.getElementsByTagName("vehicle")
print(vehicles)

vehicle_depart = 0
for vehicle in vehicles:

    print(vehicle.getAttribute("id"))
    vehicle.setAttribute("depart", str(vehicle_depart))
    print(vehicle.getAttribute("depart"))
    vehicle_depart = vehicle_depart + 300
with open("osm_pt.rou.xml", "w") as fs:
    fs.write(tree.toxml())
    fs.close()
'''
    total_simulation = 0
    packBigData = []
    tree = ET.parse("osm_pt.rou.xml")
    vehicles = tree.getElementsByTagName("vehicle")
    print(vehicles)
    # Change value of vehicles number
    for vehicle in vehicles:
        vehicle_number = int()
        vehicle.setAttribute("depart", 5)

    # Saves xml with new flow value
    with open("osm_pt.rou.xml", "w") as fs:
        fs.write(tree.toxml())
        fs.close()'''