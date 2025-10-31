import yaml
import bcrypt
from getpass import getpass
import sys

def hash_password(plain_password: str) -> str:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

def main():
    """Main function to create the config.yaml file."""
    print("--- Create config.yaml for Streamlit Authenticator v0.4.2 ---")
    print("You will be prompted to create user credentials.")
    
    users = []
    
    # --- Collect User Credentials ---
    while True:
        username = input("\nUsername (leave blank to finish): ").strip()
        if not username:
            if not users:
                print("No users added. At least one user is required.")
                continue
            break
        
        name = input(f"Full name for {username}: ").strip() or username
        email = input(f"Email for {username}: ").strip() or f"{username}@example.com"
        
        while True:
            pwd = getpass(f"Password for {username}: ")
            if not pwd:
                print("Password cannot be empty. Please try again.")
                continue
                
            pwd_confirm = getpass("Confirm password: ")
            if pwd != pwd_confirm:
                print("Passwords did not match. Please try again.")
            else:
                break
                
        hashed = hash_password(pwd)
        
        users.append({
            "name": name,
            "username": username,
            "email": email,
            "password": hashed
        })
        print(f"Added user: {username}")

    if not users:
        print("No users were added. Exiting.")
        sys.exit()

    print("\n--- Configure Cookie Settings ---")
    
    cookie_name = input("Cookie name (default 'my_app_cookie'): ").strip() or "my_app_cookie"
    # It's crucial to have a strong, random key.
    cookie_key = input("Cookie secret key (press Enter for a default, but a random string is STRONGLY recommended): ").strip() or "CHANGE_ME_KEY_PLEASE"
    if cookie_key == "CHANGE_ME_KEY_PLEASE":
        print("\nWARNING: You are using a default cookie key.")
        print("Please generate a random string for production use.\n")
        
    while True:
        try:
            cookie_expiry_days_str = input("Cookie expiry in days (default 1): ").strip() or "1"
            cookie_expiry_days = int(cookie_expiry_days_str)
            if cookie_expiry_days <= 0:
                print("Please enter a positive number of days.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # --- Build the config dictionary ---
    
    credentials = {"usernames": {}}
    for u in users:
        credentials["usernames"][u["username"]] = {
            "name": u["name"],
            "email": u["email"],
            "password": u["password"]
        }

    config = {
        "credentials": credentials,
        "cookie": {
            "name": cookie_name,
            "key": cookie_key,
            "expiry_days": cookie_expiry_days
        }
    }

    # --- Write the config file ---
    config_filename = "config.yaml"
    try:
        with open(config_filename, "w", encoding="utf-8") as f:
            yaml.dump(config, f, sort_keys=False, default_flow_style=False)
        
        print(f"\nSuccessfully wrote '{config_filename}'!")
        print("KEEP THIS FILE SAFE and do not commit it to public version control.")
        
    except Exception as e:
        print(f"\nError writing config file: {e}")

if __name__ == "__main__":
    main()