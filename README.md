# Bumblebee

A platform agnostic, containerized ETL pipeline which supports data transformation interchangeably between CSV, JSON, AVRO and PARQUET formats.

## Key Topics
* [Architecture](#architecture)
* [Technologies and Tools](#technologies-and-tools)
* [Setup](#setup)
   * [Source and Destination](#source-bucketgithub-repo-and-output-bucket)
   * [Server Setup](#bumblebee-server-1)
   * [JWT Token generation](#jwt-token-generation)
   * [Initiate Conversion](#initiate-conversion)
      * [JSON Payload](#json-payload)    
* [Current Scope](#current-scope)
* [Future Scope](#future-scope)

## Architecture
Bumblebee uses a client-server architecture. The client sends a request to the server which performs data transformations and generate output files in the desired formats. 
Communication takes place using a REST API. 
![Picture 1](https://user-images.githubusercontent.com/31576619/178139965-a9eaf0e2-531c-4960-986d-e40a7c454e38.jpg)


##### Server and Endpoints
The server provides endpoints and listens to incoming API requests. Bumblebee currently supports GET and POST requests. 
Users can check the status of the current state of the transformations by hitting a GET request. POST requests initiate the transformation.
###### Endpoints
* logging
   * POST: Initiates conversion
   * GET : Realtime status of the conversion process  
* signup
   * POST: Generate JWT authentication token
 
##### Payload/Input
Bumblebee accepts a JSON payload that is sent along with the POST request. It has information about the desired conversion types, the source and destination, and the desired transformations to take place.
###### JSON Payload:
```
{
    // Required 
    // Specify the Source of the files
    // Specify the output destination of the files

    "DEFAULT": {
      "source": "<source bucket/URL>",
      "upload": "<destination bucket>"
    },

    // Required
    // Add the required conversion formats 
    // Multiple conversion formats can be specified from the below list

    "CONVERT": {
      "formats": [
        "avro_to_parquet",
        "avro_to_csv",
        "avro_to_json",
        "parquet_to_csv",
        "parquet_to_avro",
        "parquet_to_json",
        "json_to_csv",
        "json_to_parquet"
      ]
    },

    // Required
    // Add the list of the files to be processed
    //These can be in .csv, .parquet, .json or .avro format

    "FILES": {
      "files": [
        "<file1>",
        "<file2>"
      ]
    },

    // Optional
    // Add the below column section in the JSON if filtering out columns is necessary
    // Add the required column names in the list

    "COLUMNS": {
      "columns":  [
      "<column1>",
      "<column2>"
        ]
    },

    // Optional
    // Add the below section in the JSON if a conversion from CSV to Avro is required
    // This section holds the schema for the Avro file

    "SCHEMA": {
    
  }
}
```
 
##### Parser
The parser transforms the JSON payload into a configuration file, which is further used to run the transformation logic. 
 
##### Converter(Main function)
Main function parses the configuration file and calls resepctive functions to carry out the transformations. 

## Technologies and Tools

![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=Python&logoColor=white&color=2bbc8a) ![](https://img.shields.io/badge/Tools-Docker-informational?style=flat&logo=Docker&logoColor=white&color=2bbc8a) ![](https://img.shields.io/badge/Code-Flask-informational?style=flat&logo=Flask&logoColor=white&color=2bbc8a) ![](https://img.shields.io/badge/Tools-Postman-informational?style=flat&logo=Postman&logoColor=white&color=2bbc8a) ![](https://img.shields.io/badge/Cloud-GCP-informational?style=flat&logo=Google-cloud&logoColor=white&color=2bbc8a)

## Setup
#### Source Bucket/Github Repo and Output Bucket
* The users need to input a source bucket which contains the files they want to be converted, or the URL with the files
* An output destination is required

#### Bumblebee Server

Pull the Bumblebee image from Docker Hub

Image Name: bumblebee/bumblebee
Image tag: 1.0

Use the below command to run the image:
```
docker run -d –privileged -p<port>:8080 
```
This would start the bumblebee server

#### JWT Token generation

* Token based authentication has been implemented as a security measure. The users need to generate a JWT token to establish identity.
* Hit a **POST** request to the **signup** endpoint. The token would be received as output. Use **name** and **email** as keys while generating the token.
```
http://<IP Address>:<Port>/signup
```
#### Initiate Conversion

* Send a **POST** request to the **logging** endpoint with the JSON payload which contains various desired attributes to the URL. 
* Copy the token generated from the above **signup request** and pass it as **header** along with the POST request.
<img width="500" alt="image" src="https://user-images.githubusercontent.com/31576619/178191157-5e3334e4-235a-44e9-a231-3f00cc091edc.png">


## Current Scope

* The present scope of this project supports transformation between CSV, Avro, Parquet and JSON formats.

* It offers customization by enabling users to input a list of the columns desired in the output and excludes the rest.

* Supported data sources: GCS bucket and GitHub Repo

* Supported destination sources: GCS bucket

## Future Scope

* **Build support for other clouds and local storage**: Bumblebee is supported on the Google Cloud Platform as of now. The plan is to extend the support to other cloud platforms, minio and local storage as well.

* **Enhanced/Increased number of user customizations**: The user would be able to specify features and the actions to be performed on the columns to get the desired data. For instance, replacing all the NULL values in a particular column with the required value.

* **Build support for more file formats**: Bumblebee currently supports interconversion between CSV, Avro, Parquet and JSON. The plan is to include other formats as well over time.

* **Redis Queue for continuous processing of large datasets**: Including Redis in the architecture would enable handling multiple requests simultaneously and processing large files, since multiple users may be using the tool at once.



https://user-images.githubusercontent.com/31576619/178577480-f6c09800-791b-41bc-9156-92921dd6774a.mp4

















