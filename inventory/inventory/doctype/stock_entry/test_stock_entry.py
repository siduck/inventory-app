# Copyright (c) 2025, Sidhanth and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from inventory.inventory.utils import gen_item, gen_warehouse, gen_stock_entry

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]

test_data = [
	{
		"item": "TV",
		"warehouse": "Mumbai",
		"qty_change": 10,
		"value_change": 1000.0,
		"valuation_rate": 100,
	},
	{
		"item": "TV",
		"warehouse": "Mumbai",
		"qty_change": -5,
		"value_change": -500.0,
		"valuation_rate": 100,
	},
	{
		"item": "TV",
		"warehouse": "Hyd",
		"qty_change": 5,
		"value_change": 500.0,
		"valuation_rate": 100,
	},
	{
		"item": "TV",
		"warehouse": "Mumbai",
		"qty_change": 10,
		"value_change": 2000.0,
		"valuation_rate": 166.66666666666666,
	},
	{
		"item": "TV",
		"warehouse": "Mumbai",
		"qty_change": -3,
		"value_change": -500.0,
		"valuation_rate": 166.66666666666666,
	},
]


class IntegrationTestStockEntry(IntegrationTestCase):
	"""
	Integration tests for StockEntry.
	Use this class for testing interactions between multiple components.
	"""

	def setUp(self):
		gen_item("TV")

		gen_warehouse("Mumbai")
		gen_warehouse("Hyd")

		gen_stock_entry(item="TV", to_warehouse="Mumbai", qty=10, rate=100, entry_type="Receipt")
		gen_stock_entry(item="TV", from_warehouse="Mumbai", to_warehouse="Hyd", qty=5, entry_type="Transfer")
		gen_stock_entry(item="TV", to_warehouse="Mumbai", qty=10, rate=200, entry_type="Receipt")
		gen_stock_entry(item="TV", from_warehouse="Mumbai", qty=3, entry_type="Consume")

	def test_flow(self):
		ledger_entries = frappe.db.get_list(
			"Stock Ledger Entry",
			fields=[
				"item",
				"warehouse",
				"qty_change",
				"value_change",
				"valuation_rate",
			],
			order_by="creation",
		)

		for i, data in enumerate(test_data):
			self.assertEqual(data["item"], ledger_entries[i].item)
			self.assertEqual(data["warehouse"], ledger_entries[i].warehouse)
			self.assertEqual(data["qty_change"], ledger_entries[i].qty_change)
			self.assertEqual(data["value_change"], ledger_entries[i].value_change)
			self.assertAlmostEqual(data["valuation_rate"], ledger_entries[i].valuation_rate)
