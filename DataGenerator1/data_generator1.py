import requests
# from flask import request
import pandas as pd
import time
import random

net = {
	#"Manager": "M1",
	#"Routing Port": 6060,
	#"WFM Port": 5000,
  #"Data Generator 1": "csa-6343-103.utdallas.edu",
	"M1": "csa-6343-93.utdallas.edu",
	"M2": "csa-6343-103.utdallas.edu",
	"M3": "10.176.67.248",
 	"M4": "10.176.67.247",
	"M5": "10.176.67.246",
	"M6": "10.176.67.245"
}

def generate_data():

    print("data generator1 generating data")
    # wf = request.json
    
    file_no = random.randint(1, 20)
    
    file_name = "./data/deceptive-opinion_{}.csv".format(file_no)
    opinions = pd.read_csv(file_name)
    opinionsDict = {}
    opinionsDict["DATA"] = opinions.to_json()
    # opinionsDict["WFID"] = wf['id']

    
    for key in net:
        # if item['image'] == 'aditichak/preprocessor-nlp':
          ip_add = net[key] 
          port = 6060
            
          router_addr = "http://{}:{}/pass_data_gen1".format(ip_add, port)
        
          print("Try to send to this address: ")
          print(router_addr)
          
          # if request.method == 'POST': 
                
          try:
             r = requests.post(router_addr, json=opinionsDict)
             print("status_code: " , r.status_code)
             if r.status_code == 200:
             # and r.text == '200 OK':
                print("sent data {} to {}".format(file_name , router_addr))
          except Exception as e:
             # print(e)
             print()
             
    return       
    
        
while True:
    generate_data()   
    time.sleep(10)
     