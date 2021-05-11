from collections import UserList
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from glob import glob
import datetime
import requests, json 
import json
import csv
import os
import generate-graphs

def read_csv():
    # filename = "../../charge-controller/data/tracerData2021-05-01.csv"
    filename = "../../charge-controller/data/tracerData" + str(datetime.date.today()) + ".csv"
    with open(filename, "r") as data:
        alllines = [line for line in csv.DictReader(data)]

    line = alllines[-1]
    line["PV voltage"] = float(line["PV voltage"])
    line["PV current"] = float(line["PV current"])
    line["PV power L"] = float(line["PV power L"])
    line["PV power H"] = float(line["PV power H"])
    line["battery voltage"] = float(line["battery voltage"])
    line["battery current"] = float(line["battery current"])
    line["battery power L"] = float(line["battery power L"])
    line["battery power H"] = float(line["battery power H"])
    line["load voltage"] = float(line["load voltage"])
    line["load current"] = float(line["load current"])
    line["load power"] = float(line["load power"])
    line["battery percentage"] = float(line["battery percentage"])
    return line


# def render_pages(_data, _weather, _server_data):
def render_pages(_data, _weather):
    print("Battery Percentage:" + str(_data["battery percentage"]))
    pages = [
        ("index-template.html", "index.html"),
        ("about-template.html", "about.html"),
        ("design-research-template.html", "design-research.html"),
        ("resources-template.html", "resources.html"),
        ("outputs-template.html", "outputs.html"),
        ("system-data-template.html", "system-data.html"),
    ]

    for template_filename, output_filename in pages:
        template_filename = "templates/" + template_filename
        output_filename = "../../frontend/" + output_filename
        template_file = open(template_filename).read()
        print("rendering", template_filename)
        print("battery", _data["battery percentage"]*100)
        template = Environment(loader=FileSystemLoader("templates/")).from_string(
            template_file
        )

        
        time = datetime.datetime.now()
        time = time.strftime("%I:%M %p")
        # try:
        #     tz_url = "http://localhost/api/v1/chargecontroller.php?systemInfo=tz"
        #     z = requests.get(tz_url) 
        #     zone = z.text
        #     print("ZONE", z.text)
        #     zone = zone.replace('/', ' ')
        #     print("ZONE", zone)
        # except Exception as e:
        zone = "TZ n/a"
        # print("TZ na")

        # print("UTC TIME", datetime.datetime.utcnow())
        #would be nice to swap this out if the via script fails
        leadImage="images/clock.png"
        if((_data["battery percentage"]*100)>30):
            mode="High res mode"
        else:
            mode="Low res mode"
        

        # template = Template(template_file)
        rendered_html = template.render(
            time=time,
            solarVoltage=_data["PV voltage"],
            solarCurrent=_data["PV current"],
            solarPowerL=_data["PV power L"],
            solarPowerH=_data["PV power H"],
            batteryVoltage=_data["battery voltage"],
            batteryPercentage=round(_data["battery percentage"]*100, 1),
            batteryCurrent=_data["battery current"],
            loadVoltage=_data["load voltage"],
            loadCurrent=_data["load current"],
            loadPower=_data["load power"],
            weather=_weather["description"],
            temp=_weather["temp"],
            feelsLike=_weather["feels_like"],
            sunrise=_weather["sunrise"],
            sunset=_weather["sunset"],
            description=_weather["description"],
            zone=zone,
            leadImage=leadImage,
            mode=mode, 
            # servers=_server_data
        )

        # print(rendered_html)
        open(output_filename, "w").write(rendered_html)

def get_weather():
    api_key = "24df3e6ca023273cd426f67e7ac06ac9"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    lat = 40.68
    lon = -74
    # complete_url = base_url + "lon=" + lon+  "&lat=" +lat + "&appid=" + api_key 
    complete_url = "http://api.openweathermap.org/data/2.5/weather?lon=-74&lat=40.68&appid=24df3e6ca023273cd426f67e7ac06ac9"
    print(complete_url)

    response = requests.get(complete_url)
    x = response.json()  
    y = x["main"] 
    current_temperature = y["temp"] 
    current_humidiy = y["humidity"] 
    z = x["weather"] 
    weather_description = z[0]["description"] 

    sunrise=datetime.datetime.fromtimestamp(x["sys"]["sunrise"])
    sunset=datetime.datetime.fromtimestamp(x["sys"]["sunset"])
    sunrise = sunrise.strftime("%I:%M %p")
    sunset = sunset.strftime("%I:%M %p")


    print(" Temperature (in kelvin unit) = " +
                str(current_temperature) +
        "\n humidity (in percentage) = " +
                str(current_humidiy) +
        "\n description = " +
                str(weather_description)) 
   
    output = {
        "description": x["weather"][0]["description"],
        "temp": round(x["main"]["temp"]-273.15, 1),
        "feels_like": round(x["main"]["feels_like"]-273.15, 1),
        "sunrise": sunrise,
        "sunset": sunset,
    }

    return output



def active_servers(dst):
    try:
        x = requests.get("http://" + dst + "/local",timeout=5)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))


#Call API for every IP address and get charge controller data 
def get_pv_value(dst):
    try:
        x = requests.get('http://' + dst + "/api/v1/api.php?value=PV-voltage",timeout=5)
        return x.text
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))
    
def download_file(url, local_filename=None):
    #Downloads a file from a remote URL
    if local_filename is None:
        local_filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def check_images(server_data):
    # server_images_paths = glob("../../frontend/images/servers/*.jpg")
    # server_images_names = [os.path.basename(i) for i in server_images_paths]
    #server_images_names = server_images_paths.split("/")[-1]
    # ps.path.basename[image]
    for server in server_data:
        filename = server["name"]+".gif"
        filename = filename.replace(" ", "-")
        fullpath = "../../frontend/images/servers/" + filename
        filepath = "images/servers/" + filename
        #print("server:", server)
        if "ip" in server:
            myIP = 	requests.get('http://whatismyip.akamai.com/').text
            print("Server IP:", server["ip"])
            print("myIP", myIP)
            if server["ip"] == "localhost": #if it is itself

                image_path = "/local/serverprofile.gif"
                filepath = image_path
            elif os.path.exists(fullpath): #else if the image is in the folder
                print("Got image for", server["name"])
            else: #else download image using api and save it to the folder: "../../frontend/images/servers/"
                image_path = "http://" + server["ip"] + "/local/serverprofile.gif"
                try:
                    download_file(image_path, fullpath) 
                    print("image_path", image_path)
                    print("local_path", fullpath)
                except Exception as e:           
                    print(server["name"], ": Offline. Can't get image")
            server["image_path"] = filepath
        







#Run settings
local = 1

#Global variables
path = "/home/pi/solar-protocol/backend"
if local == 1:
    path = ""   
dstIP = []
serverNames = []
myIP = " "


def main():
    generate-graphs.main()
    energy_data = read_csv()
    try:
        local_weather = get_weather()
    except Exception as e:
        print(e)
        local_weather = {
            "description": "n/a",
            "temp": "n/a",
            "feels_like": "n/a",
            "sunrise": "n/a",
            "sunset": "n/a"
        }





    render_pages(energy_data, local_weather)




if __name__ == "__main__":
    main()
