# Bumblebee

A platform agnostic, containerized ETL pipeline which supports data transformation interchangeably between CSV, JSON, AVRO and PARQUET formats.


https://user-images.githubusercontent.com/31576619/178577480-f6c09800-791b-41bc-9156-92921dd6774a.mp4

## Key Topics
* [Architecture](#architecture)
* [Technologies and Tools](#tools-and-technologies)
* [Setup](#setup)
   * [Source and Destination](#source-bucketgithub-repo-and-output-bucket)
   * [Server Setup](#bumblebee-server)
   * [JWT Token generation](#jwt-token-generation)
   * [Initiate Conversion](#initiate-conversion)
      * [JSON Payload](#json-payload)    
* [Current Scope](#current-scope)
* [Future Scope](#future-scope)

## Architecture
Bumblebee uses a client-server architecture. The client sends a request to the server which performs data transformations and generate output files in the desired formats. 
Communication takes place using a REST API. 
![Picture 1](https://user-images.githubusercontent.com/31576619/178139965-a9eaf0e2-531c-4960-986d-e40a7c454e38.jpg)


### Server and Endpoints
Provides endpoints and listens to incoming API requests.
#### Endpoints:
* **logging**
   * POST: Initiates conversion
   * GET : Realtime status of the conversion process  
* **signup**
   * POST: Generate JWT authentication token
 
 
### Payload/Input
Bumblebee accepts a JSON payload sent along with the POST request that has information about the desired conversion types, the source and destination, and the desired transformations to be carried out.
#### JSON Payload:
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
 
 
### Parser
Transforms the JSON payload into a configuration file, which is further used to run the transformation logic. 
 
 
### Converter(Main function)
Parses the configuration file and calls resepctive functions to carry out the transformations. 


## Tools and Technologies

![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=Python&logoColor=white&color=2bbc8a) ![](https://img.shields.io/badge/Tools-Docker-informational?style=flat&logo=Docker&logoColor=white&color=2bbc8a) ![](https://img.shields.io/badge/Code-Flask-informational?style=flat&logo=Flask&logoColor=white&color=2bbc8a) ![](https://img.shields.io/badge/Tools-Postman-informational?style=flat&logo=Postman&logoColor=white&color=2bbc8a) ![](https://img.shields.io/badge/Cloud-GCP-informational?style=flat&logo=Google-cloud&logoColor=white&color=2bbc8a)


## Setup
#### Source Bucket/Github Repo and Output Bucket
* The users need to input a source bucket which contains the files they want to be converted, or the URL with the files
* An output destination is required

<img width="700" alt="Pasted Graphic 5" src="https://user-images.githubusercontent.com/31576619/178580907-a1be04c7-ac18-4967-b650-fbb19ba41440.png">


#### Bumblebee Server

Pull the Bumblebee image from DockerHub:
###### Note: Ensure `docker login` is successful

Image Name: kopalc/bumblebee
Image tag: 3.0

```
docker pull kopalc/bumblebee:3.0
```

Start the container:
```
docker run -d –privileged -p<port>:8080 kopalc/bumblebee:3.0
```
This would start the bumblebee server

#### JWT Token generation

* Token based authentication has been implemented as a security measure. The users need to generate a JWT token to establish identity.
* Hit a **POST** request to the **signup** endpoint. The token would be received as output. Use **name** and **email** as keys while generating the token.
```
http://<IP Address>:<Port>/signup
```
<img width="700" alt="Pasted Graphic 4" src="https://user-images.githubusercontent.com/31576619/178580660-46789791-1beb-4495-b715-6c1dd149ef7d.png">

#### Initiate Conversion

* Send a **POST** request to the **logging** endpoint with the JSON payload which contains various desired attributes to the URL. 
* Copy the token generated from the above **signup request** and pass it as **header** along with the POST request.
<img width="700" alt="Pasted Graphic 6" src="https://user-images.githubusercontent.com/31576619/178580761-d42d22a9-7a01-4f91-aa85-44efa5107df0.png">

<img width="700" alt="Pasted Graphic 7" src="https://user-images.githubusercontent.com/31576619/178580782-edda2c6b-cef9-4466-94f5-5287f502c1b7.png">




The files converted successfully are uploaded to the output bucket. You should see a Success message upon process completion.



<img width="700" alt="Pasted Graphic 9" src="https://user-images.githubusercontent.com/31576619/178581286-51394eff-5980-4f75-8b1e-4ec2cde3d3c8.png">


<img width="800" alt="Pasted Graphic 10" src="https://user-images.githubusercontent.com/31576619/178581315-abc04aa0-a74f-405d-b544-c30223d2d23e.png">


<img width="700" alt="Pasted Graphic 11" src="https://user-images.githubusercontent.com/31576619/178581342-6a50efe6-4f9a-4043-9ebb-9b9fbea25c5f.png">



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

















