# Tools for generating API SMS Senders
**Author:** Marco Gutierrez

## Description
Ths package allows you to create SMS Senders using the API of your preference.

Features:
- Send massive text messages (SMS) using the API of your preference
- Allows for SMS customization (up to 2 parameters: Name and an additional one)

Limitations:
- Define a payload standardizer per API SMS Sender

Requirements:
- Python 3.x
- Review the `requirements.txt` file for further information

## User guide

### Install the package

1. Create a virtual environment using `venv`
2. Activate your virtual env.
3. Download the source code from our latest release in the folder of your project
4. Run `pip install -e .` in your project folder

### Create a SMS Sender

In the folder `senders`, you'll find two sample SMS Senders, each for the following APIs
- [Altiria](https://github.com/mgutierrezc/sms_api_sender/blob/master/senders/altiria_sms_sender.py)
- [Gamanet](https://github.com/mgutierrezc/sms_api_sender/blob/master/senders/gamanet_sms_sender.py)

The structure for creating one for another API is the same used for those samples:

1. Create a `.py` file on the senders folder
2. Define a Child class that inherits from AltiriaSMSSender
3. Define the parameters your API requires
- If your API requires some specific parameter for its initialization besides user, password and url, define 
your constructor in the following way:

```python
    def __init__(self, scraper_api_name, user, password, url, arg1, arg2, ...):
        super().__init__(scraper_api_name, user, password, url)
        self.arg1 = arg1
        self.arg2 = arg2
        ...
```
- Else, you can omit this step

4.  Define a `payload_standardizer` method. It'll prepare the payload to be sent on your request to the API.
As different APIs process payloads in different formats, defining this method is neccesary for your Sender to work

- It'll take as arguments the phone number and final sms text used for an specific sms receiver. 
- Additionally, It'll use the attributes `user`, `password` and `url`, as well as any
additional one you defined on the previous step.

### Using the Sender after it's creation

**Important:**
As you could use the class you defined as part of other script (using this script as a package of another one), 
it's heavily suggested you add this statement after defining your class

```python
if __name__ == "__main__":
```

All the statements added after it will only be executed if you run this as a script, but not if they it is used as
a package for another script.

**Instructions:**
1. Initializing the SMS sender workflow by creating an object from the class you defined

```python
    my_api_sms_sender = APISMSSender("API name", 
                         user = os.environ.get("api_user"),
                         password = os.environ.get("api_password"),
                         url = "http://www.api.com",
                         arg1 = "arg1",
                         arg2 = "arg2",
                         ...)
```

2. Read the data and parse it using the parser method from the parent class

```python
    csv_data_path = "Disk:\folder\\test_contacts.csv"
    parsed_sms_data =  my_api_sms_sender.parser_for_csv(csv_data_path)
```

The csv should have this structure:

| Nro | Parametro_1 | Parametro_2 |
|--------|-----|-----------|
|        |     |           |

3. Define your parameters for sending the msg

```python
    sms_base_text = "Hola{}, esta es una prueba BEX. Tu parámetro es{}. Si funciona, escríbele un wsp a Marco"
    contentType = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    timeout = (5, 60) # timeout(timeout_connect, timeout_read)
    number_of_messages = 2 
```

4. Send the msgs using the `multiple_sms_sender` attributes

```python
    sent_sms_info = my_api_sms_sender.multiple_sms_sender(
                                      parsed_db=parsed_sms_data,
                                      base_text=sms_base_text,
                                      payload_standardizer=my_api_sms_sender.payload_standardizer,
                                      contentType=contentType,
                                      timeout=timeout,
                                      number_messages=number_of_messages,
                                      output_parser=my_api_sms_sender.output_parser
                                      )
```

5. Store the sent text messages data on a `.xlsx` spreadsheet

```python
    sent_sms_info.to_excel("D:\Accesos directos\Trabajo\GECE - LEEX\Kristian\Projects\Agua\output_info\\test_1.xlsx",
                           engine="xlsxwriter")
```

Its structure will be the following

|   | API used | SMS text | SMS number | Status    |
|---|----------|----------|------------|-----------|
| 0 | Gamanet  |          |            | Succesful |
| 1 | Gamanet  |          |            | Error: Error name     |
