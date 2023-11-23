from .models import CartItem, Product

def cprod_details(id_string):
    b_item = id_string.split(',')
    print(b_item)
    while('' in b_item):
        b_item.remove('')
    b_item_id = [int(x) for x in b_item]
    print(b_item_id)
    item_details = []
    total_price = 0
    for i in b_item_id:
        product = Product.objects.get(id = i)
        title, price = product.title, product.price
        item_details.append(f'{title} ₹{price}')
        total_price = total_price+int(price)
    
    return item_details, total_price