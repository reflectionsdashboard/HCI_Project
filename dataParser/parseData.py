from bs4 import BeautifulSoup
##from dateutil import parser as DateParser
import json
import datetime

tags = ["DataStructuresInRealLife","CompOrgInRealLife"]

for tag in tags:
    contentf = open(tag + "contents.txt","r",encoding="UTF-8");

    contents = []

    pre = "";
    for line in contentf:
        if line.strip() == "x":
            item = {}
            item["full_text"] = pre
            item['user'] = {}
            contents.append(item);
            pre = "";
        else:
            pre = pre + line;
        
            
    contentf.close()

    print(len(contents))

    idf = open(tag + "ids.html","r",encoding="UTF-8")

    soup = BeautifulSoup(str(idf.readlines()), 'html.parser')
    idf.close();

    lists = soup.find_all("a");

    print(len(lists));
    i = len(lists) - 1;
    while (i >= 0):
    
    ##    print(i)
        if(i % 2 == 0):
            contents[(int) (i / 2)]["user"]['id_str']= lists[i]["data-user-id"]
            contents[(int) (i / 2)]["user"]['screen_name'] = lists[i]["href"][1:]
            contents[(int) (i / 2)]["subject"] = "#" + tag
        else:
            link = lists[i]["href"]
            contents[(int) (i / 2)]["id_str"]  = link.split("/")[-1]
            contents[(int) (i / 2)]["created_at"] = str(datetime.datetime.fromtimestamp(int(lists[i].find_all("span")[0]["data-time-ms"]) / 1000))                                              
        i = i - 1;
    with open("manualTweets.txt","a") as f:
        for item in contents:
            json.dump(item, f)
            f.write("\n")
        f.close()
##                                               
                                                
