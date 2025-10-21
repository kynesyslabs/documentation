# Run the project (MacOS)

1. Node version - **20.15.1**
2. Run the **Docker Engine** on your local machine
3. Open the project with **VS Code**
4. Create a **.env** file in the root directory (if it doesn't exist) and copy the **env.example** there.

`CONSENSUS_TIME=10`

`RPC_FEE=5`

`SERVER_PORT=53550`

`EXPOSED_URL=http://127.0.0.1:53550`

5. Make the following changes to the install file:
   1. Comment on all the **apt-get** related lines (25, 41, 42, 53, 61, 62)
   2. Change the line 93 from source **$HOME/.bashrc** to source **$HOME/.zshrc**
6. Open the **terminal**&#x20;
7. Run the command .**/install**
8. After successfully installing the dependencies, find the **public key** file in the root directory, copy the **public key**
9. Create a file **demos\_peerlist.json** in the root directory, and copy the **demos\_peerlist.json.example** there and replace the **“identity”** with your public key.

<figure><img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXceZxNlQ2gp247ZQoGCeQ_fwrh5fALwSbfVoBf6yj2qP4JTyXgvToN2hM_DIkGZnFDJ9nL2aX-sOxnuP4iuG9K5AxS-EUM8tO9YaWW3tz2EBXxmhPJVuTh0YiuW1udJUjibE0-L?key=RkbH77fVOlsq6AUc04iv4DYy" alt=""><figcaption></figcaption></figure>

10. Run the project **./run**



