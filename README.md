# A-Prometheus
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
It is computed the _danger level_ using different atmospheric conditions and the proximity property previously computed. 
The danger level has two uses. 
### 3. Heat Map
A heat map of the region is plotted. 
It can be easily transmitted to local authorities to complement their reasonings on how to manage safe zones and direct the local population.
### 4. Light Wave 
The danger level is transformed in a frequency for street lights. 
A light wave will be formed to direct people near or on the streets to the safest zones. 
The path is chosen through an algorithm that minimizes the total _danger level_ of the path.   

## Future implementations 
There are many ways through which we will be able to 
To compute the _danger level_ it is possible to use graph machine-learning models that take advantage of the graph database. 
The algo library from neo4j offers such models. 
