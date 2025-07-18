# partner_credit_restrictions

## Descripción

Este módulo extiende el proceso de ventas en Odoo 17 para **restringir automáticamente la confirmación de órdenes de venta** en los siguientes casos:
- El cliente tiene facturas vencidas mayores a 20 días.
- El cliente excede su límite de crédito (solo sobre productos 'ganados').
- Bloqueo y desbloqueo automatizado de clientes según su comportamiento de pago.

Incluye flujos de aprobación para ventas “en riesgo” y mensajes claros para usuarios comerciales y administrativos.

## Características

- Campo `blocked` automático en los clientes (`res.partner`).
- Validación de ventas por facturas vencidas.
- Validación de ventas por límite de crédito.
- Flujos de aprobación (autorización) para excepciones.
- Registros de log para auditoría.
- Preparado para localización Perú y lógica realista.

## Instalación

1. Copia la carpeta `partner_credit_restrictions` en tus addons de Odoo.
2. Actualiza la lista de apps y busca “Restricciones de crédito en ventas”.
3. Instala el módulo.

## Uso

- Al crear/editar clientes o confirmar una venta, el sistema revisa automáticamente si el cliente está bloqueado.
- Si el cliente tiene facturas vencidas > 20 días, la venta no se confirma y requiere aprobación.
- Puedes consultar y filtrar el campo “Bloqueado” en la vista de clientes.

## Contribuciones

Abierto a mejoras y sugerencias. 

---
