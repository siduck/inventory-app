import frappe
from frappe.model.document import Document


from inventory.inventory.utils import gen_stock_ledger_entry


def validate_fields(self):
	if self.from_warehouse == self.to_warehouse:
		frappe.throw("Warehouses cannot be the same")

	if self.entry_type == "Transfer":
		if not self.from_warehouse or not self.to_warehouse:
			frappe.throw("Warehouses are mandatory for Transfer entries")


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
		to_warehouse: DF.Link
	# end: auto-generated types

	def before_save(self):
		validate_fields(self)

		if self.entry_type == "Transfer":
			gen_stock_ledger_entry(
				self.item,
				self.from_warehouse,
				qty_out=self.qty,
			)

			gen_stock_ledger_entry(
				self.item,
				self.to_warehouse,
				qty_in=self.qty,
			)
		else:
			is_receipt = self.entry_type == "Receipt"
			gen_stock_ledger_entry(
				self.item,
				self.to_warehouse,
				qty_in=(is_receipt and self.qty) or None,
				qty_out=(not is_receipt and self.qty) or None,
				incoming_value=(is_receipt and self.qty * self.rate) or None,
			)
