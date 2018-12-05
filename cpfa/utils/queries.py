from __future__ import unicode_literals
import frappe
from frappe.desk.reportview import get_match_cond, get_filters_cond


 # searches for active employees
def docfield_query(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	return frappe.db.sql("""select fieldname, label, fieldtype from `tabDocField`
		where fieldtype not like '%%break%%'
			and ({key} like %(txt)s
				or label like %(txt)s)
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, fieldname), locate(%(_txt)s, fieldname), 99999),
			if(locate(%(_txt)s, label), locate(%(_txt)s, label), 99999),
			idx desc,
			fieldname, label
		limit %(start)s, %(page_len)s""".format(**{
			'key': searchfield,
			'fcond': get_filters_cond(doctype, filters, conditions),
			'mcond': get_match_cond(doctype)
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})