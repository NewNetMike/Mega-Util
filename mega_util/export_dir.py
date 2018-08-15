import subprocess
import os
import xml.etree.ElementTree as ET
import re


def export_dir(email, password, directory, megacmd=None):
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

    cmd("mega-logout")
    cmd("mega-login " + u + " " + p)
    cmd("mega-cd " + d)
    ls = cmd("mega-ls")
    files_list = [y for y in (x.strip() for x in ls.splitlines()) if y]
    print(files_list)
    print(len(files_list))

    share_links = []
    for f in files_list:
        res = cmd('mega-export -a -f "' + f + '"')
        share_links.append(re.search("(?P<url>https?://[^\s]+)", res).group("url"))

    with open("links.txt", "w") as f:
        for s in share_links:
            f.write("%s" % s)
            if s is not share_links[-1]: f.write("\n")


if __name__ == '__main__':
    u = p = d = m = None
    with open("config.xml") as f:
        e = ET.fromstringlist(["<root>", f.read(), "</root>"])
        m = e.find("megacmd").get("loc")
        u = e.find("mega").get("u")
        p = e.find("mega").get("p")
        d = e.find("mega").get("d")

    export_dir(u, p, d, m)