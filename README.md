Feel free to contribute, make pull requests, open issues, etc. 

Please be respectful of peoples wishes. 

# Erupe
This project is in its infancy and has no reliable active developer, no documentation, and no support.

This project has been solely developed in my spare time for the educational experience of making a server emulator, which I haven't done before. Expectations regarding functionally and code quality should be set accordingly.

[See original README here](./docs/ErupeServer.README.md)

## General
**WARNING:** All current features can be assumed to be very limited or buggy.

Currently allows a JP MHF client (with GameGuard removed) to:
- Login and register an account (registration is automatic if account doesn't exist).
- Create a character.
- Get ingame to the main city.
- See other players walk around.
- Do quests:
    - Only quests shipped with the game are on the counter.
    - **Requires binary quest files not in the repository.**
- Use (local) chat.
- Partial guild support.


## Server Setup Guide
The erupe server is still heavily in development and you should expect numerous bugs, crashes, and other unintended behavior during use.

Really take a moment to figure out *why* you want to do this setup, and if you're capable enough *to* do it. This guide tries to make everything as simple as possible, but will still require a fairly good understanding of how computers operate. 

This server is *experimental*, many bugs, crashes, and other unintended behavior ***WILL*** occur. This is not suited for gameplay, you can *play* the game, but keep in mind the above. This is primarily for development and research purposes. 

This guide is intended for use on **Windows 10** platforms. The server-side can also be installed on Linux pretty easily. Included further down is a guide for the server-side install on Ubuntu and Arch Linux.

## Resources
- [Erupe Server](https://github.com/ricochhet/Erupe)
- [Progression files](https://archive.org/details/mhfz_progression)

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


# Server Side Installation (Linux) Prerequisite

This part of the Guide explains to you how you can install this private server on a linux machine. This can especially useful when you want to run this server on a Virtual  Private Server (VPS) by the likes of DigitalOcean, Linode and whoever else. Most of them only deploy Linux on their VPSes. This Guide covers how to get a server running on either [Ubuntu](https://ubuntu.com/) or [Arch Linux](https://archlinux.org/) and their derivatives. This guide as of the time being assumes you are running Linux with a grapical interface, but some knowledge how to use a terminal is useful and somewhat requiered.

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

# Installation of the Server Side on Arch Linux

## Step 1: Download the Server files (Server)
- Download the [code repository (repo)](https://github.com/ricochhet/Erupe) using the dropdown within the green “Code” button and choose: Download ZIP.
- Extract the contents of the folder into the directory of you choice. Please make sure to extract into a directory which you have access to.

## Step 2: Install the required packages (Arch Linux)

We need to install some packages for the server to work on Arch Linux. Most of the stuff we need is in the official repositories of Arch, but we will need to install some stuff out of Arch User Repository, which might be a potential risk. This tutorial will use yay for that, but you can use whichever AUR-helper you like or even build it yourself with makepkg.

- Open up a Terminal (Just search for Terminal in the launcher). You will see a shell window with a block-cursor.
- Install some stuff we need, which includes posgresql (Database Server), Go (Server Language) and some other useful utilities from the official repositories with this command: `sudo pacman -Syu postgresql git curl unrar p7zip unzip go`
- Next we need some stuff from the Arch User Repository. This Guide uses yay, so install it like this:
    - Still in the terminal run the following command to download the necessary files to build yay: `git clone https://aur.archlinux.org/yay-bin.git`
    - change to this new directory: `cd yay-bin`
    - build and install the package with: `makepkg -rsi`
- With our helper now installed we can install golang-migrate from the AUR for later use: `yay -S migrate`

<!-- Installing pgadmin 4 on arch was no problem, but it would not run for me sadly. So it is not included in this guide. -->

## Step 3: Get Postgres (Database Server) running on Arch Linux

Unlike Ubuntu, on Arch Linux Postgres needs some further setup to get running and is not started automatically. Just follow these steps to setup postgres on Arch Linux:

- Open up a Terminal, if not already open.
- Create the neccessary Postgres-folder and data with this command: `sudo su postgres -c "initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'"` Make sure also to copy the used single and double-quotes as shown.
- Start & Enable the Postgres-Server (it will be started at each reboot): `sudo systemctl enable --now postgresql`
- Check that everything runs fine with: `sudo systemctl status postgresql`. It should say active (running) somewhere.

## Step 4: Setup postgres (Database Server) and create a database for erupe

With this out of the way. Lets get to setup postgres and create a database for this server to use. We need to add a password for the postgres-user for later use and also create a database for the server to use.

- Open up a Terminal (see above)
- You need to drop into a postgres-shell using this command: `sudo -Hu postgres psql` This drops you into a postgres-shell where you can run database-commands.
- Now in postgres-shell, first change the postgres-user password with this line: `ALTER ROLE postgres WITH PASSWORD 'password';` make note of the semicolon at the end of the command. Also make sure to replace 'password' with something more secure.
- Next we add a database to be used with erupe. Still in postgres-shell use this command to do that: `CREATE DATABASE erupe WITH OWNER postgres;`
- After that is done make sure exit out of postgres-shell using: `exit;`

## Step 5: Run the migrations in the erupe server files to create the database tables.
- Navigate to the root directory of your erupe server files.
- In the file browser path, right click somewhere and select 'Open a Terminal here'.
- In it run the command:
    - `migrate -database postgres://postgres:password@localhost:5432/erupe?sslmode=disable -path migrations up`.
    - **NOTE:** Replace the `password` with the password you set up during the database installation step. If you changed the default port from 5432 during the database installation step, replace it.

## Step 6: Edit the config.json
- Open the `config.json` file with the text editor of your choice.
- Under the “database” section, find the port, username, and password fields and change their values to be whatever you chose during the database installation steps.
- **NOTE:** You may not need to change the port value if you kept the default `5432` port. The default PostgreSQL username is `postgres`.
- Replace the 127.0.0.1 (localhost) with your external IPV4 address (of your router).

## Step 7: Port-forwarding (OPTIONAL)
Your network is set to block incoming requests by default (so that malicious actors aren’t able to get into your network), but sometimes we want users outside of our network to be able to reach services (for example, the server software) without being stopped by our network security. The solution to this is port forwarding, where we essentially say “Hey, if users try to reach resources on this port, let them through”.

In the config.json, there are port entries for the following services (these values can change if you’ve edited your config to use non-default values):

```
Launcher: 80
Sign: 53312
Channel: 54001
Entrance: 53310
```

You will want to forward ports for everything below the line. Once you’ve forwarded these ports for the various services that use them, outside clients IN THEORY should be able to connect to your server (once it’s running in Step 7).

## Step 8: Run the server
- Navigate to the root directory of your erupe server files.
- In the file browser path, type in cmd and then press enter to launch a command prompt at this location.
- Enter the following command: `sudo go run .`.Superuser-rights (sudo) is needed in order to bind the port 80 to the erupe-server
- Assuming everything has been set up correctly, you should now have a functioning server that clients are able to connect to (they need to follow the section about adding entries to their hosts files here, but instead of 127.0.0.1 they should be entering the IP you found in step 6.
    - In short, what this does is change the outbound request for the urls (example being `mhfg.capcom.com.tw`) routing from that actual location to the newly specified IP address. This enables the server to get this request and act as if it’s the (now offline) Capcom server.
    - If you want to play the game on the same machine you’re hosting the server on, you also need to do the host entries instructions above but you WILL KEEP the `127.0.0.1` entries.
- To close the server, press `CTRL + C`.

# Client Side Installation (WINDOWS ONLY)

The Monster Hunter Frontier Client heavily relies on Internet Explorer to work properly. So getting it to run on linux might not be possible at all. If you have some idea how to maybe get it working on linux as well please get in touch. For now the Client only works on Windows.

## Step 1: Download the Japanese Pre-Installed Client Files
- Get the [MHF-ZZ_Installed_Files.zip from archive.org](https://archive.org/details/mhfzzinstalledfiles_20200204).
- Extract the contents of this folder wherever you want the game.

## Step 2: Download Python & Install Frida

Installing frida via pip does not work with the latest python 3.10 release. You need to work around it a bit to install frida it only works on python 3.8 as far as I can see.

- Download python 3.8.10 for windows here: [Download the lastest release of Python 3.8](https://www.python.org/downloads/release/python-3810/)
- Go to fridas pypi-page: https://pypi.org/project/frida/
- Go to "Download Files"
- Download either "frida-15.1.14-py3.8-win-amd64.egg" or "frida-15.1.14-py3.8-win32.egg" depending if your system is 64-bit or 32-bit.
- Save it to: C:\Users\USERNAME
- Enter the command: `pip install frida`.

## Step 3: Download / Copy the Client Patcher
- Within your `MFH-ZZ_Installed_Files` folder (or whatever you named the folder containing mhf.exe) either [download this script](https://gist.github.com/Andoryuuta/a51d9f79114d64946b9e0656cdc0a72e) or copy and paste it into the same named file within this directory.
- **NOTE:** This has to be done for two reasons, there are protections on the mhf.exe itself called AsProtect and an ~~Anti-Cheat~~ Malware program called GameGuard. Both prevent us from being unable to connect to private servers, and this python script bypasses both to allow us to successfully launch the game.

## Step 4: Edit your HOSTS file
- We need to fool our client into thinking it’s reaching out to the official capcom jp or tw servers when in reality it’s connecting to our local ip (127.0.0.1) or an external host ip (the external ipv4 address of whomever is hosting).
- Navigate to `C:/Windows/System32/drivers/etc/hosts` and add the following entries:

```
127.0.0.1 mhfg.capcom.com.tw
127.0.0.1 mhf-n.capcom.com.tw
127.0.0.1 cog-members.mhf-z.jp
127.0.0.1 www.capcom-onlinegames.jp
127.0.0.1 srv-mhf.capcom-networks.jp
```

**NOTE:** Any time you’re messing with files in System32, really take an extra minute to verify you know what operation you’re doing and why. I imagine a lot of less technically inclined people will try this, and in general anytime you find yourself in some part of the System32 directory ensure that you’re not being led horribly astray. That’s why throughout this guide I try to give you the “why” of what you’re doing.

## Step 5: Run the Client Patcher
- For this to work, the server has to be running in order to authenticate against our private server.
- Open a command prompt as an administrator and navigate to the root directory of your MHF-ZZ_Installed_Files folder (or wherever you extracted its contents) and enter the following: `py no_gg_jp.py`.
    - The game launcher should now open and bring you to a screen with a username and password. Enter anything for these as the server will create a new entry in the db if the user doesn’t exist.
    - Select the premade character and enter the game. This will allow you to make your actual character in-game.

## Extra and Troubleshooting

Sometimes the Monster Hunter Frontier Client can act funky when testing things and reinstalling or changing the server you play on. As a first step when troubleshooting things in the MHF-Client it can help to delete *Internet Explorers* (not Edge) Cache. This is pretty easy.
- Open up Internet Explorer
- Click on the little cogwheel on the top right
- Select Safety -> Delete browsing history
- In the now opening window check all the boxes and hit "Delete".

Hyper-V support / WSL2 ports may conflict with the ones used by Erupe ([issue](https://github.com/ErupeServer/Erupe/issues/34)), to fix this, run the following:
- Run: `dism.exe /Online /Disable-Feature:Microsoft-Hyper-V`.
- Reboot your device.
- Run:
        ```
        netsh int ipv4 add excludedportrange protocol=tcp startport=53310 numberofports=1
        netsh int ipv4 add excludedportrange protocol=tcp startport=53312 numberofports=1
        netsh int ipv4 add excludedportrange protocol=tcp startport=54001 numberofports=1
        dism.exe /Online /Enable-Feature:Microsoft-Hyper-V
        ```
- Reboot your device.

## Credits
- [Erupe Contributors](https://github.com/ErupeServer/Erupe)
- [theBusBoy](https://github.com/theBusBoy)
