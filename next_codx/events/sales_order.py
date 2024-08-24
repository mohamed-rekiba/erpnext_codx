import frappe
import json
from frappe.utils import flt
from erpnext.setup.utils import get_exchange_rate
from frappe.model.mapper import get_mapped_doc


def on_submit(self, method=None):
    # Pass the items in the Sales Order to the function
    selected_items = [item.as_dict() for item in self.items]
    make_purchase_order_for_default_supplier(self.name, selected_items)


def make_purchase_order_for_default_supplier(source_name, selected_items):
    """Creates Purchase Order for each Supplier based on grouped items."""

    if not selected_items:
        return

    if isinstance(selected_items, str):
        selected_items = json.loads(selected_items)

    def set_missing_values(source, target, supplier):
        target.supplier = supplier
        target.currency = frappe.db.get_value(
            "Supplier", filters={"name": supplier}, fieldname=["default_currency"]
        )
        company_currency = frappe.db.get_value(
            "Company", filters={"name": target.company}, fieldname=["default_currency"]
        )
        try:
            conversion_rate = get_exchange_rate(target.currency, company_currency, args="for_buying")
        except:
            conversion_rate = 1.0

        target.conversion_rate = conversion_rate

        target.apply_discount_on = ""
        target.additional_discount_percentage = 0.0
        target.discount_amount = 0.0
        target.inter_company_order_reference = ""
        target.shipping_rule = ""
        target.tc_name = ""
        target.terms = ""
        target.payment_terms_template = ""
        target.payment_schedule = []

        default_price_list = frappe.get_value("Supplier", supplier, "default_price_list")
        if default_price_list:
            target.buying_price_list = default_price_list

        default_payment_terms = frappe.get_value("Supplier", supplier, "payment_terms")
        if default_payment_terms:
            target.payment_terms_template = default_payment_terms

        if any(item.delivered_by_supplier == 1 for item in source.items):
            if source.shipping_address_name:
                target.shipping_address = source.shipping_address_name
                target.shipping_address_display = source.shipping_address
            else:
                target.shipping_address = source.customer_address
                target.shipping_address_display = source.address_display

            target.customer_contact_person = source.contact_person
            target.customer_contact_display = source.contact_display
            target.customer_contact_mobile = source.contact_mobile
            target.customer_contact_email = source.contact_email
        else:
            target.customer = ""
            target.customer_name = ""

        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")

    def update_item(source, target, source_parent):
        target.schedule_date = source.delivery_date
        target.qty = flt(source.qty) - (flt(source.ordered_qty) / flt(source.conversion_factor))
        target.stock_qty = flt(source.stock_qty) - flt(source.ordered_qty)
        target.project = source_parent.project

    # Group selected items by supplier
    supplier_items_map = {}
    for item in selected_items:
        supplier = item.get("supplier")
        if supplier:
            supplier_items_map.setdefault(supplier, []).append(item)

    if not supplier_items_map:
        return  # Skip processing if there are no items with suppliers

    purchase_orders = []
    for supplier, items in supplier_items_map.items():
        if not items:
            continue  # Skip suppliers with no items

        # Create the target_doc as None for fresh document creation
        target_doc = None

        doc = get_mapped_doc(
            "Sales Order",
            source_name,
            {
                "Sales Order": {
                    "doctype": "Purchase Order",
                    "field_no_map": [
                        "address_display",
                        "contact_display",
                        "contact_mobile",
                        "contact_email",
                        "contact_person",
                        "taxes_and_charges",
                        "shipping_address",
                    ],
                    "validation": {"docstatus": ["=", 1]},
                },
                "Sales Order Item": {
                    "doctype": "Purchase Order Item",
                    "field_map": [
                        ["name", "sales_order_item"],
                        ["parent", "sales_order"],
                        ["stock_uom", "stock_uom"],
                        ["uom", "uom"],
                        ["conversion_factor", "conversion_factor"],
                        ["delivery_date", "schedule_date"],
                    ],
                    "field_no_map": [
                        "rate",
                        "price_list_rate",
                        "item_tax_template",
                        "discount_percentage",
                        "discount_amount",
                        "pricing_rules",
                    ],
                    "postprocess": update_item,
                    "condition": lambda doc: doc.ordered_qty < doc.stock_qty
                                             and doc.supplier == supplier
                                             and doc.item_code in [item.get("item_code") for item in items],
                },
            },
            target_doc,
            lambda source, target: set_missing_values(source, target, supplier),
        )
        doc.flags.ignore_mandatory = True
        doc.flags.ignore_exchange_rate = True
        doc.insert()
        frappe.db.commit()
        purchase_orders.append(doc)
