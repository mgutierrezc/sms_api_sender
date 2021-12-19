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

        payload = [
				('cmd', self.cmd),
				('domainId', self.domainId),
				('login', self.user),
				('passwd', self.password),
				# No remitente en América pero sí en España y Europa
                ('senderId', ""),
				('msg', final_sms_text)
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

        # TODO: finish parser for error msg
        if type(request_output) is dict: # for timeout failures
            parsed_output["Status"] = "Error: " + request_output["failure"]
        
        elif request_output.status == "200":
            parsed_output["Status"] = "Succesful"

        else:
            parsed_output["Status"] = "Error: " + request_output.status
            
        return parsed_output


if __name__ == "__main__":
    import os

    klo_altiria_sender = AltiriaSMSSender("Altiria", 
                         user = os.environ.get("altiria_login"),
                         password = os.environ.get("altiria_login"),
                         url = "http://www.altiria.net/api/http",
                         cmd = "sendsms",
                         domainId = "CLI_3714")
    
    # TODO: add statements for testing msg sending