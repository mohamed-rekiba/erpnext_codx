from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import frappe

def execute():
    setup_custom_fields()

def setup_custom_fields():
    custom_fields = {
        "Item": [
            dict(
                fieldname="default_supplier",
                label="Default Supplier",
                fieldtype="Link",
                options="Supplier",
                insert_after="stock_uom",
                print_hide=1,
            )
        ]
    }

    create_custom_fields(custom_fields, ignore_validate=True)
