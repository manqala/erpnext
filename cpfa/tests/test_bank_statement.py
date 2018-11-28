# -*- coding: utf-8 -*-
# Copyright (c) 2018, Manqala Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import unittest
import frappe

from frappe.utils import getdate
from datetime import timedelta
from frappe.test_runner import make_test_records


class TestBankStatement(unittest.TestCase):
	def setUp(self):
		records = [
			{
				'doctype': 'Bank Statement',
				'start_date': getdate(),
				'end_date': getdate() + timedelta(1)
			}
		]
		
		make_test_records(records)

	def upload_statement_file(self):
		statement = frappe.get_doc('Bank Statement', '_testStatement')
		statement.attach = 'test_statement.xlsx'
		statement.save()

	def test_upload_statement(self):
		pass

	def test_search_text(self):
		"""check if a key words in any other can be found in a text"""
		import re
		from cpfa.bank_statement.doctype.bank_statement.bank_statement \
			import search_text

		keywords = ['Ekanem','Grace']
		description = '''
			TRANSFER BETWEEN CUSTOMERS 000016161023190343000102097128
			200UNITS T24 636128462227560890 GRACE EKANEM to ABC ESTATE
		'''
		flags = re.DOTALL | re.IGNORECASE | re.MULTILINE
		self.assertTrue(search_text(keyword, description, flags))
		# requiring re.IGNORECASE
		self.assertFalse(search_text(keyword, description))

	def test_get_open_third_party_documents_using_search_fields(self):
		"""check if search fields match open documents"""
		
		from cpfa.bank_statement.doctype.bank_statement.bank_statement \
			import get_open_third_party_documents_using_search_fields

		from erpnext.accounts.doctype.journal_entry.journal_entry \
			import get_payment_entry_against_invoice

		invoice = self.create_sales_invoice()
		credit_txn_type = frappe.get_doc('Bank Transaction Type',
										 'XLS-TRANS-CR')
		search_fields = credit_txn_type.search_fields_third_party_doc_dr
		sta = frappe.get_doc('Bank Statement','BANK-STA-00002')
		txn = sta.bank_statement_items[2]
		txn.set('debit_amount', invoice.outstanding_amount)
		open_docs = get_open_third_party_documents_using_search_fields(
			search_fields, txn, allocated_entries=[])

		search_field = search_fields[0].field_name
		self.assertTrue(search_field in check_statement_item(txn, results[0],
						search_field).keys())
		self.assertTrue(len(open_docs) >= 1)
