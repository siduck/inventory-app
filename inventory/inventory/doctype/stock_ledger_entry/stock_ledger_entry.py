# Copyright (c) 2025, Sidhanth and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StockLedgerEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		item: DF.Link | None
		qty_change: DF.Int
		valuation_rate: DF.Currency
		value_change: DF.Currency
		voucher_code: DF.Link | None
		voucher_type: DF.Data | None
		warehouse: DF.Link | None
	# end: auto-generated types

	pass
