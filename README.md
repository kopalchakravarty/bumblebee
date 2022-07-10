# Bumblebee
<img width="123" alt="image" src="https://user-images.githubusercontent.com/31576619/178139662-55457e42-f54e-4976-ba1e-0a1faac7a932.png">

Bumblebee is a platform agnostic, containerized ETL pipeline, by which users can transform data interchangeably between CSV, JSON, AVRO and PARQUET formats.

## Architecture

Bumblebee uses a client-server architecture. The client sends a request to the server which performs data transformations and generate output files in the desired formats. 
Communication takes place using a REST API. 

<img width="482" alt="image" src="https://user-images.githubusercontent.com/31576619/178139535-c3cf233d-fb0f-4aaa-ba96-4d1dfda16bef.png">

##### Bumblebee Server
The server provides endpoints and listens to incoming API requests. Bumblebee currently supports GET and POST requests. 
Users can check the status of the current state of the transformations by hitting a GET request. POST requests initiate the transformation.
 
##### Payload/Input
Bumblebee accepts a JSON payload that is sent along with the POST request. It has information about the desired conversion types, the source and destination, and the desired transformations to take place.
 
##### Parser
The parser transforms the JSON payload into a configuration file, which is further used to run the transformation logic. 
 
##### Convert(Main function)
Main function parses the configuration file and calls resepctive functions to carry out the transformations. 



