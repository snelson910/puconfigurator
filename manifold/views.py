from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from .models import Manifold, Manifoldconfig, Projects, Customers, Parts
from django.utils import timezone
import json, xlsxwriter, io
from collections import Counter

def manifold(request):
       if request.user.is_authenticated:       
              if request.method == 'POST':
                     accountnumber = request.POST['accountnumber']
                     project = Projects()
                     project.customer = accountnumber
                     project.created_on = timezone.now()
                     project.save()
                     projectid = project.pk
                     return render (request, 'manifoldselection.html', {"accountnumber" : accountnumber , "projectid" : projectid,})
              else:
                     return redirect('/')
       else:
             return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')

def stations(request):
       if request.user.is_authenticated:       
              if request.method == 'POST':
                     accountnumber = request.POST['accountnumber']
                     details = json.loads(request.POST['details'])
                     projectid = details["0"]
                     maninum = details["1"]
                     maninotes = request.POST['notes']
                     if maninotes != "Enter any notes here...":
                            notes = Projects.objects.get(pk=projectid)
                            notes.project_notes1 = maninotes
                            notes.save()
                     manifold = Manifold()
                     manifold.customer = accountnumber
                     manifold.part_number = maninum
                     manifold.quantity = 1
                     manifold.manifold_id = projectid 
                     manifold.save()
                     if "5" in details:
                            manifold = Manifold()
                            manifold.customer = accountnumber
                            manifold.part_number = details["5"]
                            manifold.quantity = 1
                            manifold.manifold_id = projectid 
                            manifold.save()

                     return render (request, 'stationbuild.html', {"accountnumber" : accountnumber, "details" : json.dumps(details),})
              else:
                     return redirect('/')
       else:
             return redirect('/')

def bom(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     data = json.loads(request.POST['stationconfiguration'])
                     details = json.loads(request.POST['details'])
                     search = json.loads(request.POST['search'])
                     parts = json.loads(request.POST['partnumbers'])
                     maninotes = request.POST['notes']
                     projectid = details["0"]
                     i = 0
                     k = 0
                     #Raw query the database to grab the best R9 number for each valve. Impossible to make perfect, but it'll get close
                     for x in search:
                            try:
                                   valvequery = "%" + search[k][0] + search[k][1] + "_X%" + search[k][2] + "%" + search[k][3] + "%"
                                   print(valvequery)
                                   valvenumber = Parts.objects.raw('SELECT * FROM parts WHERE product_name LIKE %s ORDER BY on_hand DESC, stockstatus DESC, cost_each', [valvequery])[0]
                                   print(valvenumber.item_number)
                                   parts.append(valvenumber.item_number)
                                   k += 1
                            except:
                                   Parts.DoesNotExist
                                   parts.append(data[k]["valveCode"])
                                   k += 1
                     if maninotes != "Enter any notes here...":
                            notes = Projects.objects.get(pk=projectid)
                            notes.project_notes2 = maninotes
                            notes.save()
                     for x in data:
                            station = Manifoldconfig()
                            station.manifold_id = projectid
                            station.station = (i + 1)
                            station.fc_ports = data[i]["floworient"]
                            station.fc_direct = data[i]["flowdirect"]
                            station.cb_ports = data[i]["cborient"]
                            station.red_ports = data[i]["redorient"]
                            station.po_ports = data[i]["poorient"]
                            station.rel_ports = data[i]["relorient"]
                            station.red_checks = data[i]["redchecks"]
                            station.save()                            
                            i += 1
                     j = 0
                     if details["4"] == "D03":
                            for x in data:
                                   boltlength = 0
                                   if data[j]["valveCode"] == "AD03COP" or data[j]["valveCode"] == "AD03CPP" or data[j]["valveCode"] == "DD03COP" or data[j]["valveCode"] == "DD03CPP":
                                          boltlength = 1.15
                                   else:
                                          boltlength = 2.00
                                   if data[j]["floworient"] == "On A Port" or data[j]["floworient"] == "On B Port":
                                          parts.append("NCCB-LCN")
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("GBA/S")     
                                          else:
                                                 parts.append("GBA")
                                   if data[j]["floworient"] == "On A and B Ports":
                                          parts.append("NCCB-LCN")
                                          parts.append("NCCB-LCN")
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("GBY/S")
                                          else:
                                                 parts.append("GBY")
                                   if data[j]["cborient"] == "On A Line" or data[j]["cborient"] == "On B Line":
                                          parts.append("CBCA-LHN")
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("EBA/S")
                                          else:
                                                 parts.append("EBA")
                                   if data[j]["cborient"] == "On A and B Ports":
                                          parts.append("CBCA-LHN")
                                          parts.append("CBCA-LHN")
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("EBY/S")
                                          else:
                                                 parts.append("EBY")
                                   if data[j]["poorient"] == "On A Line" or data[j]["poorient"] == "On B Line":
                                          parts.append("CKCB-XCN")
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("EBA/S")
                                          else:
                                                 parts.append("EBA")
                                   if data[j]["poorient"] == "On A and B Ports":
                                          parts.append("CXCB-XCN")
                                          parts.append("CXCB-XCN")
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("EBY/S")
                                          else:
                                                 parts.append("EBY")
                                   if data[j]["redorient"] == "On A Port" or data[j]["redorient"] == "On B Port":
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("EBA/S")
                                                 parts.append("PPDB-LCN")
                                          else:
                                                 parts.append("EBA")
                                                 parts.append("PPDB-LAN")
                                   if data[j]["redorient"] == "On A and B Ports":
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("EBY/S")
                                                 parts.append("PPDB-LCN")
                                                 parts.append("PPDB-LCN")
                                          else:
                                                 parts.append("EBY")
                                                 parts.append("PPDB-LAN")
                                                 parts.append("PPDB-LAN")
                                   if data[j]["redorient"] == "On P Line":
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("EBP/S")
                                                 parts.append("PPDB-LCN")
                                          else:
                                                 parts.append("EBP")
                                                 parts.append("PPDB-LAN")
                                   if data[j]["redchecks"] == "On A Port":
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("EB2/S")
                                                 parts.append("PPDB-LCN")
                                          else:
                                                 parts.append("EB2")
                                                 parts.append("PPDB-LAN")
                                   if data[j]["redchecks"] == "On B Port":
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("EB3/S")
                                                 parts.append("PPDB-LCN")
                                          else:
                                                 parts.append("EB3")
                                                 parts.append("PPDB-LAN")
                                   if data[j]["redchecks"] == "On A and B Port":
                                          boltlength += 3.40
                                          if details["3"] == "D":
                                                 parts.append("EB3/S")
                                                 parts.append("PPDB-LCN")
                                                 parts.append("EB2/S")
                                                 parts.append("PPDB-LCN")
                                          else:
                                                 parts.append("EB3")
                                                 parts.append("PPDB-LAN")
                                                 parts.append("EB2")
                                                 parts.append("PPDB-LAN")
                                   if data[j]["relorient"] == "On P Line":
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("FBP/S")
                                                 parts.append("RDDA-LCN")
                                          else:
                                                 parts.append("FBP")
                                                 parts.append("RDDA-LAN")
                                   if data[j]["relorient"] == "On A Line" or data[j]["relorient"] == "On B Line":
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("FBA/S")
                                                 parts.append("RDDA-LCN")
                                          else:
                                                 parts.append("FBA")
                                                 parts.append("RDDA-LAN")
                                   if data[j]["relorient"] == "A to B, B to A":
                                          boltlength += 1.70
                                          if details["3"] == "D":
                                                 parts.append("FBY/S")
                                                 parts.append("RDDA-LCN")
                                                 parts.append("RDDA-LCN")
                                          else:
                                                 parts.append("FBY")
                                                 parts.append("RDDA-LAN")
                                                 parts.append("RDDA-LAN")
                                   if boltlength == 1.15:
                                          pass
                                   elif boltlength == 2.0:
                                          parts.append("R978833365")
                                   elif boltlength < 3.0:
                                          parts.append("J-301")
                                   elif boltlength < 3.75:
                                          parts.append("J-302")
                                   elif boltlength < 4.75:
                                          parts.append("J-303")
                                   elif boltlength < 5.5:
                                          parts.append("J-343")
                                   elif boltlength < 7.15:
                                          parts.append("992-011")
                                   else:
                                          parts.append("992-012")
                                   j += 1
                     if details["4"] == "D05":
                            for x in data:
                                   boltlength = 0
                                   if data[j]["valveCode"] == "AD05CPP" or data[j]["valveCode"] == "DD05CPP":
                                          boltlength = 1.25
                                   elif data[j]["valveCode"] == "AD05COP" or data[j]["valveCode"] == "DD05COP":
                                          boltlength = 2.00
                                   else:
                                          boltlength = 1.75
                                   if data[j]["floworient"] == "On A Port":
                                          parts.append("NCEB-LCN")
                                          boltlength += 1.94
                                          if data[j]["flowdirect"] == "Meter In":
                                                 if details["3"] == "D":
                                                        parts.append("DBB/S")                                              
                                                 else:
                                                        parts.append("DBB")
                                          else:
                                                 if details["3"] == "D":
                                                        parts.append("DBA/S")                                              
                                                 else:
                                                        parts.append("DBA")
                                   if data[j]["floworient"] == "On B Port":
                                          parts.append("NCEB-LCN")
                                          boltlength += 1.94
                                          if data[j]["flowdirect"] == "Meter In":
                                                 if details["3"] == "D":
                                                        parts.append("DBA/S")                                              
                                                 else:
                                                        parts.append("DBA")
                                          else:
                                                 if details["3"] == "D":
                                                        parts.append("DBB/S")                                              
                                                 else:
                                                        parts.append("DBB")
                                   if data[j]["floworient"] == "On A and B Ports":
                                          parts.append("NCEB-LCN")
                                          parts.append("NCEB-LCN")
                                          boltlength += 1.94
                                          if details["3"] == "D":
                                                 parts.append("DBY/S")
                                          else:
                                                 parts.append("DBY")
                                   if data[j]["cborient"] == "On A Line":
                                          boltlength += 1.94
                                          parts.append("CBEA-LHN")
                                          if details["3"] == "D":
                                                 parts.append("BBA/S")
                                          else:
                                                 parts.append("BBA")
                                   if data[j]["cborient"] == "On B Line":
                                          boltlength += 1.94
                                          parts.append("CBEA-LHN")
                                          if details["3"] == "D":
                                                 parts.append("BBB/S")
                                          else:
                                                 parts.append("BBB")
                                   if data[j]["cborient"] == "On A and B Ports":
                                          boltlength += 1.94
                                          parts.append("CBEA-LHN")
                                          parts.append("CBEA-LHN")
                                          if details["3"] == "D":
                                                 parts.append("BBY/S")
                                          else:
                                                 parts.append("BBY")
                                   if data[j]["poorient"] == "On A Port":
                                          boltlength += 1.94
                                          parts.append("CKEB-XCN")
                                          if details["3"] == "D":
                                                 parts.append("BBA/S")
                                          else:
                                                 parts.append("BBA")
                                   if data[j]["poorient"] == "On B Port":
                                          boltlength += 1.94
                                          parts.append("CKEB-XCN")
                                          if details["3"] == "D":
                                                 parts.append("BBB/S")
                                          else:
                                                 parts.append("BBB")
                                   if data[j]["poorient"] == "On A and B Ports":
                                          boltlength += 1.94
                                          parts.append("CKEB-XCN")
                                          parts.append("CKEB-XCN")
                                          if details["3"] == "D":
                                                 parts.append("BBY/S")
                                          else:
                                                 parts.append("BBY")
                                   if data[j]["redorient"] == "On A Port":
                                          boltlength += 1.94
                                          if details["3"] == "D":
                                                 parts.append("BBA/S")
                                                 parts.append("PPFB-LCN")
                                          else:
                                                 parts.append("BBA")
                                                 parts.append("PPFB-LAN")
                                   if data[j]["redorient"] == "On B Port":
                                          boltlength += 1.94
                                          if details["3"] == "D":
                                                 parts.append("BBB/S")
                                                 parts.append("PPFB-LCN")
                                          else:
                                                 parts.append("BBB")
                                                 parts.append("PPFB-LAN")
                                   if data[j]["redorient"] == "On A and B Ports":
                                          boltlength += 1.94
                                          if details["3"] == "D":
                                                 parts.append("BBY/S")
                                                 parts.append("PPFB-LCN")
                                                 parts.append("PPFB-LCN")
                                          else:
                                                 parts.append("BBY")
                                                 parts.append("PPFB-LAN")
                                                 parts.append("PPFB-LAN")
                                   if data[j]["redorient"] == "On P Line":
                                          boltlength += 2.44
                                          if details["3"] == "D":
                                                 parts.append("BBP/S")
                                                 parts.append("PPFB-LCN")
                                          else:
                                                 parts.append("BBP")
                                                 parts.append("PPFB-LAN")
                                   if data[j]["redchecks"] == "On A Port":
                                          boltlength += 2.44
                                          if details["3"] == "D":
                                                 parts.append("BB2/S")
                                                 parts.append("PPFB-LCN")
                                          else:
                                                 parts.append("BB2")
                                                 parts.append("PPFB-LAN")
                                   if data[j]["redchecks"] == "On B Port":
                                          boltlength += 2.44
                                          if details["3"] == "D":
                                                 parts.append("BB3/S")
                                                 parts.append("PPFB-LCN")
                                          else:
                                                 parts.append("BB3")
                                                 parts.append("PPFB-LAN")
                                   if data[j]["redchecks"] == "On A and B Port":
                                          boltlength += 4.88
                                          if details["3"] == "D":
                                                 parts.append("BB3/S")
                                                 parts.append("PPDB-LCN")
                                                 parts.append("BB2/S")
                                                 parts.append("PPDB-LCN")
                                          else:
                                                 parts.append("BB3")
                                                 parts.append("PPDB-LAN")
                                                 parts.append("BB2")
                                                 parts.append("PPDB-LAN")
                                   if data[j]["relorient"] == "On P Line":
                                          boltlength += 1.94
                                          if details["3"] == "D":
                                                 parts.append("CBP/S")
                                                 parts.append("RDFA-LCN")
                                          else:
                                                 parts.append("CBP")
                                                 parts.append("RDFA-LAN")
                                   if data[j]["relorient"] == "On A Line":
                                          boltlength += 1.94
                                          if details["3"] == "D":
                                                 parts.append("CBA/S")
                                                 parts.append("RDFA-LCN")
                                          else:
                                                 parts.append("CBA")
                                                 parts.append("RDFA-LAN")
                                   if data[j]["relorient"] == "On B Line":
                                          boltlength += 1.94
                                          if details["3"] == "D":
                                                 parts.append("CBB/S")
                                                 parts.append("RDFA-LCN")
                                          else:
                                                 parts.append("CBB")
                                                 parts.append("RDFA-LAN")
                                   if data[j]["relorient"] == "A to B, B to A":
                                          boltlength += 2.44
                                          if details["3"] == "D":
                                                 parts.append("CBY/S")
                                                 parts.append("RDFA-LCN")
                                                 parts.append("RDFA-LCN")
                                          else:
                                                 parts.append("CBY")
                                                 parts.append("RDFA-LAN")
                                                 parts.append("RDFA-LAN")
                                   if boltlength == 1.25:
                                          pass
                                   elif boltlength == 1.75:
                                          parts.append("B-96")
                                   elif boltlength == 2.0:
                                          pass
                                   elif boltlength < 3.25:
                                          parts.append("90044A526")
                                   elif boltlength < 3.75:
                                          parts.append("90044A527")
                                   elif boltlength < 4.25:
                                          parts.append("91251A559")
                                   elif boltlength < 4.5:
                                          parts.append("J-309")
                                   elif boltlength < 7.00:
                                          parts.append("992-001")
                                   else:
                                          parts.append("992-002")
                                   j += 1
                     if details["4"] == "D08":
                            for x in data:
                                   boltlength = 0
                                   if data[j]["valveCode"] == "AD08CPP" or data[j]["valveCode"] == "DD08CPP":
                                          boltlength = 1.00
                                   elif data[j]["valveCode"] == "AD08COP" or data[j]["valveCode"] == "DD08COP":
                                          boltlength = 3.50
                                   else:
                                          boltlength = 2.50
                                   if data[j]["floworient"] == "On A Port":
                                          boltlength += 3.44
                                          parts.append("NCGB-LCN")
                                          if data[j]["flowdirect"] == "Meter In":
                                                 if details["3"] == "D":
                                                        parts.append("IBC/S")                                              
                                                 else:
                                                        parts.append("IBC")
                                          else:
                                                 if details["3"] == "D":
                                                        parts.append("IBA/S")                                              
                                                 else:
                                                        parts.append("IBA")
                                   if data[j]["floworient"] == "On B Port":
                                          boltlength += 3.44
                                          parts.append("NCGB-LCN")
                                          if data[j]["flowdirect"] == "Meter In":
                                                 if details["3"] == "D":
                                                        parts.append("IBD/S")                                              
                                                 else:
                                                        parts.append("IBD")
                                          else:
                                                 if details["3"] == "D":
                                                        parts.append("IBB/S")                                              
                                                 else:
                                                        parts.append("IBB")
                                   if data[j]["floworient"] == "On A and B Ports":
                                          boltlength += 3.44
                                          parts.append("NCGB-LCN")
                                          parts.append("NCGB-LCN")
                                          if data[j]["flowdirect"] == "Meter In":
                                                 if details["3"] == "D":
                                                        parts.append("IBZ/S")
                                                 else:
                                                        parts.append("IBZ")
                                          else:
                                                 if details["3"] == "D":
                                                        parts.append("IBY/S")
                                                 else:
                                                        parts.append("IBY")
                                   if data[j]["cborient"] == "On A Line":
                                          boltlength += 3.44
                                          parts.append("CBIA-LHN")
                                          if details["3"] == "D":
                                                 parts.append("HBA/S")
                                          else:
                                                 parts.append("HBA")
                                   if data[j]["cborient"] == "On B Line":
                                          boltlength += 3.44
                                          parts.append("CBIA-LHN")
                                          if details["3"] == "D":
                                                 parts.append("HBB/S")
                                          else:
                                                 parts.append("HBB")
                                   if data[j]["cborient"] == "On A and B Ports":
                                          boltlength += 3.44
                                          parts.append("CBIA-LHN")
                                          parts.append("CBIA-LHN")
                                          if details["3"] == "D":
                                                 parts.append("HBY/S")
                                          else:
                                                 parts.append("HBY")
                                   if data[j]["poorient"] == "On A Port":
                                          boltlength += 3.44
                                          parts.append("CKIB-XCN")
                                          if details["3"] == "D":
                                                 parts.append("HBA/S")
                                          else:
                                                 parts.append("HBA")
                                   if data[j]["poorient"] == "On B Port":
                                          boltlength += 3.44
                                          parts.append("CKIB-XCN")
                                          if details["3"] == "D":
                                                 parts.append("HBB/S")
                                          else:
                                                 parts.append("HBB")
                                   if data[j]["poorient"] == "On A and B Ports":
                                          boltlength += 3.44
                                          parts.append("CKIB-XCN")
                                          parts.append("CKIB-XCN")
                                          if details["3"] == "D":
                                                 parts.append("HBY/S")
                                          else:
                                                 parts.append("HBY")
                                   if data[j]["redorient"] == "On A Port":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("HBA/S")
                                                 parts.append("PPJB-LCN")
                                          else:
                                                 parts.append("HBA")
                                                 parts.append("PPJB-LAN")
                                   if data[j]["redorient"] == "On B Port":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("HBB/S")
                                                 parts.append("PPJB-LCN")
                                          else:
                                                 parts.append("HBB")
                                                 parts.append("PPJB-LAN")
                                   if data[j]["redorient"] == "On A and B Ports":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("HBY/S")
                                                 parts.append("PPJB-LCN")
                                                 parts.append("PPJB-LCN")
                                          else:
                                                 parts.append("HBY")
                                                 parts.append("PPJB-LAN")
                                                 parts.append("PPJB-LAN")
                                   if data[j]["redorient"] == "On P Line":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("HBO/S")
                                                 parts.append("PPJB-LCN")
                                          else:
                                                 parts.append("HBO")
                                                 parts.append("PPJB-LAN")
                                   if data[j]["redchecks"] == "On A Port":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("KB2/S")
                                                 parts.append("PPJB-LCN")
                                          else:
                                                 parts.append("KB2")
                                                 parts.append("PPJB-LAN")
                                   if data[j]["redchecks"] == "On B Port":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("KB3/S")
                                                 parts.append("PPJB-LCN")
                                          else:
                                                 parts.append("KB3")
                                                 parts.append("PPJB-LAN")
                                   if data[j]["redchecks"] == "On A and B Port":
                                          boltlength += 6.88
                                          if details["3"] == "D":
                                                 parts.append("KB3/S")
                                                 parts.append("PPJB-LCN")
                                                 parts.append("KB2/S")
                                                 parts.append("PPJB-LCN")
                                          else:
                                                 parts.append("KB3")
                                                 parts.append("PPJB-LAN")
                                                 parts.append("KB2")
                                                 parts.append("PPJB-LAN")
                                   if data[j]["relorient"] == "On P Line":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("CDO/S")
                                                 parts.append("RDHA-LCN")
                                          else:
                                                 parts.append("CDO")
                                                 parts.append("RDHA-LAN")
                                   if data[j]["relorient"] == "On A Line":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("CDC/S")
                                                 parts.append("RDHA-LCN")
                                          else:
                                                 parts.append("CDC")
                                                 parts.append("RDHA-LAN")
                                   if data[j]["relorient"] == "On B Line":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("CDD/S")
                                                 parts.append("RDHA-LCN")
                                          else:
                                                 parts.append("CDD")
                                                 parts.append("RDHA-LAN")
                                   if data[j]["relorient"] == "A to B, B to A":
                                          boltlength += 3.44
                                          if details["3"] == "D":
                                                 parts.append("CDW/S")
                                                 parts.append("RDHA-LCN")
                                                 parts.append("RDHA-LCN")
                                          else:
                                                 parts.append("CDW")
                                                 parts.append("RDHA-LAN")
                                                 parts.append("RDHA-LAN")
                                   if boltlength == 1.00:
                                          pass
                                   elif boltlength == 2.50:
                                          parts.append("91251A722")
                                   elif boltlength == 3.50:
                                          pass
                                   elif boltlength < 4.5:
                                          parts.append("91251A730")
                                   elif boltlength < 6:
                                          parts.append("91251A736")
                                          parts.append("91251A736")
                                          parts.append("91251A736")
                                          parts.append("91251A736")
                                          parts.append("91251A736")
                                          parts.append("91251A736")
                                   elif boltlength < 8:
                                          parts.append("91251A740")
                                          parts.append("91251A740")
                                          parts.append("91251A740")
                                          parts.append("91251A740")
                                          parts.append("91251A740")
                                          parts.append("91251A740")
                                   elif boltlength < 9.5:
                                          parts.append("90044A436")
                                          parts.append("90044A436")
                                          parts.append("90044A436")
                                          parts.append("90044A436")
                                          parts.append("90044A436")
                                          parts.append("90044A436")
                                   else:
                                          parts.append("90322A159")
                                          parts.append("92066a033")
                                          parts.append("92066a033")
                                          parts.append("92066a033")
                                          parts.append("92066a033")
                                          parts.append("92066a033")
                                          parts.append("92066a033")
                                   j += 1             
                     count = Counter(parts)
                     make = list(count)
                     l = 0
                     #for x in count:
                     #       part = Manifold()
                     #       part.part_number = make[l]
                     #       part.quantity = count[make[l]]
                     #       part.manifold_id = projectid 
                     #       part.save()
                     #       l += 1
                     parts.append(details['1'])
                     if '5' in details:
                            parts.append(details['5'])
                     return render(request, 'bom.html', {"valveData" : json.dumps(data), "details" : json.dumps(details), "partnumbers" : json.dumps(parts), "search" : json.dumps(search),})
              else:
                     return redirect('/')
       else:
             return redirect('/')

def download(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     output = io.BytesIO()
                     partnumbers = json.loads(request.POST['partnumbers'])
                     details = json.loads(request.POST['details'])
                     configurations = json.loads(request.POST['valveData'])
                     workbook = xlsxwriter.Workbook(output)
                     partslist = workbook.add_worksheet('Parts')
                     config = workbook.add_worksheet('Configurations')
                     bold = workbook.add_format({'bold': True})
                     money = workbook.add_format({'num_format': '$#,##0.00'})
                     percent = workbook.add_format({'num_format':'0%'})
                     projectid = details['0']
                     project = Projects.objects.get(pk=projectid)
                     if project.project_notes1 != "" and project.project_notes2 != "":
                            notes = workbook.add_worksheet('Notes')
                            notes.write('A1', project.project_notes1)
                            notes.write('A2', project.project_notes2)
                     customer = project.customer
                     customers = Customers.objects.get(customer_account=customer)
                     count = Counter(partnumbers)
                     make = list(count)
                     l = 0
                     row = 3
                     partslist.write('A1','Customer: ' + customer, bold)
                     partslist.write('B1','Project ID: ' + projectid, bold)
                     partslist.write('C1',customers.sales_group, bold)
                     partslist.write('A2',customers.address)
                     partslist.write('B2',customers.customer_account)
                     partslist.write('A3','Item',bold)
                     partslist.write('B3','Part Name',bold)
                     partslist.write('C3','Quantity',bold)
                     partslist.write('D3','Cost',bold)
                     partslist.write('E3','Stock',bold)
                     for x in (count):
                            partslist.write(row,0,make[l])
                            partslist.write(row,2,count[make[l]])
                            try:
                                   part = Parts.objects.get(item_number=make[l])
                                   partslist.write(row,1,part.product_name)
                                   partslist.write(row,3,part.cost_each, money)
                                   partslist.write(row,4, part.on_hand)
                                   row += 1
                                   l += 1
                            except:
                                   partslist.write(row,1,make[l])
                                   partslist.write(row,3,'0.00', money)
                                   partslist.write(row,4, '0')
                                   row += 1
                                   l += 1
                     row += 1
                     partslist.write(row, 2, 'Total Cost:')
                     partslist.write(row, 3, '=SUM(D4:D' + str(row) + ')', money)
                     partslist.write(row+1, 2, 'Mark Up (%):')
                     partslist.write(row+1, 3, '.40',percent)
                     partslist.write(row+2, 2, 'Sell Price:')
                     partslist.write(row+2, 3, '=D' + str(row+1) + '/(1-D' + str(row + 2) + ')',money)
                     config.write('A1', 'Station',bold)
                     config.write('B1', 'Valve',bold)
                     config.write('C1', 'Flow Ports',bold)
                     config.write('D1', 'Flow Direction',bold)
                     config.write('E1', 'Counterbalance Ports',bold)
                     config.write('F1', 'PO Check Ports',bold)
                     config.write('G1', 'Reducing Ports',bold)
                     config.write('H1', 'Reducing Checks',bold)
                     config.write('I1', 'Relieving Ports',bold)
                     l = 0
                     row = 1
                     col = 0
                     for x in (configurations):
                            config.write(row, col, row)
                            config.write(row, col+1, configurations[l]["valveCode"])
                            config.write(row, col+2, configurations[l]["floworient"])
                            config.write(row, col+3, configurations[l]["flowdirect"])
                            config.write(row, col+4, configurations[l]["cborient"])
                            config.write(row, col+5, configurations[l]["poorient"])
                            config.write(row, col+6, configurations[l]["redorient"])
                            config.write(row, col+7, configurations[l]["redchecks"])
                            config.write(row, col+8, configurations[l]["relorient"])
                            l += 1
                            row += 1
                     workbook.close()
                     output.seek(0)
                     filename = 'Parts-Project' + projectid +  '.xlsx'
                     response = HttpResponse(
                            output,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                     )
                     response['Content-Disposition'] = 'attachment; filename=%s' % filename
                     output.close()
                     return response
              else:
                     return redirect('/')
       else:
              return redirect('/')
