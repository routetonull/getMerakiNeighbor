# getMerakiNeighbor
Get CDP/LLDP neighbors from Meraki Dashboard API.

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/routetonull/getMerakiNeighbor)

More details on [IFCONFIG.IT](https://www.ifconfig.it/hugo/2019/10/get-meraki-neighbor-with-python-and-api/)

## Requirements

Enable API access, instructions [HERE](https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API)

Install the necessary modules

	 pip3 install -r requirements.txt
  
**NOTE: I strongly advise to use [virtualenv](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) or other Virtual Environment tools.**

  ## How to
  
  Provide key from command line
  
    python3 getMerakiNeighbor.py -K 99999999999999999999999999999999999f88ec
  
  or export an env variable
  
    export apikey=MYMERAKIDASHBOARDAPIKEY

Running the script without parameters will print the list of the available organizations:

	python3 getMerakiNeighbor.py
	
	ORGANIZATIONS AVAILABLE
	
	NAME: DevNet Sandbox                            ID: 549236
	NAME: Meraki Launchpad🚀                        ID: 537758
  
  Specify an organization to print a list of all the networks of the organization
  
	python3 getMerakiNeighbor.py -O 549236
	
	NETWORKS AVAILABLE FOR ORGANIZAZION "DevNet Sandbox" with ID 549236

	NETWORK: DevNet Always On Read Only                         ID: L_646829496481099586
	NETWORK: test - mx65                                        ID: N_646829496481152899
	NETWORK: Long Island Office                                 ID: L_646829496481103488
	NETWORK: DNSMB1                                             ID: L_646829496481103758
	NETWORK: DNSMB4                                             ID: L_646829496481103761

Specify a network to get all the CDP or LLDP neighbors for that newtork:

	python3 getMerakiNeighbor.py -O 549236 -N L_646829496481099586
	CDP  LOCAL Q2QN-9J8L-SLPD           SOURCE-PORT wan0     REMOTE DEVICE main-sw                                  REMOTE PORT GigabitEthernet1/0/3     REMOTE IP 10.10.10.254
	CDP  LOCAL Q2QN-9J8L-SLPD           SOURCE-PORT port10   REMOTE DEVICE 881544dff3af                             REMOTE PORT Port 8                   REMOTE IP 10.182.255.47
	LLDP LOCAL Q2QN-9J8L-SLPD           SOURCE-PORT port10   REMOTE DEVICE Meraki MS220-8P - DevNet Always On Read  REMOTE PORT 8                        REMOTE IP 10.182.255.47
  
Apply a filter for a specific protocol, CDP:

	python3 getMerakiNeighbor.py -O 549236 -N L_646829496481099586 -P cdp
	
	CDP  LOCAL Q2QN-9J8L-SLPD           SOURCE-PORT wan0     REMOTE DEVICE main-sw                                  REMOTE PORT GigabitEthernet1/0/3     REMOTE IP 10.10.10.254
	CDP  LOCAL Q2QN-9J8L-SLPD           SOURCE-PORT port10   REMOTE DEVICE 881544dff3af                             REMOTE PORT Port 8                   REMOTE IP 10.182.255.47

or LDDP:

	python3 getMerakiNeighbor.py -O 549236 -N L_646829496481099586 -P lldp
	
	LLDP LOCAL Q2QN-9J8L-SLPD           SOURCE-PORT port10   REMOTE DEVICE Meraki MS220-8P - DevNet Always On Read  REMOTE PORT 8                        REMOTE IP 10.182.255.47

Use the **--all** flag to print all the neighbors of a specific organization

	python3 getMerakiNeighbor.py -O 549236 --all
	
	CDP  LOCAL Q2QN-9J8L-SLPD           SOURCE-PORT wan0     REMOTE DEVICE main-sw                                  REMOTE PORT GigabitEthernet1/0/3     REMOTE IP 10.10.10.254
	CDP  LOCAL Q2QN-9J8L-SLPD           SOURCE-PORT port10   REMOTE DEVICE 881544dff3af                             REMOTE PORT Port 8                   REMOTE IP 10.182.255.47
	LLDP LOCAL Q2QN-9J8L-SLPD           SOURCE-PORT port10   REMOTE DEVICE Meraki MS220-8P - DevNet Always On Read  REMOTE PORT 8                        REMOTE IP 10.182.255.47
	LLDP LOCAL Q2MD-BHHS-5FDL           SOURCE-PORT wired0   REMOTE DEVICE Meraki MS220-8P - MS220-8P-BE67          REMOTE PORT 2                        REMOTE IP 192.168.128.19

### Usefult links

[Meraki API](https://developer.cisco.com/meraki/api-v1/)

[Meraki API changelog](https://developer.cisco.com/meraki/whats-new/)

[Get a Merapi API Key](https://developer.cisco.com/meraki/meraki-platform/#step-1-add-the-meraki-api-key-to-the-postman-environment)