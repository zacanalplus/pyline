#!/usr/bin/env python3

tags = dict(
    customer_col = "customers",
    customer_id = "cid",
    
    rider_col = "riders",
    rider = dict(
        id = "rid",
        status = "status"
    ),
    
    shop_col = "shops",
    shop = dict(
        id = "shid",
        status = "status",
        unlisted = "unlisted"
    ),
    
    menu_col = "menu", 
    menu = dict(
        id = "menu_id",
        option = dict(
            id = "menu_option",
            size = "size",
            retail_price = "rrp"
        ),
        status = "status",
        unlisted = "unlisted"
    ),
    
    query_col = "query",
    query = dict(
        id = "qid",
        keyword = "keyword",
        requested_at = "requestedat",
        replied_at = "repliedat"
    ),
    
    order_col = "orders",
    order = dict(
        id = "order_id",
        count = "count",
        submitted = "submitted",
        submitted_on = "submittedon",
        picked_by = "picked_by",
        prepared_on = "preparedon",
        picked_on = "pickedon",
        delivered_on = "deliveredon",
        total = "total",
        payment = "payment"
    ),
    
    shop_indices_col = "shopidxs",
    shop_index = dict(
        status = "status",
        shop_list = "shlist",
        unlisted = "unlisted"
    ),
    user_browse_col = "user_browse",
    browse = dict(
        id = "brws_id",
        browse_on = "br_on"
    )
)