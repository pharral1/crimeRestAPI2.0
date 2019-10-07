import requests
import time
import json
valid_crime_params = ["page=2",
                      "inside_outside=inside",
                      "crimedate=2019-07-09",
                      "date_range=2019-07-09,2019-07-11",
                      "date_lte=2019-07-09",
                      "date_gte=2019-07-09",
                      "year=2018",
                      "month=10",
                      "day=9",
                      "weapon=NA",
                      "location=1000%20N%20MOUNT%20ST",
                      "post=243",
                      "latitude=39.30035681",
                      "latitude_range=39.30035681,39.30045681",
                      "latitude_lte=39.30035681",
                      "latitude_gte=39.30035681",
                      "longitude=-76.64448510",
                      "longitude_range=-76.64448510,-75.64448510",
                      "longitude_lte=-76.64448510",
                      "longitude_gte=-76.64448510",
                      "district=WESTERN",
                      ]
valid_count_params = ["crimedate=2019-09-07",
                              "crimetime=23:22:33",
                              "crimecode=9S",
                              "location=2900 JEFFERSON ST",
                              "description=SHOOTING",
                              "inside_outside=inside",
                              "weapon=HANDS",
                              "post=224",
                              "district=SOUTHEAST",
                              "neighborhood=MILTON-MONTFORD",
                              "longitude=-76.57607482",
                              "latitude=39.29700864",
                              "location1=",
                              "premise=STREET",
                             ]

def test_post():
    base_url = "http://127.0.0.1:8000/crimeinstances/"

    data = {"inside_outside": ["inside", "outside"]}
    requests.post(base_url, json=json.dumps(data))

def test_all_crime_params():
    base_url = "http://127.0.0.1:8000/inputdata/?"

    for param in valid_crime_params:
        
        full_url = base_url + param

        start_time = time.time()
        resp = requests.get(full_url)
        end_time = time.time() - start_time
        print("Response returned in approximately %fs" % end_time)

        try:
            resp.raise_for_status()
        except:
            print("Bad parameter of value: %s" % param)

def test_all_count_params():
    base_url = "http://127.0.0.1:8000/count/?"

    for param in valid_count_params:
        full_url = base_url + param

        start_time = time.time()
        resp = requests.get(full_url)
        end_time = time.time() - start_time
        print("Response returned in approximately %fs" % end_time)

        print("Query %s returned count %d" % (param, resp.json()))

        try:
            resp.raise_for_status()
        except:
            print("Bad parameter of value: %s" % param)
    
            
if __name__ == "__main__":
    test_all_crime_params()
    test_all_count_params()
    #test_post()
