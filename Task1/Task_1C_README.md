# Task 1C README

## Objective
- setting up the required environment
-  running the components
- understand the workflow and confirm successful execution.

## Steps
- made a small fastapi app, and expose endpoints according to task's problm statement
- created an exporter python file , used it expose metrics from main.py file in prometheus format 
- created docker netwrk
and confirmed communicating b/w the 2 containers
- docker compose file was created
- connected to prometheus and grafana

## Observations 
- the endpoints are accessible by the service names
- grafana dashboard works and displays data
  
## Issues faced & fixes
- faced issue during creation of docker compose yaml file and network setup
- apart from that just a few relative path errors , was wondering whether to put the exporter file in a separte folder intially during step2 of the task as the dockerfile was conflicting with the existing main.py's docker file, all other parts worked as intended...
  
