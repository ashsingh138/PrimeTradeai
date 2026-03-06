```markdown
# Binance Futures Testnet Trading Bot

A robust, structured Python application designed to place `MARKET` and `LIMIT` orders on the Binance Futures Testnet (USDT-M). This project uses direct REST API interactions (`requests`) to demonstrate a clear understanding of payload construction, HMAC SHA256 signature generation, and API dispatching.

## Features & Architecture
* **Core Functionality:** Places BUY/SELL orders for both `MARKET` and `LIMIT` types.
* **Modular Structure:** Clean separation of concerns between the API client (`client.py`), order logic (`orders.py`), input validation (`validators.py`), and presentation layers.
* **Validation & Error Handling:** Pre-validates user inputs (e.g., ensuring positive quantities and valid limits) before dispatching requests. Catches and gracefully formats network issues and Binance API errors.
* **Logging:** Implements targeted logging (`logs/trading_bot.log`). File logs contain detailed debug information (endpoints, payloads), while console logs remain clean and user-friendly.
* **Bonus UI:** Includes a lightweight Streamlit Web UI (`app.py`) for an enhanced user experience, reusing the exact same backend logic as the CLI.

## Project Structure
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py        # Binance API client, auth, and request dispatching
│   ├── orders.py        # Order placement logic
│   ├── validators.py    # Input validation
│   └── logging_config.py# Logger setup (file & console handlers)
├── cli.py               # Command Line Interface entry point
├── app.py               # Bonus: Streamlit Web UI
├── requirements.txt     # Project dependencies
├── .env.example         # Template for environment variables
└── README.md            # Project documentation

```

## Setup Instructions

1. **Extract the folder and navigate to the project directory:**
```bash
cd trading_bot

```


2. **Set up a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure Credentials:**
Rename the example environment file:
```bash
# On Windows:
copy .env.example .env
# On macOS/Linux:
cp .env.example .env

```


Open the `.env` file and insert your Binance Futures Testnet API Key and Secret.

## How to Run Examples

### Option A: Command Line Interface (CLI)

Run the `cli.py` script to execute orders directly from your terminal.

**1. Place a MARKET Order (BUY):**

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

```

**2. Place a LIMIT Order (SELL):**

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 150000.00

```

**3. View Help & Arguments:**

```bash
python cli.py --help

```

### Option B: Web UI (Bonus)

Launch the interactive web dashboard:

```bash
streamlit run app.py

```

A browser window will open at `http://localhost:8501`. Enter your trade parameters and click "Place Order" to view the execution details natively in the browser.

## Logs & Verification

All API requests, debug information, execution statuses, and errors are saved inside the `logs/trading_bot.log` file. Review this file to verify the raw API responses for the submitted MARKET and LIMIT orders.

## Assumptions

* The Testnet account is already created and funded with mock USDT.
* Local system time is sufficiently synchronized with standard internet time (required by Binance's `recvWindow` security feature).
* Inputs follow Binance's `LOT_SIZE` and `PRICE_FILTER` constraints. Violations are caught and reported via the API error handler.

