import requests
import json

header = {'api-token' : 'alphanumericvomit', #add your own api token
           'accept' : 'application/json'}
base_url = "https://yourinstance.iriusrisk.com" #add your own instance

"""
The prod_name_grab() function calls a REST endpoint that provides an output of all products in IriusRisk
It returns a list of all product names.
"""
def prod_name_grab():
    product_endpoint = "/api/v1/products"
    response = requests.get(url=base_url + product_endpoint, headers=header)
    response_list = json.loads(response.text)
    prod_name = []

    for i in response_list:
        prod_name.append(i['ref'])

    return prod_name

"""
The run_update() function takes a list of IriusRisk product names and iterates through the list
in order to call the specific product endpoint. In the event that the product is not synced (is a draft)
it calls the /sync endpoint of that specific product to run the rules engine against the model.
"""
def run_update(plist):
    for i in plist:
        prod_id_endpoint = "/api/v1/products/" + i
        draft_response = requests.get(url=base_url + prod_id_endpoint, headers=header)
        draft_response_list = json.loads(draft_response.text)

        if draft_response_list['diagram']['draft'] == True:
            print(i +" is out of sync.\nSyncing " + i)
            requests.put(url=base_url + prod_id_endpoint + '/sync', headers=header)

def main():
    prod_list = prod_name_grab()
    run_update(prod_list)

if __name__ == "__main__":
    main()