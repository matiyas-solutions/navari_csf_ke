import frappe
from erpnext.accounts.doctype.sales_invoice import sales_invoice as erpnext_sales_invoice
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_mode_of_payments_info
from frappe import _
from frappe.utils import get_link_to_form


def custom_update_multi_mode_option(doc, pos_profile):
	def append_payment(payment_mode):
		payment = doc.append("payments", {})
		payment.default = payment_mode.default
		payment.mode_of_payment = payment_mode.mop
		payment.account = payment_mode.default_account
		payment.type = payment_mode.type

	doc.set("payments", [])
	invalid_modes = []
	mode_of_payments = [d.mode_of_payment for d in pos_profile.get("payments")]
	mode_of_payments_info = get_mode_of_payments_info(mode_of_payments, doc.company)

	for row in pos_profile.get("payments"):
		payment_mode = mode_of_payments_info.get(row.mode_of_payment)
		if not payment_mode:
			invalid_modes.append(get_link_to_form("Mode of Payment", row.mode_of_payment))
			continue

		payment_mode.default = row.default
		append_payment(payment_mode)

	if invalid_modes:
		if invalid_modes == 1:
			msg = _("Please set default Cash or Bank account in Mode of Payment {}")
		else:
			msg = _("Please set default Cash or Bank account in Mode of Payments {}")
		frappe.throw(msg.format(", ".join(invalid_modes)), title=_("Missing Account"))


erpnext_sales_invoice.update_multi_mode_option = custom_update_multi_mode_option
