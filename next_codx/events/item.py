import frappe

def after_insert(doc, method=None):
    attributes = frappe.get_all('Item Variant Attribute', filters={'parent': doc.name}, fields=['attribute', 'attribute_value'])
    # Initialize fields for size and color
    size = ''
    color = ''
    # Check and set the size and color based on attributes
    for attr in attributes:
        if attr.attribute == 'Size':
            size = attr.attribute_value
        elif attr.attribute == 'Color':
            color = attr.attribute_value
    
    # Update the item with size and color values
    if size:
        doc.size = size
    if color:
        doc.color = color

    
def set_supplier(doc, method=None):
    if doc.has_variants == 0:
        doc.default_supplier = frappe.db.get_value(doc.doctype, doc.variant_of, "default_supplier")

