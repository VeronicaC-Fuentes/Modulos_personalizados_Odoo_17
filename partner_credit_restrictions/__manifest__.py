{
    'name': 'Partner Credit Restrictions',
    'version': '17.0.1.0.0',
    'summary': 'Restringe ventas a clientes con facturas vencidas y controla aprobaciones de crédito.',
    'description': """
        Este módulo agrega controles automáticos de crédito para clientes:
        - Bloquea clientes con facturas vencidas más de 20 días.
        - Solo usuarios autorizados pueden aprobar ventas de clientes bloqueados.
        - Validación del límite de crédito considerando únicamente productos GANADOS.
        - Notificaciones y bloqueo en proceso de venta.
        - Grupos de seguridad para aprobación personalizada.
    """,
    'author': 'Verónica Cruces',
    'website': 'https://veronicadev.com',
    'category': 'Sales/Custom',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'account',
    ],
    'data': [
        'data/group_custom_sale_approval.xml',
        'data/security_groups.xml',
        # Si tienes vistas, acciones, security/ir.model.access.csv agrégalas aquí
    ],
    'maintainer': 'Verónica Cruces',
    'installable': True,
    'application': False,
}
