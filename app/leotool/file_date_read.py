import os
def getDate(fileurl):
    loadfile = [fileurl]
    imagedata = []
    while(loadfile):
        try:
            path = loadfile.pop()
            #print path
            for x in os.listdir(path):
                if os.path.isfile(os.path.join(path,x)):
                    imagedata.append(x)
                else:
                    loadfile.append(os.path.join(path,x))
        except Exception,e:
            print str(e) + path
    return imagedata