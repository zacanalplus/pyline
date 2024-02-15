#!/usr/bin/env python3

import datetime
from pymongo import MongoClient
from DBParameters import DBParameters 
from config import tags


dbParams = DBParameters("env.yaml")
client = MongoClient(dbParams.uri())
db = client.cities 
t = tags

def do_query(q_id, cust_id, keyword, deli_loc):
    queries = db[t["query_col"]]
    q_data = {
        t["query"]["id"] : q_id,
        t["customer_id"] : cust_id,
        t["query"]["keyword"] : keyword,
        "delivery location" : {
            "type" : "Point",
            "coordinates" : deli_loc
        },
        t["query"]["requested_at"] : datetime.datetime.now(),
        t["query"]["replied_at"] : ""
    }

    insert_ok = queries.insert_one(q_data)
    #print(insert_ok)
    if insert_ok:
        shops = db[t["shop_col"]]
#       nearby_shops =shops.aggregate([
#           {
#               "$geonear" : {
#                   "near": {
#                       "type" : "Point", 
#                       "coordinates" : deli_loc
#                   },
#                   "distanceField" : "distance",
#                   "maxDistance" : 2000,
#                   "spherical" : True
#               }
#           }
#       ])
        query = {t["query"]["keyword"]: keyword, t["shop_index"]["status"] : "active"} 
        shop_ids = db[t["shop_indices_col"]]
        ids = shop_ids.find(query)
        shpids = []
        for id in ids:
            shpids += id[t["shop_index"]["shop_list"]]
        #print(shpids)
        query = {
            t["shop"]["id"] : {
                "$in" : shpids
            },
            t["shop"]["status"] : "active",
            t["shop"]["unlisted"] : False
        }
        shops = db[t["shop_col"]]
        nearby_shops = shops.find(query)
#       for shop in nearby_shops:
#           print(shop)
        if nearby_shops:
            update_ok = queries.update_one(
                {t["query"]["id"] : q_id},
                {"$set" : {t["query"]["replied_at"] : datetime.datetime.now()}}
            )
        return nearby_shops
    
