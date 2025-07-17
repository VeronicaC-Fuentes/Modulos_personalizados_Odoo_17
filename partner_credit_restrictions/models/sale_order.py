# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round
import logging

_logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Sale Order Line
# ------------------------------------------------------------------
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    estado_producto = fields.Selection(
        [('ganado', 'Ganado'), ('perdido', 'Perdido')],
        string="Estado del Producto",
        default='ganado',
        help="Indica si este producto está GANADO o PERDIDO"
    )
    authorized_below_cost = fields.Boolean(
        string='Autorizado por debajo del costo',
        help='Venta por debajo del costo autorizada'
    )

    def write(self, vals):
        for line in self:
            if line.product_id and line.product_id.type == 'product':
                cost = line.product_id.standard_price
                if line.order_id.currency_id != line.product_id.currency_id:
                    cost = line.product_id.currency_id._convert(
                        cost,
                        line.order_id.currency_id,
                        line.company_id,
                        line.order_id.date_order or fields.Date.today(),
                    )
                new_price = vals.get('price_unit', line.price_unit)
                if (
                    new_price < cost
                    and not vals.get('authorized_below_cost', line.authorized_below_cost)
                ):
                    raise UserError(_(
                        'No se puede guardar la cotización. El precio de venta '
                        'del producto %s es menor que su costo y no ha sido autorizado.'
                    ) % line.product_id.display_name)
        return super().write(vals)


# ------------------------------------------------------------------
# Sale Order
# ------------------------------------------------------------------
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('to_approve', 'To Approve'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Approval State', readonly=True, copy=False,
        default='draft', tracking=True)
    reference_quotation = fields.Char(string="Referencia de Cotización")

    # ---------------- helpers ----------------
    def _get_won_lines(self):
        self.ensure_one()
        return self.order_line.filtered(
            lambda l: l.estado_producto == 'ganado'
            and l.product_id
            and l.product_id.type in ['product', 'service', 'consu']
        )

    def _won_amount_company(self):
        """Subtotal SIN IGV de líneas GANADAS en moneda de compañía."""
        self.ensure_one()
        cc = self.company_id.currency_id
        total = 0.0
        for line in self._get_won_lines():
            subtotal = line.price_subtotal  # sin impuestos
            total += line.currency_id._convert(
                subtotal, cc, self.company_id,
                self.date_order or fields.Date.today()
            )
        return float_round(total, precision_rounding=cc.rounding)

    # ------------- validación de crédito SOLO GANADO -------------
    def _check_credit_limit_won(self):
        for order in self:
            # Sólo usamos el campo credit_limit (Float) — no referenciamos más property_credit_limit
            limit = order.partner_id.credit_limit or 0.0
            if not limit:
                continue

            won_amt = order._won_amount_company()
            currency = order.company_id.currency_id

            if won_amt > limit:
                raise ValidationError(_(
                    'El cliente %(p)s ha excedido su límite de crédito.\n\n'
                    'Límite: %(l)s   Importe Ganado: %(a)s'
                ) % {
                    'p': order.partner_id.display_name,
                    'l': f"{limit:,.2f} {currency.symbol}",
                    'a': f"{won_amt:,.2f} {currency.symbol}",
                })

    # ---------------- lógica GANADO / PERDIDO ----------------
    def _crear_ov_ganada(self):
        """Crea y confirma una OV con solo GANADOS; devuelve el registro."""
        self.ensure_one()
        won_lines = self._get_won_lines()
        if not won_lines:
            raise UserError(_("No hay productos GANADOS."))

        vals = {
            'partner_id': self.partner_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'warehouse_id': self.warehouse_id.id,
            'pricelist_id': self.pricelist_id.id,
            'company_id': self.company_id.id,
            'reference_quotation': self.name,
            'order_line': [
                (0, 0, {
                    'product_id': l.product_id.id,
                    'product_uom_qty': l.product_uom_qty,
                    'price_unit': l.price_unit,
                    'estado_producto': 'ganado',
                }) for l in won_lines
            ],
        }
        ov = self.env['sale.order'].create(vals)
        ov.with_context(bypass_validation=True).action_confirm()
        return ov

    # ---------------- acción CONFIRMAR ----------------
    def action_confirm(self):
        if self.env.context.get('bypass_validation'):
            return super().action_confirm()

        for order in self:
            order.partner_id.check_invoices_overdue()
            # facturas vencidas
            if order.partner_id.blocked:
                order.approval_state = 'to_approve'
                raise UserError(_(
                    "El cliente tiene facturas vencidas > 20 días. "
                    "Necesita aprobación."
                ))

            # precio < costo (ya comprobado en write)
            # crédito sobre GANADOS
            order._check_credit_limit_won()

            # genera OV
            ov = order._crear_ov_ganada()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Orden de Venta Generada',
                    'message': f'Se generó la OV {ov.name}',
                    'sticky': False,
                }
            }
        return super().action_confirm()

    # ---------------- acción APROBAR ----------------
    def action_approve(self):
        if not self.env.user.has_group(
            'partner_credit_restrictions.group_custom_sale_approval'
        ):
            raise UserError(_("No tienes permisos para aprobar esta orden."))

        for order in self:
            order.partner_id.check_invoices_overdue()
            if not order.partner_id.blocked:
                raise UserError(_("Ya no hay facturas vencidas; no requiere aprobación."))

            # Si el cliente sigue bloqueado, liberamos y seguimos
            order.partner_id.blocked = False
            order.approval_state = 'sale'

            # Validamos crédito sobre GANADOS y generamos OV
            order._check_credit_limit_won()
            ov = order._crear_ov_ganada()

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Orden de Venta Aprobada',
                    'message': f'Se generó y confirmó la OV {ov.name}',
                    'sticky': False,
                }
            }

    # ---------------- reactivación ---------------
    def action_reactivate_sale(self):
        for order in self:
            if order.state != 'cancel':
                raise UserError(_("Solo las órdenes canceladas pueden reactivarse."))
            order.state = 'sale'
            _logger.info("Orden %s reactivada a 'sale'", order.name)

