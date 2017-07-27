import argparse
import json
import collections
import os
import re
import requests
import pickle
import copy
import logging
import sys
import ast
import math

sixth_overlap_area = []
sixth_user_area = []
sixth_dish_area = []

def get_intersection_point(x1_1,y1_1,x2_1,y2_1,x1_2,y1_2,x2_2,y2_2):
    A1=((x1_1-x2_1)/(y1_1-y2_1))
    B1=(-A1 * y2_1) + x2_1

    A2=((x1_2-x2_2)/(y1_2-y2_2))
    B2=(-A1 * y2_2) + x2_2

    y=((B2-B1)/(A1-A2))
    x=((A1*y)+B1)

    return x,y

def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow((y2-y1),2) + math.pow((x2-x1),2))

def compute_area_triangle_heron(x1,y1,x2,y2,x3,y3):
    A = distance(x1,y1,x2,y2)
    B = distance(x2,y2,x3,y3)
    C = distance(x3,y3,x1,y1)
    S = (A + B + C)/2
    area = math.sqrt(S*(S-A)*(S-B)*(S-C))

    return area

def compute_area_triangle_using_angle(a,b,theta):
    return a * b * math.sin(math.radians(theta)) * 0.5

def compute_difference_in_area_for_sixth(x1_1,y1_1,x2_1,y2_1,x1_2,y1_2,x2_2,y2_2):
    area = 0
    if (((x1_1<=x1_2) and (y1_1 <= y1_2)) and ((x2_1 <= x2_2) and (y2_1 <= y2_2))):
        area += compute_area_triangle_heron(0,0,x1_1,y1_1,x2_1,y2_1)

    elif (((x1_2 <= x1_1) and (y1_2 <= y1_1)) and ((x2_2 <= x2_1) and (y2_2 <= y2_1))):
        area += compute_area_triangle_heron(0,0,x1_2,y1_2,x2_2,y2_2)

    else:
        x_temp, y_temp = get_intersection_point(x1_1,y1_1,x2_1,y2_1,x1_2,y1_2,x2_2,y2_2)
        if (((x1_1<x1_2) and (y1_1 < y1_2)) and ((x2_2 < x2_1) and (y2_2 < y2_1))):
            area += compute_area_triangle_heron(0,0,x1_1,y1_1,x_temp,y_temp)
            area += compute_area_triangle_heron(0,0,x_temp,y_temp,x2_2,y2_2)
    
        else:
            area += compute_area_triangle_heron(0,0,x1_2,y1_2,x_temp,y_temp)
            area += compute_area_triangle_heron(0,0,x_temp,y_temp,x2_1,y2_1)

    return area

def compute_difference_in_area(h1,h2):
    theta2=30
    theta2_radians=math.radians(theta2)
    area = 0

    for i in range(len(h1)):
        j = (i + 1)%len(h1)

        x1_1 = 0 
        y1_1 = h1[i]
        x2_1 = h1[j]*math.cos(theta2_radians)
        y2_1 = h1[j]*math.sin(theta2_radians)

        x1_2 = 0
        y1_2 = h2[i]
        x2_2 = h2[j]*math.cos(theta2_radians)
        y2_2 = h2[j]*math.sin(theta2_radians)

        sixth_overlap_area.append(compute_difference_in_area_for_sixth(x1_1,y1_1,x2_1,y2_1,x1_2,y1_2,x2_2,y2_2))
    
def get_hexagon_area(h):
    x = []
    for i in range(len(h)):
        j = (i + 1)%len(h)
        x.append(compute_area_triangle_using_angle(h[i],h[j],60))

    return x

def start(dishName, dishTaste):
    dish_score = []
    user_score = []
    dishTaste = ast.literal_eval(dishTaste)

    for i in sorted(dishTaste):
        dish_score.append(dishTaste[i])

    user_s = json.load(open("flavorProfile.json"))
    userID = open("lastedit.txt", "r").read().strip()
    user_s = user_s[userID]

    user_s_len = len(user_s)

    for j in sorted(dishTaste):
        flav_sum = 0
        for i in user_s:
            flav_sum += i[j]
        user_score.append(flav_sum / user_s_len)
    
    compute_difference_in_area(dish_score, user_score)
    sixth_user_area = get_hexagon_area(user_score)
    sixth_dish_area = get_hexagon_area(dish_score)

    x = max(sum(sixth_user_area), sum(sixth_dish_area))
    score_final = round((sum(sixth_overlap_area) / x * 100), 2)
    answer = {}
    answer["userID"] = userID
    answer["score"] = score_final
    return answer