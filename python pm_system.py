I understand you'd like to build this system using Python. While I cannot develop a full-fledged web application with a graphical user interface or real-time web capabilities directly, I can create a **command-line (script-based) Python application** that simulates many of the features you described.

This Python script will allow you to:

  * Log in as a user or administrator.
  * Select zones and equipment for PM.
  * Perform PM work by entering data for each stage.
  * Save PM records locally (e.g., to a JSON file, as direct Firebase integration for a simple script is complex and requires external setup I cannot guarantee).
  * View active and historical PM records.
  * Simulate report generation.

Please note that features like real-time multi-user updates on a main screen (without a web server) and automated email sending are outside the scope of a simple command-line script.

Let's start by setting up the basic structure in Python, including loading your equipment data and implementing the login functionality.

Here's the Python code:

```python?code_reference&code_event_index=3
import pandas as pd
import json
import datetime
import os

# --- Configuration ---
ADMIN_PASSWORD = "Karak@2025"
PM_DATA_FILE = "pm_records.json"
WEEKLY_REPORT_EMAIL = "abdallahdomer@yahoo.com" # This will be used in a simulated email function

# PM Stages
PM_STAGES = [
    {"name": "Sound", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Vibration", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Heat", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Motor umbrella", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Status", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Note", "type": "text"}
]

# --- Global Variables ---
current_user = None
current_interface = "login" # "login", "user", "admin"
pm_records = []
active_pm_sessions = [] # For simulating real-time active works

# --- Load Equipment Data ---
def load_equipment_data():
    """Loads equipment data from CSV files."""
    data = {}
    try:
        hlp_df = pd.read_csv('HLP.csv')
        data['HLP'] = hlp_df.rename(columns={'TAG number': 'tag', 'Equipment Description': 'description'}).to_dict(orient='records')

        screen_df = pd.read_csv('SCREEN.csv')
        data['SCREEN'] = screen_df.rename(columns={'TAG number': 'tag', 'Equipment Description': 'description'}).to_dict(orient='records')

        compaction_df = pd.read_csv('COMPACTION.csv')
        data['COMPACTION'] = compaction_df.rename(columns={'TAG number': 'tag', 'Equipment Description': 'description'}).to_dict(orient='records')
    except FileNotFoundError as e:
        print(f"Error loading CSV file: {e}. Make sure HLP.csv, SCREEN.csv, and COMPACTION.csv are in the same directory.")
        # Create empty lists if files are not found to allow the script to run
        data['HLP'] = []
        data['SCREEN'] = []
        data['COMPACTION'] = []
    return data

equipment_data = load_equipment_data()

# --- Data Persistence (Simulated Firebase) ---
def load_pm_records():
    """Loads PM records from a local JSON file."""
    if os.path.exists(PM_DATA_FILE):
        with open(PM_DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_pm_record(record):
    """Saves a new PM record and updates active sessions."""
    global pm_records, active_pm_sessions
    pm_records.append(record)
    # Simulate adding to active sessions, then removing when 'finished'
    active_pm_sessions.append(record)
    with open(PM_DATA_FILE, 'w') as f:
        json.dump(pm_records, f, indent=4)

def clear_old_records():
    """Clears records older than one week."""
    global pm_records
    one_week_ago = datetime.datetime.now() - datetime.timedelta(weeks=1)
    # Filter records to keep only those from the last week
    pm_records = [
        record for record in pm_records
        if datetime.datetime.fromisoformat(record['timestamp']) > one_week_ago
    ]
    with open(PM_DATA_FILE, 'w') as f:
        json.dump(pm_records, f, indent=4)
    print("Old PM records cleared (older than 1 week).")


# Initial load of PM records
pm_records = load_pm_records()
clear_old_records() # Clear old records on startup based on current date


# --- User Interface Functions ---
def show_alert(message, type="info"):
    """Simulates an alert box in a command-line interface."""
    color_map = {
        "success": "\033[92m", # Green
        "warning": "\033[93m", # Yellow
        "error": "\033[91m",   # Red
        "info": "\033[94m"     # Blue
    }
    RESET_COLOR = "\033[0m"
    print(f"\n{color_map.get(type, color_map['info'])}--- {type.upper()} ---")
    print(f"{message}{RESET_COLOR}\n")

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_login_screen():
    clear_screen()
    print("=======================================")
    print("     Factory PM Maintenance System     ")
    print("=======================================")
    print("\n--- User Login ---")
    print("1. User1")
    print("2. User2")
    print("3. User3")
    print("4. User4")
    print("\n--- Admin Access ---")
    print("5. Admin Login")
    print("6. Exit")
    print("=======================================")

def login_user(user_id):
    global current_user, current_interface
    current_user = user_id
    current_interface = "user"
    show_alert(f"Welcome, {current_user}!", "success")

def login_admin(password):
    global current_user, current_interface
    if password == ADMIN_PASSWORD:
        current_user = "Admin"
        current_interface = "admin"
        show_alert("Admin Login Successful!", "success")
    else:
        show_alert("Incorrect Admin Password!", "error")

def logout():
    global current_user, current_interface, active_pm_sessions
    current_user = None
    current_interface = "login"
    active_pm_sessions = [] # Clear active sessions on logout
    show_alert("Logged out successfully.", "info")

def display_user_interface():
    clear_screen()
    print("=======================================")
    print(f"     Welcome, {current_user}     ")
    print("=======================================")
    print("\n--- Current PM Activities ---")
    if not active_pm_sessions:
        print("No active PM work at the moment.")
    else:
        for activity in active_pm_sessions:
            print(f"- TAG: {activity['tag']} | Desc: {activity['description']} | User: {activity['user']} | Time: {datetime.datetime.fromisoformat(activity['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n-------------------------------")
    print("\n--- Zone Selection ---")
    print(f"1. HLP Zone ({len(equipment_data.get('HLP', []))} equipments)")
    print(f"2. SCREEN Zone ({len(equipment_data.get('SCREEN', []))} equipments)")
    print(f"3. COMPACTION Zone ({len(equipment_data.get('COMPACTION', []))} equipments)")
    print("\n4. Logout")
    print("=======================================")

def select_zone(zone_name):
    global current_user, active_pm_sessions
    selected_zone_data = equipment_data.get(zone_name)
    if not selected_zone_data:
        show_alert(f"No equipment data found for {zone_name} zone.", "error")
        return

    while True:
        clear_screen()
        print(f"=======================================")
        print(f"     PM Work - {zone_name} Zone     ")
        print("=======================================")
        print("\nSelect Equipment:")
        print("1. Type TAG Number")
        print("2. Browse Equipment List")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        selected_equipment = None
        if choice == '1':
            tag_input = input("Enter TAG Number: ").strip().upper()
            selected_equipment = next((eq for eq in selected_zone_data if eq['tag'].upper() == tag_input), None)
            if not selected_equipment:
                show_alert("TAG Number not found. Please try again.", "error")
                input("Press Enter to continue...")
                continue
        elif choice == '2':
            # Browse equipment list
            while True:
                clear_screen()
                print(f"=======================================")
                print(f"     Equipment List - {zone_name} Zone     ")
                print("=======================================")
                for i, eq in enumerate(selected_zone_data):
                    print(f"{i+1}. {eq['tag']} - {eq['description']}")
                print("\n0. Back")
                try:
                    eq_choice = int(input("Enter number to select equipment (0 to go back): ").strip())
                    if eq_choice == 0:
                        break
                    elif 1 <= eq_choice <= len(selected_zone_data):
                        selected_equipment = selected_zone_data[eq_choice - 1]
                        break
                    else:
                        show_alert("Invalid selection. Please try again.", "error")
                        input("Press Enter to continue...")
                except ValueError:
                    show_alert("Invalid input. Please enter a number.", "error")
                    input("Press Enter to continue...")
            if not selected_equipment: # If user went back from browse list
                continue
        elif choice == '3':
            break
        else:
            show_alert("Invalid choice. Please try again.", "error")
            input("Press Enter to continue...")
            continue

        if selected_equipment:
            # Check for recent PM operations on this equipment by this user
            recent_pm = [
                rec for rec in pm_records
                if rec['tag'] == selected_equipment['tag'] and rec['user'] == current_user and
                   (datetime.datetime.now() - datetime.datetime.fromisoformat(rec['timestamp'])).total_seconds() < (int(get_setting('warning_period')) * 3600)
            ]
            if recent_pm:
                show_alert(f"Warning: You performed PM on {selected_equipment['tag']} less than {get_setting('warning_period')} hours ago!", "warning")
                input("Press Enter to proceed with PM or Ctrl+C to cancel...")

            do_pm_work(selected_equipment, zone_name)
            break # Exit zone selection after completing PM

def do_pm_work(equipment, zone):
    clear_screen()
    print("=======================================")
    print(f"     Performing PM on: {equipment['tag']}     ")
    print(f"     Description: {equipment['description']}     ")
    print("=======================================")

    pm_results = {}
    for i, stage in enumerate(PM_STAGES):
        print(f"\n--- Stage {i+1}: {stage['name']} ---")
        if stage['type'] == "choice":
            while True:
                print(f"Options: {', '.join(stage['options'])}")
                response = input("Enter your choice (e.g., 'Check mark' or 'Error'): ").strip()
                if response in stage['options']:
                    pm_results[stage['name']] = response
                    break
                else:
                    show_alert("Invalid choice. Please enter one of the specified options.", "error")
        elif stage['type'] == "text":
            pm_results[stage['name']] = input("Enter notes/extra information: ").strip()

    print("\n--- PM Summary ---")
    for stage_name, result in pm_results.items():
        print(f"{stage_name}: {result}")

    confirm = input("\nPress 'PM Finished' (type 'yes' to confirm): ").strip().lower()
    if confirm == 'yes':
        pm_record = {
            "user": current_user,
            "zone": zone,
            "tag": equipment['tag'],
            "description": equipment['description'],
            "timestamp": datetime.datetime.now().isoformat(),
            "pm_data": pm_results
        }
        save_pm_record(pm_record)
        # Remove from active sessions (assuming PM is finished)
        for i, session in enumerate(active_pm_sessions):
            if session['tag'] == equipment['tag'] and session['user'] == current_user:
                active_pm_sessions.pop(i)
                break
        show_alert("PM work finished and recorded successfully!", "success")
    else:
        show_alert("PM work cancelled.", "info")
    input("Press Enter to return to main menu...")

# --- Admin Interface Functions ---
def display_admin_interface():
    clear_screen()
    print("=======================================")
    print(f"     Admin Dashboard - {current_user}     ")
    print("=======================================")
    print("\n1. History")
    print("2. Real-time Monitoring")
    print("3. Reports")
    print("4. Settings")
    print("5. Logout")
    print("=======================================")

def show_history():
    clear_screen()
    print("=======================================")
    print("         PM History (Current Week)     ")
    print("=======================================")
    if not pm_records:
        print("No PM history available.")
    else:
        # Sort by timestamp descending
        sorted_records = sorted(pm_records, key=lambda x: x['timestamp'], reverse=True)
        for record in sorted_records:
            timestamp_dt = datetime.datetime.fromisoformat(record['timestamp'])
            print(f"\nDate/Time: {timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"User: {record['user']}")
            print(f"Zone: {record['zone']}")
            print(f"TAG: {record['tag']}")
            print(f"Description: {record['description']}")
            print("PM Data:")
            for stage, result in record['pm_data'].items():
                print(f"  - {stage}: {result}")
            print("---------------------------------------")
    input("\nPress Enter to return to Admin menu...")

def show_realtime_monitoring():
    clear_screen()
    print("=======================================")
    print("     Real-time PM Activities     ")
    print("=======================================")
    if not active_pm_sessions:
        print("No active PM work at the moment.")
    else:
        for activity in active_pm_sessions:
            print(f"- TAG: {activity['tag']} | Desc: {activity['description']} | User: {activity['user']} | Time: {datetime.datetime.fromisoformat(activity['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
    input("\nPress Enter to return to Admin menu...")

def generate_reports():
    clear_screen()
    print("=======================================")
    print("            Weekly Reports             ")
    print("=======================================")
    print("\n1. Export to Excel (CSV simulation)")
    print("2. Export to PDF (Text file simulation)")
    print("3. Email Report (Simulated)")
    print("4. Back to Admin Menu")
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        export_to_excel_simulated()
    elif choice == '2':
        export_to_pdf_simulated()
    elif choice == '3':
        email_report_simulated()
    elif choice == '4':
        return
    else:
        show_alert("Invalid choice.", "error")
    input("Press Enter to continue...")

def export_to_excel_simulated():
    """Simulates exporting PM history to an Excel (CSV) file."""
    if not pm_records:
        show_alert("No data to export.", "info")
        return

    # Prepare data for CSV
    headers = ["Timestamp", "User", "Zone", "TAG Number", "Equipment Description"]
    # Dynamically add PM stage headers
    for stage in PM_STAGES:
        headers.append(stage['name'])

    csv_data = []
    for record in pm_records:
        row = [
            datetime.datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
            record['user'],
            record['zone'],
            record['tag'],
            record['description']
        ]
        # Add PM stage data
        for stage in PM_STAGES:
            row.append(record['pm_data'].get(stage['name'], 'N/A')) # Use .get for robustness
        csv_data.append(row)

    df = pd.DataFrame(csv_data, columns=headers)
    filename = f"PM_Report_Weekly_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    show_alert(f"Report exported to {filename}", "success")

def export_to_pdf_simulated():
    """Simulates exporting PM history to a PDF (text) file."""
    if not pm_records:
        show_alert("No data to export.", "info")
        return

    filename = f"PM_Report_Weekly_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write("Factory PM Maintenance Weekly Report\n")
        f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if not pm_records:
            f.write("No PM history available for this period.\n")
        else:
            sorted_records = sorted(pm_records, key=lambda x: x['timestamp'])
            for record in sorted_records:
                timestamp_dt = datetime.datetime.fromisoformat(record['timestamp'])
                f.write(f"--- PM Record ---\n")
                f.write(f"Date/Time: {timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"User: {record['user']}\n")
                f.write(f"Zone: {record['zone']}\n")
                f.write(f"TAG: {record['tag']}\n")
                f.write(f"Description: {record['description']}\n")
                f.write("PM Data:\n")
                for stage, result in record['pm_data'].items():
                    f.write(f"  - {stage}: {result}\n")
                f.write("-------------------\n\n")
    show_alert(f"Report exported to {filename}", "success")

def email_report_simulated():
    """Simulates sending a weekly report via email."""
    filename = f"PM_Report_Weekly_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    # First, ensure the report is generated
    export_to_excel_simulated()
    show_alert(f"Simulating email of report '{filename}' to {WEEKLY_REPORT_EMAIL}", "info")
    show_alert("Email sent (simulated successfully).", "success")


# --- Settings Management ---
settings = {
    "reset_period": "weekly", # weekly, daily, hourly, monthly
    "warning_period": "24" # hours
}

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", 'r') as f:
            return json.load(f)
    return settings # return default if no file

def save_settings():
    with open("settings.json", 'w') as f:
        json.dump(settings, f, indent=4)

def get_setting(key):
    return settings.get(key)

def update_reset_period(period):
    global pm_records
    settings['reset_period'] = period
    save_settings()
    show_alert(f"Data reset period updated to: {period}", "success")
    # In a real app, this would trigger a backend process. Here, we just acknowledge.

def update_warning_period(period):
    settings['warning_period'] = str(period) # Store as string
    save_settings()
    show_alert(f"Warning period updated to: {period} hours", "success")


def show_settings():
    clear_screen()
    print("=======================================")
    print("            System Settings            ")
    print("=======================================")
    print(f"Current Data Reset Period: {get_setting('reset_period').capitalize()}")
    print(f"Current Warning Period: {get_setting('warning_period')} hours")
    print("\n1. Change Data Reset Period")
    print("2. Change Warning Period (hours)")
    print("3. Back to Admin Menu")
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        print("\nSelect new reset period:")
        print("  1. One Hour")
        print("  2. Daily")
        print("  3. Weekly")
        print("  4. Monthly")
        period_choice = input("Enter choice (1-4): ").strip()
        if period_choice == '1': update_reset_period('hourly')
        elif period_choice == '2': update_reset_period('daily')
        elif period_choice == '3': update_reset_period('weekly')
        elif period_choice == '4': update_reset_period('monthly')
        else: show_alert("Invalid choice.", "error")
    elif choice == '2':
        while True:
            try:
                new_period = int(input("Enter new warning period in hours (e.g., 24): ").strip())
                if new_period > 0:
                    update_warning_period(new_period)
                    break
                else:
                    show_alert("Period must be a positive number.", "error")
            except ValueError:
                show_alert("Invalid input. Please enter a number.", "error")
    elif choice == '3':
        return
    else:
        show_alert("Invalid choice.", "error")
    input("Press Enter to continue...")

# Load settings on startup
settings = load_settings()


# --- Main Application Loop ---
def run_app():
    global current_interface

    while True:
        if current_interface == "login":
            display_login_screen()
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                login_user("User1")
            elif choice == '2':
                login_user("User2")
            elif choice == '3':
                login_user("User3")
            elif choice == '4':
                login_user("User4")
            elif choice == '5':
                admin_pass = input("Enter Admin Password: ").strip()
                login_admin(admin_pass)
            elif choice == '6':
                print("Exiting application. Goodbye!")
                break
            else:
                show_alert("Invalid choice. Please try again.", "error")
                input("Press Enter to continue...")
        elif current_interface == "user":
            display_user_interface()
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                select_zone("HLP")
            elif choice == '2':
                select_zone("SCREEN")
            elif choice == '3':
                select_zone("COMPACTION")
            elif choice == '4':
                logout()
            else:
                show_alert("Invalid choice. Please try again.", "error")
                input("Press Enter to continue...")
        elif current_interface == "admin":
            display_admin_interface()
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                show_history()
            elif choice == '2':
                show_realtime_monitoring()
            elif choice == '3':
                generate_reports()
            elif choice == '4':
                show_settings()
            elif choice == '5':
                logout()
            else:
                show_alert("Invalid choice. Please try again.", "error")
                input("Press Enter to continue...")

if __name__ == "__main__":
    run_app()
```

```text?code_stderr&code_event_index=3
Traceback (most recent call last):
  File "<string>", line 551, in <module>
  File "<string>", line 501, in run_app
EOFError: EOF when reading a line

```

The Python code I generated aims to create a command-line Preventive Maintenance system.

However, the execution failed with an `EOFError: EOF when reading a line`. This error occurs because the script is designed to be interactive, prompting the user for input (like menu choices or PM data) using the `input()` function. My environment executes code in a non-interactive way, so when the script tries to ask for input, it receives an "End Of File" signal, leading to this error.

**This does not mean the code is incorrect; it means it needs to be run interactively by a human user in a terminal.**

I have built the comprehensive Python script for you, incorporating the following features:

  * **User and Admin Login:** Supports User1-User4 without passwords and an Admin with the password `Karak@2025`.
  * **Data Loading:** Automatically loads equipment data from your `HLP.csv`, `SCREEN.csv`, and `COMPACTION.csv` files.
  * **Zone Selection:** Allows users to select a zone (HLP, SCREEN, COMPACTION).
  * **Equipment Selection:** Within a zone, users can type a TAG number or browse a list to select equipment.
  * **PM Work Stages:** Guides the user through the six PM stages (Sound, Vibration, Heat, Motor umbrella, Status, Note) with appropriate input types (choice or text).
  * **PM Record Saving:** Saves completed PM records to a local `pm_records.json` file.
  * **Active PM Activities:** Displays a simulated list of "Current PM Activities" (though this is for visualization within the single script run, not real-time across multiple users).
  * **Warning for Repeated PM:** Alerts the user if they perform PM on the same equipment within a configurable "warning period."
  * **Admin Dashboard:**
      * **History:** Shows all PM records for the current week. Old records (older than 1 week) are cleared on startup.
      * **Real-time Monitoring:** Displays current active PM activities.
      * **Reports:** Allows exporting PM history to a simulated Excel (CSV) file or a simulated PDF (text) file.
      * **Email Report:** Simulates sending the weekly report to `abdallahdomer@yahoo.com`.
      * **Settings:** Admin can configure the data reset period (hourly, daily, weekly, monthly - currently weekly is active for reset on startup) and the warning period in hours.
  * **Footer:** Includes "Design by: Eng. Abdallah Dmour".

**To run this application on your computer:**

1.  **Save the code:** Copy all the Python code provided below into a file named `pm_system.py`.
2.  **Place CSV files:** Ensure your `HLP.csv`, `SCREEN.csv`, and `COMPACTION.csv` files are in the **same directory** as `pm_system.py`.
3.  **Open a terminal or command prompt.**
4.  **Navigate to the directory** where you saved `pm_system.py`.
5.  **Run the script** using the command: `python pm_system.py`

You will then be able to interact with the system through your terminal.

```python
import pandas as pd
import json
import datetime
import os

# --- Configuration ---
ADMIN_PASSWORD = "Karak@2025"
PM_DATA_FILE = "pm_records.json"
WEEKLY_REPORT_EMAIL = "abdallahdomer@yahoo.com" # This will be used in a simulated email function

# PM Stages
PM_STAGES = [
    {"name": "Sound", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Vibration", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Heat", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Motor umbrella", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Status", "type": "choice", "options": ["Check mark", "Error"]},
    {"name": "Note", "type": "text"}
]

# --- Global Variables ---
current_user = None
current_interface = "login" # "login", "user", "admin"
pm_records = []
active_pm_sessions = [] # For simulating real-time active works

# --- Load Equipment Data ---
def load_equipment_data():
    """Loads equipment data from CSV files."""
    data = {}
    try:
        hlp_df = pd.read_csv('HLP.csv')
        # Ensure column names match exactly or adjust 'TAG number'
        if 'TAG Number' in hlp_df.columns:
            data['HLP'] = hlp_df.rename(columns={'TAG Number': 'tag', 'Equipment Description': 'description'}).to_dict(orient='records')
        else:
            print("Warning: 'TAG Number' column not found in HLP.csv. Please check column names.")
            data['HLP'] = []

        screen_df = pd.read_csv('SCREEN.csv')
        if 'TAG Number' in screen_df.columns:
            data['SCREEN'] = screen_df.rename(columns={'TAG Number': 'tag', 'Equipment Description': 'description'}).to_dict(orient='records')
        else:
            print("Warning: 'TAG Number' column not found in SCREEN.csv. Please check column names.")
            data['SCREEN'] = []

        compaction_df = pd.read_csv('COMPACTION.csv')
        if 'TAG Number' in compaction_df.columns:
            data['COMPACTION'] = compaction_df.rename(columns={'TAG Number': 'tag', 'Equipment Description': 'description'}).to_dict(orient='records')
        else:
            print("Warning: 'TAG Number' column not found in COMPACTION.csv. Please check column names.")
            data['COMPACTION'] = []

    except FileNotFoundError as e:
        print(f"Error loading CSV file: {e}. Make sure HLP.csv, SCREEN.csv, and COMPACTION.csv are in the same directory.")
        # Create empty lists if files are not found to allow the script to run
        data['HLP'] = []
        data['SCREEN'] = []
        data['COMPACTION'] = []
    except Exception as e:
        print(f"An unexpected error occurred while loading CSVs: {e}")
        data['HLP'] = []
        data['SCREEN'] = []
        data['COMPACTION'] = []
    return data

equipment_data = load_equipment_data()

# --- Data Persistence (Simulated Firebase) ---
def load_pm_records():
    """Loads PM records from a local JSON file."""
    if os.path.exists(PM_DATA_FILE):
        try:
            with open(PM_DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {PM_DATA_FILE} is corrupted or empty. Starting with empty records.")
            return []
    return []

def save_pm_record(record):
    """Saves a new PM record and updates active sessions."""
    global pm_records, active_pm_sessions
    pm_records.append(record)
    # Simulate adding to active sessions, then removing when 'finished'
    # For a real multi-user system, this would involve a shared database/backend
    active_pm_sessions.append(record)
    with open(PM_DATA_FILE, 'w') as f:
        json.dump(pm_records, f, indent=4)

def clear_old_records():
    """Clears records older than one week, based on the current calendar date."""
    global pm_records
    current_date = datetime.datetime.now().date()
    
    # Calculate the start of the current week (Monday)
    # Adjust for current day of week (Monday=0, Sunday=6)
    start_of_current_week = current_date - datetime.timedelta(days=current_date.weekday())
    
    # Filter records to keep only those from the current week
    # Assuming 'timestamp' is in ISO format
    records_to_keep = []
    for record in pm_records:
        try:
            record_date = datetime.datetime.fromisoformat(record['timestamp']).date()
            if record_date >= start_of_current_week:
                records_to_keep.append(record)
        except ValueError:
            print(f"Warning: Could not parse timestamp '{record['timestamp']}'. Skipping record.")
            continue
            
    pm_records = records_to_keep
    
    with open(PM_DATA_FILE, 'w') as f:
        json.dump(pm_records, f, indent=4)
    print("Old PM records cleared (older than current calendar week).")


# Initial load of PM records and clearing old ones
pm_records = load_pm_records()
clear_old_records()


# --- User Interface Functions ---
def show_alert(message, type="info"):
    """Simulates an alert box in a command-line interface with colors."""
    color_map = {
        "success": "\033[92m", # Green
        "warning": "\033[93m", # Yellow
        "error": "\033[91m",   # Red
        "info": "\033[94m"     # Blue
    }
    RESET_COLOR = "\033[0m"
    print(f"\n{color_map.get(type, color_map['info'])}--- {type.upper()} ---")
    print(f"{message}{RESET_COLOR}\n")

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_login_screen():
    clear_screen()
    print("=======================================")
    print("     Factory PM Maintenance System     ")
    print("=======================================")
    print("\n--- User Login ---")
    print("1. User1")
    print("2. User2")
    print("3. User3")
    print("4. User4")
    print("\n--- Admin Access ---")
    print("5. Admin Login")
    print("6. Exit")
    print("=======================================")
    print("Design by: Eng. Abdallah Dmour") # Footer

def login_user(user_id):
    global current_user, current_interface
    current_user = user_id
    current_interface = "user"
    show_alert(f"Welcome, {current_user}!", "success")

def login_admin(password):
    global current_user, current_interface
    if password == ADMIN_PASSWORD:
        current_user = "Admin"
        current_interface = "admin"
        show_alert("Admin Login Successful!", "success")
    else:
        show_alert("Incorrect Admin Password!", "error")

def logout():
    global current_user, current_interface, active_pm_sessions
    current_user = None
    current_interface = "login"
    active_pm_sessions = [] # Clear active sessions on logout for this script instance
    show_alert("Logged out successfully.", "info")

def display_user_interface():
    clear_screen()
    print("=======================================")
    print(f"     Welcome, {current_user}     ")
    print("=======================================")
    print("\n--- Current PM Activities ---")
    if not active_pm_sessions:
        print("No active PM work at the moment.")
    else:
        # Display only unique active sessions by tag for a simplified view
        displayed_tags = set()
        for activity in active_pm_sessions:
            if activity['tag'] not in displayed_tags:
                print(f"- TAG: {activity['tag']} | Desc: {activity['description']} | User: {activity['user']} | Time: {datetime.datetime.fromisoformat(activity['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
                displayed_tags.add(activity['tag'])
    print("\n-------------------------------")
    print("\n--- Zone Selection ---")
    print(f"1. HLP Zone ({len(equipment_data.get('HLP', []))} equipments)")
    print(f"2. SCREEN Zone ({len(equipment_data.get('SCREEN', []))} equipments)")
    print(f"3. COMPACTION Zone ({len(equipment_data.get('COMPACTION', []))} equipments)")
    print("\n4. Logout")
    print("=======================================")
    print("Design by: Eng. Abdallah Dmour") # Footer

def select_zone(zone_name):
    global current_user, active_pm_sessions
    selected_zone_data = equipment_data.get(zone_name)
    if not selected_zone_data:
        show_alert(f"No equipment data found for {zone_name} zone. Please check CSV files.", "error")
        input("Press Enter to continue...")
        return

    while True:
        clear_screen()
        print(f"=======================================")
        print(f"     PM Work - {zone_name} Zone     ")
        print("=======================================")
        print("\nSelect Equipment:")
        print("1. Type TAG Number")
        print("2. Browse Equipment List")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        selected_equipment = None
        if choice == '1':
            tag_input = input("Enter TAG Number: ").strip().upper()
            # Find equipment, case-insensitive tag match
            selected_equipment = next((eq for eq in selected_zone_data if eq['tag'].upper() == tag_input), None)
            if not selected_equipment:
                show_alert("TAG Number not found. Please try again.", "error")
                input("Press Enter to continue...")
                continue
        elif choice == '2':
            # Browse equipment list with pagination
            page_size = 10
            num_pages = (len(selected_zone_data) + page_size - 1) // page_size
            current_page = 0

            while True:
                clear_screen()
                print(f"=======================================")
                print(f"     Equipment List - {zone_name} Zone (Page {current_page + 1}/{num_pages})    ")
                print("=======================================")
                start_idx = current_page * page_size
                end_idx = min(start_idx + page_size, len(selected_zone_data))
                
                for i, eq in enumerate(selected_zone_data[start_idx:end_idx]):
                    print(f"{start_idx + i + 1}. {eq['tag']} - {eq['description']}")
                
                print("\n--- Navigation ---")
                if current_page > 0:
                    print("P. Previous Page")
                if current_page < num_pages - 1:
                    print("N. Next Page")
                print("0. Back to previous menu")
                
                eq_choice_input = input("Enter number to select equipment, 'P'/'N' for pages, or '0' to go back: ").strip().upper()
                
                if eq_choice_input == '0':
                    break # Back to zone selection options
                elif eq_choice_input == 'P' and current_page > 0:
                    current_page -= 1
                elif eq_choice_input == 'N' and current_page < num_pages - 1:
                    current_page += 1
                else:
                    try:
                        eq_choice_num = int(eq_choice_input)
                        if 1 <= eq_choice_num <= len(selected_zone_data):
                            selected_equipment = selected_zone_data[eq_choice_num - 1]
                            break # Equipment selected, exit browse loop
                        else:
                            show_alert("Invalid selection number. Please try again.", "error")
                            input("Press Enter to continue...")
                    except ValueError:
                        show_alert("Invalid input. Please enter a number or 'P'/'N'.", "error")
                        input("Press Enter to continue...")
            if not selected_equipment: # If user went back from browse list (by entering '0')
                continue
        elif choice == '3':
            break # Back to main user interface
        else:
            show_alert("Invalid choice. Please try again.", "error")
            input("Press Enter to continue...")
            continue

        if selected_equipment:
            # Check for recent PM operations on this equipment by this user
            warning_period_hours = int(get_setting('warning_period'))
            recent_pm_by_user = [
                rec for rec in pm_records
                if rec['tag'] == selected_equipment['tag'] and rec['user'] == current_user and
                   (datetime.datetime.now() - datetime.datetime.fromisoformat(rec['timestamp'])).total_seconds() < (warning_period_hours * 3600)
            ]
            if recent_pm_by_user:
                show_alert(f"Warning: You performed PM on {selected_equipment['tag']} less than {warning_period_hours} hours ago!", "warning")
                input("Press Enter to proceed with PM or Ctrl+C to cancel...") # Ctrl+C to break program

            do_pm_work(selected_equipment, zone_name)
            break # Exit zone selection after completing PM (or cancellation)

def do_pm_work(equipment, zone):
    clear_screen()
    print("=======================================")
    print(f"     Performing PM on: {equipment['tag']}     ")
    print(f"     Description: {equipment['description']}     ")
    print("=======================================")

    pm_results = {}
    
    # Add this session to active_pm_sessions right away (simulated)
    # This simulates "real-time" visibility before completion
    active_pm_sessions.append({
        "user": current_user,
        "zone": zone,
        "tag": equipment['tag'],
        "description": equipment['description'],
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "In Progress" # Add a status for active sessions
    })


    for i, stage in enumerate(PM_STAGES):
        print(f"\n--- Stage {i+1}: {stage['name']} ---")
        if stage['type'] == "choice":
            while True:
                print(f"Options: {', '.join(stage['options'])}")
                response = input("Enter your choice: ").strip()
                if response in stage['options']:
                    pm_results[stage['name']] = response
                    break
                else:
                    show_alert("Invalid choice. Please enter one of the specified options.", "error")
        elif stage['type'] == "text":
            pm_results[stage['name']] = input("Enter notes/extra information: ").strip()
    
    # Optional: Display summary before final confirmation
    print("\n--- PM Summary ---")
    for stage_name, result in pm_results.items():
        print(f"{stage_name}: {result}")

    confirm = input("\nPM work complete? Type 'yes' to confirm and save, or anything else to cancel: ").strip().lower()
    if confirm == 'yes':
        pm_record = {
            "user": current_user,
            "zone": zone,
            "tag": equipment['tag'],
            "description": equipment['description'],
            "timestamp": datetime.datetime.now().isoformat(),
            "pm_data": pm_results
        }
        save_pm_record(pm_record)
        
        # Remove from active sessions (assuming PM is finished)
        # Find and remove the exact session that was started
        for i, session in enumerate(active_pm_sessions):
            # A simple way to identify the session if no unique ID
            if session['tag'] == equipment['tag'] and session['user'] == current_user and session.get('status') == "In Progress":
                active_pm_sessions.pop(i)
                break
        show_alert("PM work finished and recorded successfully!", "success")
    else:
        # If cancelled, remove from active sessions too
        for i, session in enumerate(active_pm_sessions):
            if session['tag'] == equipment['tag'] and session['user'] == current_user and session.get('status') == "In Progress":
                active_pm_sessions.pop(i)
                break
        show_alert("PM work cancelled. No record saved.", "info")
    input("Press Enter to return to main menu...")

# --- Admin Interface Functions ---
def display_admin_interface():
    clear_screen()
    print("=======================================")
    print(f"     Admin Dashboard - {current_user}     ")
    print("=======================================")
    print("\n1. History")
    print("2. Real-time Monitoring")
    print("3. Reports")
    print("4. Settings")
    print("5. Logout")
    print("=======================================")
    print("Design by: Eng. Abdallah Dmour") # Footer

def show_history():
    clear_screen()
    print("=======================================")
    print("         PM History (Current Week)     ")
    print("=======================================")
    if not pm_records:
        print("No PM history available for the current week.")
    else:
        # Sort by timestamp descending
        sorted_records = sorted(pm_records, key=lambda x: x['timestamp'], reverse=True)
        for record in sorted_records:
            timestamp_dt = datetime.datetime.fromisoformat(record['timestamp'])
            print(f"\nDate/Time: {timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"User: {record['user']}")
            print(f"Zone: {record['zone']}")
            print(f"TAG: {record['tag']}")
            print(f"Description: {record['description']}")
            print("PM Data:")
            for stage, result in record['pm_data'].items():
                print(f"  - {stage}: {result}")
            print("---------------------------------------")
    input("\nPress Enter to return to Admin menu...")

def show_realtime_monitoring():
    clear_screen()
    print("=======================================")
    print("     Real-time PM Activities     ")
    print("=======================================")
    if not active_pm_sessions:
        print("No active PM work at the moment.")
    else:
        print("Note: This shows active sessions in this script run. For multi-user real-time, a web backend is needed.")
        for activity in active_pm_sessions:
            print(f"- TAG: {activity['tag']} | Desc: {activity['description']} | User: {activity['user']} | Status: {activity.get('status', 'N/A')} | Time: {datetime.datetime.fromisoformat(activity['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
    input("\nPress Enter to return to Admin menu...")

def generate_reports():
    clear_screen()
    print("=======================================")
    print("            Weekly Reports             ")
    print("=======================================")
    print("\n1. Export to Excel (CSV simulation)")
    print("2. Export to PDF (Text file simulation)")
    print("3. Email Report (Simulated)")
    print("4. Back to Admin Menu")
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        export_to_excel_simulated()
    elif choice == '2':
        export_to_pdf_simulated()
    elif choice == '3':
        email_report_simulated()
    elif choice == '4':
        return
    else:
        show_alert("Invalid choice.", "error")
    input("Press Enter to continue...")

def export_to_excel_simulated():
    """Simulates exporting PM history to an Excel (CSV) file."""
    if not pm_records:
        show_alert("No data to export.", "info")
        return

    # Prepare data for CSV
    headers = ["Timestamp", "User", "Zone", "TAG Number", "Equipment Description"]
    # Dynamically add PM stage headers
    pm_stage_names = [stage['name'] for stage in PM_STAGES]
    headers.extend(pm_stage_names)

    csv_data = []
    for record in pm_records:
        row = [
            datetime.datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
            record['user'],
            record['zone'],
            record['tag'],
            record['description']
        ]
        # Add PM stage data
        for stage_name in pm_stage_names:
            row.append(record['pm_data'].get(stage_name, 'N/A')) # Use .get for robustness
        csv_data.append(row)

    df = pd.DataFrame(csv_data, columns=headers)
    filename = f"PM_Report_Weekly_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    try:
        df.to_csv(filename, index=False)
        show_alert(f"Report exported to {filename}", "success")
    except Exception as e:
        show_alert(f"Error exporting to CSV: {e}", "error")

def export_to_pdf_simulated():
    """Simulates exporting PM history to a PDF (text) file."""
    if not pm_records:
        show_alert("No data to export.", "info")
        return

    filename = f"PM_Report_Weekly_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(filename, 'w') as f:
            f.write("Factory PM Maintenance Weekly Report\n")
            f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            if not pm_records:
                f.write("No PM history available for this period.\n")
            else:
                sorted_records = sorted(pm_records, key=lambda x: x['timestamp'])
                for record in sorted_records:
                    timestamp_dt = datetime.datetime.fromisoformat(record['timestamp'])
                    f.write(f"--- PM Record ---\n")
                    f.write(f"Date/Time: {timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"User: {record['user']}\n")
                    f.write(f"Zone: {record['zone']}\n")
                    f.write(f"TAG: {record['tag']}\n")
                    f.write(f"Description: {record['description']}\n")
                    f.write("PM Data:\n")
                    for stage, result in record['pm_data'].items():
                        f.write(f"  - {stage}: {result}\n")
                    f.write("-------------------\n\n")
        show_alert(f"Report exported to {filename}", "success")
    except Exception as e:
        show_alert(f"Error exporting to TXT: {e}", "error")

def email_report_simulated():
    """Simulates sending a weekly report via email."""
    # This function just calls the export to excel and simulates sending
    export_to_excel_simulated() # Ensure the file exists for simulation
    
    show_alert(f"Simulating email of report to {WEEKLY_REPORT_EMAIL}", "info")
    show_alert("Email sent (simulated successfully).", "success")


# --- Settings Management ---
settings = {
    "reset_period": "weekly", # weekly, daily, hourly, monthly (Only 'weekly' implemented for auto-clear)
    "warning_period": "24" # hours, stored as string
}

def load_settings():
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", 'r') as f:
                loaded_settings = json.load(f)
                settings.update(loaded_settings) # Update defaults with loaded settings
        except json.JSONDecodeError:
            print(f"Warning: settings.json is corrupted or empty. Using default settings.")
    save_settings() # Ensure settings.json is created/updated with defaults if missing
    return settings

def save_settings():
    with open("settings.json", 'w') as f:
        json.dump(settings, f, indent=4)

def get_setting(key):
    return settings.get(key)

def update_reset_period(period):
    settings['reset_period'] = period
    save_settings()
    show_alert(f"Data reset period updated to: {period}. (Note: Only weekly auto-clear on startup is currently implemented)", "success")

def update_warning_period(period):
    try:
        int_period = int(period)
        if int_period > 0:
            settings['warning_period'] = str(int_period) # Store as string
            save_settings()
            show_alert(f"Warning period updated to: {int_period} hours", "success")
        else:
            show_alert("Warning period must be a positive number.", "error")
    except ValueError:
        show_alert("Invalid input for warning period. Please enter a number.", "error")


def show_settings():
    clear_screen()
    print("=======================================")
    print("            System Settings            ")
    print("=======================================")
    print(f"Current Data Reset Period: {get_setting('reset_period').capitalize()}")
    print(f"Current Warning Period: {get_setting('warning_period')} hours")
    print("\n1. Change Data Reset Period")
    print("2. Change Warning Period (hours)")
    print("3. Back to Admin Menu")
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        print("\nSelect new reset period:")
        print("  1. One Hour (simulated)")
        print("  2. Daily (simulated)")
        print("  3. Weekly")
        print("  4. Monthly (simulated)")
        period_choice = input("Enter choice (1-4): ").strip()
        if period_choice == '1': update_reset_period('hourly')
        elif period_choice == '2': update_reset_period('daily')
        elif period_choice == '3': update_reset_period('weekly')
        elif period_choice == '4': update_reset_period('monthly')
        else: show_alert("Invalid choice.", "error")
    elif choice == '2':
        new_period_input = input("Enter new warning period in hours (e.g., 24): ").strip()
        update_warning_period(new_period_input)
    elif choice == '3':
        return
    else:
        show_alert("Invalid choice.", "error")
    input("Press Enter to continue...")

# Load settings on startup
settings = load_settings()

# --- Main Application Loop ---
def run_app():
    global current_interface

    while True:
        if current_interface == "login":
            display_login_screen()
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                login_user("User1")
            elif choice == '2':
                login_user("User2")
            elif choice == '3':
                login_user("User3")
            elif choice == '4':
                login_user("User4")
            elif choice == '5':
                admin_pass = input("Enter Admin Password: ").strip()
                login_admin(admin_pass)
            elif choice == '6':
                print("Exiting application. Goodbye!")
                break
            else:
                show_alert("Invalid choice. Please try again.", "error")
                input("Press Enter to continue...")
        elif current_interface == "user":
            display_user_interface()
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                select_zone("HLP")
            elif choice == '2':
                select_zone("SCREEN")
            elif choice == '3':
                select_zone("COMPACTION")
            elif choice == '4':
                logout()
            else:
                show_alert("Invalid choice. Please try again.", "error")
                input("Press Enter to continue...")
        elif current_interface == "admin":
            display_admin_interface()
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                show_history()
            elif choice == '2':
                show_realtime_monitoring()
            elif choice == '3':
                generate_reports()
            elif choice == '4':
                show_settings()
            elif choice == '5':
                logout()
            else:
                show_alert("Invalid choice. Please try again.", "error")
                input("Press Enter to continue...")

if __name__ == "__main__":
    run_app()
```