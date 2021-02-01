#UQO - You, Quantum and Optimization
---
UQO is an optimization framework developed by the QAR-Lab of the LMU Munich. 

# Setup
---
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
 


### Error messages while solving

If you try to solve a problem with UQO you might run into problems. Please consider updating ALL your python packages that are relevant for UQO. After you have done this, verify that your code is correct. If you still encounter problems, you can contact me (sebastian.zielinski@ifi.lmu.de) and I will try to help you with your problem.
   
