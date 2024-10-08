app_name = "next_codx"
app_title = "Next Codx"
app_publisher = "omneya"
app_description = "NEXT_CODX Custom App"
app_email = "omneyaeid827@gmail.com"
app_license = "mit"

app_logo_url = "/assets/next_codx/images/logo.jpeg",

required_apps = ["frappe/erpnext"]

permission_query_conditions = {
	"Purchase Order": "next_codx.events.purchase_order.get_permission_query_conditions",
}

doc_events = {
	"Sales Order": {
		"on_update_after_submit": ["next_codx.events.sales_order.on_submit",],
        "on_update": "next_codx.events.sales_order.on_submit",
        "autoname":  "next_codx.events.sales_order.autoname",
	},
	"Purchase Order": {
        "autoname":  "next_codx.events.purchase_order.autoname",
		"on_update": "next_codx.events.purchase_order.on_update",
	},
}

doctype_js = {
	"Sales Order" : "public/js/sales_order.js",
	"Purchase Order":  "public/js/purchase_order.js",
}

doctype_list_js = {
	"Sales Order" : "public/js/sales_order_list.js",
    "Purchase Order":  "public/js/purchase_order_list.js",
}

override_whitelisted_methods = {
	"ecommerce_integrations.shopify.page.shopify_import_products.shopify_import_products.sync_product": "next_codx.shopify.import_products.custom_sync_product",
	"ecommerce_integrations.shopify.page.shopify_import_products.shopify_import_products.resync_product" : "next_codx.shopify.import_products.custom_resync_product",
	"ecommerce_integrations.shopify.page.shopify_import_products.shopify_import_products.import_all_products" : "next_codx.shopify.import_products.custom_import_all_products",
}

fixtures = ["Role"]
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/next_codx/css/next_codx.css"
# app_include_js = "/assets/next_codx/js/next_codx.js"

# include js, css files in header of web template
# web_include_css = "/assets/next_codx/css/next_codx.css"
# web_include_js = "/assets/next_codx/js/next_codx.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "next_codx/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "next_codx/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "next_codx.utils.jinja_methods",
# 	"filters": "next_codx.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "next_codx.install.before_install"
# after_install = "next_codx.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "next_codx.uninstall.before_uninstall"
# after_uninstall = "next_codx.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "next_codx.utils.before_app_install"
# after_app_install = "next_codx.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "next_codx.utils.before_app_uninstall"
# after_app_uninstall = "next_codx.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "next_codx.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"next_codx.tasks.all"
# 	],
# 	"daily": [
# 		"next_codx.tasks.daily"
# 	],
# 	"hourly": [
# 		"next_codx.tasks.hourly"
# 	],
# 	"weekly": [
# 		"next_codx.tasks.weekly"
# 	],
# 	"monthly": [
# 		"next_codx.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "next_codx.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "next_codx.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "next_codx.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["next_codx.utils.before_request"]
# after_request = ["next_codx.utils.after_request"]

# Job Events
# ----------
# before_job = ["next_codx.utils.before_job"]
# after_job = ["next_codx.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"next_codx.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

