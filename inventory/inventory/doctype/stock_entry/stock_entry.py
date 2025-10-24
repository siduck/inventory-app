import frappe
from frappe.model.document import Document
from inventory.inventory.utils import gen_stock_ledger_entry


class StockEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from inventory.inventory.doctype.stock_entry_item.stock_entry_item import StockEntryItem

		amended_from: DF.Link | None
		entry_type: DF.Literal["Transfer", "Receipt", "Consume"]
		from_warehouse: DF.Link | None
		to_warehouse: DF.Link | None
		transactions: DF.Table[StockEntryItem]
	# end: auto-generated types

	def validate_fields(self):
		if self.from_warehouse == self.to_warehouse:
			frappe.throw("Warehouses cannot be the same")

	def before_save(self):
		self.validate_fields()

		for transaction in self.transactions:
			if self.entry_type == "Transfer":
				gen_stock_ledger_entry(
					transaction.item,
					self.from_warehouse,
					qty_change=-transaction.qty,
					value_change=0,
					entry_type=self.entry_type,
					voucher_code=self.name,
					voucher_type=self.entry_type,
				)
				gen_stock_ledger_entry(
					transaction.item,
					self.to_warehouse,
					qty_change=transaction.qty,
					entry_type=self.entry_type,
					value_change=0,
					voucher_code=self.name,
					voucher_type=self.entry_type,
				)
			else:
				is_receipt = self.entry_type == "Receipt"

				gen_stock_ledger_entry(
					transaction.item,
					(is_receipt and self.to_warehouse) or self.from_warehouse,
					qty_change=(is_receipt and transaction.qty) or -transaction.qty,
					value_change=(is_receipt and transaction.qty * transaction.rate) or 0,
					entry_type=self.entry_type,
					voucher_code=self.name,
					voucher_type=self.entry_type,
				)
