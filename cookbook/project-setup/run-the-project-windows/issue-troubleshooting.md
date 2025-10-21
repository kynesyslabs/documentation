# Issue Troubleshooting

1.  In case of facing the following issue, do the following steps



    <figure><img src="../../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>



    1.  First, remove any existing installations:

        `sudo apt-get remove nodejs npm`

        `sudo apt-get clean`

        `sudo apt-get autoremove`

        1.  Update your package lists:

            `sudo apt-get update`
        2.  Install curl if you don't have it (**you can skip this if curl is already installed**):

            `sudo apt-get install curl`
        3.  Add the NodeSource repository for Node.js 20.x (**you can change 20.x to another version if needed**):

            `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -`
        4.  Install Node.js (**this will include npm**):

            `sudo apt-get install -y nodejs`
        5.  Verify the installation:

            `node --version`

            `npm --version`


2.  Error: Command **'yarn'** failed\


    <figure><img src="../../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

    1. First, check if the **Node** version is **20.15.1**
    2.  Clean your yarn cache and remove **node\_modules**

        `yarn cache clean`\


        `rm -rf node_modules`
    3.  Make sure you have the necessary **build tools**

        `sudo apt-get update`



        `sudo apt-get install -y build-essential python3 make gcc g++`
    4.  If you’re still facing issues with **eiows**, we can try using a pre-built binary. Add this to your `package.json`

        `{`

        &#x20; `"resolutions": {`

        &#x20;   `"eiows": "^6.7.2"`

        &#x20; `}`

        `}`
    5.  Then run&#x20;

        `yarn install`

