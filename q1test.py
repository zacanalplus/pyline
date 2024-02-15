#!/usr/bin/env python3

import datetime
import query
import browse
import order
import rider
from config import tags


if __name__ == '__main__':
    t = tags
    menu = t["menu"]
    delivery_loc = [13.75, 100.56]
    id = datetime.datetime.now().microsecond
    custid = "cust000" + str(id % 5)
    queryid = "qry" + str(id + 11)
    browse_id = "brw" + str(id + 17)
    order_id = "ord" + str(id + 19)
    shop_list = query.do_query(queryid, custid, "pizza".lower(), delivery_loc)
    
    # start selecting shop by customer
    selected_shop = None
    for shop in shop_list:
        #print(shop)
        selected_shop = shop
        break
    # browse and select shop for menu
    menu_2choose = browse.browse_menu(browse_id, custid, selected_shop[t["shop"]["id"]])
    menu_selected = None 
    for menu_item in menu_2choose:
        #print(menu_item)
        menu_selected = menu_item
        
    #print menu option if available and select
    moption_selected = None
    for m_option in menu_selected[menu["option"]["id"]]:
        #print(m_option)
        moption_selected = m_option
        
    # order is confirmed by customer, broadcast to available riders
    confirmed_ordid = order.order_item(order_id, custid, menu_selected[menu["id"]], moption_selected, 1)
    #print(ord_details + " is confirmed")
    free_rider_id = ""
    riders_lst = rider.get_riders()
    for rid_info in riders_lst:
        free_rider_id = rid_info[t["rider"]["id"]]
        if(id % 4 == 0):
            break
        id += 1
        
    #order is updated, picked up, delivered
    order.update_order(confirmed_ordid, free_rider_id)
    order.update_order(confirmed_ordid, free_rider_id, False)
    order.complete_order(confirmed_ordid, delivered = True)
    print(order_id + " is completed.")