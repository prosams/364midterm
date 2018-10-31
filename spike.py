#this file is a general testing file

import requests
import json

url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
key = "AIzaSyCWhfoQXqSoKBkK0kjnrE3N0tSwVe10pWw"
searchstring = "gas stations lansing"

request = requests.get(url, params = {"query":searchstring, "key":key})
result = request.json()

# print(result)
for x in result["results"]:
    # print(x)
    # print("************")

    locationdict = x["geometry"]["location"]
    locstring = str(locationdict["lat"]) + "," + str(locationdict["lng"])
    lat = locationdict["lat"]
    long = locationdict["lng"]
    address = x["formatted_address"]
    name = x["name"]
    splitad = address.split(",")
    road = splitad[0]
    city = splitad[1]
    state = splitad[2].split()[0]

    print("**********")

    print(name)

    # print(locstring)

    print(lat)
    print(long)
    print(address)
    print(road)
    print(city)
    print(state)


# req = make_request_using_cache2("https://maps.googleapis.com/maps/api/place/textsearch/json?", params = {
# "query" : search_thing,
# "key" : googlekey
# })
# result = json.loads(req)
# locationdict = result["results"][0]["geometry"]["location"]
# locationstring = str(locationdict["lat"]) + "," + str(locationdict["lng"])
#
# resp = requests.get(url)
# CACHE_DICTION[unique_ident] = resp.text
# dumped_json_cache = json.dumps(CACHE_DICTION, indent = 4)
# fw = open(CACHE_FNAME,"w")
# fw.write(dumped_json_cache)
# fw.close() # Close the open file
# return CACHE_DICTION[unique_ident]
