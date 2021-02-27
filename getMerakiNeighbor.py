#!/usr/bin/env python3
import meraki
import sys
import os
import click
from rich.table import Table
from rich.console import Console

"""
Read CDP/LLDP neighbors from Meraki Dashboard

Required API KEY (generate it on Meraki dashboard).
    https://developer.cisco.com/meraki/api/#/rest/getting-started

Provide API KEY from command line or set as ENV VAR:
    export apikey=YOURMERAKIDASHBOARDAPIKEY

Updated to Meraki API v1. Install requirements running

    pip3 install -r requirements.txt
"""

def printCSV(m, deviceList, protocol: str):
    """
    print device neighbor in csv
    filters per protocol if protocol is provided
    """
    print("PROTOCOL,LOCAL,LOCAL-PORT,REMOTE,REMOTE-PORT,REMOTE-IP")
    for device in deviceList:
        serial, name = (
            device.get("serial"),
            device.get("name", device.get("serial", "MISSING")),
        )
        #printNei(m, serial, name, protocol)
        dp = m.devices.getDeviceLldpCdp(serial)
        for port in dp.get("ports", []):
            for proto in dp.get("ports").get(port):
                nei = dp.get("ports").get(port).get(proto)
                ip = nei.get("address", nei.get("managementAddress"))
                if proto == "cdp" and protocol != "lldp":
                    systemName = nei.get("deviceId", "noname")
                elif proto == "lldp" and protocol != "cdp":
                    systemName = nei.get("systemName", "noname")
                print(
                    f'{proto.upper()},{name},{nei.get("sourcePort")},{systemName.split(".")[0]},{nei.get("portId")},{ip}'
                )


def printRich(m, deviceList, protocol: str):
    """
    print device neighbor
    filters per protocol if protocol is provided
    """

    table = Table(title="MERAKI NEIGHBORS")
    table.add_column("PROTOCOL", style="yellow")
    table.add_column("LOCAL", style="yellow")
    table.add_column("LOCAL-PORT", style="yellow")
    table.add_column("REMOTE", style="yellow")
    table.add_column("REMOTE-PORT", style="yellow")
    table.add_column("REMOTE-IP", style="yellow")

    for device in deviceList:
        serial, name = (
            device.get("serial"),
            device.get("name", device.get("serial", "MISSING")),
        )

        dp = m.devices.getDeviceLldpCdp(serial)
        for port in dp.get("ports", []):
            for proto in dp.get("ports").get(port):
                nei = dp.get("ports").get(port).get(proto)
                ip = nei.get("address", nei.get("managementAddress"))
                if proto == "cdp" and protocol != "lldp":
                    systemName = nei.get("deviceId", "noname")
                elif proto == "lldp" and protocol != "cdp":
                    systemName = nei.get("systemName", "noname")
                table.add_row(proto,name,nei.get("sourcePort"),systemName.split(".")[0],nei.get("portId"),ip)
    console = Console()
    console.print(table)

def printSHELL(m, deviceList, protocol: str):
    """
    print device neighbor
    filters per protocol if protocol is provided
    """
    for device in deviceList:
        serial, name = (
            device.get("serial"),
            device.get("name", device.get("serial", "MISSING")),
        )
        #printNei(m, serial, name, protocol)
        dp = m.devices.getDeviceLldpCdp(serial)
        for port in dp.get("ports", []):
            for proto in dp.get("ports").get(port):
                nei = dp.get("ports").get(port).get(proto)
                ip = nei.get("address", nei.get("managementAddress"))
                if proto == "cdp" and protocol != "lldp":
                    systemName = nei.get("deviceId", "noname")
                elif proto == "lldp" and protocol != "cdp":
                    systemName = nei.get("systemName", "noname")
                print(
                    f'{proto.upper():4} LOCAL {name[:24]:24} SOURCE-PORT {nei.get("sourcePort"):8} REMOTE DEVICE {systemName.split(".")[0][:40]:40} REMOTE PORT {nei.get("portId"):24} REMOTE IP {ip}'
                )


def validate_apikey(ctx, apikey):
    """
    Used by click to validate Meraki Dashboard API Key
    """
    try:
        m = meraki.DashboardAPI(
            api_key=apikey, print_console=False, output_log=False, suppress_logging=True
        )
        m.organizations.getOrganizations()
        return apikey
    except:
        raise click.BadParameter("Provided API Key can't access Meraki Dashboard")


def validate_protocol(ctx, protocol: str):
    """
    Used by click to validate protocol
    """
    if protocol.upper() not in ["CDP", "LLDP", "ALL"]:
        raise click.BadParameter("Invalid protocol")
    else:
        return protocol


def validate_visualization(ctx, visualization: str):
    """
    Used by click to validate visualization
    """
    if visualization.upper() not in ["SHELL", "CSV", "RICH"]:
        raise click.BadParameter("Invalid visualization")
    else:
        return visualization


@click.command(help="""Get CDP and LLDP neighbors from Meraki Dashboard""")
@click.option(
    "-K",
    "--apikey",
    required=True,
    prompt=True,
    help="Meraki Dashboard API Key",
    callback=validate_apikey,
    default=os.environ.get("APIKEY", ""),
)
@click.option(
    "-O",
    "--orgid",
    required=False,
    prompt=False,
    help="Organization ID",
    default=os.environ.get("ORGID", ""),
)
@click.option(
    "-N",
    "--netid",
    required=False,
    prompt=False,
    help="Network ID",
    default=os.environ.get("NETID", ""),
)
@click.option(
    "-P",
    "--protocol",
    required=False,
    prompt=False,
    help="Protocol [CDP,LLDP,ALL]",
    callback=validate_protocol,
    default=os.environ.get("PROTOCOL", "ALL"),
)
@click.option(
    "-V",
    "--visualization",
    required=False,
    prompt=False,
    help="Visualization [SHELL,CSV,RICH]",
    callback=validate_visualization,
    default="RICH",
)
def getMerakiNeighbor(apikey: str, orgid: str, netid: str, protocol: str,visualization:str):

    # apikei validated by click callback
    m = meraki.DashboardAPI(
        api_key=apikey, print_console=False, output_log=False, suppress_logging=True
    )

    # if no organization ID is provided print list of organizations
    if not orgid:
        print("\nORGANIZATIONS AVAILABLE\n")
        orgs = m.organizations.getOrganizations()
        for org in orgs:
            print(f"NAME: {org.get('name'):40} ID: {org.get('id'):20}")
        sys.exit()

    if orgid:
        try:
            org = m.organizations.getOrganization(orgid)
            print(f"\nFOUND ORGANIZATION {orgid} NAME {org.get('name','NOT FOUND')}\n")
        except:
            print(f"\nERROR: ORGANIZATION {orgid} NOT FOUND\n")
            sys.exit()

        # if netid is not provided, print network list of the organization
        if not netid:
            print(
                f"\nNETWORKS AVAILABLE FOR ORGANIZATION {org.get('name')} with ID {orgid}\n"
            )
            networks = m.organizations.getOrganizationNetworks(orgid)
            if isinstance(networks[0], str):
                print(f"ERROR GETTING NETWORKS: {networks[0]}\n")
                sys.exit()
            else:
                for net in networks:
                    print(f"NETWORK: {net.get('name'):50} ID: {net.get('id'):20}")
        else:
            networks = m.organizations.getOrganizationNetworks(orgid)
            try:
                deviceList = m.networks.getNetworkDevices(netid)
            except:
                print(f"\nERROR: NETWORK {netid} NOT FOUND\n")
                sys.exit()

        if visualization.upper() == 'RICH':
            printRich(m,deviceList,protocol)
        elif visualization.upper() == 'SHELL':
            printSHELL(m,deviceList,protocol)
        elif visualization.upper() == 'CSV':
            printCSV(m,deviceList,protocol)


if __name__ == "__main__":
    getMerakiNeighbor()
