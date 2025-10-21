# Run the project (Windows)

1. Node version - **20.15.1**
2. Open the project with **VS Code**
3. Create a **.env** file in the root directory (if it doesn't exist) and copy the **env.example** there.

`CONSENSUS_TIME=10`

`RPC_FEE=5`

`SERVER_PORT=53550`

`EXPOSED_URL=http://127.0.0.1:53550`

4.  Run the project to get the public and private keys (**Note: It will be crushed, expected**)

    1. Find the **public key** file in the root directory, copy the **public key**
    2. Create a file **demos\_peerlist.json** in the root directory, and copy the **demos\_peerlist.json.example** there and replace the **“identity”** with your public key.



    <figure><img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXceZxNlQ2gp247ZQoGCeQ_fwrh5fALwSbfVoBf6yj2qP4JTyXgvToN2hM_DIkGZnFDJ9nL2aX-sOxnuP4iuG9K5AxS-EUM8tO9YaWW3tz2EBXxmhPJVuTh0YiuW1udJUjibE0-L?key=RkbH77fVOlsq6AUc04iv4DYy" alt=""><figcaption></figcaption></figure>
5. [Setup WSL2](wsl-2-setup-on-windows-10-and-11-only.md) on your machine if you don’t have it installed.
6. Open the Ubuntu terminal and run the following commands to install the dependencies
   1.  Go to the project folder

       `cd /mnt/c/Users/User/Desktop/node  (example for Desktop)`
   2.  Check the **node** version by running the following command (should be **20.15.1**)

       **node -v**
   3. Run the following commands
      1. `sudo apt-get update`
      2. `sudo apt-get install dos2unix`
      3. `sudo apt install nodejs`
      4. `sudo apt install npm`
      5. `sudo npm install -g n`
      6. `chmod +x install`
      7. `sed -i 's/\r$//' ./install`
      8. `./install`
   4. If you encounter any issues, please check out the [**Issue Troubleshooting**](issue-troubleshooting.md) section.
7. Run the project
   1. Again in the Ubuntu terminal, in the project directory run the **sed -i 's/\r$//' ./run** command
   2. Make sure the **Docker Engine** is running and you have enabled the **WSL2**
      1. Open the **Docker Desktop**
      2. Go to the Settings
      3.  In the **General** section enable the WSL 2-based engine



          <figure><img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXfqWOJ5hvQLb2OMTDbLEJRpbpOugZO3SPWQq8DwWnMNjo_9IsCCn2ldMZvATpFo5UeNFm-ZGLi6SDC7OAGiK3L762n28tvSC9QEVPVpnp4SWXooDcSWDHB0Gvb_FN8HxYqZpeNu1Q?key=RkbH77fVOlsq6AUc04iv4DYy" alt=""><figcaption></figcaption></figure>
      4.  In the Settings menu, go to the **Resources > WSL** **Integration** section and enable the WSL 2 and Ubuntu



          <figure><img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXe4O7Xa9lwdP2rcEcLy3HcF2bLEghScL2YSR8ZtY-4nbwzydy29mZN7a7-M9EUHp61orcUB6DL7bndy24DqclaUaF9M7ReBdx-6UAV3n__SOJwCEUDOLiX6HC4m-0DGoluRSrt9AQ?key=RkbH77fVOlsq6AUc04iv4DYy" alt=""><figcaption></figcaption></figure>
      5. After enabling WSL 2 and WSL integration, click **Apply & Restart** to restart the Docker Desktop and apply the changes.
      6. Run the **docker --version** command in the Ubuntu Terminal and check if all is set.
   3. Go to the **postgres\_5332** folder of the project by running cd postgres\_5332/&#x20;
   4. Run the **sudo usermod -aG docker $USER** command to add your user to the Docker group.
   5. Close and open a new WSL terminal window
   6. Go to the postgres folder again and run the command **docker compose up**&#x20;
   7. Go back to the root directory by running **cd ../ command**
   8. Run the project **./run**&#x20;
