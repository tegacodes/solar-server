'''
Reads list of destination IPs and posts own IP address to those other devices.
'''
import requests
import time
import json

#CHANGE KEY AND USE ENVIRONMENTAL VARIABLES FOR LIVE VERSION!!!
apiKey='tPmAT5Ab3j7F9'
#apiKey = os.getenv('SP_API_KEY')

headers = {
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/x-www-form-urlencoded',
}

deviceList = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";

myIP = 	requests.get('http://whatismyip.akamai.com/').text

print("MY IP: " + myIP)

myName = 'pi'

#this only works with linux
def getmac(interface):

	try:
		mac = open('/sys/class/net/'+interface+'/address').readline()
	except:
		mac = "00:00:00:00:00:00"

	return mac

def getIPList():

	ipList = []

	with open(deviceList) as f:
	  data = json.load(f)

	#print(data)

	for i in range(len(data)):
		ipList.append(data[i]['ip'])

	#print(ipList)

	return ipList

def getPocLog():

def makePosts(ipList):
	
	myString = "api_key="+apiKey+"&stamp="+str(time.time())+"&ip="+myIP+"&mac="+myMAC+"&name="+myName


	print(myString)

	for dst in ipList:
		print("DST: " + dst)
		#if statement only necessary if storing local IP... if not storing local IP, must auto Post regulary instead of checking for changes...
		#if dst != myIP: #does not work when testing only with local network
		try:
			x = requests.post('http://'+dst+'/api/v1/api.php', headers=headers,data = myString)
			print(x.text)
			#requests.raise_for_status()
		except requests.exceptions.HTTPError as errh:
		 	print("An Http Error occurred:" + repr(errh))
		except requests.exceptions.ConnectionError as errc:
			print("An Error Connecting to the API occurred:" + repr(errc))
		except requests.exceptions.Timeout as errt:
		 	print("A Timeout Error occurred:" + repr(errt))
		except requests.exceptions.RequestException as err:
		 	print("An Unknown Error occurred" + repr(err))

#wlan0 might need to be changed to eth0 if using an ethernet cable
myMAC = getmac("wlan0")
dstList = getIPList()
makePosts(dstList)

