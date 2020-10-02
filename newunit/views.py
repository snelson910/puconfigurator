from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import HPForm, PumpForm, FrameForm, ReservoirForm
from django.forms import inlineformset_factory, formset_factory
from .models import Motors, Pumpcodes, BellHousingSizes, CouplingCodes, Reservoir, Throughdrives
from manifold.models import Parts
from django.http import HttpResponse, JsonResponse
import json, math
from django.db import connection

def newunit(request):
       if request.user.is_authenticated:       
              if request.method == 'POST':
                     return render (request, 'powerunit/pumpmanual.html')
              else:
                     return redirect('/')
       else:
             return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')

def pumpwizard(request):
       if request.user.is_authenticated:
              return render(request, "powerunit/pumpwizard.html")
       else:
              return redirect('/')

def manual(request):
       if request.user.is_authenticated:
                     return render(request, "powerunit/pumpmanual.html")
       else:
              return redirect('/')

def coupling(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     pump = request.POST['pump']
                     tick = 0
                     try:
                            volts = request.POST['voltage']
                            num = request.POST["horsepower"]
                            a = str(volts)
                     except:
                            motor = request.POST['motor']
                            tick = 1
                     #Grab the motor from the horsepower and voltage provided. I don't have a fail safe on this, because the HTML
                     #should stop the user from picking impossible motors, but it can happen. Worry about this later.
                     #The only failure is that the AJAX does not get a response.
                     try:
                            mot = Motors.objects.get(voltage = a, hp = num)
                     except:
                            mot = Motors.objects.get(motor_number = motor)
                     frame = mot.frame_size
                     motshaft = mot.shaft_length
                     motcoup = mot.coupling_code
                     #Grab the selected pump as an object.
                     pum = Pumpcodes.objects.get(pump = pump)
                     pumframe = pum.pump_flange
                     pumshaft = pum.pump_shaft_length
                     pumcoup = pum.pump_coupling_code
                     #Add a bit of wiggle room for the shafts so that the minimum S_S distance is .15 inches. 
                     facelen = motshaft + pumshaft + .15
                     bells = BellHousingSizes.objects.order_by('face_to_face').filter(end_style = pumframe, frame_size__contains = frame)
                     i = 0
                     l = 0
                     bellnum = ""
                     finalsize = ""
                     #Check if there were any bell housings selected and make a determination on if a custom housing needs to be made
                     if len(bells)== 0:
                            custbell = BellHousingSizes.objects.get(frame_size__contains = frame, part_number__startswith = 'S')
                            #Round to nearest quarter inch.
                            length = math.ceil((facelen + .10)*4)/4
                            #Bellhousing number concatenation
                            bellnum = custbell.part_number + str(length*100)[:-3] + '2' + pumframe
                            #Set variable values for steel bellhousing
                            pref = custbell.coupling_size_pref
                            maxsize = custbell.max_coupling_size
                            #Calculate shaft to shaft distance and spit it out as a string for passing  
                            l = str(round(length - facelen + .15, 2))
                     else:
                            for x in bells:
                                   #Loop through the ordered bell housings and select the first one that is longer than the combined shafts
                                   if bells[i].face_to_face > facelen:
                                          l = str(round(bells[i].face_to_face - facelen + .15, 2))
                                          bellnum = bells[i].part_number
                                          pref = bells[i].coupling_size_pref
                                          maxsize = bells[i].max_coupling_size
                                          break                                  
                                   i += 1
                            #If the longest bellhousing is not long enough, build one using the concatenator 3000       
                            if bellnum == "":
                                   custbell = BellHousingSizes.objects.get(frame_size__contains = frame, part_number__startswith = 'S')
                                   length = math.ceil((facelen + .10)*4)/4
                                   bellnum = custbell.part_number + str(length*100)[:-3] + '2' + pumframe
                                   pref = custbell.coupling_size_pref
                                   maxsize = custbell.max_coupling_size
                                   l = str(round(length - facelen + .15, 2))
                     #Check if the coupling codes exist in the preferred size
                     if CouplingCodes.objects.filter(code = str(motcoup), sizes__contains = pref):
                            motorcoupling = "M" + str(pref) + str(motcoup)
                            finalsize = pref
                     else:
                            motorcoupling = ""
                     if CouplingCodes.objects.filter(code = str(pumcoup), sizes__contains = pref):
                            pumpcoupling = "M" + str(pref) + str(pumcoup)
                     else:
                            pumpcoupling = ""
                     #If the coupling codes do not exist, grab the largest coupling size that will fit in the housing and begin checking through
                     #downward increments
                     if motorcoupling == "" or pumpcoupling == "":
                            size = maxsize
                            while motorcoupling == "" or pumpcoupling == "":
                                   if CouplingCodes.objects.filter(code = str(motcoup), sizes__contains = size):
                                          motorcoupling = "M" + str(size) + str(motcoup)
                                          finalsize = size
                                   else:
                                          motorcoupling = ""
                                   if CouplingCodes.objects.filter(code = str(pumcoup), sizes__contains = size):
                                          pumpcoupling = "M" + str(size) + str(pumcoup)
                                          finalsize = size
                                   else:
                                          pumpcoupling = ""
                                   size = size-100
                                   #If all coupling sizes have been cycled though and no good pair has been made, build the 
                                   #coupling code with the preferred size and note that it needs to be custom made
                                   if size == 0:
                                          motorcoupling = "Custom coupling required: M" + str(pref) + str(motcoup)
                                          pumpcoupling = "Custom coupling required: M" + str(pref) + str(pumcoup)
                                          finalsize = pref
                     #Drop the data in a JSON to pass to the AJAX response
                     finalsizestr = str(finalsize)
                     if finalsizestr[0] == 1 or finalsizestr[0] == 2:
                            insert = 'M' + finalsizestr[0] + '70H5RC'
                     else:
                            insert = 'M' + finalsizestr[0] + '70H5'
                     arr = [bellnum, motorcoupling, pumpcoupling, insert]
                     j = 0
                     parts = []
                     for x in arr:
                            try:
                                   data = Parts.objects.get(item_number = arr[j])
                                   parts.append([data.item_number, data.product_name, data.on_hand, data.cost_each, data.stockstatus, data.goto_item])
                            except:
                                   parts.append([arr[j],"Custom part required","","0.00","","No"])
                            j += 1
                     jsondata = json.dumps(parts)
                     return HttpResponse(jsondata, content_type="application/json")  
              else:
                     return redirect('/')       
       else:
              return redirect('/')

def pumps(request):
       if request.user.is_authenticated:
              return render(request, "powerunit/pumps.html")
       else:
              return redirect('/')

def reservoirs(request):
       if request.user.is_authenticated:
              reservoirsall = Reservoir.objects.all().order_by('reservoir_size', 'reservoir_configuration')
              reservoirselect = []
              i = 0
              for x in reservoirsall:
                     reservoirselect.append([reservoirsall[i].reservoir_size, reservoirsall[i].reservoir_configuration, reservoirsall[i].part_number])
                     i += 1
              jsondata = json.dumps(reservoirselect)
              return render(request, "powerunit/reservoirs.html", {"reservoirs" : jsondata})
       else:
              return redirect('/')
def motors(request):
       if request.user.is_authenticated:
              motorsall = Motors.objects.all().order_by('hp', 'id')
              motorselect = []
              i = 0
              for x in motorsall:
                     voltage = ""
                     if motorsall[i].voltage == "1":
                            voltage = "120VAC/240VAC Single Phase"
                     elif motorsall[i].voltage == "2":
                            voltage = "240VAC/480VAC Three Phase"
                     elif motorsall[i].voltage == "3":
                            voltage = "575VAC Three Phase"
                     motorselect.append([motorsall[i].hp, voltage, motorsall[i].id, motorsall[i].motor_number, motorsall[i].frame_size])
                     i += 1
              jsondata = json.dumps(motorselect)
              return render(request, "powerunit/motors.html", {"allmotors" : jsondata})
       else:
              return redirect('/')

def pumpnums(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     pumptotal = int(request.POST["pumpnum"])
                     pumpcurrent = int(request.POST["pumpcurrent"])
                     selected = request.POST["selected"]
                     pumpcodes = []
                     if selected != "":
                            #If this is not the  first selection being presented
                            rearupper = Pumpcodes.objects.get(pump = selected)
                            data1 = rearupper.front_pump
                            frontpump = data1.lower()
                     if pumpcurrent == 1 and pumptotal != 1:
                            #Prevent selection of gear pump for front pump if > 1 pump
                            data = Pumpcodes.objects.all().exclude(pump__startswith = "AZP").order_by('pump_class', 'pump_size', 'id')
                            y = 0
                            for x in data:
                                   pumpcodes.append(data[y].pump)
                                   y += 1
                     elif pumptotal ==  1:
                            #allow any selection
                            data = Pumpcodes.objects.all().order_by('pump_class', 'pump_size', 'id')
                            y = 0
                            for x in data:
                                   pumpcodes.append(data[y].pump)
                                   y += 1
                     elif pumptotal - pumpcurrent == 1 or pumptotal == pumpcurrent:
                            #allow any selection that has through drive options
                            query = 'select * from pumpcodes join throughdrives on throughdrives.rear_pump = pumpcodes.rear_pump where throughdrives.' + frontpump + ' is not null order by pump_class, pump_size'
                            data = Pumpcodes.objects.raw(query)
                            y = 0
                            for x in data:
                                   pumpcodes.append(data[y].pump)
                                   y += 1
                     if len(pumpcodes) == 0:
                            pumpcodes.append("Please choose a different forward pump")
                     jsondata = json.dumps(pumpcodes)
                     return HttpResponse(jsondata, content_type="application/json")
              else:
                     return redirect('/')       
       else:
              return redirect('/')

def pumpselect(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     pumps = json.loads(request.POST['pumpparts'])
                     pumpmax = json.loads(request.POST['pumpmax'])
                     current = json.loads(request.POST['current'])
                     results = []
                     if pumps[0].count('AZP') != 0:
                            currentpump = pumps[0].replace("*","%%")
                            option1 = currentpump
                            option2 = currentpump
                            option3 = currentpump
                     else:
                            search = pumps[0].replace("*", "%%").replace("/","").split("R")
                            currentpump = '%%' + search[0] + '%%'
                            if search[1].count('K') != 0:
                                   currentpump += 'K%%'
                            if search[1].count('S') != 0:
                                   currentpump += 'S%%'
                            if pumps[0].count('31') != 0:
                                   if pumpmax - current > 1:
                                          option1 = currentpump + 'K01%%'
                                          option2 = currentpump + 'K01%%'
                                          option3 = currentpump + 'K68%%'
                                   else:
                                          option1 = currentpump + 'N00%%'
                                          option2 = currentpump + 'K01%%'
                                          option3 = currentpump + 'K68%%'
                            if pumps[0].count('32') != 0:
                                   option1 = currentpump + 'U00%%'
                                   option2 = currentpump + 'U00%%'
                                   option3 = currentpump + 'U00%%'
                            if pumps[0].count('A15') != 0:
                                   option1 = currentpump
                                   option2 = currentpump
                                   option3 = currentpump
                            if pumps[0].count('A4') != 0:   
                                   option1 = currentpump + 'U00%%'
                                   option2 = currentpump + 'N00%%'
                                   option3 = currentpump
                     query = "select * from parts where product_name like '" + option1 + "' or product_name like '" + option2 + "' or product_name like '" + option3 + "' order by on_hand desc, pref desc, stockstatus desc, goto_item desc"
                     options = Parts.objects.raw(query)
                     j = 0
                     for x in options:         
                            info = [options[j].item_number, options[j].product_name, options[j].on_hand, options[j].cost_each,options[j].stockstatus, options[j].pref, options[j].goto_item ]
                            results.append(info)
                            j += 1
                     if len(results) == 0:
                            results.append(["No pumps with this configuration."])
                     jsondata = results
                     return HttpResponse(json.dumps(jsondata), content_type="application/json")        
              else:
                     return redirect('/')       
       else:
              return redirect('/')

def pumpparts(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     pumps = json.loads(request.POST['pumpnums'])
                     parts = []
                     flows = []
                     i = 0
                     j = 1
                     for x in pumps:
                            frontupper = Pumpcodes.objects.get(pump = pumps[i])
                            if i == 0:
                                   flows.append(frontupper.pump_size)
                            data1 = frontupper.front_pump
                            frontpump = data1.lower()
                            try:
                                   rearlower = Pumpcodes.objects.get(pump = pumps[j])
                                   flows.append(rearlower.pump_size)
                                   data2 = rearlower.front_pump
                                   rearpump = data2.upper()                         
                                   if rearpump.count('AZP') != 0:
                                          rearpump += '%%'
                            except IndexError:
                                   break
                            cursor = connection.cursor()
                            sql = """SELECT %s FROM throughdrives WHERE rear_pump LIKE '%s'""" % (frontpump,rearpump)
                            cursor.execute(sql)
                            num = cursor.fetchall()
                            if num[0][0].startswith("K"):
                                   pass
                            else:
                                   parts.append(num[0][0])
                            i += 1
                            j += 1
                     jsondata = [parts,flows]
                     return HttpResponse(json.dumps(jsondata), content_type="application/json") 
              else:
                     return redirect('/')       
       else:
              return redirect('/')

def details(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     arr = json.loads(request.POST['arr'])
                     parts = []
                     i = 0
                     for x in arr:
                            try:
                                   data = Parts.objects.get(item_number = arr[i])
                                   parts.append([data.item_number, data.product_name, data.on_hand, data.cost_each, data.stockstatus, data.goto_item])
                            except:
                                   parts.append([arr[i],"Part not yet loaded into AX","","0.00","",""])
                            i += 1
                     jsondata = parts
                     return HttpResponse(json.dumps(jsondata), content_type="application/json")
              else:
                     return redirect('/')       
       else:
              return redirect('/')

def extra(request):
       if request.user.is_authenticated:
              return render(request, "powerunit/manualselection.html")
       else:
              return redirect('/')

def search(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     query = request.POST['query']
                     results = Parts.objects.filter(item_number__icontains=query)[:10] | Parts.objects.filter(product_name__icontains=query)[:10]
                     parts = []
                     i = 0
                     for x in results:
                            parts.append([results[i].item_number, results[i].product_name, results[i].on_hand, results[i].cost_each,results[i].stockstatus, results[i].goto_item ])
                            i += 1
                     jsondata = parts
                     return HttpResponse(json.dumps(jsondata), content_type="application/json")
              return redirect('/')
       else:
              return redirect('/')