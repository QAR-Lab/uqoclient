#UQO - You, Quantum and Optimization
---
UQO is an optimization framework developed by the [QAR-Lab of the LMU Munich](https://qar-lab.de). 

# Setup
---
To install UQO simply do:
```
   pip install uqo
   ```

To be able to connect to the UQO servers, you have to create a config object. There are two possibilities to do so:

1. Generate private/public keys

    UQO uses elliptic curve cryptography to securely communicate with the UQO servers. Therefore you have to generate your
    private and public key first, before you can start using UQO. This is done as follows:

    ```
      import os
      from uqo.generate_certificates import generate_certificates
      generate_certificates(os.path.dirname(os.path.realpath(__file__)))
    ```
    
    This will generate 3 folders ("certificates", "private_keys" and "public_keys") in your current working directory.
    The "certificates" folder is used as a temporary directory and should be empty after the process completed. You can
    safely delete this folder. 


2. Create the config object directly in the code:
   ```
   ip = "SERVER_IP:SERVER_PORT"
   token = "YOUR_TOKEN"
   private_key_file = "PATH_TO_YOUR_PRIVATE_KEY_FILE"
   config = Config(method="token", credentials=token, endpoint=ip, private_key_file=private_key_file)
   ```
   
   Replace "PATH_TO_YOUR_PRIVATE_KEY_FILE" with the actual path to the clien.key_secret file you generated in step 1.
3. Use a config file
   
   Create a config.json with the following structure:
    
   ```
   {
        "method": "token",
        "endpoint": "SERVER_IP:SERVER_PORT",
        "credentials": "YOUR_TOKEN",
        "private_key_file": "PATH_TO_YOUR_PRIVATE_KEY_FILE"
   }
   
   Replace "PATH_TO_YOUR_PRIVATE_KEY_FILE" with the actual path to the client.key_secret file you generated in step 1.

   
   ```
   You can then use this config file as follows:
    
   ```
   from uqo.client.config import Config
   config = Config(configpath="Path\to\the\configfile")
   ```
In the examples above please replace SERVER_IP and SERVER_PORT with the ip and port of the UQO server. Also replace YOUR_TOKEN with your personal UQO token.

###
Current State of UQO
---
Although UQO can already be used for a lot of tasks, it is still work in progress. You may very well run into problems where you 
would like to use a feature which has not yet been implemented or is not working as intended due to bugs. In this case please let me know
about the exact problem or the exact feature you want to use, so I can fix / implement it.

You find my E-mail at the bottom of this ReadMe.
###
FAQ
---
Required Python Version: >= 3.7

### Error messages while solving

If you try to solve a problem with UQO you might run into problems. Please consider updating ALL your python packages that are relevant for UQO. After you have done this, verify that your code is correct. If you still encounter problems, you can contact me (sebastian.zielinski@ifi.lmu.de) and I will try to help you with your problem.
   
