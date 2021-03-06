#!/usr/bin/env python3

import core.helper as h
import re, os
import time

class command:
    def __init__(self):
        self.name = "upload"
        self.description = "Upload local file."
        self.usage = "Usage: upload <local_file> <remote_path>"
    
    def run(self,session,cmd_data):
        if not cmd_data['args']:
            print(self.usage)
            return
        else:
            paths = re.split(r'(?<!\\) ', cmd_data['args'].rstrip())
            if len(paths) < 2:
                print("Usage: upload <local_path> <remote_path>")
                return
            
            if len(paths) > 2:
                print("Usage: upload <local_path> <remote_path>")
                return
            
            local_dir = os.path.split(paths[0])[0]
            local_file = os.path.split(paths[0])[1]
            
            remote_dir = os.path.split(paths[1])[0]
            remote_file = os.path.split(paths[1])[1]
                
            w = os.environ['OLDPWD']
            os.chdir(w)
                
            if os.path.exists(paths[0]):
                if os.path.isdir(paths[0]):
                    h.info_error("Error: "+paths[0]+": not a file!")
                    g = os.environ['HOME']
                    os.chdir(g + "/mouse")
                    return
                else:
                    pass
            else:
                h.info_error("Local file: "+paths[0]+": does not exist!")
                g = os.environ['HOME']
                os.chdir(g + "/mouse")
                return
            
            raw = paths[1]
            payload = """if [[ -d """+raw+""" ]]
            then
            echo 0
            fi"""
            dchk = session.send_command({"cmd":"","args":payload})
            chk = session.send_command({"cmd":"stat","args":raw})
            if dchk == "0\n":
                if chk[:4] != "stat":
                    h.info_general("Uploading "+local_file+"...")
                    session.upload_file(paths[0],raw,local_file)
                    if raw[-1] == "/":
                        h.info_general("Saving to "+raw+""+local_file+"...")
                        time.sleep(1)
                        h.info_success("Saved to "+raw+""+local_file+"!")
                    else:
                        h.info_general("Saving to "+raw+"/"+local_file+"...")
                        time.sleep(1)
                        h.info_success("Saved to "+raw+"/"+local_file+"!")
                else:
                    h.info_error("Remote directory: "+raw+": does not exist!")
            else:
                schk = session.send_command({"cmd":"stat","args":remote_dir})
                if schk[:4] != "stat":
                    h.info_general("Uploading "+local_file+"...")
                    session.upload_file(paths[0],remote_dir,remote_file)
                    h.info_general("Saving to "+raw+"...")
                    time.sleep(1)
                    h.info_success("Saved to "+raw+"!")
                else:
                    h.info_error("Remote directory: "+remote_dir+": does not exist!")
            g = os.environ['HOME']
            os.chdir(g + "/mouse")
