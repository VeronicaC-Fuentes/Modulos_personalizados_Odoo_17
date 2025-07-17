from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

DOCS_COMPANY = ['6', '0']
DOCS_PERSON  = ['1', '4', '7']

class ResPartner(models.Model):
    _inherit = "res.partner"

    # Contacto Comercial
    comercial_nombre = fields.Char(string="Nombre contacto comercial", required=True)
    comercial_email = fields.Char(string="Email contacto comercial", required=True)
    comercial_telefono = fields.Char(string="Teléfono contacto comercial", required=True)
    comercial_direccion = fields.Char(string="Dirección contacto comercial", required=True)

    # Tesorería
    tesoreria_nombre = fields.Char(string="Nombre contacto tesorería", required=True)
    tesoreria_email = fields.Char(string="Email contacto tesorería", required=True)
    tesoreria_telefono = fields.Char(string="Teléfono contacto tesorería", required=True)
    tesoreria_direccion = fields.Char(string="Dirección contacto tesorería", required=True)

    # Logística
    logistica_nombre = fields.Char(string="Nombre contacto logística")
    logistica_email = fields.Char(string="Email contacto logística")
    logistica_telefono = fields.Char(string="Teléfono contacto logística")
    logistica_direccion = fields.Char(string="Dirección contacto logística")

    # Otros contactos
    otros_nombre = fields.Char("Nombre contacto otros")
    otros_direccion = fields.Char("Dirección contacto otros")
    otros_email = fields.Char("Email contacto otros")
    otros_telefono = fields.Char("Teléfono contacto otros")

    company_id = fields.Many2one(
        'res.company',
        string="Compañía",
        default=lambda self: self.env.company.id
    )

    @api.constrains("is_company", "l10n_latam_identification_type_id")
    def _check_ident_type_vs_company(self):
        for rec in self.filtered("l10n_latam_identification_type_id"):
            code = rec.l10n_latam_identification_type_id.l10n_pe_vat_code
            if rec.is_company and code not in DOCS_COMPANY:
                raise ValidationError(_("Una compañía solo puede tener RUC o VAT."))
            if not rec.is_company and code not in DOCS_PERSON:
                raise ValidationError(_("Una persona solo puede tener DNI, CE o Pasaporte."))
