import os
import subprocess
import uiautomator2 as u2

class Device(object):

    def __init__(self, device_serial):
        self.device_serial=device_serial
        self.now_logcat = []
        self.screen = None
        self.last_screen = None
    
    def connect(self):
        self.use = u2.connect_usb(self.device_serial)
        self.use.implicitly_wait(5.0)
    
    def click(self,view):
        try:
            if view.text !="" and view.text !="#any#" and view.resourceId !="" and view.resourceId !="#any#":
                self.use(resourceId=view.resourceId,text=view.text).click()
            elif view.text !="" and view.text !="#any#":
                self.use(text=view.text).click()
            elif view.description !="" and view.description !="#any#":
                self.use(description=view.description).click()
            elif view.resourceId !="" and view.resourceId !="#any#" and view.className!="" and view.className!="#any#":
                self.use(className=view.className,resourceId=view.resourceId).click()
            elif view.resourceId !="" and view.resourceId !="#any#" and view.index!="" and view.index!="#any#":
                self.use(resourceId=view.resourceId,instance=view.index).click()
            elif view.resourceId !="" and view.resourceId !="#any#":
                self.use(resourceId=view.resourceId).click()
            elif view.xpath !="" and view.xpath !="#any#":
                self.use.xpath(view.xpath).click()
            elif view.x!=-1 and view.y!=-1:
                self.use.click(view.x ,view.y)
            elif view.className!="" and view.className!="#any#" and view.checked!="#any#":
                self.use(password=view.password,visibleToUser=view.visibleToUser,scrollable=view.scrollable,longClickable=view.longClickable,focusable=view.focusable,focused=view.focused,checkable=view.checkable,clickable=view.clickable,checked=view.checked,enabled=view.enabled,className=view.className,packageName=view.package).click()
            else:
                self.use(className=view.className,packageName=view.package).click()
        except:
            self.use.click(view.x ,view.y)

    def stop_app(self,app):
        self.use.app_stop(app.package_name)

    def clear_app(self,app):
        self.use.app_clear(app.package_name)
        self.use.app_stop(app.package_name)
        if app.package_name == "com.ichi2.anki":
            self.use.shell(["su"])
            self.use.shell(["rm","-r","/storage/emulated/0/AnkiDroid"])
        
    def get_current_app(self):
        self.current_app=self.use.app_current()['package']
        return self.current_app
    
    def start_app(self,app):
        self.use.app_start(app.package_name)
        print("adb"+"-s"+self.device_serial+"shell"+"am"+"start"+"-n"+app.package_name+"/"+app.main_activity)
        subprocess.run(["adb","-s",self.device_serial,"shell","am","start","-n",app.package_name+"/"+app.main_activity], stdout=subprocess.PIPE)
        return True

    def longclick(self,view):
        try:
            if view.text !="" and view.text !="#any#":
                self.use(text=view.text).long_click()
            elif view.description !="" and view.description !="#any#":
                self.use(description=view.description).long_click()
            elif view.resourceId !="" and view.resourceId !="#any#" and view.className!="" and view.className!="#any#":
                self.use(className=view.className,resourceId=view.resourceId).long_click()
            elif view.resourceId !="" and view.resourceId !="#any#" and view.index!="" and view.index!="#any#":
                self.use(resourceId=view.resourceId,instance=view.index).long_click()
            elif view.resourceId !="" and view.resourceId !="#any#":
                self.use(resourceId=view.resourceId).long_click()
            elif view.x!=-1 and view.y!=-1:
                self.use.long_click(view.x ,view.y)
            elif view.checkable!="" and view.checked!="#any#":
                self.use(password=view.password,visibleToUser=view.visibleToUser,scrollable=view.scrollable,longClickable=view.longClickable,focusable=view.focusable,focused=view.focused,checkable=view.checkable,checked=view.checked,clickable=view.clickable,enabled=view.enabled,className=view.className,packageName=view.package).long_click()
            else:
                self.use(className=view.className,packageName=view.package).long_click()
        except:
            self.use.long_click(view.x ,view.y)
    
    def scrollto(self,text):
        nowscreen =self.use.dump_hierarchy()
        lastscreen=""
        while not self.use.exists(text=text) and lastscreen != nowscreen:
            lastscreen =nowscreen
            nowscreen =self.use.dump_hierarchy()
            self.use(scrollable=True).scroll.vert.forward()

    def edit(self,view,text):
        try:
            if view.text !="" and view.text !="#any#":
                self.use(text=view.text).set_text(text)
            elif view.description !="" and view.description !="#any#":
                self.use(description=view.description).set_text(text)
            elif view.resourceId !="" and view.resourceId !="#any#":
                self.use(resourceId=view.resourceId).set_text(text)
            elif view.xpath !="" and view.xpath !="#any#":
                self.use.xpath(view.xpath).set_text(text)
            elif view.className !="" and view.className !="#any#" and view.index!="" and view.index!="#any#":
                self.use(className=view.className,instance=view.index).set_text(text)
            else:
                self.use(className=view.className,packageName=view.package).set_text(text)
        except:
            self.use(className=view.className).set_text(text)
            # self.use.send_keys(text, clear=True)
    
    def update_logcat(self,logcat_lines):
        self.last_logcat = self.now_logcat
        self.now_logcat = logcat_lines
    
    def update_screen(self,screen):
        self.last_screen=self.screen
        self.screen=screen

    def drag(self,text):
        positions = text.split(",")
        self.use.drag(int(positions[0]),int(positions[1]),int(positions[2]),int(positions[3]))
    
    def scroll(self,view,action):
        try:
            if action == "scroll_backward":
                print("scroll backward"+"\n")
                if view.resourceId !="" and view.className!="":
                    self.use(className=view.className,resourceId=view.resourceId).scroll.vert.backward(steps=100)
                elif view.resourceId !="" :
                    self.use(resourceId=view.resourceId).scroll.vert.backward(steps=100)
                elif view.className !="" :
                    self.use(className=view.className).scroll.vert.backward(steps=100)
                else:
                    self.use(scrollable=True).scroll.vert.backward(steps=100)
            elif action == "scroll_forward":
                print("scroll forward"+"\n")
                if view.resourceId !="" and view.className!="":
                    self.use(className=view.className,resourceId=view.resourceId).scroll.vert.forward(steps=100)
                elif view.resourceId !="" :
                    self.use(resourceId=view.resourceId).scroll.vert.forward(steps=100)
                elif view.className !="" :
                    self.use(className=view.className).scroll.vert.forward(steps=100)
                else:
                    self.use(scrollable=True).scroll.vert.forward(steps=100)
            elif action == "scroll_right":
                print("scroll right"+"\n")
                if view.resourceId !="" and view.className!="":
                    self.use(className=view.className,resourceId=view.resourceId).scroll.horiz.toEnd(max_swipes=10)
                elif view.resourceId !="" :
                    self.use(resourceId=view.resourceId).scroll.horiz.toEnd(max_swipes=10)
                elif view.className !="" :
                    self.use(className=view.className).scroll.horiz.toEnd(max_swipes=10)
                else:
                    self.use(scrollable=True).scroll.horiz.toEnd(max_swipes=10)
            elif action == "scroll_left":
                print("scroll left"+"\n")
                if view.resourceId !="" and view.className!="":
                    self.use(className=view.className,resourceId=view.resourceId).scroll.horiz.toBeginning(max_swipes=10)
                elif view.resourceId !="" :
                    self.use(resourceId=view.resourceId).scroll.horiz.toBeginning(max_swipes=10)
                elif view.className !="" :
                    self.use(className=view.className).scroll.horiz.toBeginning(max_swipes=10)
                else:
                    self.use(scrollable=True).scroll.horiz.toBeginning(max_swipes=10)
            return True
        except Exception as ex:
            print(ex)
            return False
            
    def close_keyboard(self):
        # subprocess.run(["adb","-s",self.device_serial,"shell","input","keyevent","111"], stdout=subprocess.PIPE)
        if "emulator" in self.device_serial:
            self.use.shell(["input","keyevent","111"])
        else:
            self.use.press("back")

    def add_file(self,resource_path,resource,path):
        subprocess.run(["adb","-s",self.device_serial,"logcat","-c"], stdout=subprocess.PIPE)
        subprocess.run(["adb","-s",self.device_serial,"push",resource_path+"/"+resource,path], stdout=subprocess.PIPE)

    def log_crash(self,path):
        print("adb -s "+self.device_serial+" logcat -b crash >"+path)
        os.popen("adb -s "+self.device_serial+" logcat -b crash >"+path)

    def clear_log(self):
        print("adb -s "+self.device_serial+" logcat -c")
        self.use.shell(["logcat","-c"])

    def install_app(self,app):
        print(app)
        subprocess.run(["adb","-s",self.device_serial,"install",app], stdout=subprocess.PIPE)
    
        
    

