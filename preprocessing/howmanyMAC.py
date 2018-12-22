import os
#Write down your folder here
path1="../anon-data"

#Put all the path in the [pathlist] form given path
def find_all_path_in_the_folder(path):
    pathlist=[]
    for i in os.walk(path):
        pathlist.append(i[0])
    #remove the root path
    pathlist.remove(pathlist[0])
    return pathlist

#pathlsit has all the paths in the path1
pathlist=find_all_path_in_the_folder(path1)

#Put all the file name in the [filelist] form given path
def find_all_files_in_the_folder(path):
    filelist=[]
    for i in os.walk(path):
        for j in i[2]:
            filelist.append(j)
    return filelist

#put all the files'name in the dict named filedict{path:filename}
filedict={}
for i in pathlist:
    filedict[i]=find_all_files_in_the_folder(i)
        

# Find all the file whose name is end with "-users.snmp"
def find_all_user_info_file(filelist):
    user_info_filelist=[]
    for i in filelist:
        if i.find("-users.snmp")!=-1:
            user_info_filelist.append(i)
    return user_info_filelist
            
#put all the files'path in the dict named user_info_dict
def extract_user_info_path(filedict):
    #I want to put all the data in a dict with the key whose name is the path
    user_info_path_dict={}
    for path in filedict.keys():
        #THE name of file in the 'path'
        user_info_file_in_path_list=[]
        #the path of each file in the 'path'
        user_info_file_path_list=[]
        #get the file name in the 'path' and put it in the filelist_in_path
        filelist_in_path_list=filedict[path]
        #find all the file whose name is end with '-suers.snmp' and put them in the [user_info_file_in_path]
        for i in filelist_in_path_list:
            if i.find('-users.snmp')!=-1:
                user_info_file_in_path_list.append(i)
        #get all the user info files' paths and put them in the [ser_info_file_path]
        for i in user_info_file_in_path_list:
            user_info_file_path=os.path.join(path,i) 
            user_info_file_path_list.append(user_info_file_path)
        user_info_path_dict[path]=user_info_file_path_list
    return user_info_path_dict

user_info_path_dict=extract_user_info_path(filedict)

#ectract all the user info in the dict named user_info_data_dict
def extract_user_info_data(user_info_path_dict):
    user_info_data_dict={}
    for path1 in user_info_path_dict.keys():
        user_info_data_path1_list=[]
        user_info_file_in_path1=user_info_path_dict[path1]
        for each in user_info_file_in_path1:
            with open(each, 'r') as f:
                list1 = f.readlines()
            user_info_data_path1_list.extend(list1)
        user_info_data_dict[path1]=user_info_data_path1_list
    return user_info_data_dict

user_info_data_dict=extract_user_info_data(user_info_path_dict)

#To combine all the file into one file
def combine_file(user_info_data_dict):
    list=[]
    for path3 in user_info_data_dict.keys():
        list.extend(user_info_data_dict[path3])
    return list

user_info_file=combine_file(user_info_data_dict)

#extract information from user_file
#n=[2,3,11]
def extract():
    info_list=[]
    for i in user_info_file:
        temp=i.split('\t')
        new=temp[1]+'\t'+temp[2]+'\t'+temp[10]
        info_list.append(new)
    return info_list
info_list=extract()    

def info_dict(info_list):
    info_dict={}
    for i in info_list:
        temp=i.split('\t')
        if temp[2] in info_dict:
            info_dict[temp[2]].append([temp[0],temp[1]])
        else:
            info_dict[temp[2]]=[]
            info_dict[temp[2]].append([temp[0],temp[1]])
    return info_dict
info_dict=info_dict(info_list)

print(len(info_dict.keys()))