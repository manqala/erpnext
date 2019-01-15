# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, csv, datetime, os, re
from frappe import _, _dict
from frappe.utils import flt, date_diff, getdate, dateutils, get_datetime
from frappe.model.document import Document
from frappe.utils.file_manager import get_file_path, get_uploaded_content

# just for reference, no longer used
dateformats = {
	'1990-01-31': '%Y-%m-%d',
	'31-01-1990': '%d-%m-%Y',
	'31/01/1990': '%d/%m/%Y',
	'31.01.1990': '%d.%m.%Y',
	'01/31/1990': '%m/%d/%Y',
	'01-31-1990': '%m-%d-%Y',
	'1990-JAN-31': '%Y-%b-%d',
	'31-JAN-1990': '%d-%b-%Y',
	'31/JAN/1990': '%d/%b/%Y',
	'31.JAN.1990': '%d.%b.%Y',
	'JAN/31/1990': '%b/%d/%Y',
	'JAN-31-1990': '%b-%d-%Y',
}

class BankStatement(Document):

	def validate(self):
		self.validate_dates()
		if not self.previous_bank_statement:
			self.fill_previous_statement()
		self.prevent_deletion_if_posted()

	def prevent_deletion_if_posted(self):
		if not self.is_new():
			if len(self.bank_statement_items) != \
					len(frappe.get_doc('Bank Statement', self.name).bank_statement_items):
				self.check_exisiting_postings()

	def on_trash(self):
		self.check_exisiting_postings()

	def delete_postings(self):
		postings = frappe.get_all('Journal Entry',{'cheque_no':self.name})
		
		for posting in postings:
			jv = frappe.get_doc('Journal Entry', posting)
			jv.cancel()
			jv.delete()

		for item in self.bank_statement_items:
			item.set('status', 'Not Started')

		self.save()

	def validate_dates(self):
		previous_sta = frappe.get_all("Bank Statement",
			fields=['statement_end_date','bank','account_no', 'name'],
			filters={
				'name': ['!=', self.get('name',"")],
				'creation': ['<', self.get('creation',get_datetime())]
			})
		
		end_dates = [(s.name,s.statement_end_date) for s in \
			previous_sta if (s.bank == self.bank and \
			s.account_no == self.account_no and \
			s.statement_end_date >= getdate(self.statement_start_date))]
		
		end_dates = filter(lambda x: isinstance(x[1], datetime.date), end_dates)
		
		if end_dates:
			previous_statement_end_date = sorted(end_dates,
								key=lambda x:x[1], reverse=True)[0]
			
			if getdate(self.statement_start_date) > getdate(self.statement_end_date):
				frappe.throw(_("Statement start date cannot be later than end date"))
			
			if getdate(self.statement_start_date) <= previous_statement_end_date[1]:
				prev_doc_name = previous_statement_end_date[0]
				frappe.throw(_("Statement start date cannot be same as or earlier than a previous statement's end date ({})".format(prev_doc_name)))

	def check_end_date(self):
		previous_sta = frappe.get_all("Bank Statement",
				fields=['statement_start_date','bank','account_no'])
		
		end_dates = [s.statement_start_date for s in previous_sta if \
			(s.bank == self.bank and s.account_no == self.account_no)]
		
		for e_date in end_dates:
			date_interval = date_diff(self.statement_start_date, e_date)
			if date_interval > 1:      # if start date is greater than an end date by a day
				return {'gap': date_interval}
		return {'gap': False}

	def fill_previous_statement(self):
		previous_sta = []
		all_previous_sta = frappe.get_all("Bank Statement",
			fields=['statement_end_date','bank','account_no', 'name'],
			filters={'name': ['!=', self.get('name',"")]},
			order_by='creation')
		
		for sta in all_previous_sta:
			if (sta.bank == self.bank) and \
					(sta.account_no == self.account_no) and \
					(getdate(self.statement_start_date) >= sta.statement_end_date):
				previous_sta.append(sta)
		if not previous_sta:
			return

		if len(previous_sta) > 1:
			previous_sta.sort(key=lambda x: x.statement_end_date, reverse=True)

		self.previous_bank_statement = previous_sta[0].name

	def check_file_format(self, csv_header_list):
		sta_format = frappe.get_doc("Bank Statement Format",self.bank_statement_format)
		source_fields = set(s.source_field for s in sta_format.bank_statement_mapping_item)
		if not (set(csv_header_list) >= source_fields):
			frappe.msgprint(_("The attached statement does not contain all the columns specified in the format selected"))

	def convert_to_internal_format(self, csv_column_header,
		csv_row_field_value, bank_statement_mapping_items, eval_data):
		""" select mapping row to be used """
		
		mapping_row = None
		
		for row in bank_statement_mapping_items:
			if row.source_field == csv_column_header:
				mapping_row = row
		if not mapping_row:
			return

		if not (mapping_row.source_field_abbr or mapping_row.transformation_rule):
			return mapping_row.target_field, csv_row_field_value
		
		if not mapping_row.transformation_rule:
			transformation_rule = mapping_row.source_field_abbr.strip()
		else:
			transformation_rule = mapping_row.transformation_rule.strip()
		
		csv_row_field_value = self.eval_transformation(
			transformation_rule, mapping_row.source_field_abbr.strip(),
			eval_data)
		
		eval_data[mapping_row.target_field_abbr.strip()] = csv_row_field_value

		return mapping_row.target_field, csv_row_field_value

	def load_attached_file(self):
		file_id = frappe.db.sql("""SELECT name FROM tabFile WHERE
			attached_to_doctype = '{0}' AND attached_to_name = '{1}'
			""".format("Bank Statement", self.name), as_dict=1)
		
		file_doc = frappe.get_doc("File",file_id[0].name)
		filename, file_extension = os.path.splitext(self.file)

		if file_extension == '.xlsx':
			from frappe.utils.xlsxutils import read_xlsx_file_from_attached_file
			
			rows = read_xlsx_file_from_attached_file(file_id=file_doc.name)
		elif file_extension == '.csv':
			from frappe.utils.file_manager import get_file
			from frappe.utils.csvutils import read_csv_content
			
			fname, fcontent = get_file(file_doc.name)
			rows = read_csv_content(fcontent)
		else:
			frappe.throw(_("Unsupported File Format"))
		return rows

	@property
	def statement_format(self):
		if not self.get('_statement_format'):
			self._statement_format = frappe.get_doc(
				"Bank Statement Format",
				self.bank_statement_format
			)
		return self._statement_format

	def get_mapped(self, row, headers, items):
		eval_data = self.get_eval_data(row, headers, items)
		sta_item = dict()
		for col_idx, col_val in enumerate(row):
			col_val = str(col_val) if col_val else None
			itm = self.convert_to_internal_format(headers[col_idx],
					col_val, items, eval_data)
			
			if not itm:
				continue
			
			target_field, eval_result = itm
			sta_item[frappe.scrub(target_field)] = eval_result

		return sta_item

	def fill_table(self):
		self.check_exisiting_postings()
		if not self.file:
			return
		
		self.bank_statement_items = []
		statement_map_itms = self.statement_format.bank_statement_mapping_item
		rows = self.load_attached_file()
		file_headers = rows[0]
		data_rows = rows[1:]

		self.check_file_format(file_headers)

		intermediate_statement_itms = []
		# create a list of maps, intermediate_bank_statement_items, to hold bank statement items based on internal
		# representation see "Bank Statement Item" definition
		for statement_row in data_rows:
			sta_item = self.get_mapped(statement_row, file_headers,
							statement_map_itms)
			if sta_item:
				intermediate_statement_itms.append(sta_item)
		
		for idx, sta in enumerate(intermediate_statement_itms):
			sta['transaction_type'] = get_txn_type(self, idx+1, sta)
			# create bank_statement_item table entries
			self.append('bank_statement_items', sta)
		
		self.save()

	def eval_transformation(self, eval_code, source_abbr, eval_data):
		if not eval_code:
			frappe.msgprint(_("There is no eval code"))
			return
		try:
			eval_result = frappe.safe_eval(eval_code, None, eval_data)
			return eval_result

		except NameError as err:
			frappe.throw(_("Name error: {0}".format(err)))
		except SyntaxError as err:
			frappe.throw(_("Syntax error in formula or condition: {0}".format(err)))
		except Exception as e:
			frappe.throw(_("Error in formula or condition: {0}".format(e)))
			raise

	def get_eval_data(self, statement_row, csv_header_list,
		bank_statement_mapping_items):
		'''Returns data object for evaluating formula'''
		data = frappe._dict()
		for column_index, column_value in enumerate(statement_row):
			source_abbr = get_source_abbr(csv_header_list[column_index],
										bank_statement_mapping_items)
			if not source_abbr:
				continue
			data[source_abbr] = str(column_value) if column_value else None
			
		data["reformat_date"] = reformat_date
		return data

	def get_account_no(self):
		bank = frappe.get_doc("Bank", self.bank)
		ret_dict = {
			'account_types': get_account_types(),
			'acc_nos': [acc.account_number for acc in bank.bank_accounts],
			'currency_map': {acc.account_number:acc.currency for acc in bank.bank_accounts}
		}
		return ret_dict

	def check_exisiting_postings(self):
		if frappe.db.sql("select name from `tabJournal Entry` \
				where cheque_no='%s' limit 1"%self.name):
			frappe.throw('Postings already exist for Bank Statement: %s\
				<br>View Postings: %s'%(self.name,self.postings_link))

	def process_statement(self):
		self.check_exisiting_postings()
		posted = 0
		
		for idx,row in enumerate(self.bank_statement_items):
			if not row.transaction_type:
				row.set('status', 'Not Started')
				continue
			data = {'row':_dict({'status':'Pending'}),
					'amount':row.credit_amount or row.debit_amount}
			self.get_posting_data(row, data)
			self.make_jv(data)
			if data['posting_jv']:
				posted += 1
				data['row']['status'] = 'Completed'
			if data['has_clearing']:
				data['row']['status'] = 'To Clear'
				self.clear_voucher(row, data)
				if data['clearing_jv']:
					data['row']['status'] = 'Completed'
			row.update(data['row'])

		frappe.msgprint('Number of rows processed: %s <br>\
						View postings: %s'%(posted,self.postings_link),
						indicator='red')
		
		self.save()

	@property
	def open_txns(self):
		if not self.get('_open_txns'):
			self._open_txns = []
			vss = frappe.get_doc('Voucher Search Specifications')
			vss_vouchers = vss.get_voucher_fields()
			txns = frappe.db.sql("select name, account, \
				(sum(debit)-sum(credit)) as `amount`, against_voucher,\
				against_voucher_type from `tabGL Entry` where \
				against_voucher_type IS NOT NULL group by \
				against_voucher", as_dict=1)
			for txn in txns:
				if txn.amount == 0:
					continue
				if txn.against_voucher_type not in vss_vouchers:
					continue
				dt,dn = txn.against_voucher_type,txn.against_voucher
				doc = frappe.get_value(dt,dn,vss_vouchers[dt], as_dict=1)
				txn.voucher_search_key = vss.get_search_key(doc, dt)
				self._open_txns.append(txn)
		return self._open_txns

	@property
	def postings_link(self):
		return """<a onclick='
			frappe.route_options = {"cheque_no": "%s"};
			frappe.set_route("List", "Journal Entry");'
			target='_self'>Journal Entry</a>"""%self.name
	

	def clear_voucher(self, row, data):
		data['clearing_jv'] = None
		match = next((x for x in self.open_txns if \
					  x.voucher_search_key in \
					  row.transaction_description), None)
		if match:
			field = 'gl_debit_account' if match.amount > 0 else \
					'gl_credit_account'
			data['row'][field] = match.account
			print match
			# clear document outstanding
			pass

	def get_posting_data(self, statement_item, data):
		done = []
		data['has_clearing'] = False
		txn_type = frappe.get_doc('Bank Transaction Type',
						statement_item.transaction_type)
		for row in txn_type.journal_template:
			if row.clear_third_party_item:
				data['has_clearing'] = True
			if row.dr_or_cr in done:
				continue
			if row.dr_or_cr == 'DR':
				data['row']['jl_debit_account'] = row.account
			elif row.dr_or_cr == 'CR':
				data['row']['jl_credit_account'] = row.account
			done.append(row.dr_or_cr)

	def make_jv(self, data):
		journal_entry = frappe.new_doc('Journal Entry')
		journal_entry.posting_date = frappe.utils.getdate()
		journal_entry.cheque_no = self.name
		journal_entry.cheque_date = frappe.utils.getdate()
		journal_entry.company = frappe.get_value('Bank',self.bank,'company')
		# credit
		journal_entry.append('accounts',{
			'account':data['row']['jl_credit_account'],
			'credit_in_account_currency':data['amount'],
			'debit_in_account_currency': 0.0,
		})
		# debit
		journal_entry.append('accounts',{
			'account':data['row']['jl_debit_account'],
			'debit_in_account_currency': data['amount'],
			'credit_in_account_currency': 0.0,
		})
		
		journal_entry.save(ignore_permissions=True)
		journal_entry.submit()
		data['posting_jv'] = journal_entry.name

	def get_gl_entries(self, voucher):
		return frappe.db.sql("SELECT account,credit,debit FROM \
			`tabGL Entry` WHERE against_voucher = '{}' AND \
			against_voucher_type = '{}'".format(voucher.name,
				voucher.doctype), as_dict=1)

def get_source_abbr(source_field, bank_statement_mapping_items):
	for row in bank_statement_mapping_items:
		if row.source_field == source_field:
			return row.source_field_abbr
	
def reformat_date(date_string, from_format):
	if date_string and from_format:
		return datetime.datetime.strptime(date_string, from_format).strftime('%Y-%m-%d')

def get_ret_msg(ret_list):
	if not ret_list: return
	for i in ret_list:
		if len(i.get('matches')) == 0:
			frappe.msgprint('No match was found for item in row {} \n'.format(i.get('row')))
			continue
		ret_msg = ''
		ret_msg += 'Multiple matches were found for item in row {} \n'.format(i.get('row'))
		for match in i.get('matches'):
			ret_msg += '<ul> {} </ul>'.format(match.get('name'))
		frappe.msgprint(ret_msg)


def get_txn_type(self, idx, itm):
	'''search transaction_description to match transaction type'''

	itm = frappe._dict(itm)
	ret_list = []
	match_type = []
	
	txn_type_derivation = frappe.db.get_value("Bank Statement Format",
		self.bank_statement_format, 'txn_type_derivation')
	
	if txn_type_derivation != "Derive Using Bank Transaction Type":
		return
	if itm.credit_amount:
		DR_or_CR = 'CR'
	elif itm.debit_amount:
		DR_or_CR = 'DR'
	else:
		DR_or_CR = None
	
	bnks_txn_types = frappe.get_all('Bank Transaction Type',
		filters={'bank_statement_format': self.bank_statement_format,
				 'debit_or_credit': DR_or_CR},
		fields=['name', 'transaction_type_match_expression',
				'ignore_case', 'multi_line', 'dot_all'])
	
	for txn_type in bnks_txn_types:
		re_flag = 0
		for i,d in [('ignore_case', re.I), ('dot_all', re.S), ('multi_line', re.M)]:
			if txn_type.get(i): re_flag = re_flag | d

		txn_match = search_text(txn_type.transaction_type_match_expression, itm.transaction_description, flags=re_flag)
		if txn_match:
			match_type.append(txn_type)

	if len(match_type) != 1:
		ret_list.append({'row': idx, 'matches': match_type})
		get_ret_msg(ret_list)
		return
	return match_type[0].name

def get_open_third_party_documents_using_search_fields(search_fields, txn,
		allocated_entries=[]):
	""" search for documents with txn.description and search_fields"""
	
	from _mysql_exceptions import OperationalError
	from frappe.exceptions import ValidationError
	from erpnext.accounts.doctype.payment_request.payment_request import get_amount

	matches, found_documents = [],[]
	result = frappe.db.sql("select name, account, against_voucher, \
		against_voucher_type from `tabGL Entry` where \
		against_voucher_type IS NOT NULL", as_dict=1)
	if not result:
		return

	for s_field in search_fields:

		try:
			for res in result:
				if res.name in allocated_entries:
					continue
				
				res.update(frappe.get_value(res.against_voucher_type,
							res.against_voucher, '*'))
				
				found = search_text(txn_match, txn.transaction_description, 26)
				match_pair = check_statement_item(txn, res, s_field.field_name)
			
				# check mandatory search fields
				if s_field.mandatory and not match_pair:
					continue
				if not (found or match_pair):
					continue
				if match_pair and match_pair not in matches:
					matches.append(match_pair)

				ret_dict = frappe._dict({
					'doc':frappe.get_doc(dt,dn),
					'account':res.account,
					'gl_entry': res.name
				})
				found_docs_tuple = [(f.account, f.gl_entry) for \
										f in found_documents]
				if (ret_dict.account, ret_dict.gl_entry) not in found_docs_tuple:
					found_documents.append(ret_dict)
		except (OperationalError, ValidationError) as e:
			continue
	return found_documents


def get_account_types():
	acc_dt = frappe.get_doc('DocType', 'Account')
	field = [f for f in acc_dt.get('fields') if f.get('fieldname') == 'account_type'][0]
	return field.get('options')

def search_text(text, base_text, flags=0):
	'''Search base_text for occurences of text
	words can be matched on any order and seperated by - _ space or . '''
	import re

	if not text or not base_text: return

	if not isinstance(base_text, basestring):
		base_text = str(base_text)
	text = isinstance(text, basestring) and text or str(text)

	if is_float(text):
		if is_float(text).is_integer():
			text = str(int(float(text)))

	search_lst = re.findall(r"[\w'\\\._-]+", text.replace('.', r'\.')) # split according to words including back slash
	search_grp = ['(?:{})'.format(x) for x in search_lst] # create re search groups like (?:xyz)
	search_txt = '|'.join(search_grp)  # check for any occurences with or operator |
	search_txt = r'(?:{}|[\s\B._-])+'.format(search_txt)  # a search group within another group 
	found = re.findall(search_txt, base_text, flags=flags) or []

	txt_lst = [x.replace('\\','') for x in search_lst]    # remove the backslashes
	min_len = txt_lst and len(sorted(txt_lst, key=len)[0]) or 1
	found = [x.strip() for x in found if isinstance(x, basestring) and len(x)>=min_len]

	match = all([txt.lower() in ' '.join(found).lower() for txt in txt_lst])
	if match:
		return found


def is_float(value):
	try:
		return float(value)
	except (ValueError, TypeError):
		return False

def check_statement_item(txn, result, search_field):
	match_pair = dict()
	search_field = frappe.scrub(search_field)
	txn_match = result.get(search_field)
	sta_format = frappe.db.get_value(txn.parenttype, txn.parent, 'bank_statement_format')
	
	sta_itm_fields = frappe.db.sql("""select target_field from
		`tabBank Statement Mapping Item` where parent = '{}'
		""".format(sta_format))
	sta_itm_fields = [frappe.scrub(x[0]) for x in sta_itm_fields]
		
	for field in sta_itm_fields:
		field_val = txn.get(field)
		if is_float(txn_match) and is_float(field_val):
			#remove decimals by converting to int
			txn_match = int(float(txn_match) * 100)
		if is_float(txn.get(field)):
			field_val = int(float(field_val) * 100)
		if str(txn_match) == str(field_val):
			match_pair = {search_field: result.get(search_field)}

	return match_pair