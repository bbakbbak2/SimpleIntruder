#-*-coding:utf-8-*-

import requests
import time
import argparse
import sys

def intruder(host, port, ofile):
    if host.endswith('/'):
        host = host[:host.rfind('/')]
    fileName = host+'.txt'
    
    fr = ''
    try:
        fr = open(ofile,'r')
    except IOError:
        print "\nCheck the \"sample.txt\" is exist or not in the same folder."
        raw_input("Enter the exit.")
        sys.exit(0)
        
    fw = open(fileName,'w')
    res = ''
    testhost = ''
    protocol = 'http://'
    
    print '\nDo you want to test the https protocol?(y/n)'
    opt = raw_input(' Answer: ')
    
    if opt == 'y':
        protocol = 'https://'
    
    # 시작 포트 번호 셋팅
    if port is '80':
        host = protocol+host
    else:
        host = protocol+host+':'+ port

    for subUrl  in fr.readlines():
        subUrl = subUrl.rstrip('\n')
        
        # 리스트 내의 Port 존재  확인하고 바꾸기
        if subUrl.startswith(':') and port is not '80':
            modifiedHost = host[:host.rfind(':')]
            #subUrlPort = subUrl.split('/')[1][1:]
            testhost = modifiedHost+subUrl
        else:
            testhost = host+subUrl
            
        try:
            # 접속 시도
            res = requests.get(testhost, timeout=2)
            code = res.status_code
            
            result = '[%d] %s' %(code,testhost)
            print result
            
            fw.write(result+'\n')
            
        except requests.exceptions.ConnectionError:
            result = '[Error] %s' %(testhost)
            fw.write(result+'\n')
            print result
        except requests.exceptions.ReadTimeout:
            result = '[Error] %s' %(testhost)
            fw.write(result+'\n')
            print result            
        
        time.sleep(0.5)
   
    print 'check the '+fileName
    fr.close()
    fw.close()
    
    time.sleep(1)

def usage():
    print
    print '*****   Welcome to Intruder *****'
    print '   Must enter the correct host name.'
    print '   Default Port: 80, File: sample.txt'
    print
    
    host = raw_input("Host: ")
    port = raw_input("Port(default=80): ")
    ofile = raw_input("File(default=sample.txt): ")    
    
    if host: pass
    else: 
        print '\n* Enter the corret host and file name.'
        raw_input("Enter the exit.")
        sys.exit(1)
    if port: pass 
    else: port = '80'
    if ofile: pass
    else: ofile = 'sample.txt'
    
    intruder(host, port, ofile)
    sys.exit(0)

def main():
       
    parser = argparse.ArgumentParser('Commander')
    parser.add_argument("-a","--host", type=str, help="-a <target host>")
    parser.add_argument("-p","--port", type=str, help="-p <port number>", default='80')
    parser.add_argument("-f","--ofile", type=str, help="-f <text file>", default='sample.txt')
    
    args = parser.parse_args()
    if args.host is None or args.ofile is None:
        usage()
            
    host = args.host
    port = args.port
    ofile = args.ofile
    
    intruder(host, port, ofile)


if __name__ == '__main__':
    main()
    

