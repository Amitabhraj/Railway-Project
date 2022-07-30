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
import datetime as DT
from railway.settings import BASE_DIR


# Create your views here.


def redircte(request):
    return redirect('/login')

##############################################################################################


##############################################
################# Main Data ###############
##############################################


def upload_data(request):
    if request.method == "POST":
        csv_data = request.FILES.get('csv')
        df = pd.read_csv(str(BASE_DIR)+"/media/data/data/" + str(csv_data))
        length = len(df)
        for i in range(0, length):
            Main_Data_Upload(
                sl_no = df['SL_NO'][i],
                reference_no = df['Ref_No'][i],
                registration_date = df['Registration_Date'][i],
                closing_date = df['Closing_Date'][i],
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
    main_data_count= Main_Data_Upload.objects.all().count()
    
    ##### Full Main data ############
    main_data=[]    
    full_data = Main_Data_Upload.objects.values_list('problem_type')
    for f_d in full_data:
        main_data.append(f_d)


   ############## Set Data ######################
    data = set(Main_Data_Upload.objects.values_list('problem_type'))
    occur = []
    for ff in data:
        occur.append(main_data.count(ff))

    # for data in data:
    #     print(data)


    context = {
        'main_data_count':main_data_count,
        'main_data':main_data,
        'data':data,
        'occur':occur
    }
    return render(request, 'dashboard.html',context)






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






