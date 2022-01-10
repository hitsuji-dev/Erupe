# Server Side Installation (Linux) Prerequisite

This part of the Guide explains to you how you can install this private server on a linux machine. This can especially useful when you want to run this server on a Virtual  Private Server (VPS) by the likes of DigitalOcean, Linode and whoever else. Most of them only deploy Linux on their VPSes. This Guide covers how to get a server running on either [Ubuntu](https://ubuntu.com/) or [Arch Linux](https://archlinux.org/) and their derivatives. This guide as of the time being assumes you are running Linux with a graphical interface, but some knowledge how to use a terminal is useful and somewhat required.

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
