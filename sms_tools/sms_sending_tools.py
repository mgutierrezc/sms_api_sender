"""
Tools for creating an email sender using any API

author: Marco Gutierrez
"""

###### Classes
import pandas as pd

class SMSSender:
    """
    Parent class for defining SMS sender
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

            data_frame["Nombre"]=list
            data_frame["Parametro"]=list
        
        data_frame=data_frame.astype(str) #transform to str
        return data_frame

    

    def sms_text_customizer(self, base_text, name, additional_param):
        """
        Adapts text for sending custom SMS

        Input: base text message (str), name of receiver (str), additional param (str) 
        Output: customized sms (str)
        """

        if len(name)>0:
            name=" "+name
            
        if len(additional_param)>0:
            additional_param=" "+additional_param

        return base_text.format(name,additional_param)

    # each child class will require its payload to be standardized
    # each child class will require an output standardizer in order to 
    # store each sent msg and its status (if failed or not)
    # each class will require an output handler in order to parse the output to
    # this format:
    # output = {"API used": self.scraper_api_name, "SMS text": None, 
    #               "SMS number": None, "Status": None}

    def sending_sms(self, payload, contentType, timeout, output_handler):
        """
        Sends a SMS to the specified number

        Input: payload standardized (dict/list of tuples), 
        text for sms (str), content type/format (dict), timeout for connect 
        and read (tuple), error handler (function)
        Output: info of sent sms (dict) 
        """

        import requests 

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

        return output_handler(req_output) # formatting and returning output
    

    def multiple_sms_sender(self, parsed_db, base_text, payload_standardizer, 
                            contentType, Timeout, number_rows):
    
        """
        Sends sms to a previously specified number of people

        Input: parsed db (df), base_text (str), payload_standardizer (function),
        contentType (dict) and Timeout (tuple), Number of rows to apply 
        this method (int)
        Output: df with all the info of sent SMS
        """

        aux_db = parsed_db.head(number_rows) # keeping first N rows

        # preparing custom msgs
        aux_db["final_sms_text"] = aux_db.apply(lambda row: 
                                                self.sms_text_customizer(base_text,
                                                row["Nombre"], row["Parametro"]), axis=1)
        
        # preparing payload for respective API
        aux_db["payload"] = aux_db.apply(lambda row: 
                                         payload_standardizer(row["Nro"], 
                                         row["final_sms_text"]),axis=1)
        
        # storing sms information 
        aux_db["sms_info"] = aux_db.apply(lambda row: 
                                              self.sending_sms(self, row["payload"],
                                              contentType,Timeout), axis=1)
        sent_sms_information = aux_db["sms_info"].apply(pd.Series)
        
        return sent_sms_information


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
