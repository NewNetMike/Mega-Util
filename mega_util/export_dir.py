import subprocess
import os
import xml.etree.ElementTree as ET
import re
import time

def export_dir(email, password, directory, megacmd=None, save=None):
    def cmd(s):
        print("> " + s)
        proc = subprocess.Popen(s, shell=True, env=env, stdout=subprocess.PIPE)
        res = proc.communicate()[0].decode()
        print(">> " + res)
        return res

    path = os.getenv('PATH')
    if megacmd is not None:
        path += megacmd
    if "MEGAcmd" not in path:
        raise Exception("""MEGAcmd was not found.
        Make sure it's installed and your PATH is set correctly. (or pass megacmd='dir/of/MEGAcmd')""")
    env = {'PATH': path}

    u = email
    p = password
    d = directory

    os.system("mega-version")
    print("")

    cmd("mega-logout")
    cmd("mega-login " + u + " " + p)
    cmd("mega-cd " + d)
    ls = cmd("mega-ls")
    files_list = [y for y in (x.strip() for x in ls.splitlines()) if y]

    share_links = []
    for f in files_list:
        res = cmd('mega-export -a -f "' + f + '"')
        share_links.append(re.search("(?P<url>https?://[^\s]+)", res).group("url"))

    if save is not None:
        with open(save, "w") as f:
            for s in share_links:
                f.write("%s" % s)
                if s is not share_links[-1]: f.write("\n")

    cmd("mega-logout")
    cmd("mega-quit")
    time.sleep(10)
    return share_links


if __name__ == '__main__':
    u = p = d = m = None

    config_path = os.path.join(os.getcwd(), "mega_config.xml")

    if os.path.isfile(config_path):
        with open(config_path) as f:
            e = ET.fromstringlist(["<root>", f.read(), "</root>"])
            m = e.find("megacmd").get("loc")
            u = e.find("mega").get("u")
            p = e.find("mega").get("p")
            d = e.find("mega").get("d")
    else:
        u = input("Email: ").strip()
        p = input("Password: ").strip()
        d = input("Directory to export: ").strip()
        m = input("[OPTIONAL] Path of MEGAcmd: ").strip()
        if len(m) <= 0: m = None

    export_dir(u, p, d, m)