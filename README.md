# ADOFAI_DELETE_TOOL WEB

This is the web version for ADOFAI_DELETE_TOOL

# How to deploy
```powershell
python -m pip install requirements.txt

python app.py 
```

We recommend deploying using a virtual environment or conda because it is more convenient for you to modify or use, without polluting the existing Python environment

When deploying, if you need to modify the port, please make sure to also modify the port in 'templates/upload.html' so that it can run properly

Please note that you should modify the IP address in the "upload.html" file located in the "templates" folder to match the IP address of your own VPS.

