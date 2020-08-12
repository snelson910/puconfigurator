from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import HPForm, PumpForm, FrameForm
from django.forms import inlineformset_factory, formset_factory
from .models import Motors, Pumpcodes, BellHousingSizes, CouplingCodes
from django.http import HttpResponse, JsonResponse
import json, math

def newunit(request):
       if request.user.is_authenticated:       
              if request.method == 'POST':
                     accountnumber = request.POST['accountnumber']
                     return render (request, 'newunit.html', {"accountnumber" : accountnumber, })
              else:
                     return redirect('/')
       else:
             return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')

def pumpwizard(request):
       if request.user.is_authenticated:
              return render(request, "pumpwizard.html")
       else:
              return redirect('/')

def manual(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     accountnumber = request.POST['accountnumber']
                     MotorFormSet = formset_factory(HPForm)
                     motor_formset = MotorFormSet(prefix = 'motor')
                     PumpFormSet = formset_factory(PumpForm)
                     pump_formset = PumpFormSet(prefix = 'pump')
                     FrameFormSet = formset_factory(FrameForm)
                     frame_formset = FrameFormSet(prefix = 'frame')
                     return render(request, "pumpmanual.html", {'motor' : motor_formset, 'pumps' : pump_formset, 'frames' : frame_formset, 'accountnumber' : accountnumber})
              return redirect('/')
       else:
              return redirect('/')

def coupling(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     num = request.POST["horsepower"]
                     pump = request.POST['pump']
                     volts = request.POST['voltage']
                     a = str(volts)
                     mot = Motors.objects.get(voltage = a, hp = num)
                     frame = mot.frame_size
                     motshaft = mot.shaft_length
                     motcoup = mot.coupling_code
                     pum = Pumpcodes.objects.get(pump = pump)
                     pumframe = pum.pump_flange
                     pumshaft = pum.pump_shaft_length
                     pumcoup = pum.pump_coupling_code 
                     facelen = motshaft + pumshaft + .15
                     bells = BellHousingSizes.objects.order_by('face_to_face').filter(end_style = pumframe, frame_size__contains = frame)
                     i = 0
                     l = 0
                     bellnum = ""
                     if len(bells)== 0:
                            custbell = BellHousingSizes.objects.get(frame_size__contains = frame, part_number__startswith = 'S')
                            length = math.ceil((facelen + .10)*4)/4
                            bellnum = custbell.part_number + str(length*100)[:-3] + '2' + pumframe
                            pref = custbell.coupling_size_pref
                            maxsize = custbell.max_coupling_size
                            l = str(round(length - facelen + .15, 2))
                     else:
                            for x in bells:
                                   if bells[i].face_to_face > facelen:
                                          l = str(round(bells[i].face_to_face - facelen + .15, 2))
                                          bellnum = bells[i].part_number
                                          pref = bells[i].coupling_size_pref
                                          maxsize = bells[i].max_coupling_size
                                          break                                  
                                   i += 1
                            if bellnum == "":
                                   custbell = BellHousingSizes.objects.get(frame_size__contains = frame, part_number__startswith = 'S')
                                   length = math.ceil((facelen + .10)*4)/4
                                   bellnum = custbell.part_number + str(length*100)[:-3] + '2' + pumframe
                                   pref = custbell.coupling_size_pref
                                   maxsize = custbell.max_coupling_size
                                   l = str(round(length - facelen + .15, 2))
                     if CouplingCodes.objects.filter(code = str(motcoup), sizes__contains = pref):
                            motorcoupling = "M" + str(pref) + str(motcoup)
                     else:
                            motorcoupling = ""
                     if CouplingCodes.objects.filter(code = str(pumcoup), sizes__contains = pref):
                            pumpcoupling = "M" + str(pref) + str(pumcoup)
                     else:
                            pumpcoupling = ""
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
                                   if size == 0:
                                          motorcoupling = "Custom coupling required: M" + str(pref) + str(motcoup)
                                          pumpcoupling = "Custom coupling required: M" + str(pref) + str(pumcoup)
                     data = [bellnum, motorcoupling, pumpcoupling, l, mot.motor_number, pump]
                     jsondata = json.dumps(data)
                     return HttpResponse(jsondata, content_type="application/json")  
              else:
                     return redirect('/')       
       else:
              return redirect('/')

def reservoir(request):
       if request.user.is_authenticated:
              if request.method == 'POST':
                     data = json.loads(request.POST['data'])
                     accountnumber = request.POST['accountnumber']
                     print(data)
                     print(accountnumber)
                     return render(request, "reservoir.html", {"data": json.dumps(data), "accountnumber" : accountnumber })
              else:
                     return redirect('/')       
       else:
              return redirect('/')