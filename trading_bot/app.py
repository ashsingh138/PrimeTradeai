import streamlit as st
import os
from dotenv import load_dotenv

# Reusing our existing bot logic!
from bot.client import BinanceFuturesClient, BinanceAPIError
from bot.orders import place_order
from bot.validators import validate_order_inputs, ValidationError
from bot.logging_config import logger

# --- Page Config ---
st.set_page_config(page_title="Binance Testnet Bot", page_icon="📈", layout="centered")

def main():
    st.title("📈 Binance Futures Trading Bot")
    st.markdown("A lightweight UI for placing testnet orders, built with Streamlit.")

    # Load credentials
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        st.error("⚠️ API credentials not found. Please set them in your `.env` file.")
        st.stop()

    # --- UI Form ---
    with st.form("order_form"):
        st.subheader("Order Details")
        
        col1, col2 = st.columns(2)
        with col1:
            symbol = st.text_input("Symbol", value="BTCUSDT").upper()
            side = st.selectbox("Side", ["BUY", "SELL"])
        with col2:
            order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
            quantity = st.number_input("Quantity", min_value=0.001, value=0.01, step=0.01, format="%.3f")
        
        price = st.number_input("Price (Required for LIMIT)", min_value=0.0, value=0.0, step=100.0)

        # Submit button
        submitted = st.form_submit_button("Place Order", use_container_width=True)

    # --- Order Execution ---
    if submitted:
        # Adjust price to None if MARKET order to pass validation
        final_price = price if order_type == "LIMIT" else None
        
        try:
            # 1. Validate
            validate_order_inputs(symbol, side, order_type, quantity, final_price)
            
            # 2. Initialize Client
            client = BinanceFuturesClient(api_key, api_secret)
            
            # 3. Place Order
            with st.spinner("Communicating with Binance Testnet..."):
                response = place_order(client, symbol, side, order_type, quantity, final_price)
            
            # 4. Success Output
            st.success("✅ Order Placed Successfully!")
            
            # Display clean JSON data
            st.json({
                "Order ID": response.get("orderId"),
                "Status": response.get("status"),
                "Symbol": response.get("symbol"),
                "Side": response.get("side"),
                "Type": response.get("type"),
                "Executed Qty": response.get("executedQty"),
                "Average Price": response.get("avgPrice", "0.0")
            })
            
            logger.info(f"UI Order Success: {response.get('orderId')} | Status: {response.get('status')}")

        except ValidationError as e:
            st.warning(f"⚠️ Validation Error: {e}")
            logger.error(f"UI Validation Failed: {e}")
        except BinanceAPIError as e:
            st.error(f"🚨 API Error: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    main()