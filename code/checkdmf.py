from device import Device
from util import Util
from dmf import DMF
from view import View
from event import Event
import time,random

class CheckRecord(object):
    instance = None
    def __init__(self,root_path,device_serial,app,json_name):
        CheckRecord.instance = self
        self.root_path=root_path
        self.device = Device(device_serial)
        self.app =app
        self.json_name = json_name
        self.util = Util(self.app.app_path,json_name)
        self.dmf_list=self.util.get_dmf(self.root_path)
    
    def dump_layout(self,path):
        xml = self.device.use.dump_hierarchy()
        f = open(path+"/"+"layout.xml",'w',encoding='utf-8')
        f.write(xml)
        f = open(path+"/"+"layout.xml",'r',encoding='utf-8')
        lines=f.readlines()
        self.now_layout = lines

    def findviewinlayout(self,now_layout, widget):
        view=None
        now_instance=0
        for line in now_layout:
            if "<node" not in line:
                continue
            view = View(line,[])
            if widget.className!="" and widget.className != view.className:
                continue
            elif widget.description!="" and widget.description != view.description:
                continue
            elif widget.resourceId!="" and widget.resourceId != view.resourceId:
                continue
            elif widget.real_text!="" and widget.real_text != view.text:
                continue
            elif widget.instance!="" and now_instance<int(widget.instance):
                now_instance=now_instance+1
            else:
                # print("widget- className:"+widget.className+",description:"+widget.description+",resourceId:"+widget.resourceId+",text:"+widget.real_text+",name:"+widget.name+"\n")
                # print("view- className:"+view.className+",description:"+view.description+"resourceId:"+view.resourceId+"text:"+view.text+"\n")
                return view
        return None

    def random_text(self):
        text_style=random.randint(0,7)
        text_length=random.randint(1,5)
        nums=["0","1","2","3","4","5","6","7","8","9"]
        letters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        symbols=[",",".","!","?"]
        i=0
        random_string=""
        print("text_style:"+str(text_style))
        if text_style == 0:
            while i < text_length:
                now_num=nums[random.randint(0,len(nums)-1)]
                random_string=random_string+now_num
                i=i+1
        elif text_style == 1:
            while i < text_length:
                now_letters=letters[random.randint(0,len(nums)-1)]
                random_string=random_string+now_letters
                i=i+1
        elif text_style == 2:
            while i < text_length:
                s_style=random.randint(0,2)
                if s_style==0:
                    now_letters=nums[random.randint(0,len(nums)-1)]
                    random_string=random_string+now_letters
                elif s_style==1:
                    now_letters=letters[random.randint(0,len(letters)-1)]
                    random_string=random_string+now_letters
                elif s_style==2:
                    now_letters=symbols[random.randint(0,len(symbols)-1)]
                    random_string=random_string+now_letters
                i=i+1
        elif text_style == 3:
            country=["b","t"]
            countrynum=random.randint(0,1)
            random_string=country[countrynum]
        elif text_style ==4:
            random_string=letters[random.randint(0,len(letters)-1)]+letters[random.randint(0,len(letters)-1)]
        elif text_style ==5:
            random_string=nums[random.randint(0,len(nums)-1)]+nums[random.randint(0,len(nums)-1)]
        elif text_style ==6:
            special_text=["123","1"]
            specialnum=random.randint(0,len(special_text)-1)
            random_string=special_text[specialnum]
        elif text_style ==7:
            random_string="?10086"
        if random_string=="" or random_string.startswith("?") or random_string.startswith(".") or random_string.startswith("x") or random_string.startswith("X") or random_string.startswith("0") or len(random_string)<3:
            random_string=self.random_text()
        return random_string
    
    def changewidgettoline(self,widget):
        line="<node NAF=\"#any#\" index=\"index_string\" text=\"text_string\" resource-id=\"resourceId_string\" class=\"className_string\" package=\"#any#\" content-desc=\"description_string\" checkable=\"#any#\" checked=\"#any#\" clickable=\"#any#\" enabled=\"#any#\" focusable=\"#any#\" focused=\"#any#\" scrollable=\"#any#\" long-clickable=\"#any#\" password=\"#any#\" selected=\"#any#\" visible-to-user=\"#any#\" bounds=\"\" />"
        line= line.replace("text_string",widget.real_text).replace("resourceId_string",widget.resourceId).replace("className_string",widget.className).replace("description_string",widget.description).replace("index_string",widget.instance)
        return line

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
            elif event.action == "scrollto":
                print("scrollto")
                device.scrollto(event.text)
            elif event.action == "sleep":
                print("sleep")
                time.sleep(int(event.text))
            elif "scroll" in event.action:
                device.scroll(event.view,event.action)
            
            print(device.device_serial+":end execute\n")
            time.sleep(3)
            return True
        except Exception as ex:
            if num ==0:
                print(ex)
                return self.execute_event(device,event,1)
            else:
                print(ex)
                return False

    def start(self):
        print("start check")
        self.root_path=self.root_path+self.json_name+"/"

        self.device.connect()
        self.device.use.set_orientation("n")
        nowdmf = None

        while(True):

            type = input("Please enter the type of DMF:")
            datatype = input("Please enter the type of target data objects of DMF:")
            # if type=="search":
            #     object = input("Please enter one existing data object:")

            for dmf in self.dmf_list:
                if type+" "+datatype == dmf.name:
                    nowdmf = dmf
            
            if nowdmf==None:
                print("No matching DMF type")
                continue
            
            pre_check = True
            self.dump_layout(self.root_path)
            for pre in nowdmf.preconditions:
                if pre.datatype!="" and pre.datatype!=datatype:
                    print("No matching data type")
                    continue
                for widget in nowdmf.widgets:
                    if widget.name == pre.widget:
                        nowwidget = widget
                view=self.findviewinlayout(self.now_layout, nowwidget)
                if pre.relation == "in" and view==None:
                    print("Pre-check failed, "+nowwidget.name+" does not exist")
                    pre_check = False
                    break
                elif pre.relation == "not in" and view!=None:
                    print("Pre-check failed, "+nowwidget.name+" exists")
                    pre_check = False
                    break
                else:
                    print("Pre-check passed")
            if pre_check==False:
                continue
            
            now_layout = 0
            for event in nowdmf.events:
                for widget in nowdmf.widgets:
                    if widget.name == event.widget:
                        nowwidget = widget
                    elif "_name" in widget.name and now_layout==int(widget.UI_layout_num):
                        try:
                            widget.real_text = widget.text
                            view=self.findviewinlayout(self.now_layout, widget)
                            widget.real_text = view.text
                        except Exception as ex:
                            print("can not find widget:"+widget.name,", please check the attributes of this widget")
                            continue
                line = self.changewidgettoline(nowwidget)
                view=View(line,[])
                view.set_xpath(nowwidget.xpath)
                execute_event = Event(view, event.action, self.device, 0)
                if event.text == "random":
                    execute_event.set_text(self.random_text())
                elif "::" in event.text:
                    object = input("Please enter one existing data object:")
                    execute_event.set_text(object)
                else:
                    execute_event.set_text(event.text)
                executeresult=self.execute_event(self.device,execute_event,0)
                if executeresult==False and event.force == True:
                    print(event.action+" "+event.widget+" failed to execute")
                elif executeresult==False and event.force == False:
                    now_layout=now_layout+1
                    continue
                else:
                    #Waiting for loading
                    waittime = 0
                    while waittime<5 and (self.device.use(className="android.widget.ProgressBar").exists and self.app.package_name!="com.ss.android.lark" or (self.device.use(text="...").exists and self.app.package_name=="io.github.hidroh.materialistic")):
                        time.sleep(1)
                        waittime=waittime+1
                    now_layout=now_layout+1
                    self.dump_layout(self.root_path)
            
            for post in nowdmf.postconditions:
                if post.datatype!="" and post.datatype!=datatype:
                    print("No matching data type")
                    continue
                for widget in nowdmf.widgets:
                    if widget.name == post.widget:
                        nowwidget = widget
                if ".text" in nowwidget.text:
                    targetwidget = nowwidget.text.split(".")
                    for widget in nowdmf.widgets:
                        if widget.name == targetwidget[0]:
                            nowwidget.real_text=widget.real_text
                elif "::" in nowwidget.text:
                    object = input("Please enter one existing data object:")
                    nowwidget.real_text=object
                view=self.findviewinlayout(self.now_layout, nowwidget)
                if post.relation == "in" and view==None:
                    print("Post-check failed, "+nowwidget.name+":"+nowwidget.real_text+" does not exist")
                    continue
                elif post.relation == "not in" and view!=None:
                    print("Post-check failed, "+nowwidget.name+":"+nowwidget.real_text+" exists")
                    continue
                else:
                    print(nowwidget.real_text+"Post-check passed")
        
        
        

            
        
        

        