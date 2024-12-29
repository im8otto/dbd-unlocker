import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mitmproxy import http
from Rules import Market, Banner, Bloodweb, Headers, GetAll, Quest
from Utils import Misc


def response(flow: http.HTTPFlow) -> None:
    if Market.status and Market.url in flow.request.path:
        Market.response(flow)
    if Banner.status and Banner.url in flow.request.path:
        Banner.response(flow)
    if Quest.status and Quest.url_response in flow.request.path:
        Quest.response(flow)

async def request(flow: http.HTTPFlow) -> None:
    if Quest.status and Quest.url_request in flow.request.path:
        await Quest.request(flow)
    if GetAll.status and GetAll.url in flow.request.path:
        GetAll.request(flow)
    if Bloodweb.status and Bloodweb.url in flow.request.path:
        Bloodweb.request(flow)
    if Headers.status and Headers.url in flow.request.path:
        Headers.request(flow)

def set_proxy_settings():
    if Misc.current_system == "Windows":
        import winreg
        proxy_server = "127.0.0.1:8082"
        registry_key = r"Software\\Microsoft\Windows\\CurrentVersion\\Internet Settings"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy_server)
    else:
        from os import path
        proxy_server = "http://localhost:8082"
        proxy_config_file = path.expanduser("~/.config/kioslaverc")
        proxy_settings = f"""
[Proxy Settings]
ProxyType=1
httpProxy={proxy_server}
httpsProxy={proxy_server}
ftpProxy={proxy_server}
socksProxy={proxy_server}
NoProxyFor=localhost,127.0.0.1
Proxy Config Script=
ReversedException=false
ProxyUrlDisplayFlags=15
"""
        with open(proxy_config_file, "w") as config_file:
            config_file.write(proxy_settings) 
    Misc.print_log("Proxy successfully started")

def disable_proxy_settings():
    if Misc.current_system == "Windows":
        import winreg
        registry_key = r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
    else:
        from os import path
        proxy_config_file = path.expanduser("~/.config/kioslaverc")
        proxy_settings = f"""
[Proxy Settings]
ProxyType=0
httpProxy=
httpsProxy=
ftpProxy=
socksProxy=
NoProxyFor=
Proxy Config Script=
ReversedException=false
ProxyUrlDisplayFlags=15
"""
        with open(proxy_config_file, "w") as config_file:
            config_file.write(proxy_settings)
    Misc.print_log("Proxy settings disabled.")