import frappe


def gen_item(title):
	doc = frappe.new_doc("Item")
	doc.title = title
	doc.insert()
	return doc


def gen_warehouse(name):
	doc = frappe.new_doc("Warehouse")
	doc.warehouse_name = name
	doc.insert()
	# frappe.rename_doc("Warehouse", doc.name, name)
	# return doc


def gen_stock_entry(entry_type, to_warehouse, from_warehouse, transactions):
	doc = frappe.new_doc("Stock Entry")

	if to_warehouse:
		doc.to_warehouse = to_warehouse

	if from_warehouse:
		doc.from_warehouse = from_warehouse

	for txn in transactions:
		doc.append(
			"transactions",
			{
				"item": txn["item"],
				"qty": txn["qty"],
				"rate": txn.get("rate"),
			},
		)

	doc.entry_type = entry_type

	doc.insert()
	doc.submit()


def get_valuation_rate(item, warehouse, entry_type, value_change, qty_change):
	stock_summary = frappe.get_list(
		"Stock Ledger Entry",
		filters={"item": item, "warehouse": warehouse},
		fields=[
			"SUM(qty_change) as qty_change",
			"SUM(value_change) as `stock_balance`",
		],
	)[0]

	valuation_rate = 0

	total_money_spent = (stock_summary.stock_balance or 0) + value_change
	total_stock_qty = stock_summary.qty_change or 0

	if entry_type == "Receipt":
		total_stock_qty += qty_change

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


def gen_stock_ledger_entry(item, warehouse, entry_type, value_change, qty_change, voucher_code):
	valuation_rate = get_valuation_rate(item, warehouse, entry_type, value_change, qty_change)

	doc = frappe.new_doc("Stock Ledger Entry")
	doc.item = item
	doc.warehouse = warehouse
	doc.qty_change = qty_change
	doc.value_change = value_change
	doc.valuation_rate = valuation_rate
	doc.voucher_code = voucher_code
	doc.voucher_type = entry_type

	if entry_type != "Receipt":
		doc.value_change = valuation_rate * qty_change

	doc.insert()
