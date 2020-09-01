from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import HPForm, PumpForm, FrameForm, ReservoirForm
from django.forms import inlineformset_factory, formset_factory
from .models import Motors, Pumpcodes, BellHousingSizes, CouplingCodes, Reservoir, Throughdrives
from manifold.models import Parts
from django.http import HttpResponse, JsonResponse
import json, math

def newunit(request):
       if request.user.is_authenticated:       
              if request.method == 'POST':
                     #Pass the account number through to the next page
                     accountnumber = request.POST['accountnumber']
                     return render (request, 'powerunit/pumpmanual.html', {"accountnumber" : accountnumber, })
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
                     num = request.POST["horsepower"]
                     pump = request.POST['pump']
                     volts = request.POST['voltage']
                     a = str(volts)
                     #Grab the motor from the horsepower and voltage provided. I don't have a fail safe on this, because the HTML
                     #should stop the user from picking impossible motors, but it can happen. Worry about this later.
                     #The only failure is that the AJAX does not get a response.
                     mot = Motors.objects.get(voltage = a, hp = num)
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
                                   else:
                                          motorcoupling = ""
                                   if CouplingCodes.objects.filter(code = str(pumcoup), sizes__contains = size):
                                          pumpcoupling = "M" + str(size) + str(pumcoup)
                                   else:
                                          pumpcoupling = ""
                                   size = size-100
                                   #If all coupling sizes have been cycled though and no good pair has been made, build the 
                                   #coupling code with the preferred size and note that it needs to be custom made
                                   if size == 0:
                                          motorcoupling = "Custom coupling required: M" + str(pref) + str(motcoup)
                                          pumpcoupling = "Custom coupling required: M" + str(pref) + str(pumcoup)
                     #Drop the data in a JSON to pass to the AJAX response
                     data = [bellnum, motorcoupling, pumpcoupling, l, mot.motor_number, pump]
                     jsondata = json.dumps(data)
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
              pass
       else:
              return redirect('/')
def motors(request):
       if request.user.is_authenticated:
              pass
       else:
              return redirect('/')

def pumpnums(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     pumptotal = int(request.POST["pumpnum"])
                     pumpcurrent = int(request.POST["pumpcurrent"])
                     selected = request.POST["selected"]
                     pumpcodes = []
                     print("pumptotal = " + str(pumptotal) + " pumpcurrent = " + str(pumpcurrent))
                     if selected != "":
                            rearupper = Pumpcodes.objects.get(pump = selected)
                            data1 = rearupper.front_pump
                            frontpump = data1.lower()
                     if pumpcurrent == 1 and pumptotal != 1:
                            data = Pumpcodes.objects.all().exclude(pump__startswith = "AZP").exclude(pump__contains="31").order_by('pump_class', 'pump_size', 'id')
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
                     query = "select * from parts where product_name like '" + option1 + "' or product_name like '" + option2 + "' or product_name like '" + option3 + "' order by on_hand desc, pref desc, stockstatus desc"
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