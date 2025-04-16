# Carbonitor

Carbon + Monitor -> Carbonitor

Carbonitor is a tool for architects to gain awareness of the environmental impact of their design.

Currently in WIP

## carbonitor V2
Carbonitor v2 is a self-hosted web application paired with Revit and Rhino plugins. 

Carbonitor is built on:

    - [lcax](https://github.com/ocni-dtu/lcax) as a standard for Environmental Product Declarations, Assemblies, and LCA.
    
    - [speckle](https://github.com/specklesystems) as a vendor-neutral, transaction-based framework for hosting geometric data
    
    - rhino and revit API for plugin integration (Revit 2025, Rhino 8).
    
    - [ETO](https://github.com/picoe/Eto) as framework for revit and rhino plugin interface

This repository contains the main app which can be deployed as an indipendent app using Docker. 

## planned features of carbonitor

### manage a list of products
products can be tagged, commented and categorized for ease of use 

### compare products
quickly visualize and compare properties out of your current product selection

### bundle products into buildups 
buildups can be composite materials like reinforced concrete, or complex assemblies like fassade systems.

buildups can be created from Rhino or Revit models using the Carbonitor plugins, or using the webapp. 

### compare buildups
get insights on the different buildups and their environmental impact. 
add classification to buildups to create in-class benchmarks.

### rhino and revit model mapping using queries
queries are defined in the applications using the rhino and revit plugin. A query binds all matching elements with a single product or buildup. 

### get instant feedback of a building´s enviromnetal impact
swap buildups to instantly see the change in the building´s calculation

### different visualisation modes
colorize elements by buildup, by total environmental impact, by enviromental impact relative contribution, by benchmark.  

### save calculation results as snapshot
calculation results are saved in the app database and a snapshot of the model is saved to Speckle. 

### compare and tweak results
visualize and compare snapshots, change mapped buildups on existing snapshot to create new scenarios within the webapp

## how to install

### Docker Quickstart
docker run -d -p 5000:5000 --name carbonitor-v2 --restart always ghcr.io/henn-dt/carbonitor-v2/carbonitor:latest

the app will run on localhost:5000, and generate its own databases. 

### Integration in own production environment
integrate with your own reverse proxy by building the app image using ghcr.io/henn-dt/carbonitor-v2/carbonitor:latest in docker-compose or kubernetes. 
example setup (port setup will change based on your own nginx.conf file and network setup):

        ```bash
         services:
            webapp:
              image: ghcr.io/henn-dt/carbonitor-v2/carbonitor:latest
              container_name: carbonitor-webapp  #change to the name of the app
              env_file: .env.prod     #create this file on the machine used for production
              restart: always
              expose:
                - "5999"
              ports: ["5999:5000"]
            nginx:
              container_name : carbonitor-ngnix  #change to the name of the app and add ngnix
              restart: always
              build: ./nginx
              expose:
                - "8999"
              ports:
              # right port is docker port
              # change left port in production
                - "8999:8999"  
        ```
## what´s next

integration of external databases

## license

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

## to run tests
from project root, 
python run_tests.py

be sure to name test as test_*.py