# Copyright (c) 2025, Sidhanth and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StockLedger(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		date: DF.Date | None
		item: DF.Link | None
		qty_in: DF.Int
		qty_out: DF.Int
		stock_qty: DF.Data | None
		warehouse: DF.Link | None
	# end: auto-generated types

	pass
