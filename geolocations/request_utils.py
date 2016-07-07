import requests
import time
import sys
import json

headers = {"User-Agent": "MyMusicalHistory/0.0.1 ( goktugercegurel@gmail.com )"}
pause_duration = 1.1
pause_exceeded = 2


def make_request(url, headers=headers):
    time.sleep(pause_duration)
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print("Failed {}".format(e))
        sys.exit(1)

    if response.status_code == 200:
        print("response ok")
        return response.json()

    # limit exceeded
    elif response.status_code == 503:
        try:
            if "exceeding the allowable rate limit" in response.json()["error"]:
                print("Limit exceeded")
                time.sleep(pause_exceeded)
        except:
            pass

        print("will try again")
        return make_request(url)

    else:
        print("failed: {}".format(response.status_code))
        return None


def save_cache_to_disk(cache, filename):
    with open(filename, "wb") as cache_file:
        cache_file.write(json.dumps(cache))
    print("saved {:,} cached items to {}".format(len(cache.keys()), filename))
