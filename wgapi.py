import os
import sys
import glob
import subprocess
import random
import datetime
import qrcode
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI()

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "WD0Wmsne87XqWsQI4nakuX4sjDc8j1":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return True

g_main_config_src = '.main.config'
g_main_config_fn = None
g_main_config_type = None
g_defclient_config_fn = "_defclient.config"

g_defserver_config = """
[Interface]
#_GenKeyTime = <SERVER_KEY_TIME>
PrivateKey = <SERVER_PRIVATE_KEY>
#_PublicKey = <SERVER_PUBLIC_KEY>
Address = <SERVER_ADDR>
ListenPort = <SERVER_PORT>
Jc = <JC>
Jmin = <JMIN>
Jmax = <JMAX>
S1 = <S1>
S2 = <S2>
H1 = <H1>
H2 = <H2>
H3 = <H3>
H4 = <H4>

PostUp = iptables -A INPUT -p udp --dport <SERVER_PORT> -m conntrack --ctstate NEW -j ACCEPT --wait 10 --wait-interval 50; iptables -A FORWARD -i <SERVER_IFACE> -o <SERVER_TUN> -j ACCEPT --wait 10 --wait-interval 50; iptables -A FORWARD -i <SERVER_TUN> -j ACCEPT --wait 10 --wait-interval 50; iptables -t nat -A POSTROUTING -o <SERVER_IFACE> -j MASQUERADE --wait 10 --wait-interval 50; ip6tables -A FORWARD -i <SERVER_TUN> -j ACCEPT --wait 10 --wait-interval 50; ip6tables -t nat -A POSTROUTING -o <SERVER_IFACE> -j MASQUERADE --wait 10 --wait-interval 50

PostDown = iptables -D INPUT -p udp --dport <SERVER_PORT> -m conntrack --ctstate NEW -j ACCEPT --wait 10 --wait-interval 50; iptables -D FORWARD -i <SERVER_IFACE> -o <SERVER_TUN> -j ACCEPT --wait 10 --wait-interval 50; iptables -D FORWARD -i <SERVER_TUN> -j ACCEPT --wait 10 --wait-interval 50; iptables -t nat -D POSTROUTING -o <SERVER_IFACE> -j MASQUERADE --wait 10 --wait-interval 50; ip6tables -D FORWARD -i <SERVER_TUN> -j ACCEPT --wait 10 --wait-interval 50; ip6tables -t nat -D POSTROUTING -o <SERVER_IFACE> -j MASQUERADE --wait 10 --wait-interval 50
"""

g_defclient_config = """
[Interface]
PrivateKey = <CLIENT_PRIVATE_KEY>
#_PublicKey = <CLIENT_PUBLIC_KEY>
Address = <CLIENT_TUNNEL_IP>
DNS = 8.8.8.8
Jc = <JC>
Jmin = <JMIN>
Jmax = <JMAX>
S1 = <S1>
S2 = <S2>
H1 = <H1>
H2 = <H2>
H3 = <H3>
H4 = <H4>

[Peer]
AllowedIPs = 0.0.0.0/5, 8.0.0.0/7, 11.0.0.0/8, 12.0.0.0/6, 16.0.0.0/4, 32.0.0.0/3, 64.0.0.0/2, 128.0.0.0/3, 160.0.0.0/5, 168.0.0.0/6, 172.0.0.0/12, 172.32.0.0/11, 172.64.0.0/10, 172.128.0.0/9, 173.0.0.0/8, 174.0.0.0/7, 176.0.0.0/4, 192.0.0.0/9, 192.128.0.0/11, 192.160.0.0/13, 192.169.0.0/16, 192.170.0.0/15, 192.172.0.0/14, 192.176.0.0/12, 192.192.0.0/10, 193.0.0.0/8, 194.0.0.0/7, 196.0.0.0/6, 200.0.0.0/5, 208.0.0.0/4, 8.8.8.8/32
Endpoint = <SERVER_ADDR>:<SERVER_PORT>
PersistentKeepalive = 60
PublicKey = <SERVER_PUBLIC_KEY>
"""

class IPAddr():
    def __init__(self, ipaddr=None):
        self.ip = [0, 0, 0, 0]
        self.mask = None
        if ipaddr:
            self.init(ipaddr)
    def init(self, ipaddr):
        _ipaddr = ipaddr
        if not ipaddr:
            raise RuntimeError(f'ERROR: Incorrect IP-Addr: "{_ipaddr}"')
        if ' ' in ipaddr:
            raise RuntimeError(f'ERROR: Incorrect IP-Addr: "{_ipaddr}"')
        if ',' in ipaddr:
            raise RuntimeError(f'ERROR: Incorrect IP-Addr: "{_ipaddr}"')
        self.ip = [0, 0, 0, 0]
        self.mask = None
        if '/' in ipaddr:
            self.mask = int(ipaddr.split('/')[1])
            ipaddr = ipaddr.split('/')[0]
        nlist = ipaddr.split('.')
        if len(nlist) != 4:
            raise RuntimeError(f'ERROR: Incorrect IP-addr: "{_ipaddr}"')
        for n, num in enumerate(nlist):
            self.ip[n] = int(num)
    def __str__(self):
        out = f'{self.ip[0]}.{self.ip[1]}.{self.ip[2]}.{self.ip[3]}'
        if self.mask:
            out += '/' + str(self.mask)
        return out

class WGConfig():
    def __init__(self, filename=None):
        self.lines = []
        self.iface = {}
        self.peer = {}
        self.idsline = {}
        self.cfg_fn = None
        if filename:
            self.load(filename)
    def load(self, filename):
        self.cfg_fn = None
        self.lines = []
        self.iface = {}
        self.peer = {}
        self.idsline = {}
        with open(filename, 'r') as file:
            lines = file.readlines()
        iface = None
        secdata = []
        secdata_item = None
        secline = []
        secline_item = None
        for n, line in enumerate(lines):
            line = line.rstrip()
            self.lines.append(line)
            if line.strip() == '':
                continue
            if line.startswith(' ') and not line.strip().startswith('#'):
                raise RuntimeError(f'ERROR_CFG: Incorrect line #{n} into config "{filename}"')
            if line.startswith('#') and not line.startswith('#_'):
                continue
            if line.startswith('[') and line.endswith(']'):
                section_name = line[1:-1]
                if not section_name:
                    raise RuntimeError(f'ERROR_CFG: Incorrect section name: "{section_name}" (#{n+1})')
                secdata_item = {"_section_name": section_name.lower()}
                secline_item = {"_section_name": n}
                if section_name.lower() == 'interface':
                    if iface:
                        raise RuntimeError(f'ERROR_CFG: Found second section Interface in line #{n+1}')
                    iface = secdata_item
                elif section_name.lower() == 'peer':
                    pass
                else:
                    raise RuntimeError(f'ERROR_CFG: Found incorrect section "{section_name}" in line #{n+1}')
                secdata.append(secdata_item)
                secline.append(secline_item)
                continue
            if line.startswith('#_') and ' = ' in line:
                line = line[2:]
            if line.startswith('#'):
                continue
            if ' = ' not in line:
                raise RuntimeError(f'ERROR_CFG: Incorrect line into config: "{line}"  (#{n+1})')
            xv = line.find(' = ')
            if xv <= 0:
                raise RuntimeError(f'ERROR_CFG: Incorrect line into config: "{line}"  (#{n+1})')
            vname = line[:xv].strip()
            value = line[xv+3:].strip()
            if not secdata_item:
                raise RuntimeError(f'ERROR_CFG: Parameter "{vname}" have unknown section! (#{n+1})')
            section_name = secdata_item['_section_name']
            if vname in secdata_item:
                raise RuntimeError(f'ERROR_CFG: Found duplicate of param "{vname}" into section "{section_name}" (#{n+1})')
            secdata_item[vname] = value
            secline_item[vname] = n
        if not iface:
            raise RuntimeError(f'ERROR_CFG: Cannot found section Interface!')
        for i, item in enumerate(secdata):
            line = secline[i]
            peer_name = ""
            if item['_section_name'] == 'interface':
                self.iface = item
                peer_name = "__this_server__"
                if 'PublicKey' not in item:
                    raise RuntimeError(f'ERROR_CFG: Cannot found PublicKey in Interface')
                if 'PrivateKey' not in item:
                    raise RuntimeError(f'ERROR_CFG: Cannot found PrivateKey in Interface')
            else:
                if 'Name' in item:
                    peer_name = item['Name']
                    if not peer_name:
                        raise RuntimeError(f'ERROR_CFG: Invalid peer Name in line #{line["Name"]}')
                elif 'PublicKey' in item:
                    peer_name = item['PublicKey']
                    if not peer_name:
                        raise RuntimeError(f'ERROR_CFG: Invalid peer PublicKey in line #{line["PublicKey"]}')
                else:
                    raise RuntimeError(f'ERROR_CFG: Invalid peer data in line #{line["_section_name"]}')
                if 'AllowedIPs' not in item:
                    raise RuntimeError(f'ERROR_CFG: Cannot found "AllowedIPs" into peer "{peer_name}"')
                if peer_name in self.peer:
                    raise RuntimeError(f'ERROR_CFG: Found duplicate peer with name "{peer_name}"')
                self.peer[peer_name] = item
            if peer_name in self.idsline:
                raise RuntimeError(f'ERROR_CFG: Found duplicate peer with name "{peer_name}"')
            min_line = line['_section_name']
            max_line = min_line
            self.idsline[f'{peer_name}'] = min_line
            for vname in item:
                self.idsline[f'{peer_name}|{vname}'] = line[vname]
                if line[vname] > max_line:
                    max_line = line[vname]
            item['_lines_range'] = (min_line, max_line)
        self.cfg_fn = filename
        return len(self.peer)
    def save(self, filename=None):
        if not filename:
            filename = self.cfg_fn
        if not self.lines:
            raise RuntimeError(f'ERROR: no data')
        with open(filename, 'w', newline='\n') as file:
            for line in self.lines:
                file.write(line + '\n')
    def del_client(self, c_name):
        if c_name not in self.peer:
            raise RuntimeError(f'ERROR: Not found client "{c_name}" in peer list!')
        client = self.peer[c_name]
        ipaddr = client['AllowedIPs']
        min_line, max_line = client['_lines_range']
        del self.lines[min_line:max_line+1]
        del self.peer[c_name]
        secsize = max_line - min_line + 1
        del_list = []
        for k, v in self.idsline.items():
            if min_line <= v <= max_line:
                del_list.append(k)
            elif v > max_line:
                self.idsline[k] = v - secsize
        for k in del_list:
            del self.idsline[k]
        return ipaddr
    def set_param(self, c_name, param_name, param_value, force=False, offset=0):
        if c_name not in self.peer:
            raise RuntimeError(f'ERROR: Not found client "{c_name}" in peer list!')
        line_prefix = ""
        if param_name.startswith('_'):
            line_prefix = "#_"
            param_name = param_name[1:]
        client = self.peer[c_name]
        min_line, max_line = client['_lines_range']
        if param_name in client:
            nline = self.idsline[f'{c_name}|{param_name}']
            line = self.lines[nline]
            if line.startswith('#_'):
                line_prefix = "#_"
            self.lines[nline] = f'{line_prefix}{param_name} = {param_value}'
            return
        if not force:
            raise RuntimeError(f'ERROR: Param "{param_name}" not found for client "{c_name}"')
        new_line = f'{line_prefix}{param_name} = {param_value}'
        client[param_name] = param_value
        secsize = max_line - min_line + 1
        if offset >= secsize:
            raise RuntimeError(f'ERROR: Incorrect offset value = {offset} (secsize = {secsize})')
        pos = max_line + 1 if offset <= 0 else min_line + offset
        for k, v in self.idsline.items():
            if v >= pos:
                self.idsline[k] = v + 1
        self.idsline[f'{c_name}|{param_name}'] = pos
        self.lines.insert(pos, new_line)

def exec_cmd(cmd, input=None, shell=True, check=True, timeout=None):
    proc = subprocess.run(cmd, input=input, shell=shell, check=check,
                          timeout=timeout, encoding='utf8',
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rc = proc.returncode
    out = proc.stdout
    return rc, out

def get_main_iface():
    rc, out = exec_cmd('ip link show')
    if rc:
        raise RuntimeError(f'ERROR: Cannot get net interfaces')
    for line in out.split('\n'):
        if '<BROADCAST' in line and 'state UP' in line:
            xv = line.split(':')
            return xv[1].strip()
    return None

def get_ext_ipaddr():
    rc, out = exec_cmd('curl -4 -s icanhazip.com')
    if rc:
        raise RuntimeError(f'ERROR: Cannot get ext IP-Addr')
    lines = out.split('\n')
    ipaddr = lines[-1] if lines[-1] else lines[-2]
    ipaddr = IPAddr(ipaddr)
    return str(ipaddr)

def gen_pair_keys(cfg_type=None):
    global g_main_config_type
    if sys.platform == 'win32':
        return 'client_priv_key', 'client_pub_key'
    if not cfg_type:
        cfg_type = g_main_config_type
    if not cfg_type:
        raise
    wgtool = cfg_type.lower()
    rc, out = exec_cmd(f'{wgtool} genkey')
    if rc:
        raise RuntimeError(f'ERROR: Cannot generate private key')
    priv_key = out.strip()
    if not priv_key:
        raise RuntimeError(f'ERROR: Cannot generate private Key')
    rc, out = exec_cmd(f'{wgtool} pubkey', input=priv_key + '\n')
    if rc:
        raise RuntimeError(f'ERROR: Cannot generate public key')
    pub_key = out.strip()
    if not pub_key:
        raise RuntimeError(f'ERROR: Cannot generate public Key')
    return priv_key, pub_key

def get_main_config_path(check=True):
    global g_main_config_fn
    global g_main_config_type
    if not os.path.exists(g_main_config_src):
        raise RuntimeError(f'ERROR: file "{g_main_config_src}" not found!')
    with open(g_main_config_src, 'r') as file:
        lines = file.readlines()
    g_main_config_fn = lines[0].strip()
    cfg_exists = os.path.exists(g_main_config_fn)
    g_main_config_type = 'WG'
    if os.path.basename(g_main_config_fn).startswith('a'):
        g_main_config_type = 'AWG'
    if check:
        if not cfg_exists:
            raise RuntimeError(f'ERROR: Main {g_main_config_type} config file "{g_main_config_fn}" not found!')
    return g_main_config_fn

class MakeCfgParams(BaseModel):
    makecfg: str
    port: int
    ipaddr: str
    tun: str = ''

class CreateParams(BaseModel):
    tmpcfg: str
    ipaddr: str = ''

class AddClientParams(BaseModel):
    addcl: str
    ipaddr: str = ''

class UpdateClientParams(BaseModel):
    update: str

class DeleteClientParams(BaseModel):
    delete: str

class ConfGenParams(BaseModel):
    tmpcfg: str = g_defclient_config_fn

@app.post("/makecfg")
def make_cfg(params: MakeCfgParams, _: bool = Depends(verify_token)):
    try:
        if os.path.exists(params.makecfg):
            raise HTTPException(status_code=400, detail=f'ERROR: file "{params.makecfg}" already exists!')
        m_cfg_type = 'WG'
        if os.path.basename(params.makecfg).startswith('a'):
            m_cfg_type = 'AWG'
        main_iface = get_main_iface()
        if not main_iface:
            raise HTTPException(status_code=400, detail='ERROR: Cannot get main network interface!')
        if params.port <= 1000 or params.port > 65530:
            raise HTTPException(status_code=400, detail=f'ERROR: Incorrect argument port = {params.port}')
        if not params.ipaddr:
            raise HTTPException(status_code=400, detail=f'ERROR: Incorrect argument ipaddr = "{params.ipaddr}"')
        ipaddr = IPAddr(params.ipaddr)
        if not ipaddr.mask:
            raise HTTPException(status_code=400, detail=f'ERROR: Incorrect argument ipaddr = "{params.ipaddr}"')
        tun_name = params.tun if params.tun else os.path.splitext(os.path.basename(params.makecfg))[0].strip()
        priv_key, pub_key = gen_pair_keys(m_cfg_type)
        random.seed()
        jc = random.randint(3, 127)
        jmin = random.randint(3, 700)
        jmax = random.randint(jmin+1, 1270)
        out = g_defserver_config
        out = out.replace('<SERVER_KEY_TIME>', datetime.datetime.now().isoformat())
        out = out.replace('<SERVER_PRIVATE_KEY>', priv_key)
        out = out.replace('<SERVER_PUBLIC_KEY>', pub_key)
        out = out.replace('<SERVER_ADDR>', str(ipaddr))
        out = out.replace('<SERVER_PORT>', str(params.port))
        if m_cfg_type == 'AWG':
            out = out.replace('<JC>', str(jc))
            out = out.replace('<JMIN>', str(jmin))
            out = out.replace('<JMAX>', str(jmax))
            out = out.replace('<S1>', str(random.randint(3, 127)))
            out = out.replace('<S2>', str(random.randint(3, 127)))
            out = out.replace('<H1>', str(random.randint(0x10000011, 0x7FFFFF00)))
            out = out.replace('<H2>', str(random.randint(0x10000011, 0x7FFFFF00)))
            out = out.replace('<H3>', str(random.randint(0x10000011, 0x7FFFFF00)))
            out = out.replace('<H4>', str(random.randint(0x10000011, 0x7FFFFF00)))
        else:
            out = out.replace('\nJc = <', '\n# ')
            out = out.replace('\nJmin = <', '\n# ')
            out = out.replace('\nJmax = <', '\n# ')
            out = out.replace('\nS1 = <', '\n# ')
            out = out.replace('\nS2 = <', '\n# ')
            out = out.replace('\nH1 = <', '\n# ')
            out = out.replace('\nH2 = <', '\n# ')
            out = out.replace('\nH3 = <', '\n# ')
            out = out.replace('\nH4 = <', '\n# ')
        out = out.replace('<SERVER_IFACE>', main_iface)
        out = out.replace('<SERVER_TUN>', tun_name)
        with open(params.makecfg, 'w', newline='\n') as file:
            file.write(out)
        with open(g_main_config_src, 'w', newline='\n') as file:
            file.write(params.makecfg)
        return {"message": f'{m_cfg_type} server config file "{params.makecfg}" created!'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create")
def create_cfg(params: CreateParams, _: bool = Depends(verify_token)):
    try:
        get_main_config_path(True)
        if os.path.exists(params.tmpcfg):
            raise HTTPException(status_code=400, detail=f'ERROR: file "{params.tmpcfg}" already exists!')
        if params.ipaddr:
            ipaddr = IPAddr(params.ipaddr)
            if ipaddr.mask:
                raise HTTPException(status_code=400, detail=f'ERROR: Incorrect argument ipaddr = "{params.ipaddr}"')
        else:
            ext_ipaddr = get_ext_ipaddr()
            ipaddr = IPAddr(ext_ipaddr)
        out = g_defclient_config
        out = out.replace('<SERVER_ADDR>', str(ipaddr))
        if g_main_config_type != 'AWG':
            out = out.replace('\nJc = <', '\n# ')
            out = out.replace('\nJmin = <', '\n# ')
            out = out.replace('\nJmax = <', '\n# ')
            out = out.replace('\nS1 = <', '\n# ')
            out = out.replace('\nS2 = <', '\n# ')
            out = out.replace('\nH1 = <', '\n# ')
            out = out.replace('\nH2 = <', '\n# ')
            out = out.replace('\nH3 = <', '\n# ')
            out = out.replace('\nH4 = <', '\n# ')
        with open(params.tmpcfg, 'w', newline='\n') as file:
            file.write(out)
        return {"message": f'Template client config file "{params.tmpcfg}" created!'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/addclient")
def add_client(params: AddClientParams, _: bool = Depends(verify_token)):
    try:
        get_main_config_path(True)
        cfg = WGConfig(g_main_config_fn)
        c_name = params.addcl
        for peer_name, peer in cfg.peer.items():
            if peer_name.lower() == c_name.lower():
                raise HTTPException(status_code=400, detail=f'ERROR: peer with name "{c_name}" already exists!')
            if params.ipaddr:
                addr_check = IPAddr(params.ipaddr)
                addr_check.mask = None
                addr_str = str(addr_check)
                p_addr = IPAddr(peer['AllowedIPs'])
                p_addr.mask = None
                p_addr_str = str(p_addr)
                if addr_str == p_addr_str:
                    raise HTTPException(status_code=400, detail=f'ERROR: IP-addr "{params.ipaddr}" already used!')
        priv_key, pub_key = gen_pair_keys()
        srv = cfg.iface
        max_addr = None
        for peer_name, peer in cfg.peer.items():
            addr = IPAddr(peer['AllowedIPs'])
            if not max_addr or addr.ip[3] > max_addr.ip[3]:
                max_addr = addr
        if params.ipaddr:
            ipaddr = params.ipaddr
        else:
            if max_addr is None:
                max_addr = IPAddr(srv['Address'])
                max_addr.ip[3] += 1
                max_addr.mask = 32
                ipaddr = str(max_addr)
            else:
                max_addr.ip[3] += 1
                ipaddr = str(max_addr)
            if max_addr.ip[3] >= 254:
                raise HTTPException(status_code=400, detail='ERROR: There are no more free IP-addresses')
        with open(g_main_config_fn, 'rb') as file:
            srvcfg = file.read().decode('utf8')
        srvcfg += f'\n[Peer]\n'
        srvcfg += f'#_Name = {c_name}\n'
        srvcfg += f'#_GenKeyTime = {datetime.datetime.now().isoformat()}\n'
        srvcfg += f'#_PrivateKey = {priv_key}\n'
        srvcfg += f'PublicKey = {pub_key}\n'
        srvcfg += f'AllowedIPs = {ipaddr}\n'
        with open(g_main_config_fn, 'w', newline='\n') as file:
            file.write(srvcfg)
        return {"message": f'New client "{c_name}" added! IP-Addr: "{ipaddr}"'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/updateclient")
def update_client(params: UpdateClientParams, _: bool = Depends(verify_token)):
    try:
        get_main_config_path(True)
        cfg = WGConfig(g_main_config_fn)
        p_name = params.update
        priv_key, pub_key = gen_pair_keys()
        cfg.set_param(p_name, '_PrivateKey', priv_key, force=True, offset=2)
        cfg.set_param(p_name, 'PublicKey', pub_key)
        gentime = datetime.datetime.now().isoformat()
        cfg.set_param(p_name, '_GenKeyTime', gentime, force=True, offset=2)
        ipaddr = cfg.peer[p_name]['AllowedIPs']
        cfg.save()
        return {"message": f'Keys for client "{p_name}" updated! IP-Addr: "{ipaddr}"'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/deleteclient")
def delete_client(params: DeleteClientParams, _: bool = Depends(verify_token)):
    try:
        get_main_config_path(True)
        cfg = WGConfig(g_main_config_fn)
        p_name = params.delete
        ipaddr = cfg.del_client(p_name)
        cfg.save()
        return {"message": f'Client "{p_name}" deleted! IP-Addr: "{ipaddr}"'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/confgen")
def confgen(params: ConfGenParams, _: bool = Depends(verify_token)):
    try:
        get_main_config_path(True)
        cfg = WGConfig(g_main_config_fn)
        srv = cfg.iface
        if not os.path.exists(params.tmpcfg):
            raise HTTPException(status_code=400, detail=f'ERROR: file "{params.tmpcfg}" not found!')
        with open(params.tmpcfg, 'r') as file:
            tmpcfg = file.read()
        flst = glob.glob("*.conf")
        for fn in flst:
            if fn.endswith('awg0.conf'):
                continue
            if os.path.exists(fn):
                os.remove(fn)
        flst = glob.glob("*.png")
        for fn in flst:
            if os.path.exists(fn):
                os.remove(fn)
        random.seed()
        for peer_name, peer in cfg.peer.items():
            if 'Name' not in peer or 'PrivateKey' not in peer:
                continue
            jc = random.randint(3, 127)
            jmin = random.randint(3, 700)
            jmax = random.randint(jmin+1, 1270)
            out = tmpcfg[:]
            out = out.replace('<CLIENT_PRIVATE_KEY>', peer['PrivateKey'])
            out = out.replace('<CLIENT_PUBLIC_KEY>', peer['PublicKey'])
            out = out.replace('<CLIENT_TUNNEL_IP>', peer['AllowedIPs'])
            out = out.replace('<JC>', str(jc))
            out = out.replace('<JMIN>', str(jmin))
            out = out.replace('<JMAX>', str(jmax))
            out = out.replace('<S1>', srv.get('S1', ''))
            out = out.replace('<S2>', srv.get('S2', ''))
            out = out.replace('<H1>', srv.get('H1', ''))
            out = out.replace('<H2>', srv.get('H2', ''))
            out = out.replace('<H3>', srv.get('H3', ''))
            out = out.replace('<H4>', srv.get('H4', ''))
            out = out.replace('<SERVER_PORT>', srv['ListenPort'])
            out = out.replace('<SERVER_PUBLIC_KEY>', srv['PublicKey'])
            fn = f'{peer_name}.conf'
            with open(fn, 'w', newline='\n') as f:
                f.write(out)
        return {"message": "Client configs generated!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/qrcode")
def generate_qrcode(_: bool = Depends(verify_token)):
    try:
        flst = glob.glob("*.png")
        for fn in flst:
            if os.path.exists(fn):
                os.remove(fn)
        flst = glob.glob("*.conf")
        if not flst:
            raise HTTPException(status_code=400, detail='ERROR: client configs not founded!')
        for fn in flst:
            if fn.endswith('awg0.conf'):
                continue
            with open(fn, 'rb') as file:
                conf = file.read().decode('utf8')
            name = os.path.splitext(fn)[0]
            img = qrcode.make(conf)
            img.save(f'{name}.png')
        return {"message": "QR codes generated!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
