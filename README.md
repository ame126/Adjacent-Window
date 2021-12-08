For the requirements to be installed 
1) Execute : **pip install requirements.txt** - It installs the required libraries for the application to work. 

Database:
It runs with MySQL database which is installed locally and connects to the port. To connect to the remote hosts in cloud databases, replace the config from config.py file to point to the specific ip address and port numbers

Run the main.py file to start the local host server in built to the flask. It serves on localhost(127.0.0.1:5000). 
The default port can be changed from 
app.run(, port = "new_port")

The sample login is testuser1 with password: test123. 
