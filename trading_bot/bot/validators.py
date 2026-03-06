from typing import Optional

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None):
    """Validates CLI inputs before hitting the API."""
    
    if not symbol or not symbol.isalnum():
        raise ValidationError(f"Invalid symbol format: {symbol}")
        
    valid_sides = ['BUY', 'SELL']
    if side.upper() not in valid_sides:
        raise ValidationError(f"Invalid side: {side}. Must be one of {valid_sides}.")
        
    valid_types = ['MARKET', 'LIMIT']
    if order_type.upper() not in valid_types:
        raise ValidationError(f"Invalid order type: {order_type}. Must be one of {valid_types}.")
        
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than 0.")
        
    if order_type.upper() == 'LIMIT':
        if price is None or price <= 0:
            raise ValidationError("A valid positive price must be provided for LIMIT orders.")