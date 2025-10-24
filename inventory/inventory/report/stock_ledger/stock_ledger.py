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
			"label": _("Incoming Value"),
			"fieldname": "incoming_value",
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"label": _("Outgoing Value"),
			"fieldname": "outgoing_value",
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"label": _("Valuation Rate"),
			"fieldname": "valuation_rate",
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"label": _("Voucher Code"),
			"fieldname": "voucher_code",
			"options": "Stock Entry",
			"fieldtype": "Link",
			"width": 150,
		}
	]


def gen_row(data):
	qty_in = (data.qty_change > 0 and data.qty_change) or 0
	qty_out = (data.qty_change < 0 and abs(data.qty_change)) or 0
	incoming_value = (data.value_change > 0 and data.value_change) or 0
	outgoing_value = (data.value_change < 0 and abs(data.value_change)) or 0

	return [
		data.item,
		data.creation,
		data.warehouse,
		qty_in,
		qty_out,
		incoming_value,
		outgoing_value,
		data.valuation_rate,
		data.voucher_code,
	]


def get_data() -> list[list]:
	li = frappe.get_list(
		"Stock Ledger Entry",
		fields=["*"],
		order_by="creation asc",
	)

	rows = []

	for data in li:
		rows.append(gen_row(data))

	"""Return data for the report."""
	return rows
