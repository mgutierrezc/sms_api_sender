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

            data_frame['Nombre']=list
            data_frame['Parametro']=list
        
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

    # each class will require its payload to be standardized
    # each class will require an output standardizer in order to 
    # store each sent msg and its status (if failed or not)

    def sending_sms(self, payload, contentType, timeout):
        """
        Sends a SMS to the specified number

        Input: payload standardized for specific API (dict/list of tuples), 
        text for sms (str), content type/format (dict), timeout for connect 
        and read (tuple)
        Output: info of sent sms (dict) 
        """
    
        output = {"API used": self.scraper_api_name, "SMS text": None, 
                  "SMS number": None, "Status": None}
        return output


###### General Functions
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

# TODO: parser that reads csv and generates df from it with everything as string
# TODO: massive sender (input: parsed db, payload standardizer, returns df with output structure, sends sms to everyone
# and , sends to each person)