from enum import Enum


class EStatus(Enum):
    # opened: Order without payments.
    # closed: Order with payments covering total amount.
    # expired: Pedido cancelado que não possui pagamentos aprovados
    # ou pendentes (todos rejeitados ou devolvidos).
    OPENED = "pedido sem pagamento"
    CLOSED = "pedido com pagamento total"
    EXPIRED = "pedido cancelado"


class EStatus2(Enum):
    CREATED = "criado"
    EXPIRED = "expirado"
    ANALYSIS = "em analíse"
    COMPLETE = "concluído"
    CHARGEBACK = "chargeback"
    PAID = "pago"
    REFUDED = "reembolsado"
    FAILED = "falha no pagamento"
