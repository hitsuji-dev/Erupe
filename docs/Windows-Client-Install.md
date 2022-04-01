# Client Side Installation (WINDOWS ONLY)

The Monster Hunter Frontier Client heavily relies on Internet Explorer to work properly. So getting it to run on Linux might not be possible at all. If you have some idea how to maybe get it working on Linux as well please get in touch. For now the Client only works on Windows.

## Step 1: Download the Japanese Pre-Installed Client Files
- Get the [MHF-ZZ_Installed_Files.zip from archive.org](https://archive.org/details/mhfzzinstalledfiles_20200204).
- Extract the contents of this folder wherever you want the game.

## Step 2: Download Python & Install Frida

Using the launcher patcher with python 3.10 does not work as it seems. It is eiter that the script has to be modified to work with python 3.10 or frida has a problem with 3.10. For this guide we will use python 3.8, which works fine for our purposes:

- Download python 3.8.10 for windows here: [Download the la test release of Python 3.8](https://www.python.org/downloads/release/python-3810/)
- Install and **MAKE SURE YOU SELECT THE OPTION TO ADD PYTHON TO PATH.**
- Open a new command prompt (not a python shell).
- Enter the command: `pip install frida`.

## Step 3: Download / Copy the Client Patcher

Download the Client-Patcher, which you can either copy or download [from here](../archive/no_gg_jp.py)

- After you downloaded the right script put it within your `MFH-ZZ_Installed_Files` folder (or whatever you named the folder containing mhf.exe). The patch has to be in the same directory as the EXE of the game.
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
