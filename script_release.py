import json
import semantic_version
import sys
import time


#arguments project_name, beta_file, release_file, version, description
if len(sys.argv) < 6:
    sys.exit("not enough arguments")

project_name = sys.argv[1]
beta_file_path = sys.argv[2]
release_file_path = sys.argv[3]
v  = semantic_version.Version(sys.argv[4])
description = sys.argv[5]

with open(beta_file_path, "r") as beta_file:
    data_beta = json.load(beta_file)
    d = data_beta['data'][str(v.major)][str(v.minor)][str(v.patch)][str(v.prerelease[1])]

    with open(release_file_path, "r") as release_file:
        data_release = json.load(release_file)

        if not data_release['data'].has_key(str(v.major)):
            data_release['data'][str(v.major)] = {}

        if not data_release['data'][str(v.major)].has_key(str(v.minor)):
            data_release['data'][str(v.major)][str(v.minor)] = {}

        if data_release['data'][str(v.major)][str(v.minor)].has_key(str(v.patch)):
            sys.exit("version aready exists")
        
        ts = time.gmtime()
        d["time"] =  time.strftime("%Y-%m-%d %H:%M:%S UTC", ts)
        d["description"] = description

        public_version = str(v.major) + '.' + str(v.minor) + '.' + str(v.patch)
        if project_name == "beacon":
            d["bundles"]["linux-amd64.supervisor"]["data"]["beacon"] = "http://public.artifacts.marlin.pro/projects/beacon/" + public_version \
                + "/beacon-linux-amd64"
        
        elif project_name == "relay_eth":
            d["bundles"]["linux-amd64.supervisor"]["data"]["relay"] = "http://public.artifacts.marlin.pro/projects/relay_eth/" + public_version \
                + "/relay_eth-linux-amd64"
            d["bundles"]["linux-amd64.supervisor"]["data"]["geth"] = "http://public.artifacts.marlin.pro/projects/relay_eth/" + public_version \
                + "/geth-linux-amd64"

        elif project_name == "gateway_eth":
            d["bundles"]["linux-amd64.supervisor"]["data"]["gateway"] = "http://public.artifacts.marlin.pro/projects/gateway_eth/" + public_version \
                + "/gateway_eth-linux-amd64"
        
        elif project_name == "gateway_near":
            d["bundles"]["linux-amd64.supervisor"]["data"]["gateway"] = "http://public.artifacts.marlin.pro/projects/gateway_near/" + public_version \
                + "/gateway_near-linux-amd64"

        elif project_name == "gateway_iris":
            d["bundles"]["linux-amd64.supervisor"]["data"]["bridge"] = "http://public.artifacts.marlin.pro/projects/gateway_iris/" + public_version \
                + "/bridge_iris-linux-amd64"

        elif project_name == "marlinctl":
            d["bundles"]["linux-amd64.supervisor"]["data"]["executable"] = "http://public.artifacts.marlin.pro/projects/marlinctl/" + public_version \
                + "/marlinctl-linux-amd64"

        data_release['data'][str(v.major)][str(v.minor)][str(v.patch)] = {
            "0": d
        }

    with open(release_file_path, "w") as fp:
        json.dump(data_release, fp, sort_keys=True, indent=4)
