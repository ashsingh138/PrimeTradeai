# Binance Futures Testnet Trading Bot

A robust, structured Python application designed to place `MARKET` and `LIMIT` orders on the Binance Futures Testnet (USDT-M). Built with standard REST API interactions (using `requests`) to demonstrate full control over payload signature generation, authentication, and API dispatching.

**Includes a Bonus Web UI built with Streamlit!**

## Features
- Connects securely to the Binance Futures Testnet.
- Places `MARKET` and `LIMIT` orders (both BUY and SELL sides).
- Pre-validates user inputs before making network calls.
- **Bonus:** Includes a lightweight, interactive Web UI (`app.py`).
- **Architecture:** Highly structured code, separating the API client layer, order execution logic, and presentation layers (CLI & UI).
- **Logging:** Comprehensive logging to both the terminal and a persistent log file (`logs/trading_bot.log`).

## Project Structure
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py        # API client, HMAC SHA256 auth, request dispatching
│   ├── orders.py        # Order payload construction
│   ├── validators.py    # Input validation logic
│   └── logging_config.py# Logger setup
├── cli.py               # Main Command Line Interface
├── app.py               # Bonus: Streamlit Web UI
├── requirements.txt     # Project dependencies
├── .env.example         # Template for environment variables
└── README.md            # Setup and execution instructions