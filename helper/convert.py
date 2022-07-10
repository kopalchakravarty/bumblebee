import pandas as pd
from fastavro import writer, parse_schema,schema
import configparser
import json
import yaml
import pyarrow
from google.cloud import storage
import logging
import pandavro as pdx
import time

client = storage.Client()
config = configparser.ConfigParser()
FORMAT = '%(asctime)s : %(levelname)s : %(message)s'
logging.basicConfig(level=logging.INFO, filename="testingapi.log", format=FORMAT)

Logs = {
    "logs":[]
}

def parquet_to_csv():
    logging.info("Inside parquet to csv")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Setting destination failed")

    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.parquet')]:
        filename = "/bucket/"+ file
        try:
            df = pd.read_parquet(filename, engine = 'pyarrow')
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                df = df[column_list]
            filename = file.split(".")[0]+".csv"
            df.to_csv(filename,index=False)
            
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info(f"File {filename} uploaded to bucket")
            
        except Exception as e:
            logging.exception("Parquet to csv failed")

def parquet_to_json():
    logging.info("Inside parquet to json")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Setting destination failed")

    
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.parquet')]:
        filename = "/bucket/"+ file
        try:
            df = pd.read_parquet(filename, engine = 'pyarrow')
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                df = df[column_list]
            result = df.to_json()
            parsed = json.loads(result)
            filename = file.split(".")[0]+".json"
            with open(filename, 'w') as f:
                f.write(json.dumps(parsed, indent=4))
            
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info(f"File {filename} uploaded to bucket")

        except Exception as e:
            logging.exception("Parquet to Json failed")


def parquet_to_avro():
    logging.info("Inside parquet to avro")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Setting destination failed")

    
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.parquet')]:
        filename = "/bucket/"+ file
        try:
            df = pd.read_parquet(filename, engine = 'pyarrow')
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                df = df[column_list]
                
            filename = file.split(".")[0]+".avro"
            pdx.to_avro(filename,df)
            
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info(f"File {filename} uploaded to bucket")

        except Exception as e:
            logging.exception("Parquet to avro failed")

def avro_to_csv():
    logging.info("Inside avro to csv")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Setting destination failed")

    
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.avro')]:
        filename = "/bucket/"+ file
        try:
            avro_df = pdx.from_avro(filename)
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                avro_df = avro_df[column_list]
                
            filename = file.split(".")[0]+".csv"
            avro_df.to_csv(filename,index=False)
            
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info(f"File {filename} uploaded to bucket")

        except Exception as e:
            logging.exception("avro to csv failed")

def avro_to_json():
    logging.info("Inside avro to json")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Setting destination failed")

    
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.avro')]:
        filename = "/bucket/"+ file
        try:
            avro_df = pdx.from_avro(filename)
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                avro_df = avro_df[column_list]
                # Convert df to json
            result = avro_df.to_json(orient="records")
            parsed = json.loads(result)
                
            filename = file.split(".")[0]+".json"
            with open(filename, 'w') as f:
                f.write(json.dumps(parsed, indent=4) )
            
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info(f"File {filename} uploaded to bucket")

        except Exception as e:
            logging.exception("avro to json failed")


def avro_to_parquet():
    logging.info("Inside avro to parquet")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Setting destination failed")

    
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.avro')]:
        filename = "/bucket/"+ file
        try:
            avro_df = pdx.from_avro(filename)
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                avro_df = avro_df[column_list]
                
            filename = file.split(".")[0]+".parquet"
            avro_df.to_parquet(filename,index=False)
            
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info(f"File {filename} uploaded to bucket")

        except Exception as e:
            logging.exception("avro to parquet failed") 

def csv_to_json():
    logging.info("Inside csv to json")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Setting destination failed")

    
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.csv')]:
        filename = "/bucket/"+ file
        try:
            # list of colums mentioned in config.ini file. JSON parsing to get list
            # Checks if the config file has a list of colums to be processed pre-defined. If not, the entire csv file is processed
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                df = pd.read_csv(filename, usecols=column_list)
            else:
                df = pd.read_csv(filename)

            # Removing .csv extension from filename
            filename = file.split(".")[0]+".json"
            result = df.to_json(orient="records")
            parsed = json.loads(result)
            with open(filename, 'w') as jsonFile:
                jsonFile.write(json.dumps(parsed, indent=4))
            
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info(f"File {filename} uploaded to bucket")

        except Exception as e:
            logging.exception("csv to json failed")   

def json_to_csv():
    logging.info("Inside json to csv")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Setting destination failed")

    
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.json')]:
        filename = "/bucket/"+ file
        try:
            df = pd.read_json(filename, orient='records')
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                df = df[column_list]
                
            filename = file.split(".")[0]+".csv"
            df.to_csv(filename,index=False)
            
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info(f"File {filename} uploaded to bucket")

        except Exception as e:
            logging.exception("json to csv failed")

def json_to_parquet():
    logging.info("Inside json to parquet")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Setting destination failed")

    
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.json')]:
        filename = "/bucket/"+ file
        try:
            df = pd.read_json(filename, orient='records')
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                df = df[column_list]
                df.columns = df.columns.astype(str) 
            filename = file.split(".")[0]+".parquet"
            df.to_parquet(filename, index=False)
            
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info(f"File {filename} uploaded to bucket")

        except Exception as e:
            logging.exception("json to parquet failed")

def csv_to_parquet():
    
    logging.info("inside csv to parquet")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        
    except Exception as e:
        logging.exception("Read config ini failed parquet")

    
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.csv')]:
        filename =  "/bucket/"+ file
        
        try:
            # list of colums mentioned in config.ini file. JSON parsing to get list
            # Checks if the config file has a list of colums to be processed pre-defined. If not, the entire csv file is processed
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                df = pd.read_csv(filename, usecols=column_list)
            else:
                df = pd.read_csv(filename)

            # Removing .csv extension from filename
            filename = file.split(".")[0]+".parquet"

            # Converting the file
            df.to_parquet(filename)
            
            logging.info("File converted parquet")

            Logs['logs'].append(f"File {filename} converted successfully ")
            
            
            # Storing in destination bucket
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            logging.info("File uploaded parqyet")

            Logs['logs'].append(f"File {filename} uploaded to bucket")
            
            
        except Exception as e:
            logging.exception("Parqet failed")

def csv_to_avro():
    
    logging.info("Inside csv to avro")
    try:
        config.read("config.ini")
        # Setting source and destination location
        destination = client.get_bucket(config["DEFAULT"]["Upload"])
        # Loading the schema
        with open('schema.json') as json_file:
            schema = json.load(json_file)
            parsed = parse_schema(schema)
    except Exception as e:
        logging.exception("Setting destination/parsing schema failed: csv to avro")

    # Looping through list of files
    files= json.loads(config.get("FILES","files"))
    for file in [file for file in files if file.endswith('.csv')]:
        filename =  "/bucket/" + file
        
        try:
            # list of colums mentioned in config.ini file. JSON parsing to get list
            # Checks if the config file has a list of colums to be processed pre-defined. If not, the entire csv file is processed
            if config.has_section("COLUMNS"):
                column_list= json.loads(config.get("COLUMNS","columns"))
                df = pd.read_csv(filename, usecols=column_list)
            else:
                df = pd.read_csv(filename)
            # Removing .csv extension from filename
            filename = file.split(".")[0]+".avro"

            records = df.to_dict('records')
            with open(filename, 'wb') as out:
                writer(out, parsed, records)
            
            #Logs['logs'] += f"File {filename} converted successfully \n"
            Logs['logs'].append(f"File {filename} converted successfully ")
            logging.info("converted avro")
            
            # Storing in destination bucket
            blob = destination.blob(filename)    
            blob.upload_from_filename(filename)    
            
            #Logs['logs'] += f"File {filename} uploaded to bucket \n"
            Logs['logs'].append(f"File {filename} uploaded to bucket")
            logging.info("uploaded avro")
            


        except Exception as e:
            logging.exception("Avro failed")

def convertini():
     # INI conversion
    
    logging.info("Inside convertini function")
    try:
        with open('config.yml') as f:
            input_data = yaml.safe_load(f)
            config.read_dict(input_data)
        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        
        with open('config.ini', 'rt') as file:
            data = file.read().replace("'","\"")

        config_file = open('config.ini', 'w')
        config_file.write(data)
        config_file.close()
        
        logging.info("converted to ini file successfully: convertini function")
        
    except Exception as e:
        logging.exception("Failed to convert yaml to ini file: convertini function")

def convertjson():
     # JSON Conversion
    logging.info("Inside convert json function ")
    logging.info(f"started at {time.strftime('%X')}")
    try:
        with open('config.yml') as file:
            result = yaml.safe_load(file)
        json_object = json.dumps(result["SCHEMA"], indent =2)
    
        with open('schema.json','w') as file:
            file.write(json_object)
        logging.info("Converted json")
        logging.info(f"finished at {time.strftime('%X')}")
    except Exception as e:
        logging.exception("Failed to convert json: convertjson function")

def avro_schema_check():
    logging.info("Inside schema check function")
    logging.info(f"started at {time.strftime('%X')}")
    if config.has_section("SCHEMA"):
        convertjson()
        csv_to_avro()
    else:
        
        logging.info("Schema not found: schema check function")
    logging.info(f"finished at {time.strftime('%X')}")
        
        

def main():
    # INI Conversion
    
    logging.info("calling convert ini function : main")
    logging.info(f"started at {time.strftime('%X')}")
    try:
        convertini()
        logging.info(f"finished at {time.strftime('%X')}")
    except Exception as e:
        logging.exception("Failed to convert to ini : main")

    # Function Dictionary
    
    functionDict = {
    "csv_to_parquet": csv_to_parquet,
    "csv_to_avro": avro_schema_check,
    "csv_to_json": csv_to_json,
    "avro_to_parquet": avro_to_parquet,
    "avro_to_csv": avro_to_csv,
    "avro_to_json": avro_to_json,
    "parquet_to_csv": parquet_to_csv,
    "parquet_to_avro": parquet_to_avro,
    "parquet_to_json": parquet_to_json,
    "json_to_csv": json_to_csv,
    "json_to_parquet": json_to_parquet
    }
    
    # Reading config.ini and calling respective functions
    try:
        logging.info("reading config.ini file : main")
        config.read("config.ini")
        convert = json.loads(config.get("CONVERT","formats"))
        logging.info(f"Convert: {convert} : main")
        for type in convert:
           logging.info(f"Type :{type} : main function")
           logging.info(f"started at {time.strftime('%X')}")
           functionDict[type]()
           logging.info(f"finished at {time.strftime('%X')}")
    except Exception as e:
        logging.exception("Failure from main function")

