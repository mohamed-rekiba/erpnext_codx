from next_codx.events.sales_order import create_purshase_order
import frappe

@frappe.whitelist()
def update_status(doctype, name, field, value):
    # Fetch the document
    doc = frappe.get_doc(doctype, name)
    
    # Use `getattr` to dynamically get the attribute (field) and set its value
    if hasattr(doc, field):
        setattr(doc, field, value)
        doc.save()
        frappe.db.commit()  # Commit the transaction to the database

        return f"{field} updated successfully to {value} in {doctype} {name}"
    else:
        return f"Field {field} does not exist in {doctype} {name}"
