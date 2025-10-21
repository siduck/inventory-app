import frappe


def gen_item(title):
	doc = frappe.new_doc("Item")
	doc.title = title
	doc.insert()
	return doc


def gen_warehouse(name):
	doc = frappe.new_doc("Warehouse")
	doc.insert()
	frappe.rename_doc("Warehouse", doc.name, name)
	# return doc


def gen_stock_entry(**kargs):
	doc = frappe.new_doc("Stock Entry")
	doc.item = kargs["item"]

	if kargs.get("to_warehouse"):
		doc.to_warehouse = kargs["to_warehouse"]

	if kargs.get("from_warehouse"):
		doc.from_warehouse = kargs["from_warehouse"]

	doc.qty = kargs["qty"]
	doc.rate = kargs["rate"]
	doc.entry_type = kargs["entry_type"]
	doc.save()

def gen_stock_ledger_entry(item, warehouse, **kargs):
	frappe.get_doc(
		{
			"doctype": "Stock Ledger Entry",
			"item": item,
			"warehouse": warehouse,
			"qty_change": kargs["qty_change"],
			"incoming_value": kargs.get("incoming_value", 0),
		}
	).insert()
