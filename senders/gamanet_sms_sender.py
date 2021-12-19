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
        Parses request output obtained from Altiria

        Input: payload (dict/list of tuples), request output (requests.models.Response)
        Output: parsed output (dict)
        """

        parsed_output = {"API used": self.scraper_api_name, 
                         "SMS text": payload["smstext"], 
                         "SMS number": payload["smsnumber"]}

        if request_output.message == "0":
            parsed_output["Status"] = "Succesful"

        else:
            parsed_output["Status"] = "Error: " + request_output.message +\
                                      ". Description: " + request_output.description
            
        return parsed_output


if __name__ == "__main__":
    import os

    klo_gamanet_sender = GamanetSMSSender("Altiria", 
                         user = os.environ.get("altiria_login"),
                         password = os.environ.get("altiria_login"),
                         url = "http://www.altiria.net/api/http",
                         cmd = "sendsms",
                         domainId = "CLI_3714")
    
    # TODO: add statements for testing msg sending