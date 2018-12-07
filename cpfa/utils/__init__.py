from __future__ import unicode_literals
import frappe


def get_pdf_link(doctype, docname, print_format='Standard', no_letterhead=0):
	return '/api/method/frappe.utils.print_format.download_pdf?doctype={doctype}&name={docname}&format={print_format}&no_letterhead={no_letterhead}'.format(
		doctype = doctype,
		docname = docname,
		print_format = print_format,
		no_letterhead = no_letterhead
	)

@frappe.whitelist()
def validate_link():
	"""validate link when updated by user"""
	import frappe
	import frappe.utils

	value, options, fetch = frappe.form_dict.get('value'), frappe.form_dict.get('options'), frappe.form_dict.get('fetch')

	# no options, don't validate
	if not options or options=='null' or options=='undefined':
		frappe.response['message'] = 'Ok'
		return

	if value == 'name':
		frappe.response['valid_value'] = 'name'
		frappe.response['message'] = 'Ok'
		return

	valid_value = frappe.db.sql("select fieldname from `tab%s` where fieldname=%s" % (frappe.db.escape(options),
		'%s'), (value,))

	if valid_value:
		valid_value = valid_value[0][0]

		# get fetch values
		if fetch:
			# escape with "`"
			fetch = ", ".join(("`{0}`".format(frappe.db.escape(f.strip())) for f in fetch.split(",")))

			frappe.response['fetch_values'] = [frappe.utils.parse_val(c) \
				for c in frappe.db.sql("select %s from `tab%s` where name=%s" \
					% (fetch, frappe.db.escape(options), '%s'), (value,))[0]]

		frappe.response['valid_value'] = valid_value
		frappe.response['message'] = 'Ok'
