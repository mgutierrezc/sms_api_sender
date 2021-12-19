# -*- coding: utf-8 -*-

# Copyright (c) 2018, Altiria TIC SL
# All rights reserved.
# El uso de este código de ejemplo es solamente para mostrar el uso de la pasarela de envío de SMS de Altiria
# Para un uso personalizado del código, es necesario consultar la API de especificaciones técnicas, donde también podrás encontrar
# más ejemplos de programación en otros lenguajes de programación y otros protocolos (http, REST, web services)
# https://www.altiria.com/api-envio-sms/

import requests
import os

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

def altiriaSms(destinations, message, debug):
	"""
	Sends SMS using Altiria API

	Input: destinations (list of strings), message (str), debug (boolean)
	Output: None
	"""
	if debug:
		try:
			#Se crea la lista de parámetros a enviar en la petición POST
			#XX, YY y ZZ se corresponden con los valores de identificación del usuario en el sistema.
			payload = [
				('cmd', 'sendsms'),
				('domainId', 'CLI_3714'),
				('login', os.environ.get("altiria_login")),
				('passwd', os.environ.get("altiria_passwd")),
				# No es posible utilizar el remitente en América pero sí en España y Europa
                ('senderId', ""),
				('msg', message)
			]

			print(os.environ.get("altiria_login"))
			print(os.environ.get("altiria_passwd"))

			#add destinations
			for destination in destinations:
				payload.append(('dest', destination))

			#Se fija la codificacion de caracteres de la peticion POST
			contentType = {'Content-Type':'application/x-www-form-urlencoded;charset=utf-8'} 
		
			#Se fija la URL sobre la que enviar la petición POST
			url = 'http://www.altiria.net/api/http'

			#Se envía la petición y se recupera la respuesta
			r = requests.post(url,
				data=payload,
				headers=contentType,
				#Se fija el tiempo máximo de espera para conectar con el servidor (5 segundos)
				#Se fija el tiempo máximo de espera de la respuesta del servidor (60 segundos)
				timeout=(5, 60)) #timeout(timeout_connect, timeout_read)

			if debug:
				print("r: ", r)
				print("r.type ", type(r))
				print("r.status: ", r.status_code)
				if str(r.status_code) != '200': #Error en la respuesta del servidor
					print('ERROR GENERAL: '+str(r.status_code))
				else: #Se procesa la respuesta 
					print('Código de estado HTTP: '+str(r.status_code))
					print("Request value: ", r)
					print("Request text: \n", r.text)

			return r.text

		except  requests.ConnectTimeout:
			print("Tiempo de conexión agotado")
		
		except  requests.ReadTimeout:
			print("Tiempo de respuesta agotado")

		except Exception as ex:
			print("Error interno: "+str(ex))
		
#altiriaSms('346xxxxxxxx,346yyyyyyyy','Mesaje de prueba', '', True)
test_msgs = txt_as_array("D:\Accesos directos\Trabajo\GECE - LEEX\Kristian\Projects\Agua\csvs\\test.csv")
print(test_msgs)
altiriaSms(test_msgs, "gaaaa", True)
