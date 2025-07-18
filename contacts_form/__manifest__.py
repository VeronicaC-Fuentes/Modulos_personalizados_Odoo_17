{
    "name": "Custom Contacts Form",
    "version": "17.0.1.0.0",
    "summary": "Personaliza el formulario de contactos con nuevos campos y validaciones para Perú.",
    "description": """
        Personalización avanzada del formulario de contactos:
        - Añade campos adicionales para contactos comerciales, tesorería, logística y otros.
        - Controla el tipo de documento permitido según persona o compañía.
        - Adapta la vista y lógica para requerimientos de Perú (l10n_pe).
        - Mejor experiencia para gestión de clientes y proveedores en Odoo.
    """,
    "author": "Verónica Cruces",
    "website": "https://veronicadev.com",
    "category": "Contacts/Custom",
    "license": "LGPL-3",
    "depends": [
        "base",
        "contacts",
        "l10n_pe",
    ],
    "data": [
        "views/res_partner_form.xml",
    ],
    "maintainer": "Verónica Cruces",
    "installable": True,
    "application": False,
}
