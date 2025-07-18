{
    'name': 'Product Name Customization',
    'version': '17.0.1.0.0',  # (O la versión de tu Odoo)
    'summary': 'Personaliza nombre, referencia interna y reglas de reorden para productos',
    'description': """
        Este módulo concatena campos personalizados para el nombre del producto,
        genera códigos internos automáticos basados en familia y línea,
        y asegura reglas de reabastecimiento para cada producto.
        
        Funcionalidades principales:
        - Nombre automático del producto según atributos y tipo (extintores, normales).
        - Código interno (default_code) autogenerado por familia y línea.
        - Creación automática de reglas de reabastecimiento (stock).
        - Validación de proveedores obligatorios.
    """,
    'author': 'Verónica Cruces',
    'website': 'https://veronicadev.com',
    'category': 'Inventory/Customization',
    'depends': [
        'product',
        'stock',
        'purchase',
        'sale_management',
        'account_accountant',
    ],
    'data': [
        'data/ir_sequence_data.xml',
    ],
    'license': 'LGPL-3',
    'maintainer': 'Verónica',
    'installable': True,
    'application': False,
}
