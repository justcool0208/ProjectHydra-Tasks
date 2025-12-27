# Task 1C README

## Objective
- Setting up the required environment
- Running the components
- Understand the workflow and confirm successful execution.

## Steps
- made a small fastapi app, and exposed required endpoints according to task's problm statement
- created an exporter python file , used it expose metrics from main.py file in prometheus format 
- created docker network and confirmed communication b/w the 2 containers
- created a docker compose file 
- connected to prometheus and grafana

## Observations 
- the endpoints are accessible by the service names
- grafana dashboard works and displays data
  
## Issues faced & fixes
- faced issue during creation of docker compose yaml file and network setup
- was wondering whether to put the exporter file in a separte folder intially during step2 of the task as the dockerfile was conflicting with the existing main.py's docker file, fix was to name it as 'Dockerfile.exporte',  all other parts worked as intended.

## Output Screenshots

- exposed endpoints

<img width="1920" height="1080" alt="Screenshot from 2025-12-27 13-20-00" src="https://github.com/user-attachments/assets/11bd6051-b924-4137-bf39-0e4ce263c73c" />

- grafana dashboard
(at 2 instances)
<img width="1920" height="1080" alt="Screenshot from 2025-12-27 13-30-30" src="https://github.com/user-attachments/assets/b7ed431e-6a57-4079-94f5-4668ba2ecb24" /><img width="1920" height="1080" alt="Screenshot from 2025-12-27 13-30-39" src="https://github.com/user-attachments/assets/2604fb4e-7f72-48c7-a1e6-4fff5b22017b" />



  

  
