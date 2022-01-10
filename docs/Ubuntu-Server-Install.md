# Server Side Installation (Linux) Prerequisite

This part of the Guide explains to you how you can install this private server on a Linux machine. This can especially useful when you want to run this server on a Virtual  Private Server (VPS) by the likes of DigitalOcean, Linode and whoever else. Most of them only deploy Linux on their VPSes. This Guide covers how to get a server running on either [Ubuntu](https://ubuntu.com/) or [Arch Linux](https://archlinux.org/) and their derivatives. This guide as of the time being assumes you are running Linux with a graphical interface, but some knowledge how to use a terminal is useful and somewhat required.

# Installation of the Server Side on Ubuntu

## Step 1: Download the Server files (Server)
- Download the [code repository (repo)](https://github.com/ricochhet/Erupe) using the dropdown within the green “Code” button and choose: Download ZIP.
- Extract the contents of the folder into the directory of you choice. Please make sure to extract into a directory which you have access to.

## Step 2: Install the required packages (Ubuntu)
In order to get the server running on Ubuntu we need to install some stuff. Most of the stuff we need is in the official repositories of Ubuntu, but we will need to install some stuff out of line.

- Open up a Terminal (Just search for Terminal in the launcher). You will see a shell window with a block-cursor.
- First install Go, Postgresql and some utilities we need later, enter the following command into the just opened terminal: `sudo apt-get install golang postgresql curl git unrar p7zip unzip`
Postgres will be started automatically on Ubuntu.
- We will also need golang-migrate, which is not in the repository of Ubuntu:
    - Go to [https://github.com/golang-migrate/migrate/releases/](https://github.com/golang-migrate/migrate/releases/) and download the lastest version availiable and save it somewhere on your pc. Download `migrate.linux-amd64.deb` for 64-bit or `migrate.linux-386.deb` for 32-bit.
    - Open the file browser and go where you saved the package.
    - To install the package double-click it. This will open the Ubuntu Software Center. In it just click the green "Install"-Button to install golang-migrate.

<!-- This part is commented out for now since I don't know if this is even useful to include in this guide right now. There is a certain advantage to having pgadmin4 installed it makes managing the database way easier, since you have a graphical interface to manage the database later on.  Right now I only list here how to install pgadmin4 in desktop-mode for testing. It is also deployable with a web-interface, but that would need a bit more configuration. But it could be run locally as well. For noe this part of the Guide is commented out since we will need to drop into a postgres-shell anyway later in order to change the password of the postgres database-user. So setting up a database for erupe to use is just a extra command at that point.-->

<!--
- The last thing we need is pgadmin4. This one is also not part of the official repositories. So we need to add a repository from the pgadmin4-developers. To install it on Ubuntu the developer has a [manual here](https://www.pgadmin.org/download/pgadmin-4-apt/). But I will walk you through the steps anyway.
    - Open up a Terminal (Just search for Terminal in the launcher). You will see a shell window with a block-cursor.
    - Add the repository-key for the pgadmin4-repo: `sudo curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add` This downloads the public-key and installs it on your system.
    - Next we add the repository itself: `sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list`
    - Now you can install pgadmin4. We will only focus on the desktop-mode for the time being (this only works when you use Ubuntu with a graphical interface): `sudo apt install pgadmin4-desktop`
-->

## Step 3: Setup postgres (Database Server) and create a database for erupe

With this out of the way. Lets get to setup postgres and create a database for this server to use. Postgres is started automatically after installing it on Ubuntu. We need to add a password for the postgres-user for later use and also create a database for the server to use.

- Open up a Terminal (see above)
- You need to drop into a postgres-shell using this command: `sudo -Hu postgres psql` This drops you into a postgres-shell where you can run database-commands.
- Now in postgres-shell, first change the postgres-user password with this line: `ALTER ROLE postgres WITH PASSWORD 'password';` make note of the semicolon at the end of the command. Also make sure to replace 'password' with something more secure.
- Next we add a database to be used with erupe. Still in postgres-shell use this command to do that: `CREATE DATABASE erupe WITH OWNER postgres;`
- After that is done make sure exit out of postgres-shell using: `exit;`

## Step 4: Run the migrations in the erupe server files to create the database tables.
- Navigate to the root directory of your erupe server files.
- In the file browser path, right click somewhere and select 'Open a Terminal here'.
- In it run the command:
    - `migrate -database postgres://postgres:password@localhost:5432/erupe?sslmode=disable -path migrations up`.
    - **NOTE:** Replace the `password` with the password you set up during the database installation step. If you changed the default port from 5432 during the database installation step, replace it.

## Step 5: Edit the config.json
- Open the `config.json` file with the text editor of your choice.
- Under the “database” section, find the port, username, and password fields and change their values to be whatever you chose during Step 3.
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
- Enter the following command: `sudo go run .`. Superuser-rights (sudo) is needed in order to bind the port 80 to the erupe-server.
- Assuming everything has been set up correctly, you should now have a functioning server that clients are able to connect to (they need to follow the section about adding entries to their hosts files here, but instead of 127.0.0.1 they should be entering the IP you found in step 6.
    - In short, what this does is change the outbound request for the urls (example being `mhfg.capcom.com.tw`) routing from that actual location to the newly specified IP address. This enables the server to get this request and act as if it’s the (now offline) Capcom server.
    - If you want to play the game on the same machine you’re hosting the server on, you also need to do the host entries instructions above but you WILL KEEP the `127.0.0.1` entries.
- To close the server, press `CTRL + C`.
