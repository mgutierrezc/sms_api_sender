from sms_tools.sms_sending_tools import SMSSender

class GamanetSMSSender(SMSSender):
    """
    SMS sender for Gamanet API

    Child class from SMSSender, obtained from 
    sms_tools.sms_sending_tools
    """
    
    
    def payload_standardizer(self, phone_number, final_sms_text):
        """
        Standardizes payload for request according to API format

        Input: phone number (str), final text for sms (str)
        Output: standardized payload (list of tuples)
        """

        payload = {
            "apicard": self.user,
            "apikey": self.password,
            "smsnumber": phone_number,
            "smstext": final_sms_text
        }

        return payload
    

    def output_parser(self, payload, request_output):
        """
        Parses request output

        Input: payload (dict/list of tuples), request output (requests.models.Response)
        Output: parsed output (dict)
        """

        parsed_output = {"API used": self.scraper_api_name, 
                         "SMS text": payload["smstext"], 
                         "SMS number": payload["smsnumber"]}


        if type(request_output) is dict: # for timeout failures
            parsed_output["Status"] = "Error: " + request_output["failure"]

        elif request_output.status_code == 200:
            parsed_output["Status"] = "Succesful"

        else:
            parsed_output["Status"] = "Error: " + str(request_output.status_code)
            
        return parsed_output


if __name__ == "__main__":
    import os

    klo_gamanet_sender = GamanetSMSSender("Gamanet", 
                         user = os.environ.get("gamanet_apicard"),
                         password = os.environ.get("gamanet_apikey"),
                         url = "http://api2.gamanet.pe/smssend")
    
    # 1. reading and parsing the data
    csv_data_path = "D:\Accesos directos\Trabajo\GECE - LEEX\Kristian\Projects\Agua\csvs\\test_custom.csv"
    parsed_sms_data =  klo_gamanet_sender.parser_for_csv(csv_data_path)

    # 2. sending the messages and storing their info
    sms_base_text = "Hola{}, esta es una prueba BEX con gamanet. Tu parámetro es{}. Si funciona, escríbele un wsp a Marco"
    contentType = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    timeout = (5, 60) # timeout(timeout_connect, timeout_read)
    number_of_messages = 2 

    sent_sms_info = klo_gamanet_sender.multiple_sms_sender(
                                      parsed_db=parsed_sms_data,
                                      base_text=sms_base_text,
                                      payload_standardizer=klo_gamanet_sender.payload_standardizer,
                                      contentType=contentType,
                                      timeout=timeout,
                                      number_messages=number_of_messages,
                                      output_parser=klo_gamanet_sender.output_parser
                                      )
    
    # 3. storing sms data
    sent_sms_info.to_excel("D:\Accesos directos\Trabajo\GECE - LEEX\Kristian\Projects\Agua\output_info\\test_1_gamanet.xlsx",
                           engine="xlsxwriter")