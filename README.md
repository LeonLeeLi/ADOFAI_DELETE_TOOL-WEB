# ADOFAI_DELETE_TOOL WEB

This is the web version for ADOFAI_DELETE_TOOL

# How to deploy
```powershell
.\venv\scripts\activate.bat

python app.py 
```


```bash
.\venv\scripts\activate

python app.py
```

We recommend deploying using a virtual environment or conda because it is more convenient for you to modify or use, without polluting the existing Python environment

When deploying, if you need to modify the port, please make sure to also modify the port in 'templates/upload.html' so that it can run properly

Please note that you should modify the IP address in the "upload.html" file located in the "templates" folder to match the IP address of your own VPS.

The default port is 5123 , you can also use nginx to deploy this.

We recommend that you use the Docker version ，There is the website.

### **This project is no longer being updated. Please migrate to the Docker version.**
