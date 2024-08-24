import frappe

def get_permission_query_conditions(*args, **kwargs):
    if "Supplier Portal" in frappe.get_roles() and frappe.session.user != "Administrator":
        supplier = frappe.db.get_value("Supplier", {"email_id": frappe.session.user})
        supplier_users = frappe.db.get_all(
            "Portal User", 
            filters={"user": frappe.session.user, "parenttype": "Supplier"}, 
            pluck="parent"
        )
        
        conditions = []
        
        if supplier:
            conditions.append(f"`tabPurchase Order`.supplier = '{supplier}'")
        
        if supplier_users:
            supplier_user_conditions = ','.join([f"'{user}'" for user in supplier_users])
            conditions.append(f"`tabPurchase Order`.supplier IN ({supplier_user_conditions})")
        
        return " OR ".join(conditions) if conditions else None
