from ecommerce_integrations.shopify.page.shopify_import_products.shopify_import_products import *
from next_codx.shopify.product import CustomShopifyProduct

@frappe.whitelist()
def custom_sync_product(product):
	try:
		shopify_product = CustomShopifyProduct(product)
		shopify_product.sync_product()

		return True
	except Exception:
		frappe.db.rollback()
		return False


@frappe.whitelist()
def custom_resync_product(product):
	return _custom_resync_product(product)


@temp_shopify_session
def _custom_resync_product(product):
	savepoint = "shopify_resync_product"
	try:
		item = Product.find(product)

		frappe.db.savepoint(savepoint)
		for variant in item.variants:
			shopify_product = CustomShopifyProduct(product, variant_id=variant.id)
			shopify_product.sync_product()

		return True
	except Exception:
		frappe.db.rollback(save_point=savepoint)
		return False


@frappe.whitelist()
def custom_import_all_products():
	frappe.enqueue(
		custom_queue_sync_all_products, queue="long", job_name=SYNC_JOB_NAME, key=REALTIME_KEY,
	)


def custom_queue_sync_all_products(*args, **kwargs):
	start_time = process_time()

	counts = get_product_count()
	publish("Syncing all products...")

	if counts["shopifyCount"] < counts["syncedCount"]:
		publish("⚠ Shopify has less products than ERPNext.")

	_sync = True
	collection = _fetch_products_from_shopify(limit=100)
	savepoint = "custom_shopify_product_sync"
	while _sync:
		for product in collection:
			try:
				publish(f"Syncing product {product.id}", br=False)
				frappe.db.savepoint(savepoint)
				if is_synced(product.id):
					publish(f"Product {product.id} already synced. Skipping...")
					continue

				shopify_product = CustomShopifyProduct(product.id)
				shopify_product.sync_product()

				publish(f"✅ Synced Product {product.id}", synced=True)

			except UniqueValidationError as e:
				publish(f"❌ Error Syncing Product {product.id} : {str(e)}", error=True)
				frappe.db.rollback(save_point=savepoint)
				continue

			except Exception as e:
				publish(f"❌ Error Syncing Product {product.id} : {str(e)}", error=True)
				frappe.db.rollback(save_point=savepoint)
				continue

		if collection.has_next_page():
			frappe.db.commit()  # prevents too many write request error
			collection = _fetch_products_from_shopify(from_=collection.next_page_url)
		else:
			_sync = False

	end_time = process_time()
	publish(f"🎉 Done in {end_time - start_time}s", done=True)
	return True
