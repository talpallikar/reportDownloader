import requests
import os
from bs4 import BeautifulSoup
import shutil
import json
from urllib2 import urlopen 
import time
from string import maketrans

BASE = "https://www.princeton.edu/~ota/"
count = 0
start_time = time.time()
PATH = ""

def main():                                #main method
    setdir()
    for x in range(74,96):                 #cycles through all years 
        get_all_reports("https://www.princeton.edu/~ota/ns20/caty"+str(x)+"_n.html") 

def setdir():                              #preps the directory for downloads
    if(os.path.isdir("OTA_Publications")): #clears existing downloads
        shutil.rmtree("OTA_Publications")
        print "Cleared Folder"
    os.mkdir("OTA_Publications")
    os.chdir("OTA_Publications")
    global PATH
    PATH = os.getcwd()
    for x in range(1972, 1997):            #makes folders for every year of reports
        os.mkdir(str(x))
    print "Folders Created"

def get_all_reports(source_url):           #populates array of links with a year's report links
    html = urlopen(source_url).read()      #finds the report pages for the given year
    soup = BeautifulSoup(html)
    l = soup.findAll("a")
    links = []                             
    for x in l:
        links.append(str(x))               #longwinded way but it makes them str
    for link in links:
        get_report_link(link)

def get_report_link(page_link):            #converts one report link into a document link and file name
    year = page_link[18:22]  
    doc = page_link[23:27]
    bob = year+"_"+doc+"_"+page_link[36:len(page_link)-4]
    if ((len(os.path.join(PATH,bob))) > 250):
        bob = bob[0:len(bob)-(2*(len(bob)-bob.find("(")))]+bob[bob.find("("):len(bob)]
        print ("Path of " + year + "_" + doc +" is too long, file name adjusted")
    intab = "/?%*:;'&|,<>. " #take this out of if
    outtab = "-------------_"
    trantab = maketrans(intab, outtab) 
    bob = bob.translate(trantab) #bob is passed as the file name
    download_file(BASE+page_link[12:27]+page_link[22:27]+".PDF",bob)

def download_file(download_url,file_name): #Given a document link and file name, downloads file into correct directory
    response = urlopen(download_url)       # and saves it with a prepped name
    print("Downloading "+file_name[0:9])
    if(os.getcwd() != PATH):
        os.chdir("..")
    os.chdir(os.path.join(PATH,file_name[0:4]))
    file = open(file_name+".pdf",'wb')
    file.write(response.read())
    file.close()
    print("Completed "+file_name)
    file_counter(file_name)

def file_counter(file_name):              #Reports on time consumed and keeps track of number of reports downloaded
    global count
    count += 1
    if (count % 10 == 0): 
        print (str(count)+" reports downloaded")
        print "Elapsed time: " + to_HMS(time.time() - start_time)
        print (str(round((float(count)/721)*100,2)) + " % Complete")
    print("")
    if (file_name[0:4] == "1996"):
    	print("")
    	print "Downloads Complete"
    	print "Total Reports Downloaded: " + str(count)
    	print "Total Elapsed Time: " + to_HMS(time.time()-start_time)

def to_HMS(seconds):                      #Converts seconds to HMS. Called by timer.
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

if __name__ == "__main__":                #for use as a library
    main()
