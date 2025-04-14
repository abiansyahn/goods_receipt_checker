import frappe

def after_install():
    check_purchase_receipt_exists_for_purchase_order_and_invoice()

def check_purchase_receipt_exists_for_purchase_order_and_invoice():
    """
    Check if the purchase order and purchase invoice has Purchase Receipt.
    """
    # Get all purchase orders
    purchase_orders = frappe.get_all('Purchase Order', filters={'docstatus': ["!=", 2]}, fields=['name'])
    
    for po in purchase_orders:
        pr_exist = frappe.db.exists('Purchase Receipt Item', {'purchase_order': po.name})
        if pr_exist:
            frappe.db.set_value('Purchase Order', po.name, 'custom_goods_receipt_available', 1)

            purchase_invoices = frappe.get_all('Purchase Invoice Item', filters={'purchase_order': po.name, 'docstatus': ["!=", 2]}, fields=["parent"])
            for pi in purchase_invoices:
                frappe.db.set_value('Purchase Invoice', pi.parent, 'custom_goods_receipt_available', 1)
        
    frappe.db.commit()