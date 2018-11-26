from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Bank Statement"),
			"items": [
				{
					"type": "doctype",
					"name": "Bank Statement",
					"label": _("Bank Statement"),
					"description": _("Bank Statement")
				},
				{
					"type": "doctype",
					"name": "Bank Transaction Type",
					"label": _("Bank Transaction Type"),
					"description": _("Bank Transaction Type")
				},
				{
					"type": "doctype",
					"name": "Bank Statement Format",
					"label": _("Bank Statement Format"),
					"description": _("Bank Statement Format")
				},
				{
					"type": "doctype",
					"name": "Bank",
					"label": _("Bank"),
					"description": _("Bank")
				}
			]
		}
	]
