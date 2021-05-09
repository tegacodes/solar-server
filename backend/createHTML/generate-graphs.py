import gizeh as g
import math

import pandas as pd
import json
import datetime
from dateutil.relativedelta import relativedelta
# from PIL import Image
import webcolors
import csv

import requests
from json.decoder import JSONDecodeError


def read_csv():
    #filename = "../../charge-controller/data/tracerData2021-03-15.csv"
    filename = (
        "../../charge-controller/data/tracerData" + str(datetime.date.today()) + ".csv"
    )
    with open(filename, "r") as data:
        alllines = [line for line in csv.DictReader(data)]
 
    # line = alllines[-1]
    # line["PV voltage"] = float(line["PV voltage"])
    # line["PV current"] = float(line["PV current"])
    # line["PV power L"] = float(line["PV power L"])
    # line["PV power H"] = float(line["PV power H"])
    # line["battery voltage"] = float(line["battery voltage"])
    # line["battery current"] = float(line["battery current"])
    # line["battery power L"] = float(line["battery power L"])
    # line["battery power H"] = float(line["battery power H"])
    # line["load voltage"] = float(line["load voltage"])
    # line["load current"] = float(line["load current"])
    # line["load power"] = float(line["load power"])
    # line["battery percentage"] = float(line["battery percentage"])
    return alllines

def remap(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

def draw_graph(surface, data, label, w, h, y_axis_min, y_axis_max):
    # print(data[0][label])
    # # for line in data:
    # #     print(line[label])
    
    #AXIS
    x_padding_left = 50
    x_padding_right = 50
    y_padding_bottom = 50
    y_padding_top = 20

    zero_y = remap(0, y_axis_min, y_axis_max, h-y_padding_bottom, y_padding_top)

    axisy = g.polyline(points=[(0+x_padding_left, 0+y_padding_top), (0+x_padding_left, h-y_padding_bottom)], stroke_width=3, stroke=(1,0,0), fill=(0,1,0))
    axisx = g.polyline(points=[(x_padding_left, zero_y), (w-x_padding_right, zero_y)], stroke_width=3, stroke=(1,0,0), fill=(0,1,0))
    
    axisy.draw(surface)
    axisx.draw(surface)

    #DATA
    px = 0 
    py = 0
    for index, line in enumerate(data):

        #print(len(data))
        x_axis_len = w - (x_padding_left+x_padding_right)
        space = x_axis_len/(len(data)+1)
        
        #DATA POINTS
        val = float(line[label])
        #print(val)
        dy = remap(val, y_axis_min, y_axis_max, h - y_padding_bottom, y_padding_top)
        dx = x_padding_left + space + (index * space)
        circle = g.circle(r=2, xy=[dx, dy], fill=(0,0,0))

        #DRAW DATA LINE
        if(index != 0):
            fit_line = g.polyline(points=[(previous_x, previous_y), (dx, dy)], stroke_width=3, stroke=(0,0,0), fill=(0,0,0))
            fit_line.draw(surface)
        previous_x = (x_padding_left + space + (index * space))
        previous_y = dy
        circle.draw(surface)
        
        #AXIS LABELS
        # if(index%5==0):
        #     date = line["datetime"]
        #     date = date[5:-10]

        #     x_label = g.text(date, fontfamily="Georgia",  fontsize=15, fill=(0,0,0), h_align="right", xy=[-1*(zero_y+20), dx], angle=-3.1416/2)
        #     x_label.draw(surface)
        x_text1 = g.text("M I D N I G H T", fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="left", xy=[x_padding_left+5, (zero_y+10)], angle=0)
        x_text1.draw(surface)
        x_text2 = g.text("N O W", fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="right", xy=[w-(x_padding_right+5), (zero_y+10)], angle=0)
        x_text2.draw(surface)
        y_text1 = g.text(str(y_axis_min), fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="right", xy=[(x_padding_left-5), h-y_padding_bottom], angle=0)
        y_text1.draw(surface)
        y_text2 = g.text("0", fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="right", xy=[x_padding_left-5, zero_y], angle=0)
        y_text2.draw(surface)
        y_text3 = g.text(str(y_axis_max), fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="right", xy=[x_padding_left-5, y_padding_top], angle=0)
        y_text3.draw(surface)



    #AXIS TITLES
    y_text = g.text("PV Voltage", fontfamily="Georgia",  fontsize=20, fill=(0,0,0), xy=[-250, 25], angle=-3.1416/2)
    y_text.draw(surface)

    x_text = g.text("Time", fontfamily="Georgia",  fontsize=20, fill=(0,0,0), xy=[250, h-(y_padding_bottom/2)], angle=0)
    x_text.draw(surface)

    file_name = "output/"+label+"_graph.png"
    surface.write_to_png(file_name)

def draw_sun_graph(surface, data, label, w, h):
    #AXIS
    x_padding_left = 50
    x_padding_right = 50
    y_padding_bottom = 20
    y_padding_top = 20

    axisy = g.polyline(points=[(0+x_padding_left, 0+y_padding_top), (0+x_padding_left, h-y_padding_bottom)], stroke_width=3, stroke=(1,0,0), fill=(0,1,0))
    axisx = g.polyline(points=[(x_padding_left, h/2), (w-x_padding_right, h/2)], stroke_width=3, stroke=(1,0,0), fill=(0,1,0))
    
    axisy.draw(surface)
    axisx.draw(surface)

    for index, line in enumerate(data):
        #get each hour
        date = line["datetime"]
        date = date[:-7]
        t1 = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
        print(t1.hour)

        # #get average for each hour

        # #calculate spacing
        # x_axis_len = w - (x_padding_left+x_padding_right)
        # space = x_axis_len/hour

        # #print(len(data))
        # x_axis_len = w - (x_padding_left+x_padding_right)
        # space = x_axis_len/(len(data)+1)
        
        # #DATA POINTS
        # val = float(line[label])
        # print(val)
        # dy = remap(val, y_axis_min, y_axis_max, h - y_padding_bottom, y_padding_top)
        # dx = x_padding_left + space + (index * space)
        # circle = g.circle(r=2, xy=[dx, dy], fill=(0,0,0))

def main():
    w = 1500
    h = 500
  
    
    d = read_csv()

    # energyParam = "load voltage"
    # y_axis_min = 0
    # y_axis_max = 1
    surface1 = g.Surface(width=w, height=h)
    surface2 = g.Surface(width=w, height=h)
    surface3 = g.Surface(width=w, height=h)
    surface4 = g.Surface(width=100, height=h)
    draw_graph(surface1, d, "battery percentage", w, h, 0, 1)
    draw_graph(surface2, d, "PV power L", w, h, -10, 40)
    draw_graph(surface3, d, "load voltage", w, h, 0, 17.5)
    draw_sun_graph(surface4, d, "PV voltage", w, h)

if __name__ == "__main__":
    main()