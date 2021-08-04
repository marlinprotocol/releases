import json
import semantic_version
import sys
import time

if len(sys.argv) < 8:
    sys.exit("not enough arguments")

file_path = sys.argv[1]
v  = semantic_version.Version(sys.argv[2])
description = sys.argv[3]
runner_version = sys.argv[4]
pg_name = ["", ""]
pg_path = ["", ""]
pg_checksum = ["", ""]

pg_name[0] = sys.argv[5]
pg_path[0] = sys.argv[6]
pg_checksum[0] = sys.argv[7]

if len(sys.argv) == 11:
    pg_name[1] = sys.argv[8]
    pg_path[1] = sys.argv[9]
    pg_checksum[1] = sys.argv[10]


with open(file_path, "r") as json_file:
    data = json.load(json_file)
    if not data['data'].has_key(str(v.major)):
        data['data'][str(v.major)] = {}

    if not data['data'][str(v.major)].has_key(str(v.minor)):
        data['data'][str(v.major)][str(v.minor)] = {}

    if not data['data'][str(v.major)][str(v.minor)].has_key(str(v.patch)):
        data['data'][str(v.major)][str(v.minor)][str(v.patch)] = {}
    
    if data['data'][str(v.major)][str(v.minor)][str(v.patch)].has_key(str(v.prerelease[1])):
        sys.exit("version aready exists")
    data['data'][str(v.major)][str(v.minor)][str(v.patch)][str(v.prerelease[1])] = {}
    ts = time.gmtime(int(time.time()) + 19800) #in +5:30 
    data['data'][str(v.major)][str(v.minor)][str(v.patch)][str(v.prerelease[1])]["time"] = time.strftime("%d %b %y %H:%M +0530", ts)
    data['data'][str(v.major)][str(v.minor)][str(v.patch)][str(v.prerelease[1])]["description"] = description
    if pg_name[0] == "marlinctl":
        data['data'][str(v.major)][str(v.minor)][str(v.patch)][str(v.prerelease[1])]["bundles"] = {
            "linux-amd64": {
                "runner": "",
                "data": {
                    "executable": pg_path[0],
                    "checksum": str(pg_checksum[0]),
                    "checksum_release": str(pg_checksum[1])
                }
            }
        }
    elif pg_name[1] == "":
        data['data'][str(v.major)][str(v.minor)][str(v.patch)][str(v.prerelease[1])]["bundles"] = {
            "linux-amd64.supervisor": {
                "runner": "linux-amd64.supervisor." + runner_version,
                "data": {
                    pg_name[0]: pg_path[0],
                    (pg_name[0]+"_checksum"): str(pg_checksum[0])
                }
            }
        }
    else:
        data['data'][str(v.major)][str(v.minor)][str(v.patch)][str(v.prerelease[1])]["bundles"] = {
            "linux-amd64.supervisor": {
                "runner": "linux-amd64.supervisor." + runner_version,
                "data": {
                    pg_name[0]: pg_path[0],
                    (pg_name[0]+"_checksum"): str(pg_checksum[0]),
                    pg_name[1]: pg_path[1],
                    (pg_name[1]+"_checksum"): str(pg_checksum[1])
                }
            }
        }
    with open(file_path, "w") as fp:
        json.dump(data, fp, sort_keys=True, indent=4)
