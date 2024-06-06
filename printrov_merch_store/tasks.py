import frappe
from frappe.integrations.utils import make_get_request, make_post_request

BASE_URL = 'https://api.printrove.com/'

def sync_products_from_printrov():
    access_token = get_printrov_access_token
    headers = {"Authorization": f"Bearer {access_token}"}
    products_route = "/api/external/products"
    all_products = make_get_request(f"{BASE_URL}{products_route}", headers= headers)
    all_products = all_products['products']

    for products in all_products:
        doc = frappe.get_doc({
            "doctype":"Store Product",
            "printrove_id" : products['id'],
            "retail_price": products['retail_price'],
            "front_mockup": products['mockup']['front_mockup'],
            "back_mockup": products['mockup']['back_mockup']
        }).insert(ignore_permissions=True)


def get_printrov_access_token():
    print_rov_setting = frappe.get_single('Printrove Setting')
    auth_route = '/api/external/token'
    response = make_post_request(
        f"{BASE_URL}{auth_route}", 
        data= {"email":print_rov_setting.email, "password":print_rov_setting.get_psasword['password']}
    )
    return response['access_token']