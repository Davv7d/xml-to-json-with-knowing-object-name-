import json
import xml.etree.ElementTree as ET

def parsingXML(file):
    try:            #do if xml is corect
        root = ET.fromstring(file)
        return root

    except:  #xml is not corect
        next = 0
        objects = []

        while True:
            objectstart = file.find('<object>',next)
            objectend = file.find('</object>',objectstart)
            objects.append(file[objectstart:objectend+9])
         #   print(next,'\n')
            next = objectend
            if file.find('<object>',next) == -1:
                break
        object_string = ""
        wrong =[]
        for i in range(len(objects)):
            try:
                correct = ET.fromstring(objects[i])
                object_string += (objects[i] + "\n")
            except:
                wrong+=(objects[i]+"\n")

        object_string ="<all>\n"+object_string+"</all>"
       # print(object_string)
        try:
            object_ready = ET.fromstring(object_string)
        except:
            object_ready = {}
            print("object_ready - error")
        return  object_ready

def checkXML(root):
    try:
        i = 1 #number of object with error
        objects = root.findall('object')
        objects_correct ={}
        #print ('number of object:', len(objects))
        for element in objects:
           # print('Name', element.find('obj_name').text)
            if element.find('obj_name').text and element.find('field').text:
                fields = element.findall('field')
                for field in fields:
                    if not ((field.find('name') is not None) and (field.find('type').text in ('string' , 'int')) and (field.find('value') is not None)):
                        i+=1
                        element.remove(field)
            else:
                root.remove(element)
        return root
    except:
        print("failed with loading xml in checkXML function")

def convertJSON(xml):
    try:
        i = 1
        readyJson ={}
        objects = xml.findall('object')
        for object in objects:
            try:
                try:
                    fields = object.findall('field')
                    element = {}
                    for field in fields:
                        element[field.find('name').text] = field.find('value').text

                except:
                    print('failed parsing json at filed in object: ',i, " ",field.find('name').text,field.find('value').text)

                readyJson[object.find('obj_name').text] = element

            except:
                print('failed parsing json at object:',i," problem with obj_name \n")
                input(" ")
            i+=1
        readyFile = json.dumps(readyJson)

        return readyFile
    except:
        print("failed with loading xml in convertJson function")

if __name__ =="__main__":
    try:
       # file1 = open('input_improved.xml').read()
        file2 = open('input.xml').read()

    except:
        print('failed load file')
    finally:
        parsedXML = parsingXML(file2)
        readyXML = checkXML(parsedXML)
        jsonfile = convertJSON(readyXML)
        with open('output.json', 'w') as outfile:
            json.dump(jsonfile,outfile)
