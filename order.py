#!/usr/bin/env python3

import datetime
from pymongo import MongoClient
from DBParameters import DBParameters 
from config import tags
import rider


dbParams = DBParameters("env.yaml")
client = MongoClient(dbParams.uri())
db = client.cities 
t = tags
order = t["order"]
menu = t["menu"]

def order_item(order_id, custid, menu_id, menu_option, count):
    order_details = ""
    
    order_data = {
        order["id"] : order_id,
        t["customer_id"] : custid,
        menu["id"] : menu_id,
        menu["option"]["id"] : menu_option,
        order["count"] : count,
        order["total"] : menu_option["rrp"] * count, 
        order["submitted"] : True,
        # order submitted 
        order["submitted_on"] : datetime.datetime.now(),
        # picked up by rider id
        order["picked_by"] : None,
        # prepare date time stamp
        order["prepared_on"] : None,
        # picked date time stamp by rider 
        order["picked_on"] : None,
        # delivered date time stamp by rider
        order["delivered_on"] : None,
        #payment is defaulted 'confirmed' even if it is COD
        order["payment"] : "confirmed"
    }
    
    order_col = db[t["order_col"]]
    order_status = order_col.insert_one(order_data)
    if(order_status):
        ord_details = order_id
    return ord_details

def update_order(order_id, rider_id, preparing = True):
    ord_col = db[t["order_col"]]
    if(preparing):
        update_ok = ord_col.update_one(
            {
                order["id"] : order_id
            }, 
            {"$set" : {order["prepared_on"] : datetime.datetime.now()}}
        )
    else:
        updated_ok = ord_col.update_one(
            {
                order["id"] : order_id
            }, 
            {"$set" : {order["picked_on"] : datetime.datetime.now()}}
        )
    if(rider_id):
        update_ok = ord_col.update_one(
            {
                order["id"] : order_id
            }, 
            {"$set" : {order["picked_by"] : rider_id}}
        )
        rider.update_rider_status(rider_id)
        

def complete_order(order_id, delivered = False):
    if(delivered):
        ord_col = db[t["order_col"]]
        order_info = ord_col.find(
            {
                order["id"] : order_id
            }
        )
        rider_id = ""
        for order_dtls in order_info:
            rider_id = order_dtls[order["picked_by"]]
        update_ok = ord_col.update_one(
            {
                order["id"] : order_id
            }, 
            {"$set" : {order["delivered_on"] : datetime.datetime.now()}}
        )
        rider.update_rider_status(rider_id, "active")