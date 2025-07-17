{
    'name': 'Partner Credit Restrictions',
    'version': '1.0',
    'summary': (
        'Restricciones de crédito y bloqueo de clientes con '
        'facturas vencidas.'
    ),
    'author': 'Veronica C',
    'depends': ['sale', 'account'],
    'data': [
        'data/group_custom_sale_approval.xml',
        'data/security_groups.xml'
    ],
    'installable': True,
    'application': False,
}
