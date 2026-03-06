from .client import BinanceFuturesClient
from .logging_config import logger
from typing import Optional

def place_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None):
    """Constructs and dispatches the order request."""
    endpoint = "/fapi/v1/order"
    
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity
    }

    if order_type.upper() == 'LIMIT':
        params["price"] = price
        params["timeInForce"] = "GTC" # Good Till Cancelled is required for Limit orders

    logger.info(f"Preparing to place {side.upper()} {order_type.upper()} order for {quantity} {symbol.upper()}...")
    
    return client.dispatch_request("POST", endpoint, params)