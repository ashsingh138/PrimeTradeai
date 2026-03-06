import argparse
import os
import sys
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient, BinanceAPIError
from bot.orders import place_order
from bot.validators import validate_order_inputs, ValidationError
from bot.logging_config import logger

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", type=str, required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=['BUY', 'SELL'], help="Order side (BUY/SELL)")
    parser.add_argument("--type", type=str, required=True, choices=['MARKET', 'LIMIT'], help="Order type (MARKET/LIMIT)")
    parser.add_argument("--quantity", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price (Required if type is LIMIT)")

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("Missing API credentials. Please set them in the .env file.")
        sys.exit(1)

    try:
        # 1. Validate Input
        validate_order_inputs(args.symbol, args.side, args.type, args.quantity, args.price)

        # 2. Initialize Client
        client = BinanceFuturesClient(api_key, api_secret)

        # 3. Place Order
        response = place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )

        # 4. Print Summary
        print("\n" + "="*40)
        print("✅ ORDER PLACED SUCCESSFULLY")
        print("="*40)
        print(f"Order ID:     {response.get('orderId')}")
        print(f"Status:       {response.get('status')}")
        print(f"Symbol:       {response.get('symbol')}")
        print(f"Side:         {response.get('side')}")
        print(f"Type:         {response.get('type')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        if response.get('avgPrice') and float(response.get('avgPrice')) > 0:
            print(f"Avg Price:    {response.get('avgPrice')}")
        print("="*40 + "\n")

        logger.info(f"Successfully placed order {response.get('orderId')} | Status: {response.get('status')}")

    except ValidationError as e:
        logger.error(f"Input Validation Failed: {e}")
        sys.exit(1)
    except BinanceAPIError as e:
        logger.error(f"Binance API Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()