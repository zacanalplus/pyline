#!/usr/bin/env python3

import datetime
from pymongo import MongoClient
from DBParameters import DBParameters 
from config import tags


dbParams = DBParameters("env.yaml")
client = MongoClient(dbParams.uri())
db = client.cities 
t = tags
rider = t["rider"]

# rider accept order and status updated
def update_rider_status(rider_id, status = "on call"):
    query = {
        rider["id"] : rider_id
    }
    rider_col = db[t["rider_col"]]
    rider_info = rider_col.find(query)
    for r_data in rider_info:
        if(r_data[rider["status"]] == "active" and status ):
            update_status = rider_col.update_one(
                {rider["id"] : rider_id},
                {"$set" : {rider["status"] : status}}
            )
            

# get free riders
def get_riders():
    query = {
        rider["status"] : "active"
    }
    rider_col = db[t["rider_col"]]
    rider_list = rider_col.find(query)
    return rider_list