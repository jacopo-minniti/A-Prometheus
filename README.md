# A-Prometheus
A-Prometeus is a highly efficient emergency information system based on data analysis from FIRMS, whose main objective is to direct citizens to areas with the lowest potential level of being affected by wildfires. A-Prometeus uses the street light web to communicate with residents about the danger- it uses the light signalization to direct them to the closest Safe Space, determined by an algorithm and with time enchanted by the historical data collected by A-Prometeus. The tool calculates the proximity of the nearest fire outbreak to the street light based on the distance, wind speed, and humidity. Then, it assigns a value called “danger level” to each streetlight, indicating the level of safety in a particular area. Then, the collected data is used to find the most optimized route to escape the fire. The residents are guided using a wave of lights that rapidly turn on and off to provide a sense of directionality toward the closest Safe Space. When the citizens get to a safe space, they can give information on both the Space and the escape route using a specially designed QR code- they are asked to rate the level of convenience and safety of the route and the same features of the Space, so the data can be used to improve the algorithm and assess the Spaces based on conditions not present in the algorithm. A-Prometeus can also be used as a tool for a community to report a need to find a new Safe Space in the area or learn if a particular place like a parking lot, football stadium, or other ample open space can serve this purpose. After sending the request, the destination will be checked based on data from recent wildfires and marked accordingly. The community will receive a QR code to officially add the spot to the web. Our solution provides the community with a tool that can be priceless in life-threatening situations, and it can also be used by First Responders to quickly identify the places where residents gathered- the pre-determined Safe Spaces would be consulted with emergency services to make sure those are appropriate to serve this role. We decided to tackle the problem of wildfires from the side of communities that, yearly or even monthly, get affected by fires. We also increased the accessibility of escape routes and easily understandable communication about the best course of action in case of a fire.

## Motivation
Astra Reges NASA Space Apps Challenge
Scene with street lighting
Wildfires occur in the middle of the wilderness and human environment. 
People have no internet to alert them. What do all have?
(Animation of the road with streetlights)
Intuitive and cheap solution. Lights won’t confuse you, but fasten evacuation.
Only a few microcomputers need the internet to receive fire data and navigate people - and others interconnect locally using the MESH grid, thus covering the remotest locations.

## Explanation
A-Prometeus is a system to respond to emergencies. 
When fires are detected, it uses street lights to guide citizens in potential dangers towards safe zones. 
It functions completely offline so that it can be implemented in rural areas and work when wildfires disrupt internet services.  
A-Prometeus comprises hardware, chips, a microcomputer, software, a graph database, and online functions.
### 1. Query to the FIRM and Meteo databases.
These two databases are used to obtain real-time data about fire positions, properties, and meteorological conditions. 
### 2. Proximity and danger levels are computed. 
Each node of the graph database representing a street light has the properties of latitude and longitude. 
The proximity to the fire is computed using the coordinates of the fire and of the street lights. 
It is then computed the _danger level_ using different atmospheric conditions and the proximity property previously computed. 
The danger level has two uses. 
### 3. Heat Map
A heat map of the region is plotted. 
It can be easily transmitted to local authorities to complement their reasonings on how to manage safe zones and direct the local population.
It is something for the community. Actually, you can think of the heat map as a visualization of the graph database. 
### 4. Light Wave 
The danger level is transformed in a frequency for street lights. 
A light wave is directed to people near or on the streets to the safest zones. 
The light wave effect is given simply by the lights turning on and off synchronously (again, the frequency) 
The path is chosen through an algorithm that minimizes the total _danger level_ of the path.   

## Mesh networks 
A mesh network is a type of network topology where each device (node) in the network is interconnected, 
allowing data to be passed from one node to another in a decentralized manner.
The infrastructure in our streetlights is interconnected through a mesh network. 
Each streetlight has a communication range of approximately 100 meters. 
Importantly, every individual streetlight serves as a node within this mesh network and functions as a router. 
This design enables us to create an expansive and resilient network.
The only component connected to the internet is a microcomputer. 
This microcomputer, situated in the streetlight system, is responsible for computing the danger level and updating the mesh network. 
It achieves this by leveraging cloud computing resources for its processing needs.

## Security
Our priority as a team is not only for physical security, but for cyber as well. 
Considering previous instances of apps that used mesh networks, some could question the security.
There are three points for which our integrated system remains secure:
  1. No internet connection, thus potential intruders need to access the mesh networks.
  2. No personal information. No data from users is needed for obvious reasons. Thus, no data can be stolen.
  3. Our mesh network is isolated. Even if someone accessed it, they would have no space to access other devices with more useful information.
  4. To actually work on the chip, someone should open and break the street lights (which are also positioned quite high) 

## Future implementations 
There are many ways through which we will be able to improve on the project. 
To compute the _danger level_ it is possible to use graph machine-learning models that take advantage of the graph database. 
The algo library from neo4j offers such models. 
A future improvement will be to encrypt the code to leave even less space for intruders.

# The developers behind the project.
We are Minerva University Freshmen, based in San Francisco. 
This project is the result of two days of intense work during the **Mountain View NASA Space Apps Challenge 2023**. 
From left to right: 
(Top) **Marina, Emilia, Rere**
(Bottom) **Kaan, Jacopo, Amina**

![space apps team](https://github.com/jacopo-minniti/A-Prometheus/assets/115539886/db2bda04-1f3a-49c3-b237-2a574a72bd3b)



