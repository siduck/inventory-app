import frappe
from frappe.model.document import Document


from inventory.inventory.utils import gen_stock_ledger_entry


def validate_fields(self):
	if self.from_warehouse == self.to_warehouse:
		frappe.throw("Warehouses cannot be the same")


class StockEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		entry_type: DF.Literal["Transfer", "Receipt", "Consume"]
		from_warehouse: DF.Link | None
		item: DF.Link
		qty: DF.Int
		rate: DF.Currency
		to_warehouse: DF.Link | None
	# end: auto-generated types

	def before_submit(self):
		validate_fields(self)

		if self.entry_type == "Transfer":
			gen_stock_ledger_entry(
				self.item,
				self.from_warehouse,
				qty_change=-self.qty,
				value_change=0,
				entry_type=self.entry_type,
			)

			gen_stock_ledger_entry(
				self.item, self.to_warehouse, qty_change=self.qty, entry_type=self.entry_type, value_change=0
			)
		else:
			is_receipt = self.entry_type == "Receipt"
			gen_stock_ledger_entry(
				self.item,
				(is_receipt and self.to_warehouse) or self.from_warehouse,
				qty_change=(is_receipt and self.qty) or -self.qty,
				value_change=(is_receipt and self.qty * self.rate) or 0,
				entry_type=self.entry_type,
			)
