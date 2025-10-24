# Copyright (c) 2025, Sidhanth and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StockEntryItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		item: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		qty: DF.Int
		rate: DF.Currency
	# end: auto-generated types

	pass
