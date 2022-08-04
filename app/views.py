from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import *
import math
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import login as auth_login
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import *
from django.db.models import Count
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import numpy as np
from matplotlib import pyplot as plt
from email.mime.image import MIMEImage
import os
import datetime
from datetime import datetime as dt
import calendar
from django.db.models import Sum
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from datetime import date, timedelta
from dateutil.rrule import rrule, MONTHLY
import calendar
from calendar import monthrange
import datetime as DT
from railway.settings import BASE_DIR


# Create your views here.


def redircte(request):
    return redirect('/login')

##############################################################################################


import os
from twilio.rest import Client


##############################################
################# Main Data ###############
##############################################


@login_required
def upload_data(request):
    if request.method == "POST":
        csv_data = request.FILES.get('csv')
        df = pd.read_csv(str(BASE_DIR)+"/media/data/data/" + str(csv_data))
        length = len(df)
        for i in range(0, length):
            if df['Registration_Date'][i] == " " or type(df['Registration_Date'][i]) == float:
                register_date = None
            else:
                split_date = df['Registration_Date'][i].split(' ')
                register_date = datetime.datetime.strptime(f'{split_date[0]}', '%d-%m-%y')

            if df['Closing_Date'][i] == " " or type(df['Closing_Date'][i]) == float:
                closing_date = None
            else:
                split_date_2 = df['Closing_Date'][i].split(' ')
                closing_date = datetime.datetime.strptime(f'{split_date_2[0]}', '%d-%m-%y')

            Main_Data_Upload(

                sl_no = df['SL_NO'][i],
                reference_no = df['Ref_No'][i],
                registration_date = register_date,
                closing_date = closing_date,
                disposal_time = df['Disposal_Time'][i],
                mode = df['Mode'][i],
                train_station = df['Train_Station'][i],
                channel = df['Channel'][i],
                Type = df['TYPE'][i],
                coach_number = df['COACH_NO'][i],
                rake_number = df['RAKE_NO'][i],
                staff_name = df['STAFF_NAME'][i],
                problem_type = df['Type'][i],
                sub_type = df['Sub_Type'][i],
                commodity = df['Commodity'][i],
                zone = df['Zone'][i],
                div = df['Div'][i],
                dept = df['Dept'][i],
                breach = df['Breach'][i],
                rating = df['Rating'][i],
                status = df['Status'][i],
                complaint_discription = df['Complaint_Description'][i],
                remark = df['Remarks'][i],
                number_of_time_forwarded = df['No_of_times_forwarded'][i],
                pnr_utc_number = df['PNR_UTS_no'][i],
                coach_type = df['Coach_Type'][i],
                coach_number_no = df['Coach_No'][i],
                feedback_remark = df['Feedback_Remarks'][i],
                upcoming_station = df['Upcoming_Station'][i],
                mobile_number_or_email = df['Mobile_No_Email_Id'][i],
                physical_coach_number = df['Physical_Coach_No'][i]
            ).save()

        account_sid = 'AC37cad0e9482615a332fce6a6b3d96a5a' 
        auth_token = 'd57b5cff62922c9769603303cd3cf825' 
        client = Client(account_sid, auth_token) 
         
        message = client.messages.create( 
                                      from_='whatsapp:+14155238886',  
                                      body='hello',
                                      to='whatsapp:+918409913276' 
                                  ) 
         
        print(message.sid)

        return redirect(request.path)

    return render(request, 'data_upload.html')

###################################################################








#################################################
########### Register & Login ####################
#################################################
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/user/dashboard')
    else:
        if request.method=="POST":
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            if User.objects.filter(username=username): 
                u_d=User.objects.get(username=username)
                user_password = u_d.check_password(password)
            else:
                user_password=False

            if User.objects.filter(username=username) and user_password==True:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/user/dashboard')
                else:
                    messages.error(request,"Invalid username or password.")
                    return redirect(request.path)
            else:
                messages.error(request,"Invalid username or password.")
                return redirect(request.path)
    
    return render(request, 'login.html')





def register_user(request):
    if request.user.is_authenticated:
        return redirect('/login')
    else:
        if request.method=="POST":
            username = request.POST.get('username')
            email = request.POST.get('email', '')
            password = request.POST.get('password')
            re_password = request.POST.get('re-password')
            phone_number = request.POST.get('phonenumber',"")

            username_match=User.objects.filter(username=username)
            email_match=User.objects.filter(email=email)
            if username_match:
                messages.error(request,"Username Already Taken")
                return redirect(request.path)
            
            elif email_match:
                messages.error(request,"Email Already Taken")
                return redirect(request.path)

            elif password!=re_password:
                messages.error(request,"Password Do not Match!")
                return redirect(request.path)
            else:
                u_name=username.split(" ")
                if len(u_name) >= 2:
                    first_name = u_name[0]
                    last_name = u_name[1]
                else:
                    first_name = u_name[0]
                    last_name = " "
                user_detail=User.objects.create_user(username=username,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    password=password,
                                                    email=email)

                user_detail.save()
                user = User.objects.get(username=user_detail.username)
                messages.success(request,'You are Successfully Register, Please Login')
                return redirect('/login')
    return render(request, 'register.html')



#################################################
########### User Detail Section ####################
#################################################

@login_required
def user_detail(request):
    user_detail=Profile.objects.get(username=request.user.id)
    context={
        'u':user_detail
    }
    return render(request, 'user_detail/user_profile.html', context)




@login_required
def edit_profile(request):
    user_detail=Profile.objects.get(username=request.user.id)
    user_d = User.objects.get(id=request.user.id)
    if request.method == "POST":
        username = request.POST.get('username','')
        phone_number = request.POST.get('phone','')
        email = request.POST.get('email','')


        user_d.username = username
        user_detail.phone_number=phone_number
        user_detail.email = email
        user_detail.save()
        messages.success(request, 'Successfully Edited')
        return redirect('/user/user_profile')
    context={
        'u':user_detail
    }
    return render(request, 'user_detail/edit_profile.html',context)

#################################################
########### Dashboard Section ####################
#################################################


@login_required
def dashboard(request):
    main_data=[]
    if request.method == "POST":
        post = True
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        if delta.days <= 0:
            return HttpResponse('<h1>Please Enter Valid Date Range</h1>')

        data_filter = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"])
        for f_d in data_filter:
            main_data.append(f_d.problem_type)
        data = set(main_data)

        occur = []
        for ff in data:
            occur.append(main_data.count(ff))

        if len(occur) == 0:
            show = False
        else:
            show=True

    else:
        post  = False
        #### Full Main data ############    
        full_data = Main_Data_Upload.objects.all()
        for f_d in full_data:
            main_data.append(f_d.problem_type)
        data = set(main_data)
        

       ############## Set Data ######################
        occur = []
        for ff in data:
            occur.append(main_data.count(ff))


        if len(occur) == 0:
            show = False
        else:
            show=True


    context = {
            'show':show,
            'post':post,
            'main_data':main_data,
            'data':data,
            'occur':occur
        }
    return render(request, 'dashboard.html',context)



@login_required
def rating(request):
   ########## Bar Graph rating ###############
    if request.method == "POST":
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        months = []

        unsatis = []
        satis = []
        excel = []
        nan = []

        if delta.days <=0:
            return HttpResponse('<h1>Please Enter Valid Date Range</h1>')

        for i in range(start_month.month,end_month.month+1):
            print(i)
            dataa = Main_Data_Upload.objects.filter(registration_date__month=i)
            data = []
            for dd in dataa:
                data.append(dd.rating)
            unsatis.append(data.count('Unsatisfactory'))
            satis.append(data.count('Satisfactory'))
            nan.append(data.count('nan'))
            excel.append(data.count('Excellent'))

            months.append(calendar.month_name[i])

        if sum(excel) == 0 and sum(nan) == 0 and sum(unsatis) == 0 and sum(satis) == 0:
            show = False
        else:
            show=True

        context = {
            'show':show,
            'post':True,
            'months':months,
            'unsatis':unsatis,
            'satis':satis,
            'excel':excel,
            'nan':nan
        }

    else:
        rating_data=[] 
        main_rating_data = []
        full_rating_data = Main_Data_Upload.objects.values_list('rating')
        for f_d in full_rating_data:
            for r_d in f_d:
                main_rating_data.append(r_d)


        unsatis = []
        satis = []
        nan = []
        excel = []


        unsatis.append(main_rating_data.count('Unsatisfactory'))
        satis.append(main_rating_data.count('Satisfactory'))
        nan.append(main_rating_data.count('nan'))
        excel.append(main_rating_data.count('Excellent'))


        if sum(excel) == 0 and sum(nan) == 0 and sum(unsatis) == 0 and sum(satis) == 0:
            show = False
        else:
            show=True


        context ={
            'show':show,
            'post':False,
            'unsatis':unsatis,
            'satis':satis,
            'excel':excel,
            'nan':nan
            }
    return render(request, 'rating.html',context)




@login_required
def trend(request):
    if request.method == "POST":
        post = True
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))



######
        coach_clean = []
        bed_roll = []
        security = []
        medical_assis = []
        punctuality = []
        water_avail = []
        electrical_equip = []
        coach_maintain = []
        miscellaneous = []
        staff_behave = []
        dates = []
########

        if delta.days <= 0:
            return HttpResponse("<center><h1>Please Enter Right Date Range</h1></center>")
        
        elif delta.days <= 45:
            for i in range(delta.days+1):
                day = sdate + timedelta(days=i)
                dates.append(str(day.day)+" "+str(calendar.month_name[day.month])+","+ str(day.year))
                
                coach_clean_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Coach - Cleanliness")
                coach_clean.append(coach_clean_data.count())

                bed_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Bed Roll")
                bed_roll.append(bed_data.count())

                security_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Security")
                security.append(security_data.count())


                medical_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Medical Assistance")
                medical_assis.append(medical_data.count())


                punctuality_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Punctuality")
                punctuality.append(punctuality_data.count())


                water_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Water Availability")
                water_avail.append(water_data.count())


                electrical_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Electrical Equipment")
                electrical_equip.append(electrical_data.count())


                coach_maintain_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Coach - Maintenance")
                coach_maintain.append(coach_maintain_data.count())


                miscellaneous_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Miscellaneous")
                miscellaneous.append(miscellaneous_data.count())


                staff_behave_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Staff Behaviour")
                staff_behave.append(staff_behave_data.count())

            total = []
            total.append(coach_clean)
            total.append(bed_roll)
            total.append(security)
            total.append(medical_assis)
            total.append(punctuality)
            total.append(water_avail)
            total.append(electrical_equip)
            total.append(coach_maintain)
            total.append(miscellaneous)
            total.append(staff_behave)
            print(total)


        elif delta.days >=46:
            strt_dt = sdate
            end_dt = edate
            datess = [dt for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
            for d in datess:
                dates.append(calendar.month_name[int(d.month)] +","+ str(d.year))
                coach_clean_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Coach - Cleanliness")
                coach_clean.append(coach_clean_data.count())

                bed_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Bed Roll")
                bed_roll.append(bed_data.count())

                security_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Security")
                security.append(security_data.count())


                medical_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Medical Assistance")
                medical_assis.append(medical_data.count())


                punctuality_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Punctuality")
                punctuality.append(punctuality_data.count())


                water_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Water Availability")
                water_avail.append(water_data.count())


                electrical_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Electrical Equipment")
                electrical_equip.append(electrical_data.count())


                coach_maintain_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Coach - Maintenance")
                coach_maintain.append(coach_maintain_data.count())


                miscellaneous_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Miscellaneous")
                miscellaneous.append(miscellaneous_data.count())


                staff_behave_data = Main_Data_Upload.objects.filter(registration_date__year = d.year , registration_date__month=d.month, problem_type = "Staff Behaviour")
                staff_behave.append(staff_behave_data.count())
            total = []
            total.append(coach_clean)
            total.append(bed_roll)
            total.append(security)
            total.append(medical_assis)
            total.append(punctuality)
            total.append(water_avail)
            total.append(electrical_equip)
            total.append(coach_maintain)
            total.append(miscellaneous)
            total.append(staff_behave)
            print(total)

    else:
        coach_clean = []
        bed_roll = []
        security = []
        medical_assis = []
        punctuality = []
        water_avail = []
        electrical_equip = []
        coach_maintain = []
        miscellaneous = []
        staff_behave = []
        dates = []
        post = False
        for i in range(0,31):
            day = datetime.datetime.now() - datetime.timedelta(i)
            dates.append(str(day.day)+" "+str(calendar.month_name[day.month])+","+ str(day.year))
            
            coach_clean_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Coach - Cleanliness")
            coach_clean.append(coach_clean_data.count())

            bed_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Bed Roll")
            bed_roll.append(bed_data.count())

            security_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Security")
            security.append(security_data.count())


            medical_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Medical Assistance")
            medical_assis.append(medical_data.count())


            punctuality_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Punctuality")
            punctuality.append(punctuality_data.count())


            water_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Water Availability")
            water_avail.append(water_data.count())


            electrical_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Electrical Equipment")
            electrical_equip.append(electrical_data.count())


            coach_maintain_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Coach - Maintenance")
            coach_maintain.append(coach_maintain_data.count())


            miscellaneous_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Miscellaneous")
            miscellaneous.append(miscellaneous_data.count())


            staff_behave_data = Main_Data_Upload.objects.filter(registration_date__year = day.year , registration_date__month=day.month, registration_date__day = day.day ,problem_type = "Staff Behaviour")
            staff_behave.append(staff_behave_data.count())
        total = []
        total.append(coach_clean)
        total.append(bed_roll)
        total.append(security)
        total.append(medical_assis)
        total.append(punctuality)
        total.append(water_avail)
        total.append(electrical_equip)
        total.append(coach_maintain)
        total.append(miscellaneous)
        total.append(staff_behave)

    all_type=['Coach - Cleanliness','Bed Roll','Security','Medical Assistance',
              'Punctuality','Water Availability','Electrical Equipment','Coach - Maintenance',
              'Miscellaneous','Staff Behaviour']

    sub_type = Main_Data_Upload.objects.values_list('sub_type')
    subtype=[]
    for s in sub_type:
        for st in s:
            subtype.append(st)

    main_sub_type = []
    for sub in subtype:
        main_sub_type.append(sub.split('/'))
    for i in range(len(main_sub_type)):
        if len(main_sub_type[i]) >= 2:
            subtype[i] = " ".join(main_sub_type[i])

    sts = (set(subtype))
    demo_sub = set(sub_type)



    context ={
        'show':True,
        'post':post,
        'coach_clean':coach_clean,
        'bed_roll':bed_roll,
        'security':security,
        'medical_assis':medical_assis,
        'punctuality':punctuality,
        'water_avail':water_avail,
        'electrical_equip':electrical_equip,
        'coach_maintain':coach_maintain,
        'miscellaneous':miscellaneous,
        'staff_behave':staff_behave,
        'dates':dates,
        'total':total,
        'all_type':all_type,
        'sub_type':sts,
        'demo_sub':demo_sub
        }
    return render(request, 'trends.html',context)




@login_required
def sub_type(request,subtype):
    if subtype == "Luggage Left Behind Unclaimed Suspected Articles":
        subtypes = "Luggage Left Behind/Unclaimed/Suspected Articles"

    elif subtype == "Harassment Extortion by Security Personnel Railway personnel":
        subtypes = "Harassment/Extortion by Security Personnel/Railway personnel"

    elif subtype == "Tap leaking/Tap not working":
        subtypes = "Tap leaking/Tap not working"

    elif subtype == "Window Seat Broken":
        subtypes = "Window/Seat Broken"

    elif subtype == "Window Door locking problem":
        subtypes = "Window/Door locking problem"

    elif subtype == "Unauthorized person in Ladies Disabled Coach SLR Reserve Coach":
        subtypes = "Unauthorized person in Ladies/Disabled Coach/SLR/Reserve Coach"

    elif subtype == "Jerks Abnormal Sound":
        subtypes = "Jerks/Abnormal Sound"

    elif subtype == "Theft of Passengers Belongings Snatching":
        subtypes = "Theft of Passengers Belongings/Snatching"

    elif subtype == "Nuisance by Hawkers Beggar Eunuch Passenger":
        subtypes = "Nuisance by Hawkers/Beggar/Eunuch/Passenger"

    elif subtype == "Smoking Drinking Alcohol Narcotics":
        subtypes = "Smoking/Drinking Alcohol/Narcotics"

    elif subtype == "Passenger Missing Not responding call":
        subtypes = "Passenger Missing/Not responding call"

    else:
        subtypes = subtype

    dates = []
    data_count = []

    if request.method == "POST":
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=45:
            for i in range(delta.days+1):
                day = sdate + timedelta(days=i)
                dates.append(str(day.day)+" "+str(calendar.month_name[day.month])+","+ str(day.year))
                sub_type_data = Main_Data_Upload.objects.filter(sub_type=f"{subtypes}",registration_date__day=day.day,registration_date__month=day.month,registration_date__year=day.year)
                data_count.append(sub_type_data.count())
            print(data_count)
        elif delta.days <=0:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")
        elif delta.days >=46:
            strt_dt = sdate
            end_dt = edate
            datess = [dt for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
            for d in datess:
                dates.append(calendar.month_name[int(d.month)] +","+ str(d.year))
                sub_type_data = Main_Data_Upload.objects.filter(sub_type=f"{subtypes}",registration_date__month=d.month,registration_date__year=d.year)
                data_count.append(sub_type_data.count())

    else:
        for i in range(0,31):
            day = datetime.datetime.now() - datetime.timedelta(i)
            dates.append(str(day.day)+" "+str(calendar.month_name[day.month])+","+ str(day.year))    
            sub_type_data = Main_Data_Upload.objects.filter(sub_type=f"{subtypes}",registration_date__day=day.day,registration_date__month=day.month,registration_date__year=day.year)
            data_count.append(sub_type_data.count())
    context = {
                'show':True,
                'data_count':data_count,
                'dates':dates,
                'subtype':subtype,
                'subtypes':subtypes
              }
    return render(request,'sub_type.html',context)




def complain_type(request, complain):
    if complain == "Luggage Left Behind Unclaimed Suspected Articles":
        complain = "Luggage Left Behind/Unclaimed/Suspected Articles"

    elif complain == "Harassment Extortion by Security Personnel Railway personnel":
        complain = "Harassment/Extortion by Security Personnel/Railway personnel"

    elif complain == "Tap leaking/Tap not working":
        complain = "Tap leaking/Tap not working"

    elif complain == "Window Seat Broken":
        complain = "Window/Seat Broken"

    elif complain == "Window Door locking problem":
        complain = "Window/Door locking problem"

    elif complain == "Unauthorized person in Ladies Disabled Coach SLR Reserve Coach":
        complain = "Unauthorized person in Ladies/Disabled Coach/SLR/Reserve Coach"

    elif complain == "Jerks Abnormal Sound":
        complain = "Jerks/Abnormal Sound"

    elif complain == "Theft of Passengers Belongings Snatching":
        complain = "Theft of Passengers Belongings/Snatching"

    elif complain == "Nuisance by Hawkers Beggar Eunuch Passenger":
        complain = "Nuisance by Hawkers/Beggar/Eunuch/Passenger"

    elif complain == "Smoking Drinking Alcohol Narcotics":
        complain = "Smoking/Drinking Alcohol/Narcotics"

    elif complain == "Passenger Missing Not responding call":
        complain = "Passenger Missing/Not responding call"

    else:
        complain = complain
    complain_type = complain
    problem_types = Main_Data_Upload.objects.values_list('coach_number',
                                                        'problem_type',
                                                        'sub_type',
                                                        'disposal_time',
                                                        'rating','complaint_discription')
    problem_type = []
    for p in problem_types:
        if p[1] == complain_type or p[2] == complain_type:
            problem_type.append(p)
    context = {'complain_type':complain_type, 'problem_type':problem_type}
    return render(request, 'complain_type.html',context)






def train_wise_data(request):
    data_count=[]
    problem_type = Main_Data_Upload.objects.values_list('problem_type')
    Type=[]
    for s in problem_type:
        for t in s:
            Type.append(t)

    problem_type = set(Type)

    if request.method == "POST":
        train_number = int(request.POST.get('train_number',''))
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")

        for p_t in problem_type:
            data = Main_Data_Upload.objects.filter(train_station=train_number,problem_type=p_t,registration_date__gte=start_date,registration_date__lte=end_date)
            data_count.append(data.count())

        if sum(data_count) == 0:
            data_show = False
        else:
            data_show = True

        print(data_count)

        context = {
                    'problem_type':problem_type,
                    'post':True,
                    'data_count':data_count,
                    'train_number':train_number,
                    'data_show':data_show
                   }

    else:
        post = False
        context = {'post':post}
    return render(request, "train_wise_data.html",context)






def voltage_chart(request):

    ###### Past 24 Hours #########
    float_past_24_hour_list=[]
    past_24_hour_list=[]
    list_voltage_past_24_hour=[]
    today = DT.date.today()

    for i in range(0,24):
        past_24_hour_ago = str(datetime.datetime.now() - datetime.timedelta(hours = i))
        splitted=past_24_hour_ago.split(" ")
        w1=splitted[0].split("-")
        w2=splitted[1].split(":")
        year=round(int(w1[0]))
        month=round(int(w1[1]))
        day = round(int(w1[2]))
        hour = round(int(w2[0]))
        minute = round(int(w2[1]))
        if hour >=12:
            format = "PM"
        elif hour == 0:
            format = "AM"
        else:
            format = "AM"
        past_24_hour_list.append(str(hour) + ":" + str(minute) + " " +format)

        vol = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month, day=day, hour = hour).aggregate(total=Sum('voltage_data'))['total']
        vol_count = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month, day=day, hour = hour).count()
        print(vol)

        if vol == None:
            float_past_24_hour_list.append(0)
        else:
            float_past_24_hour_list.append(vol/vol_count)
    for f_past in float_past_24_hour_list:
        list_voltage_past_24_hour.append(round(f_past))

    past_24_hour_list.reverse()
    list_voltage_past_24_hour.reverse()





    # ###### Past 7 Days #########
    float_past_7_day_list=[]
    past_7_day_list=[]
    list_voltage_past_7_day=[]
    today = DT.date.today()

    for i in range(0,7):
        past_7_day_ago = str(datetime.datetime.now() - datetime.timedelta(days = i))
        splitted=past_7_day_ago.split(" ")
        w1=splitted[0].split("-")
        w2=splitted[1].split(":")
        year=round(int(w1[0]))
        month=round(int(w1[1]))
        day = round(int(w1[2]))
        hour = round(int(w2[0]))
        month_name = calendar.month_name[month]
        past_7_day_list.append(str(day) + " " + str(month_name) + "," + str(year))

        vol_past_7_day = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month, day=day).aggregate(total=Sum('voltage_data'))['total']
        vol_past_7_day_count = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month, day=day).count()

        if vol_past_7_day == None:
            float_past_7_day_list.append(0)
        else:
            float_past_7_day_list.append(vol_past_7_day/vol_past_7_day_count)
    for f_past in float_past_7_day_list:
        list_voltage_past_7_day.append(round(f_past))

    past_7_day_list.reverse()
    list_voltage_past_7_day.reverse()







    # ###### Past 30 days #########
    float_past_30_day_list=[]
    past_30_day_list=[]
    list_voltage_past_30_day=[]
    today = DT.date.today()

    for i in range(0,30):
        past_30_day_ago = str(datetime.datetime.now() - datetime.timedelta(days = i))
        splitted=past_30_day_ago.split(" ")
        w1=splitted[0].split("-")
        w2=splitted[1].split(":")
        year=round(int(w1[0]))
        month=round(int(w1[1]))
        day = round(int(w1[2]))
        month_name = calendar.month_name[month]
        past_30_day_list.append(str(day) + " " + str(month_name) + "," + str(year))

        vol_past_30_day = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month, day=day).aggregate(total=Sum('voltage_data'))['total']
        vol_past_30_day_count = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month, day=day).count()

        if vol_past_30_day == None:
            float_past_30_day_list.append(0)
        else:
            float_past_30_day_list.append(vol_past_30_day/vol_past_30_day_count)
    
    for f_past in float_past_30_day_list:
        list_voltage_past_30_day.append(round(f_past))

    past_30_day_list.reverse()
    list_voltage_past_30_day.reverse()




    ###### Past 12 Months Data #########
    float_past_365_day_list=[]
    past_365_day_list=[]
    past_12_month_data=[]
    past_12_month_number = []
    past_12_month_string= []
    past_12_month_year = []
    list_voltage_past_365_day=[]
    current_date = dt.today()
    for i in range(0,12):
        past_months = str(current_date - relativedelta(months=i))
        w=past_months.split("-")
        year=int(w[0])
        month=int(w[1])

        past_12_month_number.append(str(month)+"/"+str(year))
        past_12_month_year.append(year)
        past_12_month_string.append(calendar.month_name[month] + " (" + str(year) + ")")
        past_12_month_data = dict(zip(past_12_month_number, past_12_month_string))

        past_365_day_list.append(calendar.month_name[month] + "," + str(year))

        vol_past_365_day = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month).aggregate(total=Sum('voltage_data'))['total']
        vol_past_365_day_count = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month).count()

        if vol_past_365_day == None:
            float_past_365_day_list.append(0)
        else:
            float_past_365_day_list.append(vol_past_365_day/vol_past_365_day_count)
    
    for f_past in float_past_365_day_list:
        list_voltage_past_365_day.append(round(f_past))

    past_365_day_list.reverse()
    list_voltage_past_365_day.reverse()



    ##### Past 12 Month name and Month Number ######



    context={
        'past_24_hour':past_24_hour_list,
        'past_24_hour_voltage':list_voltage_past_24_hour,
        'past_7_day':past_7_day_list,
        'voltage_past_7_day':list_voltage_past_7_day,
        'past_30_day':past_30_day_list,
        'voltage_past_30_day':list_voltage_past_30_day,
        'past_12_month':past_365_day_list,
        'voltage_past_12_month':list_voltage_past_365_day,
        'past_12_month_data':past_12_month_data,
        'past_12_month_year':past_12_month_year

    }
    return render(request, 'base/voltage_chart.html', context)




#################################################
########### Search By Month ####################
#################################################
def voltage_search_by_month(request, month_num, year):
    float_month_day_list=[]
    list_voltage_month_day=[]
    this_month_day=[]
    days_in_month = int()
    if month_num == 1 or month_num == 3 or  month_num == 5 or month_num == 7 or month_num == 8 or month_num == 10 or month_num == 12:
        days_in_month = 31

    elif month_num == 2:
        if year % 4 == 0:
            days_in_month = 29
        else:
            days_in_month = 28
    else:
        days_in_month = 30

    for i in range(1,days_in_month+1):

        vol_month_day = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month_num, day=i).aggregate(total=Sum('voltage_data'))['total']
        vol_month_day_count = Voltage_Data_Upload.objects.filter(user=request.user.id, year=year, month=month_num, day=i).count()

        this_month_day.append(str(i) + " " + calendar.month_name[month_num] + "," + str(year))
        month_this = calendar.month_name[month_num] + "," + str(year)

        if vol_month_day == None:
            float_month_day_list.append(0)
        else:
            float_month_day_list.append(vol_month_day/vol_month_day_count)
    
    for f_past in float_month_day_list:
        list_voltage_month_day.append(round(f_past))


    print(float_month_day_list)
    print(list_voltage_month_day)

    context = {
        'this_month_day':this_month_day,
        'list_voltage_month_day':list_voltage_month_day,
        'month_this':month_this
    }
    return render(request, 'base/voltage_data_month.html',context)





#################################################
########### Fill Full data Section ####################
#################################################

def fill_data(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            phone_number = request.POST.get('phone', None)
            pin_code = request.POST.get('pin', None)
            pan_number = request.POST.get('pan', None)
            system_warranty = request.POST.get('system_w', None)
            panel_warranty = request.POST.get('pannel_w', None)
            panel_company = request.POST.get('panel_c', '')
            setup_capacity = request.POST.get('setup_c', None)
            location = request.POST.get('location', '')
            type_of_user = request.POST.get('who', '')
            if type_of_user == "individual":
                type_of_user = "Individual"
                company_name = ""
                system_warranty = None
                pannel_warranty = None
                panel_company = ""
                setup_capacity = None
                pan_number = None
                logo = request.FILES.get('logo','')
            else:
                company_name = request.POST.get('c_name', '')
                type_of_user = "Company"
                logo = request.FILES.get('logo','logo')

            if pan_number == "":
                pan_number = None
            else:
                pan_number = pan_number

            if setup_capacity == "":
                setup_capacity = None
            else:
                setup_capacity = setup_capacity

            if system_warranty == "":
                system_warranty  = None
            else:
                system_warranty = system_warranty

            if panel_warranty == "":
                panel_warranty = None
            else:
                panel_warranty = panel_warranty

            if phone_number == "":
                phone_number = None
            else:
                phone_number = phone_number

            if pin_code == "":
                pin_code = None
            else:
                pin_code = pin_code


            user_pro = User.objects.get(id=request.user.id)

            if user_pro and not Profile.objects.filter(username=request.user.id):
                print(logo)
                prof=Profile(
                    username=user_pro,
                    email = request.user.email,
                    phone_number = phone_number,
                    pan_number = pan_number,
                    type_of_user = type_of_user,
                    location = location,
                    pin_code = pin_code,
                    logo=logo,
                    company_name = company_name,
                    setup_capacity = setup_capacity,
                    panel_warranty = panel_warranty,
                    system_warranty = system_warranty,
                    panel_company = panel_company
                    )
                prof.save()
                return redirect('/user/dashboard')
            else:

                update_profile=Profile.objects.get(username=request.user.id)

                update_profile.type_of_user = type_of_user
                update_profile.company_name = company_name
                update_profile.phone_number = phone_number
                update_profile.pin_code = pin_code
                update_profile.pan_number = pan_number
                update_profile.location = location
                update_profile.setup_capacity = setup_capacity
                update_profile.panel_company = panel_company
                update_profile.panel_warranty = panel_warranty
                update_profile.system_warranty = system_warranty
                update_profile.logo = logo

                update_profile.save()
                return redirect('/user/dashboard')
    else:
        pass






