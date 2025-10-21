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


class IntegrationTestStockEntry(IntegrationTestCase):
	"""
	Integration tests for StockEntry.
	Use this class for testing interactions between multiple components.
	"""

	def setUp(self):
		gen_item("Galaxy")
		gen_item("Phone")

		gen_warehouse("Mumbai")
		gen_warehouse("Hyd")
		gen_stock_entry(item="Galaxy", to_warehouse="Mumbai", qty=10, rate=100, entry_type="Receipt")
		gen_stock_entry(item="Galaxy", to_warehouse="Mumbai", qty=5, rate=130, entry_type="Receipt")
		gen_stock_entry(item="Phone", to_warehouse="Mumbai", qty=5, rate=200, entry_type="Receipt")

	def test_flow(self):
		frappe.db.get_list(
			"Stock Ledger Entry",
			fields=[
				"name",
				"item",
				"creation",
				"warehouse",
				"qty_change",
			],
			order_by="creation",
		)
