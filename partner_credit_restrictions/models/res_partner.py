from odoo import models, fields, api
from datetime import timedelta
import logging

# Logger para depuración y seguimiento de bloqueos de clientes
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    """
    Extiende res.partner para agregar lógica de bloqueo de clientes
    con facturas vencidas por más de 20 días.
    """
    _inherit = 'res.partner'

    blocked = fields.Boolean(string='Bloqueado', default=False)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        """
        Al crear un partner, verifica automáticamente si debe ser bloqueado
        por facturas vencidas (lógica centralizada en check_invoices_overdue).
        """
        record = super(ResPartner, self).create(vals)
        record.check_invoices_overdue()
        return record

    def write(self, vals):
        """
        Al editar un partner, vuelve a verificar el estado de bloqueo
        (por si cambia algo relevante: vat, facturas, etc.).
        """
        res = super(ResPartner, self).write(vals)
        self.check_invoices_overdue()
        return res

    def check_invoices_overdue(self):
        """
        Bloquea al cliente si tiene alguna factura vencida (más de 20 días),
        ignorando facturas canceladas o pagadas.
        Busca por RUC y compañía para incluir relaciones entre partners.

        También agrega un log para seguimiento.
        """
        today = fields.Date.today()
        for partner in self:
            # Buscar todos los partners relacionados por RUC y compañía
            related_partners = self.env['res.partner'].search([
                ('vat', '=', partner.vat),
                ('company_id', '=', partner.company_id.id)
            ])

            # Buscar facturas vencidas, solo facturas confirmadas, hace +20 días
            overdue_invoices = self.env['account.move'].search([
                ('partner_id', 'in', related_partners.ids),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),  # Solo facturas confirmadas
                ('invoice_date_due', '<=', today - timedelta(days=20)),  # Hace más de 20 días
                ('payment_state', 'not in', ['paid', 'reversed'])  # No pagadas ni anuladas
            ])
            
            # True si hay facturas vencidas
            is_blocked = bool(overdue_invoices)

            # Log para auditoría y debugging
            _logger.info(
                f"Cliente: {partner.name}, Facturas Vencidas: {len(overdue_invoices)}, Bloqueado: {is_blocked}"
            )
            
            # Solo actualizar si cambia el estado (evita loops y escribe menos en DB)
            if partner.blocked != is_blocked:
                partner.blocked = is_blocked
