# Server Side Installation (Windows)

## Step 1: Download the Server files (Server)
- Download the [code repository (repo)](https://github.com/ricochhet/Erupe) using the dropdown within the green “Code” button and choose: Download ZIP.
- Extract the contents of the folder into the directory of you choice (I would recommend avoiding Program Files due to possible permission errors).

## Step 2: Download and Install PostgreSQL (Database)
- Download the [PostgreSQL Installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) for your operating system and choose the latest PostgreSQL version.
- Run the Installer
    - Ensure these components are checked to install:
        - PostgreSQL Server (the actual database technology).
        - pgAdmin 4 (a GUI management tool for our PostgreSQL server).
        - Command Line Tools (a command line tool for managing PostgreSQL servers) - not used in this tutorial but you’ll want it for some management stuff in the future.
    - Select the Data Directory of your choice (the default pre-filled option should be fine).
    - Create a password for the default database user (postgres).
    - Select a port for the database server to listen to (the default 5432 should be fine).
    - Select the Locale (the default should be fine).
    - Finish the installation.

## Step 3: Download and Install Golang (Server language)
- Download the [Golang Installer](https://golang.org/dl/) for your operating system.
- Run the installer using the default options.

## Step 4: Prepare the Database & Install Migration Tools (Facilitates setting up the tables to store information in the database)
### Phase 1: Create a database called `erupe` on our PostgreSQL instance.
- Open pgAdmin 4 and connect using the credentials you supplied in the Download and Install PostgreSQL steps (the default username is postgres).
    - Right click on your PostgreSQL server and select Create -> Database (photo below for assistance).
    - Fill in the Database field with the value: `erupe`.
        - Click save.
    - You should now see a second database called `erupe` created in the browser on the left.

### Phase 2: Get the programs and tools to install `golang-migrate`.
- Open Powershell and use it to install [Scoop](https://scoop.sh/):
    - In order to install scoop we neeed to set the Execution Policy of Powershell in a certain way. Run this command and read its output carefully and allow the execution of remote-signed code: `Set-ExecutionPolicy RemoteSigned -scope CurrentUser`
    - Install scoop itself by typing the command: `iwr -useb get.scoop.sh | iex`.
- Install [golang-migrate](https://github.com/golang-migrate/migrate/tree/master/cmd/migrate) by opening a new Powershell window and typing the command:
    - `scoop install migrate`.

### Phase 3: Run the migrations in the erupe server files to create the database tables.
- Navigate to the root directory of your erupe server files (image for context below).
- In the file browser path, type in cmd and then press enter to launch a command prompt at this location.
- Run the command:
    - `migrate -database postgres://postgres:password@localhost:5432/erupe?sslmode=disable -path migrations up`.
    - **NOTE:** Replace the `password` with the password you set up during the database installation step. If you changed the default port from 5432 during the database installation step, replace it.

## Step 5: Edit the config.json
- Open the `config.json` file with the text editor of your choice.
- Under the “database” section, find the port, username, and password fields and change their values to be whatever you chose during the database installation steps.
- **NOTE:** You may not need to change the port value if you kept the default `5432` port. The default PostgreSQL username is `postgres`.
- Replace the 127.0.0.1 (localhost) with your external IPV4 address (of your router).

## Step 6: Port-forwarding (OPTIONAL)
Your network is set to block incoming requests by default (so that malicious actors aren’t able to get into your network), but sometimes we want users outside of our network to be able to reach services (for example, the server software) without being stopped by our network security. The solution to this is port forwarding, where we essentially say “Hey, if users try to reach resources on this port, let them through”.

In the config.json, there are port entries for the following services (these values can change if you’ve edited your config to use non-default values):

```
Launcher: 80
Sign: 53312
Channel: 54001
Entrance: 53310
```

You will want to forward ports for everything below the line. Once you’ve forwarded these ports for the various services that use them, outside clients IN THEORY should be able to connect to your server (once it’s running in Step 7).

## Step 7: Run the server
- Navigate to the root directory of your erupe server files.
- In the file browser path, type in cmd and then press enter to launch a command prompt at this location.
- Enter the following command: `go run .`.
- Assuming everything has been set up correctly, you should now have a functioning server that clients are able to connect to (they need to follow the section about adding entries to their hosts files here, but instead of 127.0.0.1 they should be entering the IP you found in step 6.
    - In short, what this does is change the outbound request for the urls (example being `mhfg.capcom.com.tw`) routing from that actual location to the newly specified IP address. This enables the server to get this request and act as if it’s the (now offline) Capcom server.
    - If you want to play the game on the same machine you’re hosting the server on, you also need to do the host entries instructions above but you WILL KEEP the `127.0.0.1` entries.
- To close the server, press `CTRL + C`.
