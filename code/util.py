import os
import os
import numpy as np
import os
import json
import cv2
from dmf import DMF

class Util(object):

    def __init__(self, app_path, json_name):
        self.app_path = app_path
        self.json_name = json_name
    
    def create_outputdir(self,path):
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(path+"/"+self.json_name+"screen"):
            os.makedirs(path+"/"+self.json_name+"screen")
    
    def draw_event(self,event,screenshot_path):
        import cv2
        image = cv2.imread(screenshot_path)
        if screenshot_path != "" and event.view !=None:
            if event.action == "click":
                cv2.rectangle(image, (int(event.view.xmin), int(event.view.ymin)), (int(event.view.xmax), int(event.view.ymax)), (0, 0, 255), 5)  
            elif event.action == "longclick":
                cv2.rectangle(image, (int(event.view.xmin), int(event.view.ymin)), (int(event.view.xmax), int(event.view.ymax)), (0, 225, 255), 5) 
            elif event.action == "edit":
                cv2.rectangle(image, (int(event.view.xmin), int(event.view.ymin)), (int(event.view.xmax), int(event.view.ymax)), (225, 0, 255), 5)
            else:
                cv2.rectangle(image, (int(event.view.xmin), int(event.view.ymin)), (int(event.view.xmax), int(event.view.ymax)), (225, 225, 255), 5)
        else:
            if event.action == "wrong":
                cv2.rectangle(image, (0,0), (1430, 2550), (0, 225, 255), 20)
            else:
                cv2.putText(image,event.action, (100,300), cv2.FONT_HERSHEY_SIMPLEX, 5,(0, 255, 0), 3, cv2.LINE_AA)
        # image=self.resize(image)
        try:
            cv2.imwrite(screenshot_path, image)
        except Exception as e:
            print(e)
    
    def resize(self,image):
        (h, w) = image.shape[:2]
        if w > 2000:
            (cX, cY) = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D((cX, cY), -90, 1.0)
            import numpy as np
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])
            nW = int((h * sin) + (w * cos))
            nH = int((h * cos) + (w * sin))
            M[0, 2] += (nW / 2) - cX
            M[1, 2] += (nH / 2) - cY
            image = cv2.warpAffine(image, M, (nW, nH))
            image=cv2.resize(image, (256, 512))
        elif w > 512:
            image=cv2.resize(image, (256, 512))
        return image

    def compare_images(self,path_one, path_two):
        image1 = cv2.imread(path_one)
        image2 = cv2.imread(path_two)
        difference = cv2.subtract(image1, image2)
        result = not np.any(difference) #if difference is all zeros it will return False
        if result is True:
            print("same")
            return True
        else:
            cv2.imwrite("result.jpg", difference)
            print ("different")
            return False
    
    def decompile(self,app_path,out_path):
        #use apktool
        cmd = 'apktool d -f '+app_path+' -o '+out_path
        print('--------Start Working with apktool--------')
        os.system(cmd)
        print('-----------------------------\nwork all done,output file in:\n'
            +out_path+'\n-----------------------------\n')
        # os.system('pause')
        f = open(out_path+"/res/values/"+'strings.xml','r',encoding='utf-8')
        lines=f.readlines()
        f.close()
        keywordlist = []
        for line in lines:
            num1=line.find("\">")
            num2=line.find("</")
            string=line[num1+2:num2]
            keywordlist.append(string)
        return keywordlist

    def get_keyview(self,root_path):
        keyview_list = []
        with open(os.path.join(root_path+"/dmf/"+self.json_name+"/keyviews"+self.json_name+".json"), 'r') as f:
            data = json.load(f)
        for nowview in data['keyviews']:
            print(nowview['view'])
            from view import View 
            view = View(nowview['view'],[])
            keyview_list.append(view)
        return keyview_list

    def changewidgettoline(self,widget):
        line="<node NAF=\"#any#\" index=\"index_string\" text=\"text_string\" resource-id=\"resourceId_string\" class=\"className_string\" package=\"#any#\" content-desc=\"description_string\" checkable=\"#any#\" checked=\"#any#\" clickable=\"#any#\" enabled=\"#any#\" focusable=\"#any#\" focused=\"#any#\" scrollable=\"#any#\" long-clickable=\"#any#\" password=\"#any#\" selected=\"#any#\" visible-to-user=\"#any#\" bounds=\"\" />"
        if widget.real_text !="":
            line= line.replace("text_string",widget.real_text)
        else:
            line= line.replace("text_string",widget.text)
        line= line.replace("resourceId_string",widget.resourceId).replace("className_string",widget.className).replace("description_string",widget.description).replace("index_string",widget.instance)
        return line
    
    def get_dmf(self,root_path):
        dmf_list = []
        with open(os.path.join(root_path+self.json_name+"/dmf"+self.json_name+".json"), 'r') as f:
            data = json.load(f)
        for nowdmf in data['dmfs']: 
            print(nowdmf['name']) 
            dmf = DMF(nowdmf['name'],nowdmf['proportion'],nowdmf['type'])
            for event in nowdmf['events']:
                dmf.add_event(event['action'],event['widget'],event['text'],event['force'])
            for widget in nowdmf['widgets']:
                dmf.add_widget(widget['UI_layout_num'],widget['class'],widget['content-desc'],widget['name'],widget['resource-id'],widget['text'],widget['xpath'],widget['instance'])
            for precondition in nowdmf['preconditions']:
                dmf.add_precondition(precondition['UI_layout_num'],precondition['datatype'],precondition['relation'],precondition['widget'])
            for impact in nowdmf['impacts']:
                dmf.add_impact(impact['object'],impact['operator'])
            for postcondition in nowdmf['post-conditions']:
                dmf.add_postcondition(postcondition['UI_layout_num'],postcondition['datatype'],postcondition['relation'],postcondition['widget'])
            dmf_list.append(dmf)
        return dmf_list

    


