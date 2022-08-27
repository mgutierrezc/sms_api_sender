from sms_tools.sms_sending_tools import SMSSender

class GamanetSMSSender(SMSSender):
    """
    SMS sender for Gamanet API

    Child class from SMSSender, obtained from 
    sms_tools.sms_sending_tools
    """
    
    def __init__(self, scraper_api_name, user, password, url, voice = False):
        super().__init__(scraper_api_name, user, password, url)
        self.voice = voice
    
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

        if self.voice is True:
            payload = {
                "apicard": self.user,
                "apikey": self.password,
                "number": phone_number,
                "text": final_sms_text,
                "voz": "paulina",
                "shorturl": "1"
                }

        else:
            payload = {
                "apicard": self.user,
                "apikey": self.password,
                "smsnumber": phone_number,
                "smstext": final_sms_text,
                "shorturl": "1"
            }
        return payload
    

if __name__ == "__main__":
    import os

    klo_gamanet_sender = GamanetSMSSender("Gamanet", 
                         user = os.environ.get("gamanet_apicard"),
                         password = os.environ.get("gamanet_apikey"),
                         url = "http://api2.gamanet.pe/smssend", # for sms
                         # url = "http://api10.gamanet.pe/sendtts",
                         # voice = False
                         )
    
    # 1. reading and parsing the data
    # csv_data_path = "D:\Accesos directos\Trabajo\GECE - LEEX\Kristian\Projects\Agua\csvs\\test_custom.csv"
    file_name = r"\prueba"
    input_extension = ".csv"
    csv_data_path = r"D:\Accesos directos\Trabajo\GECE - LEEX\Kristian\Projects\Agua\csvs\final data\Test audio" + file_name + input_extension
    parsed_sms_data =  klo_gamanet_sender.parser_for_csv(csv_data_path)

    # 2. sending the messages and storing their info
    sms_base_text = "Hola {}. No arrojes tus desechos al alcantarillado."
    contentType = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    timeout = (5, 60) # timeout(timeout_connect, timeout_read)
    number_of_messages = 3

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
    output_extension = ".xlsx"
    sent_sms_info.to_excel(r"D:\Accesos directos\Trabajo\GECE - LEEX\Kristian\Projects\Agua\output_info\Summary reports\Primer envío 25-08-22 17_00" + file_name + output_extension,
                           engine="xlsxwriter")