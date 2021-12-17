# Adjacent Content Window

This project is a web application tool that allows the user to create presentations that display related content of different media types parallel to a slideshow in an adjacent window.

Please read this guide in its entirety to answer all your questions related to installation, setup, and running of the application locally.

For more details and navigation of the front-end of the tool, please refer to the project report.

## Installation and Setup

Please clone the **flask_server** branch (id: 03054319).

### Requirements Installation

Run the following command in your terminal to install the necessary requirements.

```shell
pip install -r requirements.txt
```

While running the main program, you may get an error for missing a certain module, in which case you can manually run each installation from the list in **requirements.txt**. 

```shell
pip install -U [requirement_name]
```

### SQL Database Setup

The tool runs on **MySQL** database which is installed locally and connects to the program using a port and user login credentials. If you do not already have MySQL Shell installed on your device, you can follow the instructions here to set it up: [https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html) 

To check if you have MySQL installed properly with root access, run the following command in your terminal and enter your chosen password when prompted

```shell
mysql -u root -p
```

Once inside the MySQL Shell, you will need to create a new database to connect to the application. This can be done by running the following command, replacing **[my_database]** with the database name of your choice.

```
mysql> CREATE DATABASE [my_database];
mysql> USE [my_database];
```

The list of existing databases can be verified by running the following command

```
mysql> SHOW databases;
```

Next a new table will need to be created to store the created presentations. This can be done by running the following CREATE TABLE command in MySQL Shell.

```Shell
mysql> CREATE TABLE userfiles (
  username varchar(100) NOT NULL,
  images text,
  videos text,
  documents text,
  presentation text NOT NULL,
  PRIMARY KEY (username)
);
```

Again, this can be verified by looking at the list of existing tables in the database.

```
mysql> SHOW tables;
```

The remaining setup is done by setting the correct credentials and port values for your device in the Config class in the **config.py** file. An example is shown below.

```python
class Config():
    def __init__(self):
        self.dbuser = "root"
        self.dbpassword = "password123" #root user password
        self.dbport = "3306" #database port
        self.authplugin = "mysql_native_password"
        self.database = "adjacent_window" #database name created in your system [my_database]
```

To verify your local credentials, you can run the following commands in the MySQL Shell. Note that the *user* value should be **"root"** if you entered the MySQL shell using the root password, but you are free to create any new users to connect to the tool if so desired.

```
mysql> SHOW variables WHERE variable_name in ('port');
mysql> SHOW host, user FROM mysql.user;
```

To connect to the remote hosts in cloud databases, replace the details in  **config.py file** to point to the appropriate IP address and port numbers instead of **localhost**. 

## Running the Application Locally

Once all the installations and database setup have been completed, the application can be run by entering the project directory and running the following command in the terminal.

```Shell
python main.py
```

Note that the current setup will start the local host server as a development environment and is run on the localhost **[127.0.0.1:5000](127.0.0.1:5000)**. The default port can be changed from *app.run(, port = "new_port")*.

The landing page should be the login page of the application. A sample login is testuser1 with password: test123. Additional user credentials can be added manually in **login_cred** in **main.py**. 

After login, the user will be directed to the default presentation page with the option of starting a new presentation from scratch (adding embedding links) or retrieving a previously saved presentation, accessible from the two buttons at the top of the screen.

** Please note that each user can only have up to 1 presentation saved in the database and saving a new presentation will override previous projects. The Retrieve button will display the most recently saved presentation for the logged in user. If you would like to save multiple presentations, we recommend creating a new login user for each presentation and saving the credentials. **

## Error Handling

If all the above steps were followed correctly, the tool should run properly on a local device and database. However, the following changes can be made to the source code but it is only advised *if* no other option is working.

- If there is an error with importing installments or modules, please run the installation commands listed in the **Installation** section above. The most common issue may be with the Werkzeug module.

```shell
pip install -U Werkzeug
```

- In **main.py**, changing all instances of the *host* field when connecting to the database (6 in total). It is set to **'localhost'/'127.0.0.1'** by default, but can be altered if the port is changed to an online database or otherwise.
- In **launch.json**, details of the launching the Flask App environment can be changed if necessary. The most likely change would be to change the **Flask App** assignment to **"main.py"** on line 13.

## Authors and Acknowledgement

Planning and Development: Arwa EL-Hawwat & Srikar Nomula

Supervision and Advising: Dr. James Abello Monedero, Dr. Saed Sayad, Haoyang Zhang

Developed for Rutgers University Summer & Fall 2021 Independent Study and Capstone Projects