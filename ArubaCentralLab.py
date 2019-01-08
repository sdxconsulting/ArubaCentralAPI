import ArubaCentralAPI

# CONFIRM OR CREATE VALID USER FOR SUBSEQUENT API CALLS
user = ArubaCentralAPI.getUser()

# SAMPLE USE CASE 1 -> Client Count (Wireless + Wired)
wireless_clients = ArubaCentralAPI.genericQuery(user, "/monitoring/v1/clients/wireless")
wired_clients = ArubaCentralAPI.genericQuery(user, "/monitoring/v1/clients/wired")
print("Client Count: %s (wireless) + %s (wired)" % (wireless_clients['count'], wired_clients['count']))

# SAMPLE USE CASE 2 -> Access Points (Names + Radio Status)
ap_list = ArubaCentralAPI.genericQuery(user, "/monitoring/v1/aps")
output = "Access Points (Name|2.4G|5G):"
for ap_single in ap_list['aps']:
    output += " " + ap_single['name']
    for ap_radio in ap_single['radios']:
        output += "|" + ap_radio['status']
print(output)
