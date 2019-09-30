import requests

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

def main():
    base_url = "http://127.0.0.1:8000/crimeinstances/?"

    for param in valid_crime_params:
        full_url = base_url + param

        resp = requests.get(full_url)

        try:
            resp.raise_for_status()
        except:
            print("Bad parameter of value: %s" % param)

if __name__ == "__main__":
    main()
