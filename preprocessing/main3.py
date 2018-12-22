# -- coding: UTF-8 -- 
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

#阈值为1s
#对不同MAC地址进行遍历
#输入某一个MAC的某一个天的时间戳，输出离开次数，也就是会话数
def count_ave_session_for_each_MAC(timestamp,threshold):
    #这一天的时间戳
    #将所有时间转化成s，put it in the new list timestamp2[]
    timestamp2=[]
    for time1 in timestamp:
        hms=time1.split(':')
        second=int(hms[0])*60*60+int(hms[1])*60+int(hms[2])
        timestamp2.append(second)
    gap_time_list=[]
    #the number of time
    len_timestamp2=len(timestamp2)
    #the number of gap
    gap_num=len_timestamp2-1
    for i in range(0,gap_num):
        gap_time_value=timestamp2[1+i]-timestamp2[0+i]
        gap_time_list.append(gap_time_value)
    #初始化，认为离开网络次数为0,等于会话数
    num_depart=0
    for i in gap_time_list:
        if int(i) > threshold:
            num_depart+=1
    return num_depart

def time_in_each_day(MAC):
    day_dict={}
    for each_msg in MAC:
        if each_msg[0] in day_dict:
            day_dict[each_msg[0]].append(each_msg[1])
        else:
            day_dict[each_msg[0]]=[]
            day_dict[each_msg[0]].append(each_msg[1])
    return day_dict 

def count_ave_session(threshold):
    sum_session_all_MAC=0
    num_MAC=0
    for key in info_dict.keys():
        MAC=info_dict[key]
        #调用函数time_in_each_day
        day_dict=time_in_each_day(MAC) 
        #hwo many days we count
        days=0
        #下面的key就是第几天
        sum_session=0
        for day1 in day_dict.keys():
            days+=1
            #extract all the time on the ith day
            timestamp=day_dict[day1]
            timestamp = sorted(timestamp, reverse=False)
            num_depart=count_ave_session_for_each_MAC(timestamp,threshold)   
            sum_session+=num_depart
        ave_session=sum_session/days*1.0
        num_MAC+=1
        sum_session_all_MAC+=ave_session
    ave_session_all_MAC=sum_session_all_MAC/num_MAC*1.0
    return ave_session_all_MAC

#ave_session_all_MAC=count_ave_session(600)


"""
time_in_each_day
{'02-07-20': ['04:46:40', '04:51:40',


"""            
#info_dict['e23f35f126d5f2f7b7b090b950481064143f1483']

#['02-07-20', '04:46:40'], ['02-07-20', '04:51:40'], ['02-07-20', '04:56:40'],     
"""
day_dict
{'02-07-20': ['04:46:40',
  '04:51:40',
  '04:56:40',
  '05:01:40',
  '05:06:41',
  '05:11:40',
  '05:16:40',
  '05:21:40',
"""  
'''
MAC: 
[['02-07-20', '04:46:40'],
 ['02-07-20', '04:51:40'],
 ['02-07-20', '04:56:40'],
 ['02-07-20', '05:01:40'],
 ['02-07-20', '05:06:41'],
 ['02-07-20', '05:11:40'],
 ...]
''' 


ave_session_all_MAC_list=[]
threshold_list=[]
#for threshold in range(300,5400):
#for threshold in range(5,10):
for threshold in range(300,5400,300):
    threshold_list.append(threshold)
    print(threshold)
    avg = count_ave_session(threshold)
    ave_session_all_MAC_list.append(avg)
    print(avg)

with open("plot_data3.txt", 'w') as f:
	f.write("")
for i in range(0,len(threshold_list)):
#for i in ave_session_all_MAC_list:
	with open("plot_data3.txt", 'a') as f:
		f.write(str(threshold_list[i])+'\t'+str(ave_session_all_MAC_list[i])+'\n')
