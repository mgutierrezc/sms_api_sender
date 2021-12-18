"""
Tools for creating an email sender using any API

author: Marco Gutierrez
"""

###### Classes

class SMSSender:
    """
    Parent class for defining SMS sender
    """

    def __init__(self, scraper_api_name, user, password, url):
        self.scraper_api_name = scraper_api_name
        self.user = user
        self.password = password
        self.url = url
        

    def sms_text_customizer(self, base_text, name, additional_param):
        """
        Adapts text for sending custom SMS

        Input:base text message (str), name of receiver (str), additional param (str) 
        Output: customized sms (str)
        """
        # TODO: code customizer
        pass

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

        req_output = requests.post(self.url,
				data=payload,
				headers=contentType,
				timeout=timeout)

        return output_handler(req_output) # formatting and returning output


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