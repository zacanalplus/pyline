#!/usr/bin/env python3

import datetime
from pymongo import MongoClient
from DBParameters import DBParameters 
from config import tags


dbParams = DBParameters("env.yaml")
client = MongoClient(dbParams.uri())
db = client.cities 
t = tags

def browse_menu(browse_id, cusid, shopid):
    browse_data = {
        t["browse"]["id"] : browse_id,
        t["customer_id"] : cusid,
        t["shop"]["id"] : shopid,
        t["browse"]["browse_on"] : datetime.datetime.now() 
    }
    br_col = db[t["user_browse_col"]]
    insert_ok = br_col.insert_one(browse_data)
    if(insert_ok):
        menus = db[t["menu_col"]]
        query = {
            t["shop"]["id"] : shopid,
            t["shop"]["status"] : "available",
            t["shop"]["unlisted"] : False
        }
        menu_list = menus.find(query)
        return menu_list