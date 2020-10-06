#!/usr/bin/env python3
import meraki
import argparse
import sys
import os

"""
Read CDP/LLDP neighbors from Meraki Dashboard

Required API KEY (generate it on Meraki dashboard).
    https://developer.cisco.com/meraki/api/#/rest/getting-started

Provide API KEY from command line or set as ENV VAR:
    export apikey=YOURMERAKIDASHBOARDAPIKEY

Updated to Meraki API v1. Install requirements running

    pip3 install -r requirements.txt
"""


def printNei(m, serial, name, protocol):
    """
    print device neighbor
    filters per protocol if protocol is provided
    """
    dp = m.devices.getDeviceLldpCdp(serial)
    for port in dp.get("ports", []):
        for proto in dp.get("ports").get(port):
            nei = dp.get("ports").get(port).get(proto)
            ip = nei.get("address", nei.get("managementAddress"))
            if proto == "cdp" and protocol != "lldp":
                systemName = nei.get("deviceId", "noname")
                print(
                    f'{proto.upper():4} LOCAL {name[:24]:24} SOURCE-PORT {nei.get("sourcePort"):8} REMOTE DEVICE {systemName.split(".")[0][:40]:40} REMOTE PORT {nei.get("portId"):24} REMOTE IP {ip}'
                )
            elif proto == "lldp" and protocol != "cdp":
                systemName = nei.get("systemName", "noname")
                print(
                    f'{proto.upper():4} LOCAL {name[:24]:24} SOURCE-PORT {nei.get("sourcePort"):8} REMOTE DEVICE {systemName.split(".")[0][:40]:40} REMOTE PORT {nei.get("portId"):24} REMOTE IP {ip}'
                )


def getIdName(objectId, objectList):
    """
    find object name and ID if object exists
    returns ID and NAME
    """
    l = list(filter(lambda o: o.get("name") == objectId, objectList))
    if not l:
        l = list(filter(lambda o: o.get("id") == objectId, objectList))
        if l:
            return l[0].get("id", False), l[0].get("name", False)


def main():
    # getting arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-K",
        "--apikey",
        help="Meraki dashboard API key or set env var",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-O", "--organization", help="organization ID or NAME", type=str, required=False
    )
    parser.add_argument("-N", "--network", help="network", type=str, required=False)
    parser.add_argument(
        "-P",
        "--protocol",
        help="filter protocol",
        type=str,
        choices=["cdp", "lldp"],
        default="",
        required=False,
    )
    parser.add_argument(
        "-A",
        "--all",
        help="print information for all networks in organization",
        dest="all",
        action="store_true",
        default=False,
        required=False,
    )

    args = parser.parse_args()
    org = args.organization
    protocol = args.protocol
    organization = org
    all = args.all

    # verify apikey is provided
    if args.apikey:
        apikey = args.apikey
    else:
        try:
            apikey = os.environ["apikey"]
        except:
            print(
                "\nERROR: MISSING MERAKI DASHBOARD API KEY IN ARGUMENTS AND ENV VAR\n"
            )
            sys.exit()

    # verify apikey is valid and get organizations
    try:
        m = meraki.DashboardAPI(api_key=apikey, print_console=False, output_log=False, suppress_logging=True)
        orgs = m.organizations.getOrganizations()
    except:
        print("\nERROR GETTING ORGANIZATIONS - VERIFY API KEY IS CORRECT\n")
        sys.exit()

    # if no organization is provided print list of organizations
    if not args.organization:
        print("\nORGANIZATIONS AVAILABLE\n")
        for org in orgs:
            print(f"NAME: {org.get('name'):40} ID: {org.get('id'):20}")
        sys.exit()

    if organization:
        try:
            orgId, orgNname = getIdName(
                args.organization, orgs
            )  # verify organization exists
        except:
            print(f"\nERROR: ORGANIZATION {args.organization} NOT FOUND\n")
            sys.exit()
        try:
            network = args.network
        except:
            network = False
        if orgId:
            networks = m.organizations.getOrganizationNetworks(orgId)
            if network:  # if network is provided print neighbors
                try:
                    netId, netName = getIdName(network, networks)
                except:
                    print(f"\nERROR: NETWORK {network} NOT FOUND\n")
                    sys.exit()
                if netId:  # verify network exists
                    deviceList = m.networks.getNetworkDevices(netId)
                    for device in deviceList:
                        serial, name = device.get("serial"), device.get(
                            "name", device.get("serial", "MISSING")
                        )
                        printNei(m, serial, name, protocol)
            else:  # if no network is specified print network list
                if not all:
                    print(
                        f'\nNETWORKS AVAILABLE FOR ORGANIZATION "{orgNname}" with ID {orgId}\n'
                    )
                    networks = m.organizations.getOrganizationNetworks(orgId)
                    if isinstance(networks[0], str):
                        print(f"ERROR GETTING NETWORKS: {networks[0]}\n")
                        sys.exit()
                    else:
                        for net in networks:
                            print(
                                f"NETWORK: {net.get('name'):50} ID: {net.get('id'):20}"
                            )
                else:  # if all flag is set print neigh for all networks
                    for net in networks:
                        netId = net.get("id")
                        deviceList = m.networks.getNetworkDevices(netId)
                        for device in deviceList:
                            serial, name = device.get("serial"), device.get(
                                "name", device.get("serial", "MISSING")
                            )
                            printNei(m, serial, name, protocol)


main()
