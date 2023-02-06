class View(object):

    def __init__(self, line, keywordlist):
        self.line=line
        self.extract_attributes()
        self.findkey(keywordlist)
        self.img = None
        self.imgpath = None
        self.xpath = ""

    def findkey(self,keywordlist):
        self.key = self.resourceId+"::"+self.className+"::"+self.package+"::"+self.checkable
        self.key = self.key+"::"+self.clickable+"::"+self.enabled+"::"+self.focusable+"::"+self.focused
        self.key = self.key+"::"+self.scrollable+"::"+self.longClickable+"::"+self.selected+"::"+self.visibleToUser
        textflag=False
        if self.text.strip() !="":
            for keyword in keywordlist:
                if keyword == self.text or "Allow" in self.text:
                    self.key = self.key+"::"+self.text.strip()
                    textflag=True
                    break
        if textflag == False:
            self.key = self.key+"::text"

        descriptionflag=False
        if self.description.strip() !="":
            for keyword in keywordlist:
                if keyword == self.description or "Allow" in self.description:
                    self.key = self.key+"::"+self.description.strip()
                    descriptionflag=True
                    break
        if descriptionflag == False:
            self.key = self.key+"::description"

    def extract_attributes(self):
        self.x = -1
        self.y = -1
        self.index=self.get_attribute('index=')
        self.text=self.get_attribute('text=')
        self.resourceId=self.get_attribute('resource-id=')
        self.className=self.get_attribute('class=')
        self.package=self.get_attribute('package=')
        self.description=self.get_attribute('content-desc=')
        self.checkable=self.get_attribute('checkable=')
        self.checked=self.get_attribute('checked=')
        self.clickable=self.get_attribute('clickable=')
        self.enabled=self.get_attribute('enabled=')
        self.focusable=self.get_attribute('focusable=')
        self.focused=self.get_attribute('focused=')
        self.scrollable=self.get_attribute('scrollable=')
        self.longClickable=self.get_attribute('long-clickable=')
        self.password=self.get_attribute('password=')
        self.selected=self.get_attribute('selected=')
        self.visibleToUser=self.get_attribute('visible-to-user=')
        self.bounds=self.get_attribute('bounds=')
        self.get_bounds_value()
    
    def set_xpath(self,xpath):
        self.xpath = xpath

    def get_attribute(self,keywords):
        line=self.line
        attributenum=line.find(keywords)
        line=line[attributenum+len(keywords)+1:len(line)-1]
        marksnum=line.find('\"')
        attribute=line[0:marksnum]
        return attribute

    def get_bounds_value(self):
        num1=self.bounds.find(",")
        self.xmin=self.bounds[1:num1]
        num2=self.bounds.find("]")
        self.ymin=self.bounds[num1+1:num2]
        line=self.bounds[num2+1:len(self.bounds)]
        num1=line.find(",")
        self.xmax=line[1:num1]
        num2=line.find("]")
        self.ymax=line[num1+1:num2]
        if self.xmax!= "" and self.xmin!="" and self.ymax!= "" and self.ymin!="":
            self.x = (int(self.xmin)+int(self.xmax)) /2
            self.y = (int(self.ymin)+int(self.ymax)) /2
            
    def same(self,view):
        if self.className !="#any#" and view.className !="#any#" and self.className != view.className:
            return False
        if self.resourceId !="#any#" and view.resourceId !="#any#" and self.resourceId != view.resourceId:
            return False
        if self.package !="#any#" and view.package !="#any#" and self.package != view.package:
            return False
        if self.selected !="#any#" and view.selected !="#any#" and self.selected != view.selected:
            return False
        if self.description !="#any#" and view.description !="#any#" and self.description != view.description:
            return False
        if self.focused !="#any#" and view.focused !="#any#" and self.focused != view.focused:
            return False
        if self.enabled !="#any#" and view.enabled !="#any#" and self.enabled != view.enabled:
            return False
        if self.clickable !="#any#" and view.clickable !="#any#" and self.clickable != view.clickable:
            return False
        if self.checked !="#any#" and view.checked !="#any#" and self.checked != view.checked:
            return False
        if self.checkable !="#any#" and view.checkable !="#any#" and self.checkable != view.checkable:
            return False
        if self.text !="#any#" and view.text !="#any#" and self.text != view.text:
            return False
        if self.visibleToUser !="#any#" and view.visibleToUser !="#any#" and self.visibleToUser != view.visibleToUser:
            return False
        if self.password !="#any#" and view.password !="#any#" and self.password != view.password:
            return False
        if self.longClickable !="#any#" and view.longClickable !="#any#" and self.longClickable != view.longClickable:
            return False
        if self.scrollable !="#any#" and view.scrollable !="#any#" and self.scrollable != view.scrollable:
            return False
        if self.bounds !="#any#" and view.bounds !="#any#" and self.bounds !="" and view.bounds !="" and self.bounds != view.bounds:
            return False
        return True
    
    def notin(self,viewlist):
        for now_view in viewlist:
            if self.same(now_view):
                return False
        return True
    
    

   