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
                      "weapon=NA"]

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
