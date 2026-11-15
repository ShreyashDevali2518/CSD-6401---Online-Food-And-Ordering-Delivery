# Member 2 – Cart and Customization

A standalone Flask web application for managing a shopping cart, customizing individual food items and building meal combos.

## Features
- Browse a small food menu.
- Add items to the cart with optional extras.
- Increase/decrease item quantities and remove cart lines.
- Build a meal combo with one main item, one side and one drink.
- View the cart subtotal.
- Cart data is stored in the Flask session.

## Design patterns
1. **Command – `commands.py`:** Add, remove and quantity changes are represented as command objects. `CartInvoker` executes them. Add and remove commands also support undo.
2. **Decorator – `decorators.py` and `customization.py`:** add-ons wrap a basic food object and change its description and price without modifying the original food class.
3. **Builder – `meal_builder.py`:** constructs a meal combo step by step and validates that it contains one main, one side and one drink.

## Run on Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5002.

## Run tests
```powershell
pytest -v
```

## GitHub (independent repository)
Create a separate repository, for example `Member2-Cart-Customization`, then:
```powershell
git init
git add .
git commit -m "Implement cart and customization design patterns"
git branch -M feature/cart-customization
git remote add origin https://github.com/USERNAME/Member2-Cart-Customization.git
git push -u origin feature/cart-customization
```
Replace `USERNAME` with your GitHub username.
