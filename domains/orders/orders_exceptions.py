from core.exceptions import BadRequestError, NotFoundError


class OrderNotFound(NotFoundError):
    detail = "Pedido nao encontrado"


class OrderCannotBeCanceled(BadRequestError):
    detail = "Este pedido nao pode mais ser cancelado"
