#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 17:06:08 2021

@author: aaronlinder
"""

"""
@author: TMartin
"""

import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
import sys
import re
import pandas

import heapq
from ast import literal_eval 
# graph dependency  




city_locations ={}

city_locations = {
'albanyNY':        ('42n66',  '73w78'),
'atlanta':        ('33n76',  '84w40'),
'austin':          ('30n30',  '97w75'),
'boston':          ('42n32',  '71w09'),
'buffalo':         ('42n90',  '78w85'),
'calgary':         ('51n00', '114w00'),
'charlotte':       ('35n21',  '80w83'),
'chicago':         ('41n84',  '87w68'),
'cleveland':       ('41n48',  '81w67'),
'dallas':          ('32n80',  '96w79'),
'dayton':          ('39n76',  '84w20'),
'denver':          ('39n73', '104w97'),
'desMoines':       ('41n59',  '93w62'),
'elPaso':          ('31n79', '106w42'),
'europe':          ('48n87',  '-2w33'),
'ftWorth':         ('32n74',  '97w33'),
'houston':         ('29n76',  '95w38'),
'indianapolis':    ('39n79',  '86w15'),
'jacksonville':    ('30n32',  '81w66'),
'japan':           ('35n68', '220w23'),
'kansasCity':      ('39n08',  '94w56'),
'keyWest':         ('24n56',  '81w78'),
'lakeCity':        ('30n19',  '82w64'),
'lasVegas':        ('36n19', '115w22'),
'losAngeles':      ('34n03', '118w17'),
'medford':         ('42n33', '122w86'),
'memphis':         ('35n12',  '89w97'),
'mexico':          ('19n40',  '99w12'),
'miami':           ('25n79',  '80w22'),
'minneapolis':     ('44n96',  '93w27'),
'modesto':	       ('37n3' , '120w9'),
'montreal':        ('45n50',  '73w67'),
'newHaven':        ('41n31',  '72w92'),
'newOrleans':      ('29n97',  '90w06'),
'newYork':         ('40n70',  '73w92'),
'omaha':           ('41n26',  '96w01'),
'orlando':         ('28n53',  '81w38'),
'philadelphia':    ('40n72',  '76w12'),
'phoenix':         ('33n53', '112w08'),
'pointReyes':      ('38n07', '122w81'),
'portland':        ('45n52', '122w64'),
'provo':           ('40n24', '111w66'),
'raleigh':        ('35n82',  '78w64'),
'reno':            ('39n53', '119w82'),
'sacramento':      ('38n56', '121w47'),
'saltLakeCity':    ('40n75', '111w89'),
'sanAntonio':      ('29n45',  '98w51'),
'sanDiego':        ('32n78', '117w15'),
'sanFrancisco':    ('37n76', '122w44'),
'sanJose':         ('37n30', '121w87'),
'sanLuisObispo':   ('35n27', '120w66'),
'santaFe':         ('35n67', '105w96'),
'saultSteMarie':   ('46n49',  '84w35'),
'seattle':         ('47n63', '122w33'),
'tallahassee':     ('30n45',  '84w27'),
'tampa':           ('27n97',  '82w46'),
'toledo':          ('41n67',  '83w58'),
'toronto':         ('43n65',  '79w38'),
'tucson':          ('32n21', '110w92'),
'tulsa':           ('36n13',  '95w94'),
'uk':              ('51n30',   '0w00'),
'vancouver':       ('49n25', '123w10'),
'washington':      ('38n91',  '77w01'),
'wichita':         ('37n69',  '97w34'),
'winnipeg':        ('49n90',  '97w13')
}
city_distances ={}
# dependencies for our dijkstra's implementation



import os

           




def open_file(in_file):
    roadsList = []

    with open(infile, 'r') as words:
        for line in words:
            mystring = line
            myString = re.sub(r"[\n\t\s]*","", mystring)
            roadsList.append(myString.strip().split(','))
            
        
    return roadsList

def city_coordinates(city):
    """
    given the coordinates of the city in WWW.ASTRO.COM format
    return the coordinates in radians, negative to the south and west
    """
    if city in city_locations:
        lat1 = city_locations[city][0]
        lng1 = city_locations[city][1]
        if 'n' in lat1:
            hr, mn = lat1.split('n')
            deg = float(hr) + float(mn)/60
            lat_rad = math.radians(deg)
        elif 's' in lat1:
            hr, mn = lat1.split('s')
            deg = float(hr) + float(mn)/60
            lat_rad = -math.radians(deg)
        if 'e' in lng1:
            hr, mn = lng1.split('e')
            deg = float(hr) + float(mn)/60
            lng_rad = math.radians(deg)
        elif 'w' in lng1:
            hr, mn = lng1.split('w')
            deg = float(hr) + float(mn)/60
            lng_rad = -math.radians(deg)
    
     
    return (lat_rad, lng_rad)
def city_distance(city1, city2):
    """
    calculate the distance (air) in miles between 2 cities given their coordinates
    """
    # get coordinates in radians
    lat1, lng1 = city_coordinates(city1)
    lat2, lng2 = city_coordinates(city2)
    # circumference in miles at equator, if you want km, use km value here
    circ = 24830.0  
    a = lng1 - lng2
    if a < 0.0:
        a = -a
    if a > math.pi:
        a = 2.0 * math.pi - a
    angle = math.acos(math.sin(lat2) * math.sin(lat1) + 
        math.cos(lat2) * math.cos(lat1) * math.cos(a))
    distance = circ * angle / (2.0 * math.pi)
    return (city1, city2, distance)

def dijkstra(G,source,target, cutoff= None, weight='weight'):
     (length,path)=single_source(G, source, target=target,
                                         weight=weight)
     try:
        return path[target]
     except KeyError:
        raise nx.NetworkXNoPath("node %s not reachable from %s"%(source,target))
def single_source(G,source,target=None,cutoff=None,weight='weight'):
    
    if source==target:
        return ({source:0}, {source:[source]})
    dist = {}  # dictionary of final distances
    paths = {source:[source]}  # dictionary of paths
    seen = {source:0}
    fringe=[] # use heapq with (distance,label) tuples
    heapq.heappush(fringe,(0,source))
    while fringe:
        (d,v)=heapq.heappop(fringe)
        if v in dist:
            continue # already searched this node.
        dist[v] = d
        if v == target:
            break
        #for ignore,w,edgedata in G.edges_iter(v,data=True):
        #is about 30% slower than the following
        if G.is_multigraph():
            edata=[]
            for w,keydata in G[v].items():
                minweight=min((dd.get(weight,1)
                               for k,dd in keydata.items()))
                edata.append((w,{weight:minweight}))
        else:
            edata=iter(G[v].items())
 
        for w,edgedata in edata:
            vw_dist = dist[v] + edgedata.get(weight,1)
            if cutoff is not None:
                if vw_dist>cutoff:
                    continue
            if w in dist:
                if vw_dist < dist[w]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif w not in seen or vw_dist < seen[w]:
                seen[w] = vw_dist
                heapq.heappush(fringe,(vw_dist,w))
                paths[w] = paths[v]+[w]
    return (dist,paths) 

      

      
        


if __name__ == "__main__":
    city_distance_list = {}
    city_distance_list[0] = city_distance('albanyNY', 'montreal')
    city_distance_list[1] = city_distance('albanyNY', 'boston')
    city_distance_list[2] = city_distance('albanyNY', 'buffalo')
    city_distance_list[3] = city_distance('atlanta','memphis')
    city_distance_list[4] = city_distance('atlanta', 'tallahassee')
    city_distance_list[5] = city_distance('austin','houston')
    city_distance_list[6] = city_distance('austin','sanAntonio')
    city_distance_list[7] = city_distance('boston','newHaven')
    city_distance_list[8] = city_distance('buffalo','toronto')
    city_distance_list[9] = city_distance('buffalo','cleveland')
    city_distance_list[10] = city_distance('calgary','vancouver')
    city_distance_list[11] = city_distance('calgary','winnipeg')
    city_distance_list[12] = city_distance('charlotte','jacksonville')
    city_distance_list[13] = city_distance('charlotte', 'raleigh')
    city_distance_list[14] = city_distance('chicago', 'minneapolis')
    city_distance_list[15] = city_distance('chicago', 'toledo')
    city_distance_list[16] = city_distance('cleveland', 'philadelphia')
    city_distance_list[17] = city_distance('cleveland', 'dayton')
    city_distance_list[18] = city_distance('dallas', 'denver')
    city_distance_list[19] = city_distance('dallas','houston')
    city_distance_list[20] = city_distance('dayton','indianapolis')
    city_distance_list[21] = city_distance('denver','wichita')
    city_distance_list[22] = city_distance('denver','provo')
    city_distance_list[23]= city_distance('denver','santaFe')
    city_distance_list[24] = city_distance('desMoines','omaha')
    city_distance_list[25]= city_distance('desMoines','minneapolis')
    city_distance_list[26] = city_distance('elPaso','sanAntonio')
    city_distance_list[27] = city_distance('elPaso','tucson')
    city_distance_list[28] = city_distance('elPaso', 'santaFe')
    city_distance_list[29] = city_distance('europe','philadelphia')
    city_distance_list[30] = city_distance('ftWorth', 'tulsa')
    city_distance_list[31] = city_distance('houston','newOrleans')
    city_distance_list[32] = city_distance('indianapolis','kansasCity')
    city_distance_list[33] = city_distance('jacksonville', 'orlando')
    city_distance_list[34] = city_distance('jacksonville', 'lakeCity')
    city_distance_list[35] = city_distance('japan','pointReyes')
    city_distance_list[36] = city_distance('japan','sanLuisObispo')
    city_distance_list[37] = city_distance('kansasCity','tulsa')
    city_distance_list[38] = city_distance('kansasCity', 'wichita')
    city_distance_list[39] = city_distance('keyWest','tampa')
    city_distance_list[40] = city_distance('lakeCity', 'tampa')
    city_distance_list[41] = city_distance('lakeCity','tallahassee')
    city_distance_list[42] = city_distance('lasVegas','losAngeles')
    city_distance_list[43] = city_distance('lasVegas','saltLakeCity')
    city_distance_list[44] = city_distance('losAngeles','sanDiego')
    city_distance_list[45] = city_distance('losAngeles','sanLuisObispo')
    city_distance_list[46] = city_distance('losAngeles','modesto')
    city_distance_list[47] = city_distance('medford','portland')
    city_distance_list[48] = city_distance('medford','pointReyes')
    city_distance_list[49] = city_distance('memphis','tulsa')
    city_distance_list[50] = city_distance('miami','orlando')
    city_distance_list[51] = city_distance('minneapolis', 'winnipeg')
    city_distance_list[52] = city_distance('modesto', 'sacramento')
    city_distance_list[53] = city_distance('montreal', 'toronto')
    city_distance_list[54] = city_distance('newOrleans','tallahassee')
    city_distance_list[55] = city_distance('newYork','philadelphia')
    city_distance_list[56] = city_distance('orlando','tampa')
    city_distance_list[57] = city_distance('philadelphia', 'uk')
    city_distance_list[58] = city_distance('philadelphia','washington')
    city_distance_list[59] = city_distance('phoenix','tucson')
    city_distance_list[60] = city_distance('phoenix','sanDiego')
    city_distance_list[61] = city_distance('pointReyes','sacramento')
    city_distance_list[62] = city_distance('portland','seattle')
    city_distance_list[63] = city_distance('portland','saltLakeCity')
    city_distance_list[64] = city_distance('raleigh','washington')
    city_distance_list[65] = city_distance('reno','saltLakeCity')
    city_distance_list[66] = city_distance('reno','sacramento')
    city_distance_list[67] = city_distance('sacramento','sanFrancisco')
    city_distance_list[68] = city_distance('sanAntonio','mexico')
    city_distance_list[69] = city_distance('sanFrancisco','sanJose')
    city_distance_list[70] = city_distance('sanJose','sanLuisObispo')
    city_distance_list[71] = city_distance('saultSteMarie', 'winnipeg')
    city_distance_list[72] = city_distance('saultSteMarie','toronto')
    city_distance_list[73] = city_distance('seattle','vancouver')
    city_distance_list[74] = city_distance('wichita','omaha')
    infile= './myfile5.txt'
    a_file = open("myfile5.txt", "w")
 

    writer = csv.writer(a_file)
    for key, value in city_distance_list.items():
        writer.writerow([key, value])

    a_file.close()
    with open("myfile5.txt", 'r') as my_file:
        text = my_file.read()
        text = text.replace("(", "")
        text = text.replace(")", "")
        text = text.replace("'", "")
        text = text.replace('"','')
    # If you wish to save the updates back into a cleaned up file
    with open('myfile5.txt', 'w') as my_file:
        my_file.write(text)

    my_file.close()




    road_list = open_file(infile)
 
    
    StartCity= sys.argv[1]

    GoalCity= sys.argv[2]
    df = pandas.DataFrame(road_list, columns=['key','City1', 'City2', 'MI' ])
    df.pop('key')
   
    print(df)                           
    G = nx.from_pandas_edgelist(df,'City1', 'City2', 'MI')
    nx.draw(G, with_labels=True, arrows=True)
    plt.show()
    print("Starting Node: " + StartCity)
    print(dijkstra(G, StartCity, GoalCity, cutoff=None, weight='weight'))    
    