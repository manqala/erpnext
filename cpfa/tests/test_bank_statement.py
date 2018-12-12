# -*- coding: utf-8 -*-
# Copyright (c) 2018, Manqala Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import unittest
import frappe

from frappe.utils import getdate
from datetime import timedelta
from collections import defaultdict
from frappe.test_runner import make_test_records
from erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice import unlink_payment_on_cancel_of_invoice


class TestBankStatement(unittest.TestCase):
	def setUp(self):
		unlink_payment_on_cancel_of_invoice()
		self.docs = build_test_records(verbose=1)

	def tearDown(self):
		delete_test_records(self.docs, verbose=1)
		unlink_payment_on_cancel_of_invoice(0)

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

		invoice = self.docs[1]['Sales Invoice'][0]
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


def build_test_records(verbose=0):
	frappe.local.lang = 'en-GB'
	docs = [defaultdict(list),defaultdict(list)]
	for count,record in enumerate((setup_docs,  txn_docs)):
		for data in record:
			name_filter = data['name_filter']
			del data['name_filter']

			try:
				d = frappe.get_doc(data)
				if verbose:
					print 'Inserting ' + d.doctype
				d.insert()
				if d.docstatus == 1:
					if verbose:
						print 'Submitting ' + d.doctype
					d.reload()
					d.submit()
			except (frappe.DuplicateEntryError, frappe.NameError):
				d = frappe.get_doc(data['doctype'], name_filter)

			#insert so last in is first out
			docs[count][d.doctype].insert(0, d.name)

	return docs

def delete_test_records(records, verbose=0):
	records.reverse()
	for dt, dnames in [d for tmp in records for d in tmp.iteritems()]:
		for dn in dnames:
			try:
				if verbose:
					print 'deleting ', dt, ': ',dn
				doc = frappe.get_doc(dt, dn)
				if doc.docstatus == 1:
					doc.cancel()
				frappe.delete_doc(dt, dn, force=1, ignore_on_trash=1)
				if verbose:
					print dt, ': ',dn, ' deleted'
				del doc
			except frappe.DoesNotExistError:
				if verbose:
					print dt, ': ', dn, ' not found'
				continue


setup_docs = [
	{'doctype': 'Fiscal Year',
	'year': '_Test Fiscal Year 2018',
	'year_end_date': '2018-12-31',
	'name_filter': {'year': '_Test Fiscal Year 2018'},
	'year_start_date': '2018-01-01'},
	{'doctype':'Domain',
	'name_filter':{'domain':'Services'},
	'domain':'Services'},
	{'abbr': '_TCX',
	'chart_of_accounts': 'Standard',
	'company_name': '_Test Company X',
	'country': 'Nigeria',
	'name_filter': {'company_name': '_Test Company X'},
	'default_currency': 'NGN',
	'doctype': 'Company',
	'domain': 'Services'},
	{'is_group':1,
	'item_group_name':'All Item Groups',
	'name_filter':{'item_group_name':'All Item Groups'},
	'doctype':'Item Group'},
	{'uom_name':'_Test UOM X',
	'name_filter':{'uom_name':'_Test UOM X'},
	'doctype':'UOM'},
	{'doctype':'Territory',
	'territory_name':'All Territories',
	'name_filter':{'territory_name':'All Territories'},
	'is_group':1},
	{'doctype':'Customer Group',
	'name_filter':{'customer_group_name':'All Customer Groups'},
	'customer_group_name':'All Customer Groups',
	'is_group':1},
	{'buying': 1,
	'currency': 'NGN',
	'doctype': 'Price List',
	'enabled': 1,
	'name_filter':{'price_list_name':'_Test Price List X'},
	'price_list_name': '_Test Price List X',
	'selling': 1}
]

txn_docs = [
	{'cost_center': u'_Test Cost Center - _TCX',
	'description': '_Test Item X',
	'doctype': 'Item',
	'name_filter':{'item_code':'_Test Item X'},
	'expense_account': 'Cost of Goods Sold - _TCX',
	'has_batch_no': 0,
	'has_serial_no': 0,
	'income_account': 'Sales - _TCX',
	'inspection_required': 0,
	'is_stock_item': 0,
	'is_sub_contracted_item': 1,
	'item_code': '_Test Item X',
	'item_name': '_Test Item X',
	'item_group': 'All Item Groups',
	'stock_uom': '_Test UOM X'},
	{'doctype':'Customer',
	'customer_name':'_Test Customer X',
	'customer_group':'All Customer Groups',
	'name_filter':{'customer_name':'_Test Customer X'},
	'territory':'All Territories'},
	{'doctype':'Sales Invoice',
	'name_filter':{'customer':'_Test Customer X'},
	'company':'_Test Company X',
	'customer':'_Test Customer X',
	'currency':'NGN',
	'due_date':frappe.utils.getdate(),
	'docstatus':1,
	'debit_to':'Debtors - _TCX',
	'items': [{
		'item_name':'_Test Item X',
		'item_code':'_Test Item X',
		'qty':1,
		'conversion_factor':1,
		'uom':'_Test UOM X',
		'cost_center':'Main - _TCX',
		'rate':'1000'}]
	}
]

sample_statement = [
	{
		'Trans Date': '24-Oct-16',
		'Reference': '',
		'Value Date': '24-Oct-16',
		'Debit': '1000',
		'Credit': '',
		'Balance': '4000',
		'Remarks': '''TRANSFER BETWEEN CUSTOMERS
			PINV-00001 T40 OCTOBER PAYMENT
			AND 500 UNITS T40 OCTOBER PAYMENT AND 500 UNITS
			_TEST CUSTOMER to ABC ESTATE RESD.&OWNER'''
	},{
		'Trans Date': '24-Oct-16',
		'Reference': '',
		'Value Date': '24-Oct-16',
		'Debit': '',
		'Credit': '1000',
		'Balance': '5000',
		'Remarks': '''TRANSFER BETWEEN CUSTOMERS
			SINV-00001/ABCSUPP NIP - TRF IFO
			RIVTAF GOLF ESTATE RESD.andOWNER. 10 106::482701520
			_TEST CUSTOMER to ABC ESTATE RESD.&OWNER'''
	}
]
