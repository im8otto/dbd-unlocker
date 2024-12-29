from datetime import datetime
import requests
import tempfile
from Utils import Misc
import os
import subprocess
import time

def init():
    if Misc.current_system == "Windows":
        import win32crypt as wcrypt
        try:
            CERT_STORE_PROV_SYSTEM = 0x0000000A
            CERT_SYSTEM_STORE_LOCAL_MACHINE = 0x00020000
            CERT_SYSTEM_STORE_CURRENT_USER = 0x00010000
            
            cert_path = os.path.join(tempfile.gettempdir(), "mitmproxy.cer")
            
            store = wcrypt.CertOpenStore(CERT_STORE_PROV_SYSTEM, 0, None, CERT_SYSTEM_STORE_CURRENT_USER, "Root")
            mitm_cert = None
            for cert in store.CertEnumCertificatesInStore():
                if "mitmproxy" in wcrypt.CertNameToStr(cert.Subject):
                    mitm_cert = {"Subject": wcrypt.CertNameToStr(cert.Subject), "Expiration": (cert.NotAfter).replace(tzinfo=None)}
                    print("Certificate found! Expiration:", mitm_cert["Expiration"].strftime("%Y-%m-%d %H:%M:%S"))
                    break
            if mitm_cert is None or mitm_cert["Expiration"] <= datetime.now():
                temp_proxy = subprocess.Popen(["mitmdump", "--listen-port", "8082"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(1)
                response = requests.get("http://mitm.it/cert/cer", proxies={"http": "http://127.0.0.1:8082"})
                if response.status_code == 200:
                    with open(cert_path , "wb") as f:
                        f.write(response.content)
                    while os.system('certutil -user -addstore Root "' + cert_path + '"') != 0:
                        pass
                temp_proxy.terminate()
        except Exception as e:
            print("Error generating/adding certificate:", e)
    else:
        cert_path = "/etc/ca-certificates/extracted/cadir/mitmproxy.pem"
        result = subprocess.run(["openssl", "x509", "-noout", "-subject", "-dates", "-in", cert_path], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            expiration_line = [line for line in output.splitlines() if "notAfter=" in line]
            if expiration_line:
                expiration_str = expiration_line[0].split("=")[-1]
                expiration_date = datetime.strptime(expiration_str, "%b %d %H:%M:%S %Y GMT")
                print("Certificate found! Expiration:", expiration_date)
        else:
            temp_proxy = subprocess.Popen(["mitmdump"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
            subprocess.run(["sudo", "trust", "anchor", os.path.expanduser("~/.mitmproxy/mitmproxy-ca-cert.cer")], check=True)
            temp_proxy.terminate()