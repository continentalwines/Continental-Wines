from odoo import models, fields, api, _
from datetime import datetime

class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    gjs_tags_logo = fields.Image(string="Company Logo")
    gjs_company_name = fields.Char(string="Company Name")
    gjs_address = fields.Text(string="Address")
    gjs_bank_information = fields.Text(string="Bank Information")
    gjs_bank_qr_code = fields.Image(string="Bank QR Code")

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_address_format(self):
        if self.env.context.get('customer_statement'):
            return """
                %(street)s
                %(street2)s %(city)s %(state_code)s %(zip)s %(country_name)s
            """
        return super(ResPartner, self)._get_address_format()

    def _get_statement_company(self):
        return self and self[0].company_id or self.env.company

    def _get_report_customer_statement_filename(self):
        self.ensure_one()
        today = datetime.strftime(datetime.now(), '%d%m%Y')
        return '%s-%s' % (self.name, today)

    def _get_aged_receivable_data(self):
        self.ensure_one()
        data = []
        ar = self.env.ref('account_reports.aged_receivable_report')
        options_dict = {}
        options = ar.get_options(options_dict)
        options['unfold_all'] = True
        options['partner'] = True
        options['partner_ids'] = [self.id]
        options['selected_partner_ids'] = [self.commercial_partner_id.name]
        ar_model = self.env['account.aged.receivable.report.handler']
        rslt = ar_model._aged_partner_report_custom_engine_common(
            options, 'asset_receivable', 'partner_id', 'id')
        for r in rslt:
            if len(r) <= 1 or not isinstance(r[1], dict):
                continue
            data.append(r[1])
        return data

    def _get_studio_po_number_field(self):
        so_fields = self.env['sale.order']._fields.keys()
        for sof in so_fields:
            if 'po_number' in sof:
                return sof
        return False
