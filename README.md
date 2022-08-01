# Random Menu Generator

Random menu generating web application.

Features
--------
* Users can get, add, bulk add with comma separated string, and delete menus
* Users can get random lunch and dinner menus from the given pool of menus
* Users can set starting date, how long he/she wants to get the menus, and how long he/she wants to avoid duplication.
* Random generation is deterministic as long as the menu pool and the deduplication day is the same
* The app doesn't store history but just stores user given menu list.

Requirements
------------
Install MongoDB on the same host and default port 27017


How to Build
------------
### 1. backend ###
```sh
cd backend
```
In python3 virtual environment,
```sh
pip install -r requirements.txt
python api.py
```
The server uses port 5000

### 2. frontend ###
```sh
cd frontend
npm install
npm start
```
The UI uses port 3000
