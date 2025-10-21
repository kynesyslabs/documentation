# WSL 2 Setup on Windows (10 and 11 only)

1. Run the Windows **PowerShell as Administrator**
2.  Enable **WSL** by running the command:

    `dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`
3.  Enable the Virtual Machine Platform by running the following command:

    `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`
4. Restart the computer to apply the changes
5. Install the **WSL2** Update package (**Note: If you are using Windows 11 skip this step**)
   1. Download the **WSL2** [Linux kernel update](https://learn.microsoft.com/en-us/windows/wsl/install-manual) package.
   2. Run the installer and follow the on-screen instructions.
6. Open **PowerShell as Administrator** again
7.  Run the following command to set **WSL2** as the default version:

    `wsl --set-default-version 2`
8. Install [Ubuntu ](https://apps.microsoft.com/detail/9pdxgncfsczv?hl=en-us\&gl=US)from the Microsoft Store.
9. Click Install and follow the on-screen instructions. (**Note: Make sure to keep the set password**)
10. You’re all set, to make sure that you are successfully done you can run the following command:

    `wsl --list --verbose`

    You should see this

    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXd8XCoT-kBT_xlw4fX2axwSoS1QWkIhk2NOMH7Ms5-XRLX62XFk1B_efGlQVDyLwTJGKw19yrlUstM-1OI0EzZPJWL-PRM19SLUVeK1303T4kIAha2u-9dgcs4MfPPo_TQBE0pU9Q?key=RkbH77fVOlsq6AUc04iv4DYy)
