# -*- coding: utf-8 -*-
# Copyright (c) 2018, Manqala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint

class VoucherSearchSpecifications(Document):
	def __init__(self, *args, **kwargs):
		super(VoucherSearchSpecifications, self).__init__(*args, **kwargs)
		self.flags.ignore_links = True

	def transform_fields(self, dn, idx=None):
		row = [r for r in self.voucher_search_keys if r.name==dn][0]
		duplicate = False
		res = []
		for i in range(1, 11):
			field = 'field_%s'%i
			eval_rule_field = field + '_transformation_rule'
			field_val = row.get(field, '')
			if field_val:
				# check if the selected already exists
				if (idx != None) and cint(idx) != i:
					if field_val == row.get('field_%s'%idx):
						frappe.msgprint('Field: %s already selected in Field %s'%(field_val,field))
						row.set('field_%s'%idx, '')
						duplicate = True
						break

				if row.get(eval_rule_field, ''):
					res.append(self.transform_field(field, dn) or '')
				else:
					res.append(field_val)
		if not duplicate:
			return (row.separator or '-').join(res)
		return row.search_key_specification

	def transform_field(self, field, dn):
		eval_rule_field = field + '_transformation_rule'
		row = [r for r in self.voucher_search_keys if r.name==dn][0]
		eval_code = row.get(eval_rule_field, '')
		if not eval_code:
			return

		eval_data = {field: row.get(field, '')}
		
		try:
			return frappe.safe_eval(eval_code, None, eval_data)

		except NameError as err:
			frappe.throw(_("Name error: {0}".format(err)))
		except SyntaxError as err:
			frappe.throw(_("Syntax error in formula or condition: {0}".format(err)))
		except Exception as e:
			frappe.throw(_("Error in formula or condition: {0}".format(e)))

	def get_search_key(self, doc):
		"""returns a key as specified in the search key spec"""
		vals = []
		dn = doc.doctype
		row = [r for r in self.voucher_search_keys if r.voucher_type==dn][0]
		for i in range(1, 11): #for fields field_1 to field_10
			field = 'field_%s'%i
			eval_rule_field = field + '_transformation_rule'
			field_name = row.get(field, '')
			eval_rule = row.get(eval_rule_field, '')
			if field_name:
				val = doc.get(field_name)
				if eval_rule:
					eval_rule = eval_rule.replace(field, field_name)
					eval_data = {field_name: val}
					val = frappe.safe_eval(eval_rule, None, eval_data)
				if val != None:
					vals.append(val)
		return (row.separator or '-').join(vals)
