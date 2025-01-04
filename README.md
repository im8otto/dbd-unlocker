# Dead by Daylight Unlocker
Proxy written in Python that uses mitmproxy to unlock all in DbD.\
Use it ONLY with Epic or Microsoft game version.

# Usage
Install Python 3\
(For Linux only create a venv i used ~/.venv as location called in DbD Unlocker Launcher.sh)\
Install requirements with pip (for linux make sure to install them in your venv)\
Run the script (Windows double click, Linux open DbD Unlocker Launcher.sh flag it as executable)

# Docker usage
Configure your container using this [Dockerfile](https://raw.githubusercontent.com/im8otto/dbd-unlocker/refs/heads/main/Dockerfile)\
Run container\
On machine where you run DbD:
 - Set proxy with Container machine IP port 8082
 - Open http://mitm.it/cert/cer
 - Download certificate and import
 - Launch DbD
