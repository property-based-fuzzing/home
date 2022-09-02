from view import View
class BackLink(object):
    def __init__(self,nowscreen,lastscreen,backevent,last_event,now_event,last_activity,now_activity,now_testcase):
        self.nowscreen = nowscreen
        self.lastscreen = lastscreen
        self.backevent = backevent
        self.last_event = last_event
        self.now_event = now_event
        self.last_activity = last_activity
        self.now_activity = now_activity
        self.now_testcase = now_testcase

class Screen(object):
    def __init__(self, lines, keywordlist):
        self.lines = lines
        self.text = ""
        self.realallviews = []
        self.allleafviews=self.get_view(keywordlist)
        
        self.keyviews = []
        for view in self.allleafviews:
            if view.notin(self.keyviews):
                self.keyviews.append(view)
        self.keyviews.sort(key = lambda x: x.key, reverse=False)
        self.num = -1

    def get_view(self, keywordlist):
        allleafviews=[]
        for line in self.lines:
            self.text = self.text + line
            if '<node ' in line :
                view=View(line,keywordlist)
                self.realallviews.append(view)
                if '/>' in line:
                    allleafviews.append(view)
        allleafviews.sort(key = lambda x: x.key, reverse=False)
        return allleafviews
    
    def notin(self,screenlist):
        for now_screen in screenlist:
            if self.allsame(now_screen):
                return now_screen
        return None
    
    def allsame(self,now_state):
        if len(self.keyviews) != len(now_state.keyviews):
            return False
        i=0
        while(i<len(self.keyviews)):
            if not self.keyviews[i].same(now_state.keyviews[i]):
                return False
            i=i+1
        return True
    
