"""
Tools for creating an email sender using any API

author: Marco Gutierrez
"""

###### General Imports

from datetime import date
import pandas as pd

###### Classes

class SMSSender:
    """
    Parent class for defining SMS sender

    Notes: 
    - each child class will require:
        - payload standardizer
        - each class will require an output handler in order 
        to parse the output to this format:
        output = {"API used": self.scraper_api_name, "SMS text": None, 
                  "SMS number": None, "Status": None}
        - output handler should determine msg status (if failed or not)
    """

    def __init__(self, scraper_api_name, user, password, url):
        self.scraper_api_name = scraper_api_name
        self.user = user
        self.password = password
        self.url = url

    
    def parser_for_csv(self,csv_name):
        """
        Adapts a csv to a data frame


        Input: the name of the csv file (str)
        
        Output: data frame of the csv (str)
        """

        data_frame=pd.read_csv(csv_name)

        if data_frame.shape[1] == 1:
            list=[""]*len(data_frame)
            #list with as many empty spaces as many rows in the csv

            data_frame["Parametros"]=list
        
        data_frame=data_frame.astype(str) #transform to str
        return data_frame


    def sms_text_customizer(self, base_text, params):
        """
        Adapts text for sending custom SMS


        Input: base text message (str), parameters (str) 
        
        Output: customized sms (str)
        """

        if "," in params:
            splitted_params = params.split(",")
            return base_text.format(*splitted_params)
        else:
            return base_text.format(params)


    def sending_sms(self, payload, final_sms_text, phone_number, 
                    contentType, timeout, output_parser):
        """
        Sends a SMS to the specified number


        Input: payload standardized (dict/list of tuples), 
        text for sms (str), phone number (str), content type/format (dict), 
        timeout for connect and read (tuple), output parser (function)
        
        Output: info of sent sms (dict) 
        """

        import requests, datetime

        timestamp = datetime.datetime.now()

        try:
            req_output = requests.post(self.url,
                    data=payload,
                    headers=contentType,
                    timeout=timeout)
        
        except requests.ConnectTimeout:
            req_output = {"failure": "ConnectTimeout"}
        except requests.ReadTimeout:
            req_output = {"failure": "ReadTimeout"}
        except Exception as ex:
            req_output = {"failure": f"{ex}"}

        return output_parser(final_sms_text, phone_number, req_output, timestamp) # formatting and returning output


    def output_parser(self, final_sms_text, phone_number, request_output, timestamp):
        """
        Parses SMS request output


        Input: payload (dict/list of tuples), request output (requests.models.Response)
        
        Output: parsed output (dict)
        """

        parsed_output = {"API used": self.scraper_api_name, 
                         "SMS text": final_sms_text, 
                         "SMS number": phone_number,
                         "Timestamp": timestamp}

        if type(request_output) is dict: # for timeout failures
            parsed_output["Status"] = "Error: " + request_output["failure"]
        
        elif request_output.status_code == 200:
            parsed_output["Status"] = "Succesful"

        else:
            parsed_output["Status"] = "Error: " + str(request_output.status_code)
            
        return parsed_output


    def multiple_sms_sender(self, parsed_db, base_text, payload_standardizer, 
                            contentType, timeout, number_messages, output_parser):
    
        """
        Sends sms to a previously specified number of people


        Input: parsed db (df), base_text (str), payload_standardizer (function),
        contentType (dict) and Timeout (tuple), Number of rows to apply 
        this method (int), output parser (function)
        
        Output: df with all the info of sent SMS
        """

        aux_db = parsed_db.head(number_messages).copy() # keeping first N rows

        # preparing custom msgs
        aux_db["final_sms_text"] = aux_db.apply(lambda row: 
                                                self.sms_text_customizer(base_text,
                                                row["Parametros"]), axis=1)
        
        # preparing payload for respective API
        aux_db["payload"] = aux_db.apply(lambda row: 
                                         payload_standardizer(row["Nro"], 
                                         row["final_sms_text"]),axis=1)
        
        # storing sms information TODO: add timestamp here?
        aux_db["sms_info"] = aux_db.apply(lambda row: 
                                          self.sending_sms(row["payload"],
                                                           row["final_sms_text"],
                                                           row["Nro"],    
                                                           contentType, 
                                                           timeout, output_parser), 
                                                           axis=1)
        
        sent_sms_information = aux_db["sms_info"].apply(pd.Series)
        
        return sent_sms_information


###### Functions

def txt_as_array(txt_path):
    """
    Reads txt file as array

    Input: Txt file path (string)
    
    Output: Lines (list of strings)
    """

    with open(txt_path) as file:
        lines = file.read().splitlines() 
    
    output_list = []
    for line in lines:
        updated_line = str(line)
        output_list.append(updated_line)

    return output_list
