# QuickBite – Checkout and Payment

A standalone Flask application demonstrating discount calculation, payment processing and a simplified checkout flow.

## Features
- Enter customer name and order subtotal.
- Apply no discount, 10% discount or ₹50 flat discount.
- Select Card, UPI or Digital Wallet.
- Calculate the final amount automatically.
- Display a payment receipt with reference ID and timestamp.
- Validate customer details, amount, discount and payment selection.

## Design patterns
1. **Strategy – `discounts.py`:** `NoDiscount`, `PercentageDiscount` and `FlatDiscount` implement a common discount calculation interface.
2. **Adapter – `payment_adapters.py`:** Card, UPI and Wallet gateways expose different methods. Their adapters convert them into a common `pay()` interface.
3. **Facade – `checkout_facade.py`:** `CheckoutFacade` gives the application one checkout method and coordinates validation, discount calculation and payment.

## Run on Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5003.

## Run tests
```powershell
pytest -v
```

## Payment safety note
This is a coursework simulation. It does not connect to real payment gateways, transfer money, or collect card/UPI credentials.

## GitHub (independent repository)
Create a separate repository, for example `Member3-Checkout-Payment`, then:
```powershell
git init
git add .
git commit -m "Implement checkout and payment patterns"
git branch -M feature/checkout-payment
git remote add origin https://github.com/USERNAME/Member3-Checkout-Payment.git
git push -u origin feature/checkout-payment
```
Replace `USERNAME` with your GitHub username.


## UI redesign
The checkout interface has been visually redesigned with a dark navy/coral QuickBite theme, responsive layout, refreshed form controls, and a client-side estimated total preview. Existing Flask routes, form field names, discount logic, payment adapters, facade, and receipt behavior are retained. The preview is informational only; the server remains authoritative for calculations.
