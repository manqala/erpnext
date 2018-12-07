# -*- coding: utf-8 -*-
# Copyright (c) 2018, Manqala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class VoucherSearchSpecifications(Document):
	def __init__(self, *args, **kwargs):
		super(VoucherSearchSpecifications, self).__init__(*args, **kwargs)
		self.flags.ignore_links = True

	def transform_fields(self, dn):
		row = [r for r in self.voucher_search_keys if r.name==dn][0]
		res = []
		for i in range(1, 11):
			field = 'field_%s'%i
			eval_rule_field = field + '_transformation_rule'
			if row.get(field, ''):
				if row.get(eval_rule_field, ''):
					res.append(self.transform_field(field, dn) or '')
				else:
					res.append(row.get(field, ''))
		return (row.separator or '-').join(res)

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
