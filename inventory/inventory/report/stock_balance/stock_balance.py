# Copyright (c) 2025, Sidhanth and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the Stock Ledger report."""
	return [
		{
			"label": _("Item"),
			"fieldname": "item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Datetime",
			"width": 200,
		},
		{
			"label": _("warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 100,
		},
		{
			"label": _("Qty In"),
			"fieldname": "qty_in",
			"fieldtype": "Int",
			"width": 80,
		},
		{
			"label": _("Qty Out"),
			"fieldname": "qty_out",
			"fieldtype": "Int",
			"width": 80,
		},
		{
			"label": _("Valuation Rate"),
			"fieldname": "valuation_rate",
			"fieldtype": "currency",
			"width": 150,
		},
		{"label": _("Total Qty"), "fieldname": "total_qty", "fieldtype": "Int", "width": 80},
		{
			"label": _("Stock Value"),
			"fieldname": "stock_value",
			"fieldtype": "Currency",
			"width": 130,
		},
	]


def gen_row(data):
	previous_rows = frappe.get_list(
		"Stock Ledger Entry",
		filters={"item": data.item, "creation": ["<=", data.creation], "warehouse": data.warehouse},
		fields=["SUM(qty_change) as qty_change", "SUM(value_change) as `stock_balance`"],
	)

	prev_vals = previous_rows[0]
	qty_in = (data.qty_change > 0 and data.qty_change) or 0
	qty_out = (data.qty_change < 0 and abs(data.qty_change)) or 0

	return [
		data.item,
		data.creation,
		data.warehouse,
		qty_in,
		qty_out,
		data.valuation_rate,
		prev_vals["qty_change"],
		prev_vals["stock_balance"],
	]


def get_data() -> list[list]:
	li = frappe.get_list("Stock Ledger Entry", fields=["*"], order_by="creation asc")

	rows = []

	for data in li:
		rows.append(gen_row(data))

	"""Return data for the report."""
	return rows
