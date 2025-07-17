{
    'name': 'Product Name Customization',
    'version': '1.0',
    'depends': [
        'product',
        'stock',
        'purchase',
        'sale_management',
        'account_accountant',
    ],
    'author': 'Verónica',
    'category': 'Customization',
    'summary': 'Concatenación de campos personalizados para el nombre del producto, referencia interna y regla de reordenamiento',
    'data': ['data/ir_sequence_data.xml'],
    'installable': True,
    'application': False,
}
