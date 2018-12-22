import xml.etree.ElementTree as ET
import os
import pickle

path1 = "..\SJTU-WiFi-clients-data"

#Put all the path in the [pathlist] form given path
def find_all_file_in_the_folder(path):
    pathlist=[]
    for i in os.listdir(path):
        pathlist.append(i)
    return pathlist


def buildDic_time_AP_users(path, filelist):
    time_AP_users = {}
    for filename in filelist:
        dom = ET.parse(os.path.join(path,filename))
        root = dom.getroot()
        if len(root) == 0:
            continue
        rootChildList = root[0]
        for child in rootChildList:
            username = None

            if child.tag == 'association':
                connect_time = child[2].text
                date = connect_time.split('T')[0]
                if date not in time_AP_users.keys():
                    time_AP_users[date] = [{}] * 24 * 60# use -1 to denote in this time, there is nobody in any AP
                else:
                    time = connect_time.split('T')[1]
                    minute_index = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
                    # since some data may lose the username, however, for a same file, the username should be the same, so we simply user the last user name
                    ap = ''
                    for i in child:
                        if i.tag == 'ap':
                            ap = i.text
                        if i.tag == 'username':
                            username = i.text
                    ap_userlist = time_AP_users[date][minute_index]
                    if ap not in ap_userlist.keys():
                        ap_userlist[ap] = []
                        ap_userlist[ap].append(username)
                    else:
                        if username not in ap_userlist[ap]:
                            ap_userlist[ap].append(username)

    return time_AP_users



filelst = find_all_file_in_the_folder(path1)
# for i in pathlst:
#     manage_data_in_file(path1+ '/' + i)
time_AP_users = buildDic_time_AP_users(path1, filelst)
f =  open('time_AP_users.pk', 'w')
pickle.dump(time_AP_users, f)