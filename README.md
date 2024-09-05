# Async Using Django Channels

**SysOpsSuite** is an educational project aimed at demonstrating the capabilities of Django Channels for real-time, asynchronous communication in web applications. It showcases how Django Channels can be used to implement WebSocket-based features, such as live task tracking, backup status updates, and converting network switch backups into searchable JSON data.

The project is designed for learning and exploration purposes, highlighting how real-time updates can be integrated into a Django-based application. Users can create, update, delete, and monitor tasks, as well as observe live progress during backup processing.

This application is intended strictly for development and internal environments. It is not production-ready and should only be used as an example for learning how Django Channels works.

**Note:** This is a demo project, created for educational purposes only, to illustrate the use of Django Channels and WebSockets.

## Features

- **Backup Processing:** Upload and process backup configuration files from network devices.
- **Real-Time Progress Tracking:** See live updates of the backup processing status through a progress bar using WebSockets.
- **Config Search:** Search device configurations based on various filters like VLANs, Hostnames, Interfaces, Routing protocols, ACLs, etc.
- **Database Storage:** Automatically store device configuration data into a Django-managed database.
- **Mobile Responsive:** Fully mobile-responsive interface using TailwindCSS for a clean and modern UI.
- **WebSocket Integration:** WebSocket-based real-time communication for dynamic updates.

## Project Structure

- **Django Backend**: The core of the application, handling routing, database models, and processing logic.
- **WebSocket Communication**: Real-time communication is handled using Django Channels and WebSockets, which enable live updates of the backup processing progress.
- **Frontend**: HTML, JavaScript (with TailwindCSS), and WebSocket integration to display real-time progress, initiate backup processes, and provide search functionality for stored configurations.

## How It Works

1. **Manual Backup Processing:**
   - Users can trigger manual processing of network device backups via a button on the "Manual Triggers" page.
   - The progress is updated in real-time, and after completion, users are notified to check the status or search configurations.

2. **Configuration Search:**
   - Provides advanced filtering and sorting options (by VLAN, Hostname, Routing, etc.) to help admins quickly find the relevant data from stored configurations.

3. **Real-Time Updates:**
   - Through the use of WebSockets, progress bars are dynamically updated on the frontend as backups are processed in the backend. A final message notifies the user upon successful completion.

## Requirements

To run **SysOpsSuite**, you'll need:

- Python 3.8+
- Django 4.x
- Django Channels
- PostgreSQL (or any other supported database)
- Redis (for WebSocket handling)
- TailwindCSS (for UI)
- Web browser with WebSocket support

## Setup and Installation

Follow these steps to set up the **SysOpsSuite** application for local development:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/sysopssuite.git
```
```bash
cd sysopssuite
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
```
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies and create super user
```bash
pip install -r requirements.txt
```
```bash
python3 manage.py createsuperuser
```
username: john.doe@app.com
email: john.doe@app.com
password: Welcome100!

### 4. Set Up Django
Make sure you have PostgreSQL or SQLite installed, and update your settings.py to reflect the correct database setup. Then run:
```bash
python manage.py migrate
```
### 5. Install Redis (For WebSockets)
SysOpsSuite uses Redis for WebSocket message brokering. Install Redis:
```bash
macOS: Use Homebrew: brew install redis
```
Linux: Use your package manager (e.g., apt install redis-server)
Windows: Download Redis for Windows
### 6. Run Redis Server
After installing Redis, ensure it's running:
```bash
redis-server
```
### 7. Run the Application
To start the development server, run:
```bash
python manage.py runserver
```
This will run the Django development server at http://127.0.0.1:8000/.

### 8. Running Channels Worker
SysOpsSuite uses Django Channels for WebSockets. To run the channels worker, use:
```bash
python manage.py runworker
```
You may also need to run the channels layer using daphne or uvicorn if configured for production.

### 9. Access the App
Open your browser and navigate to:

http://127.0.0.1:8000/


Login and head over the "manual triggers" and start the running config to json task.

Once finished you should be able to search through the dummy running config data, see backup statuses, etc.

## Usage
Manual Triggers: Navigate to the "Manual Triggers" page and click the "Start Backup Processing" button. You'll see a progress bar that dynamically updates as backups are processed.

Search Configurations: Go to the "Config Search" page to filter and sort device configurations by categories like VLANs, Interfaces, and Routing.

### License
SysOpsSuite is licensed under the MIT License. See the LICENSE file for more details.

# Happy SysAdmin-ing!
