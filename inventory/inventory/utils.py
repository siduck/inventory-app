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
	doc.rate = kargs.get("rate", 0)
	doc.entry_type = kargs["entry_type"]
	doc.save()


def get_valuation_rate(item, warehouse, **kargs):
	stock_summary = frappe.get_list(
		"Stock Ledger Entry",
		filters={"item": item, "warehouse": warehouse},
		fields=[
			"SUM(qty_change) as qty_change",
			"SUM(value_change) as `stock_balance`",
		],
	)[0]

	valuation_rate = 0

	total_money_spent = (stock_summary.stock_balance or 0) + kargs["value_change"]
	total_stock_qty = stock_summary.qty_change or 0

	if kargs["entry_type"] == "Receipt":
		total_stock_qty += kargs["qty_change"]

	if total_stock_qty == 0:
		# old valuation rate for transfers
		valuation_rate = frappe.get_list(
			"Stock Ledger Entry",
			filters={"item": item},
			fields=["SUM(value_change)/SUM(qty_change) as `valuation_rate`"],
		)[0].valuation_rate
	else:
		valuation_rate = total_money_spent / total_stock_qty

	return valuation_rate


def gen_stock_ledger_entry(item, warehouse, **kargs):
	valuation_rate = get_valuation_rate(item, warehouse, **kargs)

	doc = frappe.new_doc("Stock Ledger Entry")
	doc.item = item
	doc.warehouse = warehouse
	doc.qty_change = kargs["qty_change"]
	doc.value_change = kargs["value_change"]
	doc.valuation_rate = valuation_rate

	if kargs["entry_type"] != "Receipt":
		doc.value_change = valuation_rate * kargs["qty_change"]

	doc.insert()
