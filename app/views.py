from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import *
import math
import more_itertools
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import login as auth_login
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import *
from django.db.models import Count
from operator import itemgetter
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
from django.views.decorators.csrf import csrf_exempt
import os
from twilio.rest import Client

# Create your views here.


def redircte(request):
    return redirect('/login')

##############################################################################################




@login_required
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    context = {'user':user}
    return render(request,'user_profile.html',context)


@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('c-password','')
        future_password = request.POST.get('f-password','')
        user = User.objects.get(id=request.user.id)
        user_password = user.check_password(current_password)
        if user_password:
            user.set_password(future_password)
            user.save()
            messages.success(request,'You Have Successfully Changed Your Password')
            return redirect(request.path)
        else:
            messages.error(request,'You Current Password is Wrong, Please Try Again')
            return redirect(request.path)
    context = {}
    return render(request,'change_password.html',context)


##############################################
################# Main Data ###############
##############################################


@login_required
@csrf_exempt
def upload_data(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        if user.groups.filter(name='Moderator').exists():
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print("date and time =", dt_string) 
            csv_data = request.FILES.get('csv')
            convert_data = str(csv_data).split(" ")
            main_csv_data = "_".join(convert_data)
            data = CsvFile(csv_data=csv_data).save()
            df = pd.read_csv(str(BASE_DIR)+"/media/data/railway/" + str(main_csv_data))
            print(df['Registration Date'])
            length = len(df)
            for i in range(0, length):
                print(df['Registration Date'][i])
                if df['Registration Date'][i] == " " or type(df['Registration Date'][i]) == float:
                    register_date = None
                else:
                    split_date = df['Registration Date'][i].split(' ')
                    register_date = datetime.datetime.strptime(f'{split_date[0]}', '%d-%m-%y')
                if df['Closing Date'][i] == " " or type(df['Closing Date'][i]) == float:
                    closing_date = None
                else:
                    split_date_2 = df['Closing Date'][i].split(' ')
                    closing_date = datetime.datetime.strptime(f'{split_date_2[0]}', '%d-%m-%y')
                Main_Data_Upload(
                    sl_no = df['Sl. No.'][i],
                    reference_no = df['Ref. No.'][i],
                    registration_date = register_date,
                    closing_date = closing_date,
                    disposal_time = df['Disposal Time'][i],
                    # mode = df['Mode'][i],
                    train_station = df['Train'][i],
                    channel = df['Channel'][i],
                    # Type = df['Type'][i],
                    coach_number = df['Physical Coach No'][i],
                    # rake_number = df['Rake no'][i],
                    # staff_name = df['Escort staff'][i],
                    problem_type = df['Type'][i],
                    sub_type = df['Sub Type'][i],
                    commodity = df['Commodity'][i],
                    zone = df['Zone'][i],
                    div = df['Div'][i],
                    dept = df['Dept'][i],
                    breach = df['Breach'][i],
                    rating = df['Rating'][i],
                    status = df['Status'][i],
                    complaint_discription = df['Complaint Description'][i],
                    remark = df['Remarks'][i],
                    number_of_time_forwarded = df['No. of times forwarded'][i],
                    pnr_utc_number = df['PNR/UTS No'][i],
                    coach_type = df['Coach Type'][i],
                    # coach_number_no = df['Coach no'][i],
                    # coach_type_2 = df['Coach Type'][i],
                    coach_number_no_2 = df['Coach No.'][i],
                    feedback_remark = df['Feedback Remarks'][i],
                    upcoming_station = df['Upcoming Station'][i],
                    mobile_number_or_email = df['Mobile No./Email Id'][i],
                    # physical_coach_number = df['Physical Coach No'][i],
                    train_name = df['Train Name'][i]
                ).save()
            print("successfully uploaded")

            mobile_number = PhoneNumber.objects.all()
            phone_number = []
            for m_n in mobile_number:
                phone_number.append("whatsapp:+91"+str(m_n))

            account_sid = 'AC37cad0e9482615a332fce6a6b3d96a5a' 
            auth_token = 'd57b5cff62922c9769603303cd3cf825' 
            client = Client(account_sid, auth_token) 

            for p_n in phone_number:
                message = client.messages.create( 
                                              from_='whatsapp:+14155238886',  
                                              body=f'File has been uploaded on the Server--> on date:- {dt_string}',
                                              to= f'{p_n}'
                                          ) 


            return redirect(request.path)
        else:
            messages.error(request,"You Cannot Upload Data")
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

    if request.method != 'POST':
        start_date = None
        end_date = None
        post = False
    context = {
            'show':show,
            'post':post,
            'main_data':main_data,
            'data':data,
            'occur':occur,
            'start_date':start_date,
            'end_date':end_date
        }
    return render(request, 'dashboard.html',context)



@login_required
def rating(request):
    train_numbers_list = Main_Data_Upload.objects.values_list('train_station')
    train = []
    for tr_nums in train_numbers_list:
        train.append(tr_nums)
    train_numbers = set(train)


    trainsss = Main_Data_Upload.objects.all()
    main_trains = []
    for ttt in trainsss:
        main_trains.append(float(ttt.train_station))

   ########## Bar Graph rating ###############
    if request.method == "POST":
        train_number = request.POST.getlist('train_number')
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


        trains_num = []
        for t_r in train_numbers:
            trains_num.append(t_r)

        if delta.days <=0:
            return HttpResponse('<h1>Please Enter Valid Date Range</h1>')


        if len(train_number)  == 0:
            main_trains = main_trains
        else:
            main_trains = train_number

        dataa = Main_Data_Upload.objects.filter(train_station__in = main_trains,registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"])
        print(dataa)
        data = []
        for dd in dataa:
            data.append(dd.rating)
        unsatis.append(data.count('Unsatisfactory'))
        satis.append(data.count('Satisfactory'))
        nan.append(data.count('nan'))
        excel.append(data.count('Excellent'))

        print(unsatis)

            # months.append(calendar.month_name[i])

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
            'nan':nan,
            'train_number':train_numbers,
            'start_date': start_date,
            'end_date':end_date
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


        start_date = None
        end_date = None


        context ={
            'show':show,
            'post':False,
            'unsatis':unsatis,
            'satis':satis,
            'excel':excel,
            'nan':nan,
            'train_number':train_numbers,
            # 'start_date':start_date,
            # 'end_date':end_date
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

        dates.reverse()
        coach_clean.reverse()
        bed_roll.reverse()
        security.reverse()
        medical_assis.reverse()
        punctuality.reverse()
        water_avail.reverse()
        electrical_equip.reverse()
        coach_maintain.reverse()
        miscellaneous.reverse()
        staff_behave.reverse()


    all_type=['Coach - Cleanliness','Bed Roll','Security','Medical Assistance',
              'Punctuality','Water Availability','Electrical Equipment','Coach - Maintenance',
              'Miscellaneous','Staff Behaviour']
    critical_type = ['Coach - Cleanliness','Bed Roll', 'Water Availability',
                     'Electrical Equipment','Coach - Maintenance',]

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
    if request.method != 'POST':
        start_date = None
        end_date = None
        post = False


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
        'demo_sub':demo_sub,
        'critical_type':critical_type,
        'start_date':start_date,
        'end_date':end_date
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
        dates.reverse()
        data_count.reverse()
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
                                                        'train_station',
                                                        'problem_type',
                                                        'sub_type',
                                                        'disposal_time',
                                                        'rating',
                                                        'registration_date',
                                                        'complaint_discription')
    problem_type = []
    for p in problem_types:
        if str(int(p[1])) == complain_type:
            problem_type.append(p)
        # if p[2] == complain_type or p[3] == complain_type or str(int(p[0])) == complain_type or str(int(p[1])) == complain_type or str(calendar.month_name[p[6].month]) == str(complain_type):
        #     problem_type.append(p)
        elif complain_type == "All_data":
            problem_type.append(p)

        elif complain_type == str(p[3]):
            problem_type.append(p)

        elif complain_type == str(p[2]):
            problem_type.append(p)

    context = {'complain_type':complain_type, 'problem_type':problem_type}
    return render(request, 'complain_type.html',context)






def train_wise_data(request):
    data_count=[]
    problem_type = Main_Data_Upload.objects.values_list('problem_type')
    train_numbers_list = Main_Data_Upload.objects.values_list('train_station')
    Type=[]
    for s in problem_type:
        for t in s:
            Type.append(t)

    train = []
    for tr_nums in train_numbers_list:
        train.append(tr_nums)
    train_numbers = set(train)


    problem_type = set(Type)

    if request.method == "POST":
        train_number = request.POST.getlist('train_number')
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")
        
        trains = []
        for t_r in train_number:
            trains.append(int(t_r))

        for p_t in problem_type:
            data = Main_Data_Upload.objects.filter(train_station__in=trains,problem_type=p_t,registration_date__gte=start_date,registration_date__lte=end_date)
            data_count.append(data.count())

        if sum(data_count) == 0:
            data_show = False
        else:
            data_show = True
        
        if request.method != 'POST':
            start_date = None
            end_date = None
            post = False

        context = {
                    'problem_type':problem_type,
                    'post':True,
                    'data_count':data_count,
                    'train':trains,
                    'data_show':data_show,
                    'train_number':train_numbers,
                    'start_date':start_date,
                    'end_date':end_date
                   }

    else:
        post = False
        context = {'post':post,'train_number':train_numbers}
    return render(request, "train_wise_data.html",context)






def bottom_train_data_pie(request):
    bottom_train = []
    bottom_data_count = []
    if request.method == "POST":
        post=True
        train_count  = int(request.POST.get('train_count',''))
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")
        
        data_count=[]
        problem_type = Main_Data_Upload.objects.values_list('problem_type')
        train_numbers = Main_Data_Upload.objects.all()

        Type=[]
        for s in problem_type:
            for t in s:
                Type.append(t)

        train_number = []
        str_train_number = [] 
        for t_n in train_numbers:
            train_number.append(t_n.train_station)
            str_train_number.append(str(t_n.train_station))

        problem_types = set(Type)

        for tr_n in train_number:
            a = Main_Data_Upload.objects.filter(problem_type__in=problem_types,train_station=tr_n,registration_date__gte=start_date,registration_date__lte=end_date)
            data_count.append(a.count())

        make_dict = dict(zip(str_train_number,data_count))
        a1_sorted_keys = sorted(make_dict, key=make_dict.get, reverse=True)
        for r in a1_sorted_keys:
            bottom_train.append(int(float(r)))
            bottom_data_count.append(make_dict[r])

    else:
        train_count = 10
        post = False
        data_count=[]
        problem_type = Main_Data_Upload.objects.values_list('problem_type')
        train_numbers = Main_Data_Upload.objects.all()

        Type=[]
        for s in problem_type:
            for t in s:
                Type.append(t)

        train_number = []
        str_train_number = [] 
        for t_n in train_numbers:
            train_number.append(t_n.train_station)
            str_train_number.append(str(t_n.train_station))

        problem_types = set(Type)

        for tr_n in train_number:
            a = Main_Data_Upload.objects.filter(problem_type__in=problem_types,train_station=tr_n)
            data_count.append(a.count())

        make_dict = dict(zip(str_train_number,data_count))
        a1_sorted_keys = sorted(make_dict, key=make_dict.get, reverse=True)
        for r in a1_sorted_keys:
            bottom_train.append(int(float(r)))
            bottom_data_count.append(make_dict[r])

    if request.method != 'POST':
        start_date = None
        end_date = None
        post = False
    
    context = {
                'bottom_train':bottom_train[0:train_count],
                'post':post,
                'bottom_data_count':bottom_data_count[0:train_count],
                'train_count':train_count,
                'start_date':start_date,
                'end_date':end_date
               }
    return render(request, "bottom_train_data_pie.html",context)








def bottom_train_data_bar(request):
    bottom_train = []
    bottom_data_count = []
    if request.method == "POST":
        post=True
        train_count  = int(request.POST.get('train_count',''))
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")
        
        data_count=[]
        problem_type = Main_Data_Upload.objects.values_list('problem_type')
        train_numbers = Main_Data_Upload.objects.all()

        Type=[]
        for s in problem_type:
            for t in s:
                Type.append(t)

        train_number = []
        str_train_number = [] 
        for t_n in train_numbers:
            train_number.append(t_n.train_station)
            str_train_number.append(str(t_n.train_station))

        problem_types = set(Type)

        for tr_n in train_number:
            a = Main_Data_Upload.objects.filter(problem_type__in=problem_types,train_station=tr_n,registration_date__gte=start_date,registration_date__lte=end_date)
            data_count.append(a.count())

        make_dict = dict(zip(str_train_number,data_count))
        a1_sorted_keys = sorted(make_dict, key=make_dict.get, reverse=True)
        for r in a1_sorted_keys:
            bottom_train.append(int(float(r)))
            bottom_data_count.append(make_dict[r])

    else:
        train_count=10
        post = False
        data_count=[]
        problem_type = Main_Data_Upload.objects.values_list('problem_type')
        train_numbers = Main_Data_Upload.objects.all()

        Type=[]
        for s in problem_type:
            for t in s:
                Type.append(t)

        train_number = []
        str_train_number = [] 
        for t_n in train_numbers:
            train_number.append(t_n.train_station)
            str_train_number.append(str(t_n.train_station))

        problem_types = set(Type)

        for tr_n in train_number:
            a = Main_Data_Upload.objects.filter(problem_type__in=problem_types,train_station=tr_n)
            data_count.append(a.count())

        make_dict = dict(zip(str_train_number,data_count))
        a1_sorted_keys = sorted(make_dict, key=make_dict.get, reverse=True)
        for r in a1_sorted_keys:
            bottom_train.append(int(float(r)))
            bottom_data_count.append(make_dict[r])
    
    context = {
                'bottom_train':bottom_train[0:train_count],
                'post':post,
                'bottom_data_count':bottom_data_count[0:train_count],
                'train_count':train_count
               }
    return render(request, "bottom_train_data_bar.html",context)









@login_required
def all_complain_train(request):
    train_numbers_list = Main_Data_Upload.objects.values_list('train_station')
    train = []
    for tr_nums in train_numbers_list:
        train.append(tr_nums)
    train_num = set(train)
    train_numbers = []
    for t_nums in train_num:
        for tt in t_nums:
            train_numbers.append(tt)


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
        
        else:
            for t_r in train_numbers:
                
                coach_clean_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r, problem_type = "Coach - Cleanliness")
                coach_clean.append(coach_clean_data.count())


                bed_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r,problem_type = "Bed Roll")
                bed_roll.append(bed_data.count())


                security_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r,problem_type = "Security")
                security.append(security_data.count())


                medical_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r,problem_type = "Medical Assistance")
                medical_assis.append(medical_data.count())


                punctuality_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r,problem_type = "Punctuality")
                punctuality.append(punctuality_data.count())


                water_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r,problem_type = "Water Availability")
                water_avail.append(water_data.count())


                electrical_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r,problem_type = "Electrical Equipment")
                electrical_equip.append(electrical_data.count())


                coach_maintain_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r,problem_type = "Coach - Maintenance")
                coach_maintain.append(coach_maintain_data.count())


                miscellaneous_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r,problem_type = "Miscellaneous")
                miscellaneous.append(miscellaneous_data.count())


                staff_behave_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station = t_r,problem_type = "Staff Behaviour")
                staff_behave.append(staff_behave_data.count())


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
        for t_r in train_numbers:
            coach_clean_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Coach - Cleanliness")
            coach_clean.append(coach_clean_data.count())

            bed_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Bed Roll")
            bed_roll.append(bed_data.count())

            security_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Security")
            security.append(security_data.count())


            medical_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Medical Assistance")
            medical_assis.append(medical_data.count())


            punctuality_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Punctuality")
            punctuality.append(punctuality_data.count())


            water_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Water Availability")
            water_avail.append(water_data.count())


            electrical_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Electrical Equipment")
            electrical_equip.append(electrical_data.count())


            coach_maintain_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Coach - Maintenance")
            coach_maintain.append(coach_maintain_data.count())


            miscellaneous_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Miscellaneous")
            miscellaneous.append(miscellaneous_data.count())


            staff_behave_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Staff Behaviour")
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

    if request.method != 'POST':
        start_date = None
        end_date = None
        post = False

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
        'demo_sub':demo_sub,
        'train_number':train_numbers,
        'start_date':start_date,
        'end_date':end_date
        }
    return render(request, 'all_complain_train.html',context)










def all_sub_complain_train(request,subtype):
    train_numbers_list = Main_Data_Upload.objects.values_list('train_station')
    train = []
    for tr_nums in train_numbers_list:
        train.append(tr_nums)
    train_num = set(train)
    train_numbers = []
    data_count = []
    for t_nums in train_num:
        for tt in t_nums:
            train_numbers.append(tt)

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


    if request.method == "POST":
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")


        for t_r in train_numbers:
            sub_type_data = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],sub_type=f"{subtypes}",train_station=t_r)
            data_count.append(sub_type_data.count())      
    
    else:
        for t_r in train_numbers:
            sub_type_data = Main_Data_Upload.objects.filter(sub_type=f"{subtypes}",train_station=t_r)
            data_count.append(sub_type_data.count())
    
    if request.method != "POST":
        start_date = None
        end_date = None
        post = False

    else:
        post=True
    context = {
                'post':post,
                'show':True,
                'data_count':data_count,
                'subtype':subtype,
                'subtypes':subtypes,
                'train_numbers':train_numbers,
                'start_date':start_date,
                'end_date':end_date
              }
    return render(request,'all_sub_complain_train.html',context)







def max_complain_train(request):
    main_all = Main_Data_Upload.objects.all()
    train_nums = []
    for m in main_all:
        train_nums.append(m.train_station)
    all_type=['Coach - Cleanliness','Bed Roll','Security','Medical Assistance',
              'Punctuality','Water Availability','Electrical Equipment','Coach - Maintenance',
              'Miscellaneous','Staff Behaviour']
    critical_type = ['Coach - Cleanliness','Bed Roll', 'Water Availability',
                     'Electrical Equipment','Coach - Maintenance',]
    train_numbers = set(train_nums)
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
    total = []
    if request.method == "POST":
        post = True
        complain_type = request.POST.getlist('complain_type')
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<center><h1>Please Enter valid date Range</center></h1>")

        for t_r in train_numbers:
            coach_clean_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Coach - Cleanliness")
            c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
            coach_clean.append(list(c1))

            bed_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Bed Roll")
            b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
            bed_roll.append(list(b1))

            security_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Security")
            s1 = (int(security_data.count()), int(t_r), "Security")
            security.append(list(s1))


            medical_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Medical Assistance")
            m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
            medical_assis.append(list(m1))


            punctuality_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Punctuality")
            p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
            punctuality.append(list(p1))


            water_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Water Availability")
            w1 = (int(water_data.count()), int(t_r), "Water Availability")
            water_avail.append(list(w1))


            electrical_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Electrical Equipment")
            e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
            electrical_equip.append(list(e1))


            coach_maintain_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Coach - Maintenance")
            c2 = (int(coach_maintain_data.count()), int(t_r) , "Coach - Maintenance")
            coach_maintain.append(list(c2))


            miscellaneous_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Miscellaneous")
            m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
            miscellaneous.append(list(m1))


            staff_behave_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Staff Behaviour")
            s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
            staff_behave.append(list(s2))
    else:
        for t_r in train_numbers:
            coach_clean_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Coach - Cleanliness")
            c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
            coach_clean.append(list(c1))

            bed_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Bed Roll")
            b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
            bed_roll.append(list(b1))

            security_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Security")
            s1 = (int(security_data.count()), int(t_r), "Security")
            security.append(list(s1))


            medical_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Medical Assistance")
            m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
            medical_assis.append(list(m1))


            punctuality_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Punctuality")
            p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
            punctuality.append(list(p1))


            water_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Water Availability")
            w1 = (int(water_data.count()), int(t_r), "Water Availability")
            water_avail.append(list(w1))


            electrical_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Electrical Equipment")
            e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
            electrical_equip.append(list(e1))


            coach_maintain_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Coach - Maintenance")
            c2 = (int(coach_maintain_data.count()), int(t_r) , "Coach - Maintenance")
            coach_maintain.append(list(c2))


            miscellaneous_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Miscellaneous")
            m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
            miscellaneous.append(list(m1))


            staff_behave_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Staff Behaviour")
            s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
            staff_behave.append(list(s2))


    coach_maintain.sort(key=lambda x: x[0])
    bed_roll.sort(key=lambda x: x[0])
    coach_clean.sort(key=lambda x: x[0])
    staff_behave.sort(key=lambda x: x[0])
    electrical_equip.sort(key=lambda x: x[0])
    water_avail.sort(key=lambda x: x[0])
    punctuality.sort(key=lambda x: x[0])
    security.sort(key=lambda x: x[0])
    medical_assis.sort(key=lambda x: x[0])
    miscellaneous.sort(key=lambda x: x[0])

    if request.method != "POST":
        total.append(coach_maintain[-1])
        total.append(bed_roll[-1])
        total.append(staff_behave[-1])
        total.append(electrical_equip[-1])
        total.append(water_avail[-1])
        total.append(punctuality[-1])
        total.append(security[-1])
        total.append(medical_assis[-1])
        total.append(miscellaneous[-1])
        total.append(coach_clean[-1])
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 
    else:
        if "Coach - Maintenance" in complain_type:
            total.append(coach_maintain[-1])
        if "Bed Roll" in complain_type:
            total.append(bed_roll[-1])
        if "Staff Behaviour" in complain_type:
            total.append(staff_behave[-1])
        if "Electrical Equipment" in complain_type:
            total.append(electrical_equip[-1])
        if "Water Availability" in complain_type:
            total.append(water_avail[-1])
        if "Punctuality" in complain_type:
            total.append(punctuality[-1])
        if "Security" in complain_type:
            total.append(security[-1])
        if "Medical Assistance" in complain_type:
            total.append(medical_assis[-1])
        if "Miscellaneous" in complain_type:
            total.append(miscellaneous[-1])
        if "Coach - Cleanliness" in complain_type:
            total.append(coach_clean[-1])
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 
    if request.method != "POST":
        start_date = None
        end_date = None
        post = False
    
    context = {'post':post,'total':total,'show':show,'all_type':all_type, 'critical_type':critical_type, 'start_date':start_date,
                'end_date':end_date}
    return render(request, 'max_complain_train.html',context)










def min_complain_train(request):
    main_all = Main_Data_Upload.objects.all()
    train_nums = []
    for m in main_all:
        train_nums.append(m.train_station)
    all_type=['Coach - Cleanliness','Bed Roll','Security','Medical Assistance',
              'Punctuality','Water Availability','Electrical Equipment','Coach - Maintenance',
              'Miscellaneous','Staff Behaviour']
    critical_type = ['Coach - Cleanliness','Bed Roll', 'Water Availability',
                     'Electrical Equipment','Coach - Maintenance',]
    train_numbers = set(train_nums)
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
    total = []
    if request.method == "POST":
        post = True
        complain_type = request.POST.getlist('complain_type')
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<center><h1>Please Enter valid date Range</center></h1>")

        for t_r in train_numbers:
            coach_clean_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Coach - Cleanliness")
            c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
            coach_clean.append(list(c1))

            bed_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Bed Roll")
            b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
            bed_roll.append(list(b1))

            security_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Security")
            s1 = (int(security_data.count()), int(t_r), "Security")
            security.append(list(s1))


            medical_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Medical Assistance")
            m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
            medical_assis.append(list(m1))


            punctuality_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Punctuality")
            p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
            punctuality.append(list(p1))


            water_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Water Availability")
            w1 = (int(water_data.count()), int(t_r), "Water Availability")
            water_avail.append(list(w1))


            electrical_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Electrical Equipment")
            e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
            electrical_equip.append(list(e1))


            coach_maintain_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Coach - Maintenance")
            c2 = (int(coach_maintain_data.count()), int(t_r) , "Coach - Maintenance")
            coach_maintain.append(list(c2))


            miscellaneous_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Miscellaneous")
            m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
            miscellaneous.append(list(m1))


            staff_behave_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,train_station = t_r ,problem_type = "Staff Behaviour")
            s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
            staff_behave.append(list(s2))
    else:
        for t_r in train_numbers:
            coach_clean_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Coach - Cleanliness")
            c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
            coach_clean.append(list(c1))

            bed_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Bed Roll")
            b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
            bed_roll.append(list(b1))

            security_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Security")
            s1 = (int(security_data.count()), int(t_r), "Security")
            security.append(list(s1))


            medical_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Medical Assistance")
            m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
            medical_assis.append(list(m1))


            punctuality_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Punctuality")
            p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
            punctuality.append(list(p1))


            water_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Water Availability")
            w1 = (int(water_data.count()), int(t_r), "Water Availability")
            water_avail.append(list(w1))


            electrical_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Electrical Equipment")
            e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
            electrical_equip.append(list(e1))


            coach_maintain_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Coach - Maintenance")
            c2 = (int(coach_maintain_data.count()), int(t_r) , "Coach - Maintenance")
            coach_maintain.append(list(c2))


            miscellaneous_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Miscellaneous")
            m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
            miscellaneous.append(list(m1))


            staff_behave_data = Main_Data_Upload.objects.filter(train_station = t_r ,problem_type = "Staff Behaviour")
            s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
            staff_behave.append(list(s2))


    coach_maintain.sort(key=lambda x: x[0])
    bed_roll.sort(key=lambda x: x[0])
    coach_clean.sort(key=lambda x: x[0])
    staff_behave.sort(key=lambda x: x[0])
    electrical_equip.sort(key=lambda x: x[0])
    water_avail.sort(key=lambda x: x[0])
    punctuality.sort(key=lambda x: x[0])
    security.sort(key=lambda x: x[0])
    medical_assis.sort(key=lambda x: x[0])
    miscellaneous.sort(key=lambda x: x[0])

    if request.method != "POST":
        total.append(coach_maintain[0])
        total.append(bed_roll[0])
        total.append(staff_behave[0])
        total.append(electrical_equip[0])
        total.append(water_avail[0])
        total.append(punctuality[0])
        total.append(security[0])
        total.append(medical_assis[0])
        total.append(miscellaneous[0])
        total.append(coach_clean[0])
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 
    else:
        if "Coach - Maintenance" in complain_type:
            total.append(coach_maintain[0])
        if "Bed Roll" in complain_type:
            total.append(bed_roll[0])
        if "Staff Behaviour" in complain_type:
            total.append(staff_behave[0])
        if "Electrical Equipment" in complain_type:
            total.append(electrical_equip[0])
        if "Water Availability" in complain_type:
            total.append(water_avail[0])
        if "Punctuality" in complain_type:
            total.append(punctuality[0])
        if "Security" in complain_type:
            total.append(security[0])
        if "Medical Assistance" in complain_type:
            total.append(medical_assis[0])
        if "Miscellaneous" in complain_type:
            total.append(miscellaneous[0])
        if "Coach - Cleanliness" in complain_type:
            total.append(coach_clean[0])
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 

    if request.method != "POST":
        start_date = None
        end_date = None   
        post = False
    context = {'post':post,'total':total,'show':show,'all_type':all_type, 'critical_type': critical_type, 'start_date':start_date,
                'end_date':end_date}
    return render(request, 'min_complain_train.html',context)

















def max_complain_coach(request):
    main_all = Main_Data_Upload.objects.all()
    coach = []
    for m in main_all:
        if m.coach_number == None:
            pass
        else:
            coach.append(m.coach_number)
    all_type=['Coach - Cleanliness','Bed Roll','Security','Medical Assistance',
              'Punctuality','Water Availability','Electrical Equipment','Coach - Maintenance',
              'Miscellaneous','Staff Behaviour']
    critical_type = ['Coach - Cleanliness','Bed Roll', 'Water Availability',
                     'Electrical Equipment','Coach - Maintenance',]
    coaches = set(coach)
    print(coaches)
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
    total = []
    if request.method == "POST":
        post = True
        complain_type = request.POST.getlist('complain_type')
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<center><h1>Please Enter valid date Range</center></h1>")

        for t_r in coaches:
            coach_clean_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Coach - Cleanliness")
            c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
            coach_clean.append(list(c1))

            bed_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Bed Roll")
            b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
            bed_roll.append(list(b1))

            security_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Security")
            s1 = (int(security_data.count()), int(t_r), "Security")
            security.append(list(s1))


            medical_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Medical Assistance")
            m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
            medical_assis.append(list(m1))


            punctuality_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Punctuality")
            p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
            punctuality.append(list(p1))


            water_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Water Availability")
            w1 = (int(water_data.count()), int(t_r), "Water Availability")
            water_avail.append(list(w1))


            electrical_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Electrical Equipment")
            e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
            electrical_equip.append(list(e1))


            coach_maintain_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Coach - Maintenance")
            c2 = (int(coach_maintain_data.count()), int(t_r) , "Coach - Maintenance")
            coach_maintain.append(list(c2))


            miscellaneous_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Miscellaneous")
            m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
            miscellaneous.append(list(m1))


            staff_behave_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Staff Behaviour")
            s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
            staff_behave.append(list(s2))
    else:
        for t_r in coaches:
            coach_clean_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Coach - Cleanliness")
            c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
            coach_clean.append(list(c1))

            bed_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Bed Roll")
            b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
            bed_roll.append(list(b1))

            security_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Security")
            s1 = (int(security_data.count()), int(t_r), "Security")
            security.append(list(s1))


            medical_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Medical Assistance")
            m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
            medical_assis.append(list(m1))


            punctuality_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Punctuality")
            p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
            punctuality.append(list(p1))


            water_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Water Availability")
            w1 = (int(water_data.count()), int(t_r), "Water Availability")
            water_avail.append(list(w1))


            electrical_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Electrical Equipment")
            e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
            electrical_equip.append(list(e1))


            coach_maintain_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Coach - Maintenance")
            c2 = (int(coach_maintain_data.count()), int(t_r) , "Coach - Maintenance")
            coach_maintain.append(list(c2))


            miscellaneous_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Miscellaneous")
            m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
            miscellaneous.append(list(m1))


            staff_behave_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Staff Behaviour")
            s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
            staff_behave.append(list(s2))


    coach_maintain.sort(key=lambda x: x[0])
    bed_roll.sort(key=lambda x: x[0])
    coach_clean.sort(key=lambda x: x[0])
    staff_behave.sort(key=lambda x: x[0])
    electrical_equip.sort(key=lambda x: x[0])
    water_avail.sort(key=lambda x: x[0])
    punctuality.sort(key=lambda x: x[0])
    security.sort(key=lambda x: x[0])
    medical_assis.sort(key=lambda x: x[0])
    miscellaneous.sort(key=lambda x: x[0])

    if request.method != "POST":
        total.append(coach_maintain[-1])
        total.append(bed_roll[-1])
        total.append(staff_behave[-1])
        total.append(electrical_equip[-1])
        total.append(water_avail[-1])
        total.append(punctuality[-1])
        total.append(security[-1])
        total.append(medical_assis[-1])
        total.append(miscellaneous[-1])
        total.append(coach_clean[-1])
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 
    else:
        if "Coach - Maintenance" in complain_type:
            total.append(coach_maintain[-1])
        if "Bed Roll" in complain_type:
            total.append(bed_roll[-1])
        if "Staff Behaviour" in complain_type:
            total.append(staff_behave[-1])
        if "Electrical Equipment" in complain_type:
            total.append(electrical_equip[-1])
        if "Water Availability" in complain_type:
            total.append(water_avail[-1])
        if "Punctuality" in complain_type:
            total.append(punctuality[-1])
        if "Security" in complain_type:
            total.append(security[-1])
        if "Medical Assistance" in complain_type:
            total.append(medical_assis[-1])
        if "Miscellaneous" in complain_type:
            total.append(miscellaneous[-1])
        if "Coach - Cleanliness" in complain_type:
            total.append(coach_clean[-1])
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 
    if request.method != "POST":
        start_date = None
        end_date = None
        post = False
    
    context = {'post':post,'total':total,'show':show,'all_type':all_type, 'critical_type': critical_type,'start_date':start_date,
                'end_date':end_date}
    return render(request, 'max_complain_coach.html',context)












def min_complain_coach(request):
    main_all = Main_Data_Upload.objects.all()
    coach = []
    for m in main_all:
        if m.coach_number == None:
            pass
        else:
            coach.append(m.coach_number)
    all_type=['Coach - Cleanliness','Bed Roll','Security','Medical Assistance',
              'Punctuality','Water Availability','Electrical Equipment','Coach - Maintenance',
              'Miscellaneous','Staff Behaviour']
    critical_type = ['Coach - Cleanliness','Bed Roll', 'Water Availability',
                     'Electrical Equipment','Coach - Maintenance',]
    coaches = set(coach)
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
    total = []
    if request.method == "POST":
        post = True
        complain_type = request.POST.getlist('complain_type')
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<center><h1>Please Enter valid date Range</center></h1>")

        for t_r in coaches:
            coach_clean_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Coach - Cleanliness")
            c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
            coach_clean.append(list(c1))

            bed_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Bed Roll")
            b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
            bed_roll.append(list(b1))

            security_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Security")
            s1 = (int(security_data.count()), int(t_r), "Security")
            security.append(list(s1))


            medical_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Medical Assistance")
            m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
            medical_assis.append(list(m1))


            punctuality_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Punctuality")
            p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
            punctuality.append(list(p1))


            water_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Water Availability")
            w1 = (int(water_data.count()), int(t_r), "Water Availability")
            water_avail.append(list(w1))


            electrical_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Electrical Equipment")
            e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
            electrical_equip.append(list(e1))


            coach_maintain_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Coach - Maintenance")
            c2 = (int(coach_maintain_data.count()), int(t_r) , "Coach - Maintenance")
            coach_maintain.append(list(c2))


            miscellaneous_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Miscellaneous")
            m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
            miscellaneous.append(list(m1))


            staff_behave_data = Main_Data_Upload.objects.filter(registration_date__gte=start_date,registration_date__lte=end_date,coach_number = t_r ,problem_type = "Staff Behaviour")
            s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
            staff_behave.append(list(s2))
    else:
        for t_r in coaches:
            coach_clean_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Coach - Cleanliness")
            c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
            coach_clean.append(list(c1))

            bed_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Bed Roll")
            b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
            bed_roll.append(list(b1))

            security_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Security")
            s1 = (int(security_data.count()), int(t_r), "Security")
            security.append(list(s1))


            medical_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Medical Assistance")
            m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
            medical_assis.append(list(m1))


            punctuality_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Punctuality")
            p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
            punctuality.append(list(p1))


            water_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Water Availability")
            w1 = (int(water_data.count()), int(t_r), "Water Availability")
            water_avail.append(list(w1))


            electrical_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Electrical Equipment")
            e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
            electrical_equip.append(list(e1))


            coach_maintain_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Coach - Maintenance")
            c2 = (int(coach_maintain_data.count()), int(t_r) , "Coach - Maintenance")
            coach_maintain.append(list(c2))


            miscellaneous_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Miscellaneous")
            m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
            miscellaneous.append(list(m1))


            staff_behave_data = Main_Data_Upload.objects.filter(coach_number = t_r ,problem_type = "Staff Behaviour")
            s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
            staff_behave.append(list(s2))


    coach_maintain.sort(key=lambda x: x[0])
    bed_roll.sort(key=lambda x: x[0])
    coach_clean.sort(key=lambda x: x[0])
    staff_behave.sort(key=lambda x: x[0])
    electrical_equip.sort(key=lambda x: x[0])
    water_avail.sort(key=lambda x: x[0])
    punctuality.sort(key=lambda x: x[0])
    security.sort(key=lambda x: x[0])
    medical_assis.sort(key=lambda x: x[0])
    miscellaneous.sort(key=lambda x: x[0])

    if request.method != "POST":
        total.append(coach_maintain[0])
        total.append(bed_roll[0])
        total.append(staff_behave[0])
        total.append(electrical_equip[0])
        total.append(water_avail[0])
        total.append(punctuality[0])
        total.append(security[0])
        total.append(medical_assis[0])
        total.append(miscellaneous[0])
        total.append(coach_clean[0])
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 
    else:
        if "Coach - Maintenance" in complain_type:
            total.append(coach_maintain[0])
        if "Bed Roll" in complain_type:
            total.append(bed_roll[0])
        if "Staff Behaviour" in complain_type:
            total.append(staff_behave[0])
        if "Electrical Equipment" in complain_type:
            total.append(electrical_equip[0])
        if "Water Availability" in complain_type:
            total.append(water_avail[0])
        if "Punctuality" in complain_type:
            total.append(punctuality[0])
        if "Security" in complain_type:
            total.append(security[0])
        if "Medical Assistance" in complain_type:
            total.append(medical_assis[0])
        if "Miscellaneous" in complain_type:
            total.append(miscellaneous[0])
        if "Coach - Cleanliness" in complain_type:
            total.append(coach_clean[0])
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 
    if request.method != "POST":
        start_date = None
        end_date = None
        post = False
    
    context = {'post':post,'total':total,'show':show,'all_type':all_type, 'critical_type':critical_type,'start_date':start_date,
                'end_date':end_date}
    return render(request, 'min_complain_coach.html',context)




import operator


def mix_chart(request):
    bottom_train = []
    bottom_data_count = []
    all_type=['Coach - Cleanliness','Bed Roll','Security','Medical Assistance',
              'Punctuality','Water Availability','Electrical Equipment','Coach - Maintenance',
              'Miscellaneous','Staff Behaviour']
    critical_type = ['Coach - Cleanliness','Bed Roll', 'Water Availability',
                     'Electrical Equipment','Coach - Maintenance',]
    color_code = ['#FF3838','#FFB3B3','#006441','#FF8300','#EEFF70','#00FF83','#00E8FF',
                '#4200FF','#BD00FF','#FF8ED3']
    coach_clean = []
    bed_roll = []
    security = []
    medical_assis = []
    punctuality = []
    water_avail = []
    electrical_equip = []
    coach_maintain = []
    miscellaneous = []
    total_entries = Main_Data_Upload.objects.count()
    staff_behave = []

    if request.method == "POST":
        post=True
        complain_type = request.POST.getlist('complain_type')
        train_count  = int(request.POST.get('train-count',''))
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(int(start_month.year), int(start_month.month), int(start_month.day))
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <=0:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")
        
        data_count=[]
        problem_type = Main_Data_Upload.objects.values_list('problem_type')
        train_numbers = Main_Data_Upload.objects.all()


        Type=[]
        for s in problem_type:
            for t in s:
                Type.append(t)

        train_number = []
        str_train_number = [] 
        for t_n in train_numbers:
            train_number.append(t_n.train_station)
            str_train_number.append(str(t_n.train_station))

        problem_types = set(Type)

        for tr_n in train_number:
            a = Main_Data_Upload.objects.filter(problem_type__in=problem_types,train_station=tr_n,registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"])
            data_count.append(a.count())

        make_dict = dict(zip(str_train_number,data_count))
        a1_sorted_keys = dict(sorted(make_dict.items(), key=operator.itemgetter(1),reverse=True))
        first_n = sorted(a1_sorted_keys, key=a1_sorted_keys.get, reverse=True)[:train_count]
        for r in first_n:
            print(int(float(r))," ---> ",make_dict[r])
            bottom_train.append(int(float(r)))
            bottom_data_count.append(make_dict[r])

            data1 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Coach - Cleanliness")
            coach_clean.append(data1.count())


            data2 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Bed Roll")
            bed_roll.append(data2.count())


            data3 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Security")
            security.append(data3.count())


            data4 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Medical Assistance")
            medical_assis.append(data4.count())


            data5 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Punctuality")
            punctuality.append(data5.count())


            data6 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Water Availability")
            water_avail.append(data6.count())


            data7 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Electrical Equipment")
            electrical_equip.append(data7.count())



            data8 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Coach - Maintenance")
            coach_maintain.append(data8.count())


            data9 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Miscellaneous")
            miscellaneous.append(data9.count())


            data10 = Main_Data_Upload.objects.filter(registration_date__range=[f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00"],train_station=float(r), problem_type = "Staff Behaviour")
            staff_behave.append(data10.count())

    else:
        train_count=10
        post = False
        data_count=[]
        problem_type = Main_Data_Upload.objects.values_list('problem_type')
        train_numbers = Main_Data_Upload.objects.all()

        Type=[]
        for s in problem_type:
            for t in s:
                Type.append(t)

        train_number = []
        str_train_number = [] 
        for t_n in train_numbers:
            train_number.append(t_n.train_station)
            str_train_number.append(str(t_n.train_station))

        problem_types = set(Type)

        for tr_n in train_number:
            a = Main_Data_Upload.objects.filter(problem_type__in=problem_types,train_station=tr_n)
            data_count.append(a.count())

        make_dict = dict(zip(str_train_number,data_count))
        a1_sorted_keys = dict(sorted(make_dict.items(), key=operator.itemgetter(1),reverse=True))
        first_n = sorted(a1_sorted_keys, key=a1_sorted_keys.get, reverse=True)[:train_count]
        for trains_nums in first_n:
            bottom_train.append(int(float(trains_nums)))
            bottom_data_count.append(make_dict[trains_nums])


            data1 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Coach - Cleanliness")
            coach_clean.append(data1.count())

            data2 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Bed Roll")
            bed_roll.append(data2.count())


            data3 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Security")
            security.append(data3.count())


            data4 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Medical Assistance")
            medical_assis.append(data4.count())


            data5 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Punctuality")
            punctuality.append(data5.count())


            data6 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Water Availability")
            water_avail.append(data6.count())


            data7 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Electrical Equipment")
            electrical_equip.append(data7.count())


            data8 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Coach - Maintenance")
            coach_maintain.append(data8.count())


            data9 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Miscellaneous")
            miscellaneous.append(data9.count())


            data10 = Main_Data_Upload.objects.filter(train_station=trains_nums, problem_type = "Staff Behaviour")
            staff_behave.append(data10.count())
    total = []
    if request.method != "POST":
        total.append(coach_maintain)
        total.append(bed_roll)
        total.append(staff_behave)
        total.append(electrical_equip)
        total.append(water_avail)
        total.append(punctuality)
        total.append(security)
        total.append(medical_assis)
        total.append(miscellaneous)
        total.append(coach_clean)
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 
    else:
        if "Coach - Maintenance" in complain_type:
            total.append(coach_maintain)
        if "Bed Roll" in complain_type:
            total.append(bed_roll)
        if "Staff Behaviour" in complain_type:
            total.append(staff_behave)
        if "Electrical Equipment" in complain_type:
            total.append(electrical_equip)
        if "Water Availability" in complain_type:
            total.append(water_avail)
        if "Punctuality" in complain_type:
            total.append(punctuality)
        if "Security" in complain_type:
            total.append(security)
        if "Medical Assistance" in complain_type:
            total.append(medical_assis)
        if "Miscellaneous" in complain_type:
            total.append(miscellaneous)
        if "Coach - Cleanliness" in complain_type:
            total.append(coach_clean)
        if len(total) == 0:
            show = False
        if len(total)>=1:
            show = True 
    if request.method != "POST":
        start_date = None
        end_date = None
        post = False
        complain_type = None

    context = {
                'bottom_train':bottom_train,
                'post':post,
                'bottom_data_count':bottom_data_count[0:train_count],
                'train_count':train_count,
                'total':total,
                'all_type':all_type,
                'critical_type': critical_type,
                'color_code':color_code,
                'total_entries': total_entries,
                'start_date':start_date,
                'end_date':end_date,
                'color_code':color_code,
                'complain_type':complain_type
               }
    return render(request, "responsive.html",context)

