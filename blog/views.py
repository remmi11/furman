from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Form, FormAll, MasterGeom, County
from .forms import PostForm, newForm, UserForm, UserEditForm
from django.shortcuts import redirect
from django.shortcuts import render
from .models import *
#from django.utils import simplejson
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import time
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
from textwrap import wrap

from django.db.models import Q

# from django.core.cache import caches
# from mysite.settings import M_CLIENT

# def post_list(request):
#     posts = Form.objects.all() #filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_list(request):
    # filter(published_date__lte=timezone.now()).order_by('published_date')
    # posts = FormAll.objects.all()[:100]
    return render(request, 'blog/post_list.html', {})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Form, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def ajaxPagination(request):
    start = int(request.GET.get("start"))
    length = int(request.GET.get("length"))
    draw = int(request.GET.get("draw"))
    search_key = request.GET.get('search[value]')
    if search_key == None or search_key == "":
        count = FormAll.objects.all().count()
        posts = FormAll.objects.all().order_by('pk')[start:start+length]
    else:
        condition = Q(pk__icontains=search_key) | Q(project_no__icontains=search_key) | \
            Q(survey_type__icontains=search_key) | Q(client__icontains=search_key) | \
            Q(county__icontains=search_key) | Q(address_street__icontains=search_key) | \
            Q(survey__icontains=search_key) | Q(rural_block__icontains=search_key) | \
            Q(rural_section__icontains=search_key) | Q(subdivision__icontains=search_key) | \
            Q(unit__icontains=search_key) | Q(sub_block__icontains=search_key) | \
            Q(lot__icontains=search_key) | Q(meridian__icontains=search_key) | \
            Q(t_r__icontains=search_key) | Q(plss_section__icontains=search_key)
        count = FormAll.objects.filter(condition).count()
        posts = FormAll.objects.filter(condition).order_by('pk')[start:start+length]

    data = []
    for post in posts:
        data.append([post.pk, post.project_no, post.survey_type, \
            post.client, post.county, post.address_street, post.survey, \
            post.rural_block, post.rural_section, post.subdivision, \
            post.unit, post.sub_block, post.lot, post.meridian, post.t_r, \
            post.plss_section, \
            '<a class="btn btn-default" href="/post/'+str(post.pk)+'/edit/"> \
                    <span><i class="fa fa-pencil" style="font-size:24px"></i></span> \
                </a> <a class="btn btn-default" target="_blank" href="/get_pdf/'+str(post.pk)+'/"> \
                <span><i class="fa fa-eye" style="font-size:24px"></i></span> \
            </a>'])
    posts = {
            "draw": draw,
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": data
        }
    return HttpResponse(json.dumps(posts), content_type='application/json')

@login_required
def ajaxClientData(request):
    clients = []
    temp = FormAll.objects.all().distinct('client')
    clients = [tp.client for tp in temp if tp.client != None]
    return HttpResponse(json.dumps(clients), content_type='application/json')

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            form.save()
            return render(request, 'blog/post_list.html', {'posts': posts})
            #return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        join_type = MasterGeom.objects.all().distinct('join_type')
    return render(request, 'blog/post_new.html', {'form': form, 'join_types': join_type})

def loadCounties(request):
    #survey_types = MasterGeom.objects.all().distinct('join_type')
    # county_id = request.GET.get('surveytype')
    # print (county_id)
    result_set = []
    counties = MasterGeom.objects.filter(join_type=request.GET.get('join_type')).distinct('county')
    
    for county in counties:
        if county == None:
            continue
        result_set.append(county.county)
    #counties = MasterGeom.objects.filter(join_type=county_id).order_by('county_code')
    return HttpResponse(json.dumps(result_set), content_type='application/json')

@login_required
def getdetails(request):
    result_set = []
    tmp_res = []
    tokens = []

    join_type = request.GET.get("join_type")
    county = request.GET.get("county")
    type_val = request.GET.get("type")

    res = MasterGeom.objects.filter(join_type=join_type, county=county).distinct('join_field')
    for element in res:
        if element == None or element.join_field == None:
            continue
        tokens.append([tmp.strip() for tmp in element.join_field.split("\\") \
            if tmp.strip()!="" and county.lower() != tmp.strip().lower()])

    for token in tokens:
        if type_val in ["survey", "subdivision", "meridian"]:
            try:
                if token[0] not in tmp_res:
                    tmp_res.append(token[0].strip())
            except:
                pass
        elif type_val in ["unit", "block", "town_range"]:
            level1 = request.GET.get("level1")
            try:
                if token[1] not in tmp_res and level1.lower() == token[0].strip().lower():
                    tmp_res.append(token[1].strip())
            except:
                pass
        elif type_val in ["subblock", "rural_section", "section"]:
            level1 = request.GET.get("level1")
            level2 = request.GET.get("level2")
            try:
                if token[2] not in tmp_res and level1.lower() == token[0].strip().lower() and \
                        level2.lower() == token[1].strip().lower():
                    tmp_res.append(token[2].strip())
            except:
                pass
        elif type_val == "lot":
            level1 = request.GET.get("level1")
            level2 = request.GET.get("level2")
            level3 = request.GET.get("level3")
            try:
                if level2.lower() == token[1].strip().lower() and \
                        token[3] not in tmp_res and level1.lower() == token[0].strip().lower() and \
                        level3.lower() == token[2].strip().lower():
                    tmp_res.append(token[3].strip())
            except:
                pass

    for tp in tmp_res:
        if tp == None:
            continue
        result_set.append(tp)

    return HttpResponse(json.dumps(result_set), content_type='application/json')

'''@login_required
def getdetails(request):
    
    #country_name = request.POST['country_name']
    country_name = request.GET['surveytype']
    print ("ajax country_name " + country_name)

    result_set = []
    all_cities = []

    answer = str(country_name[1:-1])
    selected_country = MasterGeom.objects.get(join_type=answer)
    print ("selected country name ", selected_country)

    all_cities = selected_country.city_set.all()
    for city in all_cities:
        print ("city name", city.county)
        result_set.append({'name': city.county})

    return HttpResponse(simplejson.dumps(result_set), mimetype='application/json', content_type='application/json')'''

@login_required
def post_edit(request, pk):
    posts = FormAll.objects.all()
    post = get_object_or_404(FormAll, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            post.date_entered = timezone.now()
            post.date_needed = None if request.POST.get('date-needed') == "" else request.POST.get('date-needed')
            post.client = request.POST.get('client')
            post.project_no = request.POST.get('projectno')
            post.map_no = request.POST.get('mapno')
            post.contact = request.POST.get('jobcontact')
            post.phone = request.POST.get('phone')
            post.notes = request.POST.get('notes')
            post.certify_to = request.POST.get('certify')
            post.lender = request.POST.get('lender')
            post.gf_no = request.POST.get('gf')
            post.survey_type = request.POST.get('surveytype')
            if request.POST.get('surveytype') == "prad":
                post.county = request.POST.get('county')
                post.subdivision = request.POST.get('subdivision')
                post.unit = request.POST.get('unit')
                post.sub_block = request.POST.get('subblock')
                post.lot = request.POST.get('lot')
            elif request.POST.get('surveytype') == "rural":
                post.survey = request.POST.get('survey')
                post.rural_block = request.POST.get('block')
                post.rural_section = request.POST.get('rural_section')
            else:
                post.meridian = request.POST.get('meridian')
                post.t_r = request.POST.get('town_range')
                post.plss_section = request.POST.get('section')
            post.folder_path = request.POST.get('fpath')

            form.save()
            return render(request, 'blog/post_list.html', {'posts': posts})
            # return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        join_types = ['prad', 'plss', 'rural']#MasterGeom.objects.all().distinct('join_type')
        
        '''if M_CLIENT.get("counties-%s" % post.survey_type):
            print ("pp" * 20)
            data = json.loads(M_CLIENT.get("counties-%s" % post.survey_type).decode("utf8"))
            counties = data

        else:'''
        counties = MasterGeom.objects.filter(join_type=post.survey_type).distinct('county')
        counties = [tp.county.strip() for tp in counties if tp.county!=None]

        # M_CLIENT.set("counties-%s" % post.survey_type, json.dumps(counties))

        res = MasterGeom.objects.filter(join_type=post.survey_type, county=post.county.title()).distinct('join_field')
        
        level = [[], [], [], []]
        tokens = []

        for element in res:
            if element == None or element.join_field == None:
                continue
            tokens.append([tmp.strip() for tmp in element.join_field.split("\\") \
                if tmp.strip()!="" and post.county.lower() != tmp.strip().lower()])


        if post.survey_type == "prad":
            keys = [post.subdivision, post.unit, post.sub_block, post.lot]
        elif post.survey_type == "plss":
            keys = [post.meridian, post.t_r, post.plss_section, ""]
        elif post.survey_type == "rural":
            keys = [post.survey, post.rural_block, post.rural_section, ""]

        for token in tokens:
            try:
                if token[0] not in level[0]:
                    level[0].append(token[0])
            except:
                pass
            try:
                if token[0].lower() == keys[0].lower() and token[1] not in level[1]:
                    level[1].append(token[1])
            except:
                pass
            try:
                if token[0].lower() == keys[0].lower() and \
                    token[1].lower() == keys[1].lower() and token[2] not in level[2]:
                    level[2].append(token[2])
            except:
                pass
            try:
                if token[0].lower() == keys[0].lower() and \
                    token[1].lower() == keys[1].lower() and \
                    token[2].lower() == keys[2].lower() and token[3] not in level[3]:
                    level[3].append(token[3])
            except:
                pass

        # print (level)
        # print (keys)


    return render(request, 'blog/post_edit.html', {'form': form, "join_types": join_types, \
        'counties': counties, "level1": level[0], "level2": level[1], \
        "level3": level[2], "level4": level[3], 'pk': post.pk})

# def post_edit(request, pk):
#     posts = Form.objects.all()
#     post = get_object_or_404(Form, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             #post.date_entered=request.POST.get('date_entered')
#             #post.date_needed=request.POST.get('date_needed')
#             #post.client=request.POST.get('client')
#             #post.project_no = request.POST.get('project_no')
#             post.project_no=request.POST.get('project_no')
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             # return redirect('post_detail', pk=post.pk)
#             return render(request, 'blog/post_list.html', {'posts': posts})

#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def user_list(request):

    if not request.user.is_superuser:
        return redirect('/')

    # filter(published_date__lte=timezone.now()).order_by('published_date')
    users = Users.objects.all().order_by('pk')
    return render(request, 'registration/user_list.html', {'users': users})

@login_required
def user_new(request):
    if not request.user.is_superuser:
        return redirect('/')

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
            form.cleaned_data['password'])
            new_user.save()

            return redirect('/user/')
    else:
        form = UserForm()
    return render(request, 'registration/user_new.html', {'user_form': form})

@login_required
def user_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('/')

    users = Users.objects.all()
    user = get_object_or_404(Users, pk=pk)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if request.POST.get('new_password') != "":
                user.set_password(request.POST.get('new_password'))
            user.save()
            return redirect('/user/')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'registration/user_edit.html', {'user_form': form})

@login_required
def user_remove(request, pk):
    if not request.user.is_superuser:
        return redirect('/')

    user = get_object_or_404(Users, pk=pk)
    if user:
        user.delete()

    return redirect('/user/')

def drawText(canvasObj, text, length, x, y, line_space=22):
    if text == "":
        return 1
    wraped_text = wrap(text, length)
    for index in range(0, len(wraped_text)):
        canvasObj.drawString(x, y-(index+1)*line_space, wraped_text[index])

    return len(wraped_text)

def clean(data):
    return "" if data == None else data
def cleanDate(data):
    try:
        return data.strftime('%m/%d/%Y')
    except:
        return ""

@login_required
def getpdf(request, pk):
    post = get_object_or_404(FormAll, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%sWO.pdf"' % post.project_no

    start_x = 50
    start_y = 680
    line_space = 22
    bgColor = colors.Color(red=(211.0/255),green=(211.0/255),blue=(211.0/255))

    canvas1 = canvas.Canvas(response, pagesize=letter)
    canvas1.setLineWidth(.3)

    canvas1.setFont('Helvetica-Bold', 15)
    canvas1.drawString(start_x+140,start_y+40, clean(post.title))

    canvas1.setFont('Helvetica', 12)
     
    canvas1.drawString(start_x+50,start_y,'Date Created %s' % cleanDate(post.date_entered))

    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,start_y-85,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, start_y-80,'Client Info')

    canvas1.drawString(start_x, start_y-80-line_space,'Client')
    lines = drawText(canvas1, clean(post.client), 17, start_x+130, start_y-80)

    offsetY = start_y-180-lines*line_space
    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,offsetY-5,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, offsetY,'Client Info')

    canvas1.drawString(start_x, offsetY-line_space,'Job Contact')
    lines = drawText(canvas1, clean(post.contact), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Job Phone')
    lines = drawText(canvas1, clean(post.phone), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space


    canvas1.drawString(start_x, offsetY-line_space,'Job City')
    lines = drawText(canvas1, clean(post.city), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'JobSt:')
    linesst = drawText(canvas1, clean(post.state), 13, start_x+40, offsetY)
    canvas1.drawString(start_x+130, offsetY-line_space,'JobZip:')
    lineszip = drawText(canvas1, clean(post.zipcode), 13, start_x+180, offsetY)
    lines = linesst if linesst > lineszip else lineszip

    offsetY = offsetY - 80 - lines*line_space
    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,offsetY-5,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, offsetY,'Notes')

    lines = drawText(canvas1, clean(post.notes), 40, start_x, offsetY)
    offsetY = offsetY-lines*line_space-80

    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,offsetY-5,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, offsetY,'Certify To:')

    canvas1.drawString(start_x, offsetY-line_space,'Certify To')
    lines = drawText(canvas1, clean(post.certify_to), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Lender')
    lines = drawText(canvas1, clean(post.lender), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Gf#')
    lines = drawText(canvas1, clean(post.gf_no), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    start_x = 310
    canvas1.setFont('Helvetica-Bold', 12)
    canvas1.drawString(start_x+60,start_y,'Survey Work Order')
    canvas1.line(start_x+60,start_y-2,start_x+165,start_y-2)

    offsetY = start_y - 20
    canvas1.setFont('Helvetica', 12)
    canvas1.drawString(start_x+60, offsetY-18,'Project #')
    lines = drawText(canvas1, clean(post.project_no), 17, start_x+150, offsetY, 20)
    offsetY = offsetY-lines*18

    canvas1.drawString(start_x+60, offsetY-18,'Date Needed')
    lines = drawText(canvas1, cleanDate(post.date_needed), 17, start_x+150, offsetY, 20)
    offsetY = offsetY-lines*18

    canvas1.drawString(start_x+60, offsetY-18,'Requested By')
    lines = drawText(canvas1, clean(post.surveyor), 17, start_x+150, offsetY, 20)
    offsetY = offsetY-lines*18

    offsetY = offsetY - 65
    start_x = start_x + 12
    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,offsetY-5,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, offsetY,'Job Location')

    canvas1.drawString(start_x, offsetY-line_space,'Address')
    lines = drawText(canvas1, clean(post.address_street), 15, start_x+140, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'City')
    lines = drawText(canvas1, clean(post.city), 15, start_x+140, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'State / Province / Region')
    lines = drawText(canvas1, clean(post.state), 15, start_x+140, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Postal / Zip Code')
    lines = drawText(canvas1, clean(post.zipcode), 15, start_x+140, offsetY)
    offsetY = offsetY-lines*line_space

    offsetY = offsetY - 65
    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,offsetY-5,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, offsetY,'Legal')

    canvas1.drawString(start_x, offsetY-line_space,'County')
    lines = drawText(canvas1, clean(post.county), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    if post.survey_type == "prad":
        canvas1.drawString(start_x, offsetY-line_space,'Subdivision')
        lines = drawText(canvas1, clean(post.subdivision), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space

        canvas1.drawString(start_x, offsetY-line_space,'Unit')
        lines = drawText(canvas1, clean(post.unit), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space

        canvas1.drawString(start_x, offsetY-line_space,'Block')
        lines = drawText(canvas1, clean(post.sub_block), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space

        canvas1.drawString(start_x, offsetY-line_space,'Lot')
        lines = drawText(canvas1, clean(post.lot), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space
    elif post.survey_type == "plss":
        canvas1.drawString(start_x, offsetY-line_space,'Meridian')
        lines = drawText(canvas1, clean(post.meridian), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space

        canvas1.drawString(start_x, offsetY-line_space,'Twnshp/Range')
        lines = drawText(canvas1,clean(post.t_r), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space

        canvas1.drawString(start_x, offsetY-line_space,'Section')
        lines = drawText(canvas1, clean(post.plss_section), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space
    elif post.survey_type == "rural":
        canvas1.drawString(start_x, offsetY-line_space,'Survey')
        lines = drawText(canvas1, clean(post.survey), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space

        canvas1.drawString(start_x, offsetY-line_space,'Block')
        lines = drawText(canvas1, clean(post.rural_block), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space

        canvas1.drawString(start_x, offsetY-line_space,'Section')
        lines = drawText(canvas1, clean(post.rural_section), 17, start_x+130, offsetY)
        offsetY = offsetY-lines*line_space

    canvas1.save()
    return response