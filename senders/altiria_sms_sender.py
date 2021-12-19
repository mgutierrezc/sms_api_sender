from sms_tools.sms_sending_tools import SMSSender

class AltiriaSMSSender(SMSSender):
    """
    SMS sender for Altiria API

    Child class from SMSSender, obtained from 
    sms_tools.sms_sending_tools
    """
    
    def __init__(self, scraper_api_name, user, password, url, cmd, domainId):
        super().__init__(scraper_api_name, user, password, url)
        self.cmd = cmd
        self.domainId = domainId

    
    def payload_standardizer(self, phone_number, final_sms_text):
        """
        Standardizes payload for request according to API format

        Input: phone number (str), final text for sms (str)
        Output: standardized payload (list of tuples)
        """

        peruvian_phone_code = "51"

        if phone_number[:2] != peruvian_phone_code: # adding peruvian code if req
            phone_number = peruvian_phone_code + phone_number

        payload = [
				('cmd', self.cmd),
				('domainId', self.domainId),
				('login', self.user),
				('passwd', self.password),
				# No remitente en América pero sí en España y Europa
                ('senderId', ""),
				('msg', final_sms_text),
                ('dest', phone_number)
			]

        return payload
    

    def output_parser(self, payload, request_output):
        """
        Parses request output obtained from Altiria

        Input: payload (dict/list of tuples), request output (requests.models.Response)
        Output: parsed output (dict)
        """

        parsed_output = {"API used": self.scraper_api_name, 
                         "SMS text": payload[5][1], 
                         "SMS number": payload[6][1]}

        if type(request_output) is dict: # for timeout failures
            parsed_output["Status"] = "Error: " + request_output["failure"]
        
        elif request_output.status_code == 200:
            parsed_output["Status"] = "Succesful"

        else:
            parsed_output["Status"] = "Error: " + str(request_output.status_code)
            
        return parsed_output


if __name__ == "__main__":
    import os

    # initializing SMS sender workflow
    klo_altiria_sender = AltiriaSMSSender("Altiria", 
                         user = os.environ.get("altiria_login"),
                         password = os.environ.get("altiria_passwd"),
                         url = "http://www.altiria.net/api/http",
                         cmd = "sendsms",
                         domainId = "CLI_3714")
    
    # 1. reading and parsing the data
    csv_data_path = "D:\Accesos directos\Trabajo\GECE - LEEX\Kristian\Projects\Agua\csvs\\test_custom.csv"
    parsed_sms_data =  klo_altiria_sender.parser_for_csv(csv_data_path)

    # 2. sending the messages and storing their info
    sms_base_text = "Hola{}, esta es una prueba BEX. Tu parámetro es{}. Si funciona, escríbele un wsp a Marco"
    contentType = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    timeout = (5, 60) # timeout(timeout_connect, timeout_read)
    number_of_messages = 2 

    sent_sms_info = klo_altiria_sender.multiple_sms_sender(
                                      parsed_db=parsed_sms_data,
                                      base_text=sms_base_text,
                                      payload_standardizer=klo_altiria_sender.payload_standardizer,
                                      contentType=contentType,
                                      timeout=timeout,
                                      number_messages=number_of_messages,
                                      output_parser=klo_altiria_sender.output_parser
                                      )

    # 3. storing sms data
    sent_sms_info.to_excel("D:\Accesos directos\Trabajo\GECE - LEEX\Kristian\Projects\Agua\output_info\\test_1.xlsx",
                           engine="xlsxwriter")

