import frappe
from frappe.model.document import Document


def validate_fields(self):
	if self.from_warehouse == self.to_warehouse:
		frappe.throw("Warehouses cannot be the same")

	if self.entry_type == "Transfer":
		if not self.from_warehouse or not self.to_warehouse:
			frappe.throw("Warehouses are mandatory for Transfer entries")


def get_prev_stockqty(self):
	ledgers = frappe.db.get_list("Stock Ledger", filters={"item": self.item}, pluck="stock_qty")
	return len(ledgers) > 0 and ledgers[0] or 0


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
		to_warehouse: DF.Link
	# end: auto-generated types

	def before_save(self):
		validate_fields(self)

		ledger_data = {
			"doctype": "Stock Ledger",
			"item": self.item,
			"date": self.creation,
			"warehouse": self.from_warehouse if self.entry_type == "Transfer" else self.to_warehouse,
			"qty_in": self.qty if self.entry_type == "Receipt" else 0,
			"qty_out": 0 if self.entry_type == "Receipt" else self.qty,
		}

		ledger_data["stock_qty"] = get_prev_stockqty(self) + (ledger_data["qty_in"] - ledger_data["qty_out"])
		ledger_doc1 = frappe.get_doc(ledger_data)
		ledger_doc1.insert()

		if self.entry_type == "Transfer":
			transfer_ledger = frappe.get_doc(
				{
					**ledger_data,
					"qty_in": self.qty,
					"qty_out": 0,
					"qty_balance": self.qty - 0,
					"warehouse": self.to_warehouse,
				}
			)
			transfer_ledger.insert()
