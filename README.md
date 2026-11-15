# Member 1 – Authentication and Restaurant Menu

A standalone Flask application for customer registration/login and restaurant menu browsing/management.

## Features
- Customer registration and login with hashed passwords.
- Session-based login and logout.
- Restaurant menu grouped by food category.
- Admin-only menu management: add and remove menu items.
- SQLite database.
- Unit tests for the three assigned design patterns.

## Design patterns
1. **Singleton – `DatabaseManager`:** ensures the application uses one shared database manager configuration.
2. **Factory Method – `MenuItemFactory`:** creates menu items after validating their category and details.
3. **Proxy – `MenuManagementProxy`:** checks administrator permissions before allowing menu changes.

## Run on Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5001.

The SQLite database is created automatically on first run.

## Demo administrator account
- Email: `admin@goodbite.local`
- Password: `Admin123!`

Change the demo password before using this application beyond local coursework testing. New registrations receive the customer role; the registration form cannot grant administrator access.

## Run tests
```powershell
pytest -v
```

## GitHub (independent repository)
Create a new repository, for example `Member1-Authentication-RestaurantMenu`, then:
```powershell
git init
git add .
git commit -m "Implement authentication and restaurant menu"
git branch -M feature/auth-restaurant-menu
git remote add origin https://github.com/USERNAME/Member1-Authentication-RestaurantMenu.git
git push -u origin feature/auth-restaurant-menu
```
Replace `USERNAME` with your GitHub username.
