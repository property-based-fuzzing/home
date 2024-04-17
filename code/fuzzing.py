from locale import str
import uiautomator2 as u2
from device import Device
from app import App
from policy import RandomPolicy
from executor import Executor
from util import Util
import random
from screen import Screen
import os
import time
import shutil
from view import View
from event import Event

class Fuzzing(object):
    instance = None
    
    def __init__(self,
                device_serial,
                root_path,
                app_path,
                policy_name,
                testcase_count,
                event_num,
                json_name,
                app,
                start_time,
                max_time,
                start_testcase,
                result_path):
        Fuzzing.instance = self
        self.app_path = app_path
        self.policy_name = policy_name
        self.testcase_count = testcase_count
        self.event_num = event_num
        self.device_serial = device_serial
        self.app = app
        self.start_time = start_time
        self.root_path = root_path
        self.device = Device(device_serial)
        self.executor = Executor(self.device,self.app)
        self.policy =  self.get_policy()
        self.json_name = json_name
        self.util = Util(app_path,json_name)
        self.keywordlist = []
        self.items = []
        self.itemsdetail = []
        self.nowscreenshotpath = ""
        self.end_position = ''
        self.max_time =max_time
        self.endtimeflag = True
        self.start_testcase = start_testcase
        self.result_path = result_path
    
    def get_policy(self):
        if self.policy_name=="random":
            print("Policy: Random")
            policy = RandomPolicy(self.device,self.app,40,30,40,30,5,1)
        else:
            print("No valid input policy specified. Using policy \"none\".")
            policy = None
        return policy

    def save_screen(self,path,event_count):
        #Obtain and save screen of all devices
        self.device.use.screenshot(path+"/"+self.json_name+"screen/"+str(self.now_testcase)+"/"+str(event_count)+".png")
        self.nowscreenshotpath = path+"/"+self.json_name+"screen/"+str(self.now_testcase)+"/"+str(event_count)+".png"
        xml = self.device.use.dump_hierarchy()
        f = open(path+"/"+self.json_name+"screen/"+str(self.now_testcase)+"/"+str(event_count)+".xml",'w',encoding='utf-8')
        f.write(xml)
        f = open(path+"/"+self.json_name+"screen/"+str(self.now_testcase)+"/"+str(event_count)+".xml",'r',encoding='utf-8')
        lines=f.readlines()
        f.close()
        #Record crash
        f = open(path+"/"+self.json_name+"screen/"+self.device.device_serial+"_logcat.txt")
        logcat_lines=f.readlines()
        f.close()
        self.device.update_logcat(logcat_lines)
        if self.device.last_logcat!=self.device.now_logcat:
            for line in self.device.now_logcat:
                if line not in self.device.last_logcat:
                    self.f_event.write(line)
                    self.f_event.flush()
        
        screen = Screen(lines,[])
        self.device.update_screen(screen)
    
    def start(self):
        #Read the DMF list and the list of blocked controls
        self.dmf_list=self.util.get_dmf(self.root_path+"/dmf/")
        self.keyview_list=self.util.get_keyview(self.root_path)
        self.noresponse_list=[]

        #Connect device and initialize
        self.device.connect()
        if self.app.package_name!="com.ss.android.lark":
            self.device.install_app(self.app.app_path)
        self.device.use.set_orientation("n")
        
        #Generate output folder
        self.util.create_outputdir(self.result_path)
        self.now_testcase =self.start_testcase

        if not os.path.exists(self.result_path+"/"+self.json_name+"screen/"+"noresponse"):
            os.makedirs(self.result_path+"/"+self.json_name+"screen/noresponse")
        self.f_noresponse = open(self.result_path+"/"+self.json_name+"screen/noresponse/noresponse_record.txt",'w',encoding='utf-8')

        #Initialize crash log
        self.f_logcat = open(self.result_path+"/"+self.json_name+"screen/"+self.device.device_serial+"_logcat.txt",'w',encoding='utf-8')
        self.f_logcat.close()
        self.device.log_crash(self.result_path+"/"+self.json_name+"screen/"+self.device.device_serial+"_logcat.txt")
        self.f_logcat = open(self.result_path+"/"+self.json_name+"screen/"+self.device.device_serial+"_logcat.txt")
        logcat_lines=self.f_logcat.readlines()
        self.f_logcat.close()
        self.device.update_logcat(logcat_lines)

        while self.now_testcase<self.testcase_count:
            
            #At the beginning of each test case, clear the app information and restart the app
            if not os.path.exists(self.result_path+"/"+self.json_name+"screen/"+str(self.now_testcase)):
                os.makedirs(self.result_path+"/"+self.json_name+"screen/"+str(self.now_testcase))
            f_dmf = open(self.result_path+"/"+self.json_name+"screen/"+str(self.now_testcase)+"/dmf_record.txt",'w',encoding='utf-8')
            self.f_event = open(self.result_path+"/"+self.json_name+"screen/"+str(self.now_testcase)+"/event_record.txt",'w',encoding='utf-8')
            
            #Initialization of each round of test cases
            self.device.clear_app(self.app)
            self.device.start_app(self.app)
            self.now_event = 0
            self.save_screen(self.result_path,self.now_event)
            self.items = []
            self.itemsdetail = [] 
            
            while self.now_event<self.event_num:

                #Stop running if maximum running time is reached
                during_time=time.time() - self.start_time
                if during_time>self.max_time and self.endtimeflag==True:
                    self.f_event.write("Start Time:"+time.asctime( time.localtime(self.start_time))+"\nEnd Time:"+time.asctime( time.localtime(time.time()))+"\n")
                    self.end_position = "End testcase:"+str(self.now_testcase)+", end event:"+str(self.now_event)
                    self.endtimeflag = False

                #First check whether there are DMFs on the current interface that meet the preconditions
                dmfnum=self.check_dmf(self.device.screen)
                #If there is, select a DMF to execute with a certain probability
                if dmfnum>-1:
                    execute_result=self.execute_dmf(dmfnum,f_dmf)
                    print("************")
                    if execute_result == "True":
                        print("success")
                        i=0
                        while i<len(self.items):
                            f_dmf.write("list::"+self.items[i]+"::"+'::'.join(self.itemsdetail[i])+"\n")
                            print("list::"+self.items[i]+"::"+'::'.join(self.itemsdetail[i])+"\n")
                            i=i+1
                        f_dmf.write("success"+"\n\n")
                        f_dmf.flush()
                    elif execute_result != "False":
                        print("fail"+"::"+execute_result+"\n\n")
                        f_dmf.write("fail"+"::"+execute_result+"\n\n")
                        f_dmf.flush()
                        i=0
                        while i<len(self.items):
                            f_dmf.write("list::"+self.items[i]+"::"+'::'.join(self.itemsdetail[i])+"\n")
                            print("list::"+self.items[i]+"::"+'::'.join(self.itemsdetail[i])+"\n")
                            i=i+1
                    else:
                        print("fail")
                        f_dmf.write("fail"+self.dmf_list[dmfnum].name+"\n")
                    print("************")
                #Otherwise, select an event to execute according to the exploration rules
                else:     
                    event = self.policy.choice_event(self.device,self.now_event,False,self.keyview_list)
                    self.util.draw_event(event,self.nowscreenshotpath)
                    execute_result=self.executor.execute_event(self.device,event,0)
                    if execute_result == True:
                        if event.action == "edit":
                            self.device.close_keyboard()
                        time.sleep(1)
                        #Waiting for loading
                        waittime = 0
                        while waittime<10 and (self.device.use(className="android.widget.ProgressBar",packageName=self.app.package_name).exists and self.app.package_name!="com.ss.android.lark" or (self.device.use(text="...").exists and self.app.package_name=="io.github.hidroh.materialistic")):
                            time.sleep(1)
                            waittime=waittime+1
                        #Add the count of events and take a screenshot
                        self.now_event=self.now_event+1
                        self.save_screen(self.result_path,self.now_event)
                        #Detects whether a widget does not respond
                        click_classname_lists=["android.widget.Button","android.widget.ImageButton"]
                        if event.action=="click" and event.view.notin(self.noresponse_list) and self.now_event>1 and event.view.className in click_classname_lists and self.device.last_screen.allsame(self.device.screen):
                            self.noresponse_list.append(event.view)
                            self.f_noresponse.write("noresponse::"+str(self.now_testcase)+"_"+str(self.now_event-1)+"::"+str(self.now_testcase)+"_"+str(self.now_event)+"::"+event.view.line+"\n")
                            self.f_noresponse.flush()
                            shutil.copyfile(self.result_path+"/"+self.json_name+"screen/"+str(self.now_testcase)+"/"+str(self.now_event)+".png", self.result_path+"/"+self.json_name+"screen/noresponse/"+str(self.now_testcase)+"_"+str(self.now_event)+".png")
                            shutil.copyfile(self.result_path+"/"+self.json_name+"screen/"+str(self.now_testcase)+"/"+str(self.now_event-1)+".png", self.result_path+"/"+self.json_name+"screen/noresponse/"+str(self.now_testcase)+"_"+str(self.now_event-1)+".png")
                            
                        #Record event
                        if event.view!=None:
                            self.f_event.write(str(self.now_event)+"::"+event.action+"::"+event.text+"::"+event.view.line+"\n")
                        else:
                            self.f_event.write(str(self.now_event)+"::"+event.action+"\n")
                        self.f_event.flush()
                    else:
                        self.save_screen(self.result_path,self.now_event)
            
            self.f_event.write("Start Time:"+time.asctime( time.localtime(self.start_time))+"\nEnd Time:"+time.asctime( time.localtime(time.time()))+"\n")
            self.f_event.write(self.end_position)
            self.f_event.close()
            f_dmf.close()
            self.now_testcase=self.now_testcase+1

    def execute_dmf(self,dmfnum,f_dmf):
        nowdmf = self.dmf_list[dmfnum]
        print("********************************")
        print(nowdmf.name)
        # for widget in nowdmf.widgets:
        #     widget.real_text=""
        print("********************************")
        inputtext = ""
        now_layout = 0
        for widget in nowdmf.widgets:
            widget.real_text = widget.text
        for event in nowdmf.events:
            #Find the target widget
            for widget in nowdmf.widgets:
                if widget.name == event.widget:
                    nowwidget = widget
                elif "_name" in widget.name and now_layout==int(widget.UI_layout_num):
                    try:
                        view=self.findviewinlayout(self.device.screen.lines, widget, None)
                        if view == None:
                            print(event.action+" "+widget.name+" find fail")
                            return "False"
                        widget.real_text = view.text
                    except Exception as e:
                        print(e)
                        self.f_event.write(e)
                        return "False"
            line = self.util.changewidgettoline(nowwidget)
            view=View(line,[])
            view.set_xpath(nowwidget.xpath)
            execute_event = Event(view, event.action, self.device, 0)
            #Generate or get input value
            if event.text == "random":
                execute_event.set_text(self.random_text())
                inputtext = execute_event.text
            elif "::" in event.text:
                eventtext = event.text.split("::")
                i=0
                while i < len(self.items):
                    item = self.items[i]
                    itemlist = self.itemsdetail[i]
                    if item == eventtext[0] and eventtext[1]=="random":
                        randomnum = random.randint(0,len(itemlist)-1)
                        execute_event.set_text(itemlist[randomnum])
                        inputtext = execute_event.text
                    i=i+1
            else:
                execute_event.set_text(event.text)
                inputtext = execute_event.text
            #Execute and determine whether the event that must be executed is executed successfully
            executeresult=self.executor.execute_event(self.device,execute_event,0)
            if executeresult==False and event.force == True:
                print(event.action+" "+event.widget+" execute fail")
                return "False"
            elif executeresult==False and event.force == False:
                now_layout=now_layout+1
                continue
            #If the execution is successful:
            else:
                now_layout=now_layout+1
                if "_name" in widget.name and now_layout==int(widget.UI_layout_num):
                    view=self.findviewinlayout(self.device.screen.lines, widget, None)
                    widget.real_text = view.text
                #Wait for loading after execution
                time.sleep(1)
                waittime = 0
                while (waittime<5 and self.device.use(resourceId="com.ss.android.lark:id/search_result_loading_txt").exists and self.app.package_name=="com.ss.android.lark" ) or (waittime<10 and self.device.use(className="android.widget.ProgressBar",packageName=self.app.package_name).exists and self.app.package_name!="com.ss.android.lark"):
                    time.sleep(1)
                    waittime=waittime+1
                #Update screen
                self.now_event=self.now_event+1
                self.save_screen(self.result_path,self.now_event)
                #Output execution result
                if execute_event.view!=None:
                    self.f_event.write(str(self.now_event)+"::"+execute_event.action+"::"+execute_event.text+"::"+execute_event.view.line+"\n")
                else:
                    self.f_event.write(str(self.now_event)+"::"+execute_event.action+"\n")
                self.f_event.flush()
        #After successful execution, record the currently executed DMF
        f_dmf.write(str(self.now_event)+"::dmf::"+nowdmf.name+"::"+inputtext+"\n")
        print(nowdmf.name+" execute end")
        f_dmf.flush()
        #Update the stored background data according to the "impacts" corresponding to the DMF
        i=0
        findflag = False
        while i < len(self.items):
            if self.items[i] == nowdmf.datatype:
                datatype = self.items[i]
                itemlist = self.itemsdetail[i]
                findflag=True
                break
        if findflag == False:
            self.items.append(nowdmf.datatype)
            self.itemsdetail.append([])
            datatype = self.items[len(self.items)-1]
            itemlist = self.itemsdetail[len(self.itemsdetail)-1]
        for impact in nowdmf.impacts:
            if ".text" in impact.object:
                widgetname = impact.object[0:impact.object.find(".text")]
                for widget in nowdmf.widgets:
                    if widget.name == widgetname:
                        impactwidget = widget
                        impacttext = impactwidget.real_text
                        break
            if "add" in impact.operator:
                if "conflict" in impact.operator and impacttext in itemlist:
                    try:
                        itemlist.remove(impacttext)
                        f_dmf.write("delete::"+impacttext+"::"+datatype+"\n")
                    except Exception as ex:
                        f_dmf.write("delete::"+impacttext+"::"+datatype+"::nothave"+"\n")
                elif "noduplicate" in impact.operator and impacttext in itemlist:
                    f_dmf.write("duplicate::"+impacttext+"::"+datatype+"\n")
                else:
                    itemlist.append(impacttext)
                    f_dmf.write("add::"+impacttext+"::"+datatype+"\n")
            elif impact.operator=="delete":
                try:
                    itemlist.remove(impacttext)
                    f_dmf.write("delete::"+impacttext+"::"+datatype+"\n")
                except Exception as ex:
                    f_dmf.write("delete::"+impacttext+"::"+datatype+"::nothave"+"\n")
            elif impact.operator=="clear":
                itemlist.clear()
                f_dmf.write("\nclear::"+datatype+"\n")
        f_dmf.flush()

        #Check whether the post-condition is satisfied
        time.sleep(1)
        self.save_screen(self.result_path,self.now_event)
        for postcondition in nowdmf.postconditions:
            for widget in nowdmf.widgets:
                if widget.name == postcondition.widget:
                    postwidget = widget
            if ".text" in postwidget.text:
                widgetname = postwidget.text[0:postwidget.text.find(".text")]
                for widget in nowdmf.widgets:
                    if widget.name == widgetname:
                        postwidget.real_text=widget.real_text
                        break
            elif "::" in postwidget.text:
                eventtext = postwidget.text.split("::")
                i=0
                while i < len(self.items):
                    item = self.items[i]
                    itemlist = self.itemsdetail[i]
                    if item == eventtext[0] and eventtext[1]=="random":
                        randomnum = random.randint(0,len(itemlist)-1)
                        postwidget.real_text = itemlist[randomnum]
                    i=i+1
            #The first type of judgment is to check whether a specific widget is in the current interface
            if postcondition.datatype=="":
                view=self.findviewinlayout(self.device.screen.lines, postwidget, None)
                findinfo = postcondition.relation+"::"+postwidget.real_text
                if postcondition.relation == "in" and view==None:
                    return findinfo
                elif postcondition.relation == "not in" and view!=None:
                    return findinfo
                f_dmf.write(findinfo+"\n")
                f_dmf.flush()
            #The second type is to judge whether there is a widget with recorded text in a data list in the current interface
            else:
                i = 0 
                while i<self.items:
                    if postcondition.datatype == self.items[i]:
                        postdatatypelist = self.itemsdetail[i]
                    i=i+1
                view=self.findviewinlayout(self.device.screen.lines, postwidget, postdatatypelist)
                if postcondition.relation == "in" and view==None:
                    return findinfo
                elif postcondition.relation == "not in" and view!=None:
                    return findinfo
                f_dmf.write(findinfo+"\n")
                f_dmf.flush()
        
        return "True"

    def findviewinlayout(self, now_layout, widget, datalist):
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
            elif datalist==None and widget.real_text!="" and widget.real_text != view.text:
                continue
            elif view.package != self.app.package_name:
                continue
            elif widget.instance!="" and now_instance<int(widget.instance):
                now_instance=now_instance+1
                continue
            elif datalist!=None:
                findFlag = False
                for data in datalist:
                    if data == view.text:
                        findFlag = True
                if findFlag == False:
                    continue
            # print("widget- className:"+widget.className+",description:"+widget.description+",resourceId:"+widget.resourceId+",text:"+widget.real_text+",name:"+widget.name+"\n")
            # print("view- className:"+view.className+",description:"+view.description+"resourceId:"+view.resourceId+"text:"+view.text+"\n")
            return view
        return None

    def check_dmf(self,screen):
        candidate = []
        dmfnum = 0
        allcandidate="candidate:"
        while dmfnum < len(self.dmf_list):
            dmf = self.dmf_list[dmfnum]
            conditionpass = True
            for precondition in dmf.preconditions:
                #The first type of judgment is to check whether a specific widget is in the current interface
                if precondition.datatype=="":
                    for widget in dmf.widgets:
                        if widget.name == precondition.widget:
                            perwidget = widget
                    view=self.findviewinlayout(self.device.screen.lines, perwidget, None)
                    if precondition.relation == "in" and view==None:
                        conditionpass = False
                    elif precondition.relation == "not in" and view!=None:
                        conditionpass = False
                else:
                    predatatypelist=[]
                    i = 0 
                    while i<len(self.items):
                        if precondition.datatype == self.items[i]:
                            predatatypelist = self.itemsdetail[i]
                        i=i+1
                    #The second type is to judge whether a data list is empty
                    if precondition.widget=="":
                        if precondition.relation == "is empty" and len(predatatypelist)!=0:
                            conditionpass = False
                        elif precondition.relation == "is not empty" and len(predatatypelist)==0:
                            conditionpass = False
                        elif "smaller" in precondition.relation and len(predatatypelist)>5:
                            conditionpass = False
                    #The third type is to judge whether there is a widget with recorded text in a data list in the current interface
                    else:
                        for widget in dmf.widgets:
                            if widget.name == precondition.widget:
                                perwidget = widget
                        view=self.findviewinlayout(self.device.screen.lines, perwidget, predatatypelist)
                        if precondition.relation == "in" and view==None:
                            conditionpass = False
                        elif precondition.relation == "not in" and view!=None:
                            conditionpass = False
            if conditionpass == True:
                candidate.append(dmfnum)
                allcandidate=allcandidate+self.dmf_list[dmfnum].name+","
                j = 1
                while j < int(dmf.proportion):
                    j=j+1
                    candidate.append(dmfnum)
            dmfnum=dmfnum+1
        print(allcandidate)
        #Even if there is a DMF in the current interface that meets the preconditions, it is still possible not to select DMF
        proportion_random = 30
        k=0
        while k<proportion_random:
            k=k+1
            candidate.append(-1)
        
        candidatenum=random.randint(0,len(candidate)-1)
        if candidate[candidatenum]==-1:
            return -1
        else:
            return candidate[candidatenum]
    
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
            while i < 3:
                now_num=nums[random.randint(0,len(nums)-1)]
                random_string=random_string+now_num
                i=i+1
        elif text_style ==4:
            random_string=letters[random.randint(0,len(letters)-1)]+letters[random.randint(0,len(letters)-1)]
        elif text_style ==5:
            random_string=nums[random.randint(0,len(nums)-1)]+nums[random.randint(0,len(nums)-1)]
        elif text_style ==6:
            while i < 3:
                now_letters=letters[random.randint(0,len(nums)-1)]
                random_string=random_string+now_letters
                i=i+1
        elif text_style ==7:
            random_string="?10086"
        # if random_string=="" or random_string.startswith("?") or random_string.startswith(".") or random_string.startswith("x") or random_string.startswith("X") or random_string.startswith("0") or len(random_string)<3:
        #     random_string=self.random_text()
        else:
            for itemlist in self.itemsdetail:
                if random_string in itemlist:
                    random_string=self.random_text()
        return random_string

 

        
