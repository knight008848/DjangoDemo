############################################################################
# Copyright (C) 2015 Pegatron Corp.
#
# NAME        : GTA.py
#
# DESCRIPTION : Sync BTOA contents to all line servers.
# INPUT:   None
# 
#
# CHANGE ACTIVITY:
#  Jul 10 2015 Vincent - Initial release
#  Jul 14 2015 Vincent - Modify the time spec.
#  Jul 16 2015 Vincent - release alpha version.
#  Jul 17 2015 Vincent - release beta version.
#  Oct 23 2015 Vincent - Support IOT OSes
#  Nov 03 2015 Vincent - Support argv and fix a timestamp issue.
#  Dec 23 2015 Vincent - Support NKX OS.
#  Mar 17 2016 Vincent - Change get method of OSV
#  
############################################################################
import os, sys, shutil
import os.path
import time, datetime
import filecmp
import re
import mysql.connector as dbapi

sys.path.append(r'D:\GCFstore\batch')

import fppapi

N = 2

config = { 'host' : '127.0.0.1',
           'user' : 'test',
           'password': 'ev-2015',
           'port': '3306',
           'database': 'platform',
           'charset': 'utf8'
           }

OS_mapping = {'W72':1, 'W74':1, 'W82':2, 'W84':2, 'WB2':3, 'WB4':3,'UBX':4, 'NKX':4, 'WT2':5, 'WT4':5, 'APL':6}

# def timer(n):
#     while True:
#         print "Task starting on %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#         FIOD()
#         BTOA()
#         print "\n\n######End########\n"
#         time.sleep(n)
#         print "\n\n######Start########\n"

def getOSP(xmlfile):
 
    srv = ''

    doc = fppapi.getSDRfromGCF(xmlfile)

    for line in doc.split('\n'):

        if re.search('SI SW', line) != None and re.search('2T613', line) == None:
            srv = line.split( )[2]
            break

    assert len(srv) > 0
    return srv

def getOSD(xmlfile):
   
    srv = ''

    doc = fppapi.getSDRfromGCF(xmlfile)

    for line in doc.split('\n'):

        if re.search('SI SW', line) != None and re.search('2T613', line) == None:
            srv = line[12:]
            break

    assert len(srv) > 0
    return srv

def GCF2SQL(xmlfile):

    region = fppapi.getRegionfromGCF(xmlfile)
    level = fppapi.getLevelfromGCF(xmlfile)
    cto = fppapi.getCTOfromGCF(xmlfile)
    des = fppapi.getDstfromGCF(xmlfile)
    model = fppapi.getProductfromGCF(xmlfile)
    family = fppapi.getModelfromGCF(xmlfile)
    sia = fppapi.getSIaccountfromGCF(xmlfile)
    osp = getOSP(xmlfile)
    osd = getOSD(xmlfile)
    po = fppapi.getPOfromGCF(xmlfile)

    file_time = os.path.getmtime(xmlfile)
    timestamp = time.localtime(file_time)
    month1 = time.strftime('%Y%m', timestamp)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)

    newfile = xmlfile.replace('process', 'backup'+ os.sep + month1)

    mod = fppapi.getMODfromGCF(xmlfile)
    sdr = fppapi.getSDRfromGCF(xmlfile)

    for text in sdr.split('\n'): 
        if text.find('odm_package ') != -1:
            osv = text.split()[3].upper() 

    if sia == '':
        cfiflag = False
    else:
        cfiflag = True

    if fppapi.hasSRV('J471G', xmlfile):
        muiflag = True
    else:
        muiflag = False

    # record a gcf note and insert it into database
    cmd = ("insert into `gtaman_gcfnote`" + \
        " (`po`, `timestamp`, `model`, `family`, `level`, `region`, `ctomod`," + \
        " `destination`, `OSP`, `OSD`, `OSV`, `siaccount`, `mod`, `sdr`, `filepath`, `cfiflag`, `muiflag`)" + \
        " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',  '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d'); " % \
    (po, timestamp, model, family, level, region, cto, des, osp, osd, osv, sia, mod, sdr, newfile.replace("\\", "\\\\") \
        ,cfiflag, muiflag))
    # print cmd    

    return cmd

def timer(n):
    while True:
        if int(time.time() % n) == 0:
            time.sleep(120)
            try:
                # Note GCF to database
                GCF_Note()
            except Exception, e:
                print e
            print "\n\n######End########\n"           

def GCF_Gather():
    # Populate local file path
    source_path = os.path.join(r"\\172.24.57.4\gcf_arc")
    storage_path = os.path.join(r"D:\GCFstore\process")
    abandon_path = os.path.join(r"D:\GCFstore\abandon")
    log_path = os.path.join(r"D:\GCFstore\batch\LOG")

    current_time = time.time()
    start = time.time()

    t = time.localtime(current_time)
    date1 = time.strftime('%Y%m%d', t)
    time1 = time.strftime('%Y-%m-%d %H:%M:%S', t)
    month1 = time.strftime('%Y%m', t)

    traTimeA = time.strftime('%H:%M:%S', time.localtime(current_time - 7500))
    traTimeB = time.strftime('%H:%M:%S', time.localtime(current_time - 301))
    
    if os.path.isdir(log_path):        
        #print date1, time1
        logname = 'GTAlog' + date1 + '.txt'
        logfile = os.path.join(log_path, logname)
        
        fout = open(logfile, 'a')
        
        fout.write('\n\n***********************************\n\n')
        fout.write('GCF timestamp checking start on %s.\n' % time1)

    print "Task starting on %s" % time1

    num = 0
    if os.path.isdir(source_path) and os.path.isdir(storage_path):
        print "File link passed!"
        for file in os.listdir(source_path):
            PO = file[:-8]
            po_pattern = re.compile('^[_0-9]',re.IGNORECASE)
            if po_pattern.search(file):
                file_path = os.path.join(source_path, file)
                if os.path.isfile(file_path):
                    file_time = os.path.getmtime(file_path)
                    diff_time = int(current_time - file_time)
                    # Catch from 00:00:00 ~ 01:59:59 (2 hours)
                    if diff_time in range(301, (N * 3600 + 301)):
                        t = time.localtime(file_time)
                        t1 = time.strftime('%Y-%m-%d %H:%M:%S', t)
                        try:
                            shutil.copy2(file_path, storage_path + os.sep + file)
                            # fout.write('%15s - %s\n' % (PO, t1))
                            # print('%15s - %s\n' % (PO, t1))
                            num += 1
                        except Exception, e:
                            print e
            else:
                file_path = os.path.join(source_path, file)
                try:
                    shutil.copy2(file_path, abandon_path + os.sep + file)
                except Exception, e:
                        print e

    fout.write('Total find %d files in %s ~ %s!' % (num, traTimeA, traTimeB))

    if fout != None:
        fout.close()

    finish = time.time()
    print('\n***********************************\n')
    print "Collect gcf completed in %ds. " % (finish - start)
    print('\n***********************************\n')      

def GCF_Note():
    # Populate local file path
    source_path = os.path.join(r"D:\GCFstore\process")
    storage_path = os.path.join(r"D:\GCFstore\backup")
    error_path = os.path.join(r"D:\GCFstore\errorhandle")
    log_path = os.path.join(r"D:\GCFstore\batch\LOG")

    current_time = time.time()
    start = time.time()

    t = time.localtime(current_time)
    date1 = time.strftime('%Y%m%d', t)
    time1 = time.strftime('%Y-%m-%d %H:%M:%S', t)
    # month1 = time.strftime('%Y%m', t)
    
    if os.path.isdir(log_path):        
        #print date1, time1
        logname = 'GTAlog' + date1 + '.txt'
        logfile = os.path.join(log_path, logname)
        
        fout = open(logfile, 'a')

    fout.write('\nGCF               Time                  Result')
    fout.write('\n***************   *******************   *******\n\n')

    print "Task starting on %s" % time1

    connection = dbapi.connect(**config)
    cursor = connection.cursor()

    num = 0
    if os.path.isdir(source_path) and os.path.isdir(storage_path):
        print "File link passed!"
        for file in os.listdir(source_path):
            result = 'Initial'
            po = file[:-8]
            xmlfile = os.path.join(source_path, file)
            if os.path.isfile(xmlfile):

                file_time = os.path.getmtime(xmlfile)
                timestamp = time.localtime(file_time)
                month1 = time.strftime('%Y%m', timestamp)
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
                
                try:
                    cmd = GCF2SQL(xmlfile)
                    cursor.execute(cmd)
                    connection.commit()

                    new_path = storage_path + os.sep + month1
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)
                    newfile = os.path.join(new_path, file)

                    shutil.copy2(xmlfile, newfile)
                    os.remove(xmlfile)
                    result = 'Passed'
                    num += 1
                except Exception, e:
                    print e
                    shutil.copy2(xmlfile, error_path + os.sep + file)
                    os.remove(xmlfile)
                    result = 'Failed: ' + str(e)

            fout.write('%15s - %s - %s\n' % (po, timestamp, result))

    fout.write('Total note %d files into database!' % num)

    connection.close()

    if fout != None:
        fout.write('\nGCF timestamp checking finished.\n')
        fout.close()

    finish = time.time()
    print('\n***********************************\n')
    print "Note gcf completed in %ds. " % (finish - start)
    print('\n***********************************\n')  

def main(argv):
    if len(argv) == 2 and argv[1] in ('-s', '-S'):
        GCF_Note()
    else:
        n = N * 3600
        timer(n)        

if __name__ == "__main__":
    main(sys.argv)


    