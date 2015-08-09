import math
import argparse
import dns
import os
from netaddr import IPNetwork

def banner():
    print "#######                                    "
    print "#       #    # #    # #    # ###### #      "
    print "#       #    # ##   # ##   # #      #      "
    print "#####   #    # # #  # # #  # #####  #      "
    print "#       #    # #  # # #  # # #      #      "
    print "#       #    # #   ## #   ## #      #      "
    print "#        ####  #    # #    # ###### ###### "
    print '\n'
    print "[+]=========================================[+]"
    print "     Developed    :   Israel Araoz"
    print "     Twitter      :   iara0z"
    print "     Version      :   1.0"
    print "[+]=========================================[+]\n"
    
def checkFile(nameFile):
    try:
        os.stat("data/"+str(nameFile))
        return True
    except Exception, e:
        return False


def getSizeOfFile(pathFile):
    file = open(pathFile)
    file.seek(0,2)
    size = file.tell()
    file.close()
    return size


def getIP(country="BO", nic="lacnic",ipv="ipv4",convert=False):
        sizeOfFile = getSizeOfFile("data/"+str(nic))
        ipFile = open("data/lacnic","rb")
        if sizeOfFile > 0:
            print "[+] Size of file :   ",(sizeOfFile / 1024), "KB"
            ipTuple = ipFile.readlines()
            for ipData in ipTuple:
                if ((ipv in ipData) & (country in ipData)) :
                    row = ipData.split("|")
                    print "[+] NIC           : ",row[0]
                    print "[+] Country       : ",row[1]
                    print "[+] IP Version    : ",row[2]
                    cidr = (row[3],(32-math.log (float(row[4]),2)))
                    print "[+] CIDR          : ","%s/%d" % cidr        
                    if convert:
                        print "\t [+][+] IP Address"
                        for ipaddr in IPNetwork(str(cidr[0]+"/"+str(int(cidr[1])))):
                            print "IP   : ", ipaddr
        else:
            print "[-] Check the file, maybe something is wrong :("
   

def main():
    banner()
    Des = "Gathering global IP data tool  :)"
    parser = argparse.ArgumentParser(description = Des)
    parser.add_argument("-co","--country", dest="country",help="Domain e.i --country BO")
    parser.add_argument("-n","--nic", dest="nic",help="NIC, Network Information Center you can use lacnic | afrinic | arin | ripencc | aprinic")
    parser.add_argument("-ipv","--ipversion", dest="ipversion",help="IP Version e.i --country ipv4 | ipv6")
    parser.add_argument("-rip","--resolveip", dest="resolveip",help="Get information about CIDR")
    #parser.add_argument("-u","--update", dest="update",help="Update about Data")
    #parser.add_argument("-a","--all", dest="all",help="Initiating War")
    args = parser.parse_args()
    argCountry = args.country
    argNic = args.nic
    argIPv = args.ipversion
    argRip = args.resolveip
    if argNic and argIPv:
        if checkFile(argNic):
            if str(argIPv) == "ipv4" or str(argIPv) == "ipv6":
                getIP(argCountry,argNic,argIPv,True)
            else:
                print "[-] The parameter ipv  : (ipv4 | ipv6) not :", str(argIPv)
        else:
            print "[-] NIC : ", argNic , "does not exist"
            print "[+] List nic : lacnic | afrinic | arin | ripencc | aprinic"
            
    else:
        print parser.usage
        exit(0)
    

if __name__=="__main__":
    main()

