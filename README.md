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

## Useful Resources
- [Erupe Server](https://github.com/ricochhet/Erupe)
- [Progression files](https://archive.org/details/mhfz_progression)

## Server Setup Guide
The erupe server is still heavily in development and you should expect numerous bugs, crashes, and other unintended behavior during use.

Really take a moment to figure out *why* you want to do this setup, and if you're capable enough *to* do it. This guide tries to make everything as simple as possible, but will still require a fairly good understanding of how computers operate. 

This server is *experimental*, many bugs, crashes, and other unintended behavior ***WILL*** occur. This is not suited for gameplay, you can *play* the game, but keep in mind the above. This is primarily for development and research purposes. 

The Server is written in Go, so it basically should support any Operating system that can run golang and golang-migrate as well as postgres for the database-server. Here are a few Guides to help get you started on some different Operating Systems. If you feel like we miss an important OS feel free to add a Guide via Pull Request.

- [Guide to Install Server Side on Windows (10)](./docs/Windows-Server-Install.md)
- [Guide to Install Server Side on Ubuntu](./docs/Ubuntu-Server-Install.md)
- [Guide to Install Server Side on Arch Linux](./docs/Arch-Server-Install.md)

## Client Setup Guide

The Monster Hunter Frontier Client heavily relies on Internet Explorer to work properly. So getting it to run on Linux might not be possible at all. If you have some idea how to maybe get it working on Linux as well please get in touch. For now the Client only works on Windows. Here is the Guide on how to set it up:

- [Guide to install the MHF Client on Windows (10)](./docs/Windows-Client-Install.md)

## Troubleshooting

There are some common problems which can occur while trying to setup either the Server Side or the Client Side of this. If you run into a problem please refer to the [Troubleshooting-Section](./docs/Troubleshooting.md) of the documentation. It lists some common solutions. If you have a fix that is not listed there yet, please feel free to send a pull request.
s
## Credits
- [Erupe Contributors](https://github.com/ErupeServer/Erupe)
- [theBusBoy](https://github.com/theBusBoy)
