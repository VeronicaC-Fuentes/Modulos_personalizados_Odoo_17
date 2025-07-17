from odoo import models, fields, api
from datetime import timedelta
import logging

# Definir _logger para usar en mensajes de depuración
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    blocked = fields.Boolean(string='Bloqueado', default=False)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        record = super(ResPartner, self).create(vals)
        record.check_invoices_overdue()
        return record

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        self.check_invoices_overdue()
        return res

    def check_invoices_overdue(self):
        today = fields.Date.today()
        for partner in self:
            # Buscar socios relacionados con el mismo RUC
            related_partners = self.env['res.partner'].search([
                ('vat', '=', partner.vat),
                ('company_id', '=', partner.company_id.id)
            ])

            # Buscar facturas vencidas, excluyendo las canceladas
            overdue_invoices = self.env['account.move'].search([
                ('partner_id', 'in', related_partners.ids),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),  # Solo facturas confirmadas
                ('invoice_date_due', '<=', today - timedelta(days=20)),  # Hace más de 20 días
                ('payment_state', 'not in', ['paid', 'reversed'])  # Excluir pagadas o anuladas
            ])
            
            # Determinar si debe bloquearse
            is_blocked = bool(overdue_invoices)

            # Agregar logs para depuración
            _logger.info(
                f"Cliente: {partner.name}, Facturas Vencidas: {len(overdue_invoices)}, Bloqueado: {is_blocked}"
            )
            
            # Actualizar solo si cambia el estado
            if partner.blocked != is_blocked:
                partner.blocked = is_blocked
