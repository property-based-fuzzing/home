import time
import subprocess
class Executor(object):

    def __init__(self,device,app):
        
        self.app = app
        self.device = device
        
    def execute_event(self,device,event,num):
        try:
            print("------------------")
            if event.action == "click":
                print("click"+event.view.line+"\n")
                device.click(event.view)
            elif event.action == "longclick":
                print("longclick"+event.view.line+"\n")
                device.longclick(event.view)
            elif event.action == "edit":
                print("edit"+event.view.line+"\n")
                device.edit(event.view,event.text)
            elif event.action == "drag":
                print("drag"+event.text+"\n")
                device.drag(event.text)
            elif event.action == "back":
                print("back"+"\n")
                device.use.press("back")
            elif event.action == "home":
                device.use.press("home")
                print("home"+"\n") 
            elif event.action == "naturalscreen":
                print("naturalscreen"+"\n")
                device.use.set_orientation("n")
            elif event.action == "leftscreen":
                print("leftscreen"+"\n")
                device.use.set_orientation("l")
            elif event.action == "start":
                if event.data=="":
                    print("start"+"\n")
                    device.stop_app(self.app)
                    device.start_app(self.app)
                else:
                    subprocess.run(["adb","-s",device.device_serial,"shell","am","start","-n",event.data], stdout=subprocess.PIPE)
            elif event.action == "stop":
                print("stop")
                device.stop_app(self.app)
            elif event.action == "clear":
                print("clear")
                device.clear_app(self.app)
            elif event.action == "sleep":
                print("sleep")
                time.sleep(int(event.text))
            elif event.action == "scrollto":
                print("scrollto")
                device.scrollto(event.text)
            elif "scroll" in event.action:
                device.scroll(event.view,event.action)
            
            print(device.device_serial+":end execute\n")
            return True
        except Exception as ex:
            if num ==0:
                print(ex)
                return self.execute_event(device,event,1)
            else:
                print(ex)
                return False
   