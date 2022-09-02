class Condition(object):
    def __init__(self,preorpost,UI_layout_num,datatype,relation,widget):
        self.preorpost = preorpost
        self.UI_layout_num = UI_layout_num
        self.datatype = datatype
        self.relation = relation
        self.widget = widget

class Impact(object):
    def __init__(self,object,operator):
        self.object = object
        self.operator = operator

class Event(object):
    def __init__(self,action,widget,text,force):
        self.action = action
        self.widget = widget
        self.text = text
        self.force = force

class Widget(object):
    def __init__(self,UI_layout_num,className,description,name,resourceId,text,xpath,instance):
        self.UI_layout_num = UI_layout_num
        self.className = className
        self.description = description
        self.name = name
        self.resourceId = resourceId
        self.text = text
        self.xpath = xpath
        self.real_text = text
        self.instance = instance

class DMF(object):

    def __init__(self, name, proportion, type):
        self.name = name
        self.proportion = proportion
        self.type = type
        self.events = []
        self.widgets = []
        self.preconditions = []
        self.postconditions = []
        self.impacts = []
        self.datatype = self.name.split(" ")
        self.datatype = self.datatype[1]
    
    def add_widget(self,UI_layout_num,className,description,name,resourceId,text,xpath,instance):
        widget = Widget(UI_layout_num,className,description,name,resourceId,text,xpath,instance)
        self.widgets.append(widget)

    def add_precondition(self,UI_layout_num,datatype,relation,widget):
        precondition = Condition("pre",UI_layout_num,datatype,relation,widget)
        self.preconditions.append(precondition)
    
    def add_event(self,action,widget,text,force):
        event = Event(action,widget,text,force)
        self.events.append(event)
    
    def add_impact(self,object,operator):
        impact = Impact(object,operator)
        self.impacts.append(impact)
    
    def add_postcondition(self,UI_layout_num,datatype,relation,widget):
        postcondition = Condition("post",UI_layout_num,datatype,relation,widget)
        self.postconditions.append(postcondition)
    
