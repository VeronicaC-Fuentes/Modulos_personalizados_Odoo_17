from odoo import models, fields, api, _
from odoo.exceptions import UserError

# --------------------
# FUNCIONES Y MAPEOS
# --------------------

def normalize(text):
    return ''.join(text.upper().split())

FAMILY_CODE_MAP = {
    "ALTURAS": "10",
    "AURICULAR": "20",
    "BLOQUEADOR": "30",
    "CALZADO": "40",
    "CRANEAL": "50",
    "FAJAS LUMBARES": "60",
    "MANUAL": "70",
    "OTROS": "80",
    "RESPIRATORIA": "90",
    "ROPA DE TRABAJO": "100",
    "SEÑALIZACION": "110",
    "VISUAL": "120",
    "CONSUMIBLES": "130",
    "BLOQUEO": "140",
    "PRIMEROS AUXILIOS": "150",
    "ABSORBENTES": "190",
    "SERVICIOS": "170",
    "ACTIVO FIJO": "900",
}
LINE_CODE_MAP = {
    ("ALTURAS", "ARNESES"): "10000",
    ("ALTURAS", "LINEA DE VIDA"): "20000",
    ("ALTURAS", "ANCLAJE MOVIL"): "30000",
    ("ALTURAS", "KIT"): "40000",
    ("ALTURAS", "CINTURON"): "50000",
    ("ALTURAS", "BLOQUE RETRACTIL"): "60000",
    ("ALTURAS", "LINEA DE RESTRICCION"): "70000",
    ("ALTURAS", "LINEA RETRACTIL"): "80000",
    ("AURICULAR", "TAPONES AUDITIVO"): "10000",
    ("AURICULAR", "OREJERAS VINCHA"): "20000",
    ("AURICULAR", "OREJERAS ADAPTABLES"): "30000",
    ("BLOQUEADOR", "FPS 50"): "10000",
    ("BLOQUEADOR", "FPS 55"): "20000",
    ("BLOQUEADOR", "OTROS"): "30000",
    ("BLOQUEADOR", "FPS 90"): "40000",
    ("BLOQUEADOR", "FPS 100"): "50000",
    ("CALZADO", "BOTIN DE CUERO"): "30000",
    ("CALZADO", "BOTAS SINTETICAS"): "80000",
    ("CALZADO", "ZAPATILLAS"): "90000",
    ("CRANEAL", "BARBIQUEJO"): "10000",
    ("CRANEAL", "CASCOS"): "20000",
    ("CRANEAL", "CASQUETE"): "30000",
    ("CRANEAL", "OTROS"): "40000",
    ("FAJAS LUMBARES", "FAJAS"): "10000",
    ("MANUAL", "CUERO"): "10000",
    ("MANUAL", "DIELECTRICO"): "20000",
    ("MANUAL", "HILO"): "30000",
    ("MANUAL", "METALICOS"): "40000",
    ("MANUAL", "RECUBIERTOS"): "50000",
    ("MANUAL", "SINTETICOS"): "60000",
    ("MANUAL", "ALUMINIZADO"): "70000",
    ("MANUAL", "ACCESORIOS"): "80000",
    ("OTROS", "OTROS"): "10000",
    ("OTROS", "CONSUMIBLES"): "20000",
    ("OTROS", "REPUESTOS"): "30000",
    ("OTROS", "ESLINGA"): "40000",
    ("OTROS", "SAFETY"): "50000",
    ("OTROS", "ABRASIVOS"): "60000",
    ("OTROS", "HERRAMIENTAS"): "70000",
    ("RESPIRATORIA", "ADAPTADOR"): "10000",
    ("RESPIRATORIA", "AUTORESCATADOR"): "20000",
    ("RESPIRATORIA", "CARTUCHO"): "30000",
    ("RESPIRATORIA", "FILTRO"): "40000",
    ("RESPIRATORIA", "MASCARILLA"): "50000",
    ("RESPIRATORIA", "RESPIRADOR"): "60000",
    ("RESPIRATORIA", "RETENEDOR"): "70000",
    ("RESPIRATORIA", "ACCESORIO"): "80000",
    ("ROPA DE TRABAJO", "CAMISA"): "1000",
    ("ROPA DE TRABAJO", "CHALECO"): "2000",
    ("ROPA DE TRABAJO", "TRAJE DESCARTABLE"): "3000",
    ("ROPA DE TRABAJO", "GORRO"): "4000",
    ("ROPA DE TRABAJO", "PANTALON"): "5000",
    ("ROPA DE TRABAJO", "POLO"): "6000",
    ("ROPA DE TRABAJO", "ROPA FRIO"): "7000",
    ("ROPA DE TRABAJO", "CALCETIN"): "8000",
    ("ROPA DE TRABAJO", "SOLDADOR"): "9000",
    ("ROPA DE TRABAJO", "TRAJE DE LLUVIA"): "10000",
    ("ROPA DE TRABAJO", "POLAR"): "11000",
    ("ROPA DE TRABAJO", "OVEROL"): "12000",
    ("ROPA DE TRABAJO", "CHOMPA"): "13000",
    ("ROPA DE TRABAJO", "TRAJE DE FUMIGACION"): "14000",
    ("ROPA DE TRABAJO", "ROPA DE CALOR"): "15000",
    ("ROPA DE TRABAJO", "ACCESORIOS"): "16000",
    ("SEÑALIZACION", "ACCESORIOS"): "1000",
    ("SEÑALIZACION", "CINTA DE PELIGRO"): "2000",
    ("SEÑALIZACION", "CONO"): "3000",
    ("SEÑALIZACION", "LAMPARA"): "4000",
    ("SEÑALIZACION", "PALETA"): "5000",
    ("SEÑALIZACION", "ROLLO MALLA"): "6000",
    ("SEÑALIZACION", "CINTA REFLECTIVA"): "7000",
    ("SEÑALIZACION", "SEÑALIZACION ESTATICA"): "8000",
    ("SEÑALIZACION", "LINTERNA"): "9000",
    ("VISUAL", "ANTIPARRA"): "1000",
    ("VISUAL", "LENTES"): "2000",
    ("VISUAL", "MASCARAS"): "3000",
    ("VISUAL", "REPUESTO"): "4000",
    ("VISUAL", "OTROS"): "5000",
    ("CONSUMIBLES", "BOLSAS"): "1000",
    ("CONSUMIBLES", "ETIQUETAS"): "2000",
    ("CONSUMIBLES", "STRECH FILM"): "3000",
    ("CONSUMIBLES", "HOJAS"): "4000",
    ("CONSUMIBLES", "VARIOS"): "5000",
    ("BLOQUEO", "CANDADOS"): "10000",
    ("BLOQUEO", "PINZAS"): "20000",
    ("BLOQUEO", "TARJETA"): "30000",
    ("BLOQUEO", "OTROS"): "40000",
    ("PRIMEROS AUXILIOS", "BOTIQUINES"): "10000",
    ("PRIMEROS AUXILIOS", "OTROS"): "20000",
    ("PRIMEROS AUXILIOS", "MEDICAMENTOS"): "30000",
    ("ABSORBENTES", "BANDEJAS"): "1000",
    ("ABSORBENTES", "PAÑOS P/ACEITE"): "2000",
    ("ABSORBENTES", "PAÑOS P/QUÍMICO"): "3000",
    ("ABSORBENTES", "CORDONES P/ACEITE"): "4000",
    ("ABSORBENTES", "CORDONES P/QUÍMICO"): "5000",
    ("ABSORBENTES", "ALMOHADILLA P/ACEITE"): "6000",
    ("ABSORBENTES", "ALMOHADILLA P/QUÍMICO"): "7000",
    ("ABSORBENTES", "KIT P/ACEITE"): "8000",
    ("ABSORBENTES", "KIT P/QUÍMICOS"): "9000",
    ("ACTIVO FIJO", "1000"): "1000",
}

FAMILY_CODE_MAP_NORM = {normalize(k): v for k, v in FAMILY_CODE_MAP.items()}
LINE_CODE_MAP_NORM = {(normalize(k1), normalize(k2)): v for (k1, k2), v in LINE_CODE_MAP.items()}

# --------------------
# MODELO ODOO
# --------------------


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # ------------------------------------------------
    # CAMPOS
    # ------------------------------------------------

    # Tipo general del producto
    tipo_producto = fields.Selection([
        ("normal", "Producto Normal"),
        ("extintor", "Extintor"),
    ], string="Tipo de producto", default="normal", required=True)

    # --- Extintores ---
    tipo_extintor = fields.Selection([
        ("pqs", "PQS"),
        ("co2", "CO₂"),
        ("otro", "Otro"),
    ], string="Tipo", help="Selecciona el tipo de extintor")

    porcentaje = fields.Float(
        "Porcentaje",
        help="Porcentaje para extintores PQS",
        digits=(5, 2),
    )

    clase_extintor = fields.Char("Clase")
    codigo_un = fields.Char("Código UN")
    peso = fields.Float("Peso")
    uom_peso = fields.Selection([
        ("kg", "Kg"),
        ("lb", "Lb"),
    ], string="Unidad de Peso", default="kg")
    fecha_fabricacion = fields.Date("Fecha de Fabricación")
    fecha_recarga = fields.Date("Fecha de Recarga")

    # --- Campos comunes ---
    descripcion_basica = fields.Char("Descripción Básica")
    modelo = fields.Char("Modelo")
    color = fields.Char("Color")
    marca = fields.Char("Marca")
    talla = fields.Char("Talla/Medida")

    # ------------------------------------------------
    # CAMPOS COMPUTADOS
    # ------------------------------------------------

    name = fields.Char(
        string="Nombre del Producto",
        compute="_compute_name",
        store=True,
        readonly=False,
    )

    default_code = fields.Char(
        string="Referencia Interna",
        compute="_compute_default_code",
        store=True,
        readonly=False,
    )

    has_reorder_rule = fields.Boolean(
        string="Tiene Regla de Reorden",
        compute="_compute_has_reorder_rule",
    )

    _ORDERPOINT_MIN = 0
    _ORDERPOINT_MAX = 0
    _ORDERPOINT_MULTIPLE = 1

    # ------------------------------------------------
    # MÉTODOS COMPUTADOS
    # ------------------------------------------------

    @api.depends(
        "tipo_producto",
        # --------- normales ---------
        "descripcion_basica", "modelo", "color", "marca", "talla",
        # --------- extintor ---------
        "tipo_extintor", "porcentaje",
        "peso", "uom_peso", "codigo_un", "clase_extintor",
    )
    def _compute_name(self):
        """Genera el nombre automáticamente con las reglas acordadas."""
        for product in self:
            if product.tipo_producto == "extintor":
                parts = [product.descripcion_basica]

                # a) Tipo + %
                if product.tipo_extintor:
                    parts.append(product.tipo_extintor.upper())
                    if product.porcentaje:
                        pct = int(product.porcentaje) if product.porcentaje.is_integer() else product.porcentaje
                        parts.append(f"{pct}%")

                # b) Peso + unidad
                if product.peso:
                    val = int(product.peso) if product.peso.is_integer() else product.peso
                    parts.append(f"{val} {product.uom_peso}")

                # c) Código UN y Clase
                if product.codigo_un:
                    parts.append(f"UN:{product.codigo_un}")
                if product.clase_extintor:
                    parts.append(f"CLASE {product.clase_extintor}")

                name_parts = parts
            else:
                # Productos normales
                name_parts = [
                    product.descripcion_basica,
                    product.modelo,
                    product.color,
                    product.marca,
                    product.talla,
                ]

            product.name = " ".join(filter(None, name_parts)) or _("[Sin nombre]")

    # --------------------
    # DEFAULT CODE
    # --------------------

    @api.depends("categ_id", "company_id")
    def _compute_default_code(self):
        for product in self:
            if product.categ_id and product.company_id:
                family_name = normalize(product.categ_id.parent_id.name) if product.categ_id.parent_id else None
                line_name = normalize(product.categ_id.name)

                family_code = FAMILY_CODE_MAP_NORM.get(family_name, "99") if family_name else "99"
                line_code = LINE_CODE_MAP_NORM.get((family_name, line_name), "99999") if family_name else "99999"

                domain = [
                    ("default_code", "like", f"{family_code}{line_code}%"),
                    ("company_id", "=", product.company_id.id),
                ]
                existing = self.env["product.template"].search(domain)
                max_seq = 0
                for rec in existing:
                    code = rec.default_code or ""
                    if code.startswith(f"{family_code}{line_code}") and len(code) == len(family_code) + len(line_code) + 6:
                        try:
                            seq_val = int(code[-6:])
                            max_seq = max(max_seq, seq_val)
                        except ValueError:
                            pass
                next_seq = str(max_seq + 1).zfill(6)
                product.default_code = f"{family_code}{line_code}{next_seq}"
            else:
                product.default_code = "N/A"

    # --------------------
    # REORDER RULE FLAG
    # --------------------

    @api.depends("product_variant_ids.orderpoint_ids")
    def _compute_has_reorder_rule(self):
        OrderPoint = self.env["stock.warehouse.orderpoint"]
        for product in self:
            vids = product.product_variant_ids.ids
            product.has_reorder_rule = bool(vids and OrderPoint.search_count([("product_id", "in", vids)], limit=1))

    # ------------------------------------------------
    # CRUD
    # ------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        products._ensure_reorder_rule()
        return products

    def write(self, vals):
        res = super().write(vals)
        self._ensure_reorder_rule()
        return res

    # ------------------------------------------------
    # REGLA DE REABASTECIMIENTO
    # ------------------------------------------------

    def _ensure_reorder_rule(self):
        OrderPoint = self.env["stock.warehouse.orderpoint"]
        Warehouse = self.env["stock.warehouse"]
        cache_wh = {}
        for product in self:
            if not product.seller_ids:
                raise UserError(_(
                    "El producto '%s' debe tener al menos un proveedor definido." % product.display_name))

            company = product.company_id or self.env.company
            wh = cache_wh.setdefault(company.id, Warehouse.search([("company_id", "=", company.id)], limit=1))
            if not wh:
                raise UserError(_(
                    "No se encontró ningún almacén para la compañía '%s'." % company.display_name))

            for variant in product.product_variant_ids:
                exists = OrderPoint.search_count([
                    ("product_id", "=", variant.id),
                    ("company_id", "=", company.id),
                ])
                if not exists:
                    OrderPoint.create({
                        "product_id": variant.id,
                        "product_min_qty": self._ORDERPOINT_MIN,
                        "product_max_qty": self._ORDERPOINT_MAX,
                        "qty_multiple": self._ORDERPOINT_MULTIPLE,
                        "location_id": wh.lot_stock_id.id,
                        "warehouse_id": wh.id,
                        "company_id": company.id,
                        "trigger": "auto",
                    })
