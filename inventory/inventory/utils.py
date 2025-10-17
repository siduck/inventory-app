import frappe


def gen_stock_ledger_entry(item, warehouse, **kargs):
	frappe.get_doc(
		{
			"doctype": "Stock Ledger Entry",
			"item": item,
			"warehouse": warehouse,
			"qty_in": kargs.get("qty_in", 0),
			"qty_out": kargs.get("qty_out", 0),
			"incoming_value": kargs.get("incoming_value", 0),
		}
	).insert()
