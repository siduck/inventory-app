import frappe


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
