# Member 4 – Orders, Delivery and Notifications

A standalone Flask application for creating sample food orders, tracking their delivery lifecycle and notifying observers when an order changes.

## Features
- Create an order with customer, food item and delivery address.
- Track orders through Placed, Preparing, Out for delivery and Delivered.
- Cancel an order while it is Placed or Preparing.
- Store order records and statuses in SQLite.
- Notify registered observers when an order is placed or its status changes.
- Display order progress on a simple web dashboard.

## Design patterns
1. **State – `order_states.py`:** Each order state is represented by a class that controls which transition is allowed next. Invalid transitions raise a clear error.
2. **Observer – `observers.py`:** `NotificationCenter` is the subject. Notification objects subscribe to it and receive updates when an order is created, advanced or cancelled. The included email notification is a console simulation, not a real email sender.

## Order lifecycle
Placed → Preparing → Out for delivery → Delivered

Cancellation is allowed from Placed or Preparing.

## Run on Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5004.

The SQLite database is created automatically on first run.

## Run tests
```powershell
pytest -v
```

## GitHub (independent repository)
Create a separate repository, for example `Member4-Orders-Delivery-Notifications`, then:
```powershell
git init
git add .
git commit -m "Implement orders delivery and notification patterns"
git branch -M feature/orders-delivery-notifications
git remote add origin https://github.com/USERNAME/Member4-Orders-Delivery-Notifications.git
git push -u origin feature/orders-delivery-notifications
```
Replace `USERNAME` with your GitHub username.
