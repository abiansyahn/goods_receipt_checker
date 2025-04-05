import frappe
from frappe import _

def update_goods_received_status(doc, method):
    purchase_order_list = []
    for item in doc.items:
        if item.purchase_order and item.purchase_order not in purchase_order_list:
            purchase_order_list.append(item.purchase_order)

    for purchase_order in purchase_order_list:
        if frappe.get_value("Purchase Order", purchase_order, "custom_goods_receipt_available") != 1:
            frappe.db.set_value("Purchase Order", purchase_order, "custom_goods_receipt_available", 1)

            purchase_invoices = frappe.get_all('Purchase Invoice Item', filters={'purchase_order': purchase_order, 'docstatus': ["!=", 2]}, fields=["parent"])
            for pi in purchase_invoices:
                if frappe.get_value("Purchase Invoice", pi.parent, "custom_goods_receipt_available") != 1:
                    frappe.db.set_value('Purchase Invoice', pi.parent, 'custom_goods_receipt_available', 1)
        
    frappe.db.commit()

def update_purchase_invoice_goods_received_status(doc, method):
    purchase_order_list = []
    for item in doc.items:
        if item.purchase_order and item.purchase_order not in purchase_order_list:
            purchase_order_list.append(item.purchase_order)

    for purchase_order in purchase_order_list:
        if doc.custom_goods_receipt_available != 1:
            if frappe.get_value("Purchase Order", purchase_order, "custom_goods_receipt_available") == 1:
                doc.custom_goods_receipt_available = 1