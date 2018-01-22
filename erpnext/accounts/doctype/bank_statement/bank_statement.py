# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, csv, datetime, os, re
from frappe import _
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
		if not self.previous_bank_statement: self.fill_previous_statement()

	def validate_dates(self):
		previous_sta = frappe.get_all("Bank Statement", fields=['statement_end_date','bank','account_no', 'name'],
						filters={'name': ['!=', getattr(self,'name',"")], 'creation': ['<', getattr(self,'creation',get_datetime())]})
		end_dates = [(s.name,s.statement_end_date) for s in previous_sta if (s.bank == self.bank \
			and s.account_no == self.account_no and s.statement_end_date >= getdate(self.statement_start_date))]
		end_dates = filter(lambda x: isinstance(x[1], datetime.date), end_dates)
		if end_dates:
			previous_statement_end_date = sorted(end_dates, key=lambda x:x[1], reverse=True)[0]
			if getdate(self.statement_start_date) > getdate(self.statement_end_date):
				frappe.throw(_("Statement start date cannot be later than end date"))
			if getdate(self.statement_start_date) <= previous_statement_end_date[1]:
				prev_doc_name = previous_statement_end_date[0]
				frappe.throw(_("Statement start date cannot be same as or earlier than a previous statement's end date ({})".format(prev_doc_name)))

	def check_end_date(self):
		previous_sta = frappe.get_all("Bank Statement", fields=['statement_start_date','bank','account_no'])
		end_dates = [s.statement_start_date for s in previous_sta if (s.bank == self.bank and s.account_no == self.account_no)]
		for e_date in end_dates:
			date_interval = date_diff(self.statement_start_date, e_date)
			if date_interval > 1:      # if start date is greater than an end date by a day
				return {'gap': date_interval}
		return {'gap': False}

	def fill_previous_statement(self):
		previous_sta = []
		all_previous_sta = frappe.get_all("Bank Statement", fields=['statement_end_date','bank','account_no', 'name'],
							filters={'name': ['!=', getattr(self,'name',"")]}, order_by='creation')
		for sta in all_previous_sta:
			if (sta.bank == self.bank) and (sta.account_no == self.account_no) and (getdate(self.statement_start_date) >= sta.statement_end_date):
				previous_sta.append(sta)
		if not previous_sta: return

		if len(previous_sta) > 1:
			previous_sta.sort(key=lambda x: x.statement_end_date, reverse=True)

		self.previous_bank_statement = previous_sta[0].name

	def check_file_format(self, csv_header_list):
		sta_format = frappe.get_doc("Bank Statement Format",self.bank_statement_format)
		source_fields = set(s.source_field for s in sta_format.bank_statement_mapping_item)
		if not (set(csv_header_list) >= source_fields):
			frappe.msgprint(_("The attached statement does not contain all the columns specified in the format selected"))

	def convert_to_internal_format(self, csv_column_header, csv_row_field_value, bank_statement_mapping_items, eval_data):
		""" select mapping row to be used """
		mapping_row = None
		for row in bank_statement_mapping_items:
			if row.source_field == csv_column_header:
				mapping_row = row
		if not mapping_row: return

		if not (mapping_row.source_field_abbr or mapping_row.transformation_rule):
			return mapping_row.target_field, csv_row_field_value
		transformation_rule = mapping_row.source_field_abbr.strip() if not mapping_row.transformation_rule else mapping_row.transformation_rule.strip()
		csv_row_field_value = self.eval_transformation(transformation_rule, mapping_row.source_field_abbr.strip(), eval_data)
		eval_data[mapping_row.target_field_abbr.strip()] = csv_row_field_value

		return mapping_row.target_field, csv_row_field_value

	def fill_table(self):
		if not self.file: return
		file_doc = frappe._dict()
		self.bank_statement_items = []
		bank_statement_mapping_items = frappe.get_doc("Bank Statement Format", self.bank_statement_format).bank_statement_mapping_item
		file_id = frappe.db.sql("""SELECT name FROM tabFile WHERE attached_to_doctype = '{0}' AND attached_to_name = '{1}'
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

		csv_header_list = rows[0]
		data_rows = rows[1:]

		self.check_file_format(csv_header_list)

		intermediate_bank_statement_items = []
		# create a list of maps, intermediate_bank_statement_items, to hold bank statement items based on internal
		# representation see "Bank Statement Item" definition
		for statement_row in data_rows:
			bank_sta_item = dict()
			eval_data = self.get_data_for_eval(statement_row, csv_header_list, bank_statement_mapping_items)
			for column_index, column_value in enumerate(statement_row):
				column_value = str(column_value) if column_value else None
				itm = self.convert_to_internal_format(csv_header_list[column_index], column_value, bank_statement_mapping_items, eval_data)
				if not itm: continue
				target_field, eval_result = itm
				bank_sta_item[frappe.scrub(target_field)] = eval_result
			intermediate_bank_statement_items.append(bank_sta_item) if bank_sta_item else None

		for idx, sta in enumerate(intermediate_bank_statement_items):
			sta['transaction_type'] = get_txn_type(self, idx+1, sta)
			self.append('bank_statement_items', sta)  # create bank_statement_item table entries

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

	def get_data_for_eval(self, statement_row, csv_header_list, bank_statement_mapping_items):
		'''Returns data object for evaluating formula'''
		data = frappe._dict()
		for column_index, column_value in enumerate(statement_row):
			source_abbr = get_source_abbr(csv_header_list[column_index], bank_statement_mapping_items)
			if not source_abbr: continue
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

	def process_statement(self):
		allocated_entries = []
		processed_rows = []
		for bank_statement_item in self.bank_statement_items:
			if not bank_statement_item.transaction_type: continue
			txn_type = frappe.get_doc('Bank Transaction Type', bank_statement_item.transaction_type)
			if txn_type.debit_account_party_type:
				# create new item in bank_statement_item.third_party_journal_items
				# set debit_account_type of newly created third_party_journal_item to 
				# bank_statement_item.txn_type.debit_account_party_type
				if not txn_type.debit_account:
					dr_open_items = get_open_third_party_documents_using_search_fields(
						txn_type.search_fields_third_party_doc_dr, bank_statement_item, allocated_entries
					)
					print '\n\n\n', 'dr_open_items: \n', dr_open_items, '\n\n\n'
					if len(dr_open_items) >= 1:
						print '\n\n\n', 'dr_open_items[0]: \n', dr_open_items[0], '\n\n\n'
						# set debit_account of of newly created third_party_journal_item to
						# dr_open_items[0].third_party
						bank_statement_item.jl_credit_account = dr_open_items[0].account
						allocated_entries.append(dr_open_items[0].gl_entry)
						processed_rows.append(str(bank_statement_item.idx))
					else:
						continue
				else:
					# set debit_account of of newly created third_party_journal_item to
					# bank_statement_item.txn_type.debit_account
					bank_statement_item.jl_credit_account = txn_type.debit_account

			if txn_type.credit_account_party_type:
				# create new item in bank_statement_item.third_party_journal_items
				# set credit_account_type of newly created third_party_journal_item to
				# bank_statement_item.txn_type.credit_account_party_type
				if not txn_type.credit_account:
					cr_open_items = get_open_third_party_documents_using_search_fields(
						txn_type.search_fields_third_party_doc_cr, bank_statement_item, allocated_entries
					)
					print '\n\n\n', 'cr_open_items: \n', cr_open_items, '\n\n\n'
					if len(cr_open_items) >= 1:
						print '\n\n\n', 'cr_open_items[0]: \n', cr_open_items[0], '\n\n\n'
						# set credit_account of of newly created third_party_journal_item to
						# cr_open_items[0].third_party
						bank_statement_item.jl_credit_account = cr_open_items[0].account
						bank_statement_item.jl_credit_account_type = frappe.db.get_value(
							'Account', cr_open_items[0].account,'account_type')
						allocated_entries.append(cr_open_items[0].gl_entry)
						processed_rows.append(str(bank_statement_item.idx))
					else:
						continue
			else :
				# set credit_account of of newly created third_party_journal_item to
				# bank_statement_item.txn_type.credit_account
				bank_statement_item.jl_credit_account = txn_type.credit_account
		if processed_rows:
			frappe.msgprint('The following rows were processed: <br> row {}'.format(', '.join(processed_rows)))
		else:
			frappe.msgprint('0 rows processed', indicator='red')
		self.save()

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
	txn_type_derivation = frappe.db.get_value("Bank Statement Format", self.bank_statement_format, 'txn_type_derivation')
	if not txn_type_derivation == "Derive Using Bank Transaction Type": return
	match_type = []
	if itm.credit_amount:
		DR_or_CR = 'CR'
	elif itm.debit_amount:
		DR_or_CR = 'DR'
	else:
		DR_or_CR = None
	bnks_txn_types = frappe.get_all('Bank Transaction Type',
							filters={'bank_statement_format': self.bank_statement_format, 'debit_or_credit': DR_or_CR},
							fields=['name', 'transaction_type_match_expression', 'ignore_case', 'multi_line', 'dot_all'])
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

def make_query(pairs):
	if not isinstance(pairs, list): return ''
	query = ''
	for pair in pairs:
		if not isinstance(pair, dict): continue
		for key in pair:
			if isinstance(pair[key], basestring):
				query += " and {0} = '{1}'".format(key, pair[key])
				continue
			query += " and {0} = {1}".format(key, pair[key])
	return query

def get_open_third_party_documents_using_search_fields(search_fields, txn, allocated_entries=[]):
	from _mysql_exceptions import OperationalError
	from frappe.exceptions import ValidationError
	from erpnext.accounts.doctype.payment_request.payment_request import get_amount

	print_variables(['search_fields', 'txn.__dict__', 'allocated_entries'], locals())

	matches = []
	found_documents = []
	sta_format = frappe.db.get_value(txn.parenttype, txn.parent, 'bank_statement_format')
	sta_itm_fields = frappe.db.sql("select target_field from `tabBank Statement Mapping Item` \
									where parent = '{}'".format(sta_format))
	sta_itm_fields = [frappe.scrub(x[0]) for x in sta_itm_fields]
	for s_field in search_fields:
		#search for all documents in general ledger where outstanding amount <> 0 and value of search_field in document is 
		#contained in txn_description. Append result to found_documents
		search_field = '_'.join(s_field.field_name.replace(' ','_').split(' ')).lower()
		try:
			query = """select name, account, against_voucher,against_voucher_type,{0} from `tabGL Entry` where
							against_voucher_type IS NOT NULL{1}""".format(search_field, make_query(matches))
			result = frappe.db.sql(query, as_dict=1)

			print_variables(['s_field.__dict__', 'search_field', 'matches', 'query', 'result'], locals())

			if not result: continue
			for res in result:
				if res.name in allocated_entries: continue
				dt,dn = res.against_voucher_type, res.against_voucher

				# this throws an error if the amount is not greater than 0
				#amt_outstanding = get_amount(frappe.get_doc(dt,dn), dt)

				# match the search field content in any order, can be separated by space or underscore('pet cat' or 'cat_pet')
				# avoid using '.' or - in searches, to avoid conflict with re operation
				txn_match = res.get(search_field)
				found = search_text(txn_match, txn.transaction_description)

				match_pair = dict()

				for field in sta_itm_fields:
					field_val = txn.get(field)
					if is_float(txn_match) and is_float(field_val): txn_match = int(float(txn_match) * 100)
					if is_float(txn.get(field)): field_val = int(float(field_val) * 100)
					if str(txn_match) == str(field_val):
						match_pair = {search_field: res.get(search_field)}
						if not match_pair in matches: matches.append(match_pair)


				print_variables(['res', 'txn_match', 'match_pair', 'found'], locals())

				# check mandatory search fields
				if s_field.mandatory and not match_pair: continue
				if not (found or match_pair): continue

				ret_dict = frappe._dict({'doc':frappe.get_doc(dt,dn), 'account':res.account, 'gl_entry': res.name})
				found_docs_tuple = [(f.account, f.gl_entry) for f in found_documents]
				if not (ret_dict.account, ret_dict.gl_entry) in found_docs_tuple: found_documents.append(ret_dict)
		except OperationalError, ValidationError:
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

	if not isinstance(base_text, basestring): base_text = str(base_text)
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
	if match: return found

def print_variables(var_list, local={}):
	'''Print list of variable to terminal'''
	if not isinstance(var_list, list): return
	if not isinstance(local, dict): local = local()
	for var in var_list:
		name = var
		var = local.get(name)
		if '.' in name:
			var = local.get(name.split('.')[0])
			for atr in name.split('.')[1:]:
				var = getattr(var, atr, None)
				if '()' in atr: var = getattr(var, atr, None)()
			name = name.split('.')[0]
		print '\n\n', '{}: \n'.format(name), var, '\n\n'

def is_float(value):
	try:
		return float(value)
	except (ValueError, TypeError):
		return False