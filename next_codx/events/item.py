import frappe

def set_supplier(doc, method=None):
    if doc.has_variants == 0:
        doc.default_supplier = frappe.db.get_value(doc.doctype, doc.variant_of, "default_supplier")
