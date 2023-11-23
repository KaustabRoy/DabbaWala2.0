# from . import views

def validate_domain(email):
    user_email = email
    split_email = user_email.split('@')

    dname = split_email[1]
    split_dname = dname.split('.')

    dname_dom = split_dname[0]
    dname_role = split_dname[1]

    if dname_dom == 'dbw' and dname_role == 'seller':
        return "seller"
    
    else:
        return "customer"