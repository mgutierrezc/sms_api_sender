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
    

    