# Troubleshooting and Tips

## General Tips

Sometimes the Monster Hunter Frontier Client can act funky when testing things and reinstalling or changing the server you play on. As a first step when troubleshooting things in the MHF-Client it can help to delete *Internet Explorers* (not Edge) Cache. This is pretty easy.
- Open up Internet Explorer
- Click on the little cogwheel on the top right
- Select Safety -> Delete browsing history
- In the now opening window check all the boxes and hit "Delete".

## Port conflicts

- Hyper-V support / WSL2 ports may conflict with the ones used by Erupe ([issue](https://github.com/ErupeServer/Erupe/issues/34)), to fix this, run the following:
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

## No Sound while Ingame

It seems like there is an issue, where the sound ingame is all the way down, so you won't hear anything. Going into the Settings and increase Volume there should help.

If you find another common problem feel free to leave a pull request so the solution can be added here.
