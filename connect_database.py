import requests
import json
import copy

class ConnectDB() :
    def __init__(self) :
        self.url = "https://bookboxbook.duckdns.org/bookboxbook/"

    def check_seller(self, register_id, seller_id) :
    
        userdata = {"register_id" : register_id, "seller_id" : seller_id}
        resp = requests.post(self.url + "check-seller.php", data=userdata)
        print(resp.text)
        res_data = json.loads(resp.text)
    
        print(res_data['success'])
        print(res_data)
        return res_data
    
    def check_buyer(self, register_id, buyer_id) :
    
        userdata = {"register_id" : register_id, "buyer_id" : buyer_id}
        resp = requests.post(self.url + "check-buyer.php", data=userdata)
        res_data = json.loads(resp.text)

        print(res_data['success'])
        print(res_data)
        return res_data
    

    def update_trade_state(self, register_id, role) :
    
        userdata = {"register_id" : register_id, "role": role}
        resp = requests.post(self.url + "update-trade-state.php", data=userdata)
        print(resp.text)