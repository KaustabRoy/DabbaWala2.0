from .models import CartItem

def gen_od_id():
    
    if CartItem.objects.filter(order_id__istartswith = 'DW').last() == None:
        new_oid = "DW001"
        return new_oid
    
    last_oid = last_oid = CartItem.objects.filter(order_id__istartswith = 'DW').last().order_id
    if last_oid is not None:
        init = last_oid[:2]
        sl = last_oid[2:]
        n_sl = int(sl)
        n_sl += 1
        str_sl = str(n_sl)
        z_sl = str_sl.zfill(3)
        new_oid = init+z_sl
        return new_oid
    else:
        new_id = "DW001"
        return new_id

    
    