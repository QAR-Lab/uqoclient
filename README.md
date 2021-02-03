#UQO - You, Quantum and Optimization
---
UQO is an optimization framework developed by the QAR-Lab of the LMU Munich. 

# Setup
---
To install UQO simply do:
```
   pip install uqoclient
   ```

To be able to connect to the UQO servers, you have to create a config object. There are two possibilities to do so:

1. Create the config object directly in the code:
   ```
   ip = "SERVER_IP:SERVER_PORT"
   token = "YOUR_TOKEN"
   config = Config(method="token", credentials=token, endpoint=ip)
   ```
2. Use a config file
   
   Create a config.json with the following structure:
    
   ```
   {
        "method": "token",
        "endpoint": "SERVER_IP:SERVER_PORT",
        "credentials": "YOUR_TOKEN"
   }
   ```
   You can then use this config file as follows:
    
   ```
   from uqoclient.client.config import Config
   config = Config(config_path="Path\to\the\configfile")
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
   
