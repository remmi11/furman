from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import FormAll, MasterGeom, County
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
from django.views.decorators.csrf import csrf_exempt

@login_required
def post_list(request):
    return render(request, 'blog/post_list.html', {})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Form, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
@csrf_exempt
def ajaxPagination(request):
    order_cols = ['pk', 'project_no', 'survey_type', 'client', 'map_no', 'county', 'address_street',
                    'survey', 'rural_block', 'rural_section', 'subdivision', 
                    'unit', 'sub_block', 'lot', 'meridian', 't_r', 'plss_section', 'notes', 'aka']

    start = int(request.POST.get("start"))
    length = int(request.POST.get("length"))
    draw = int(request.POST.get("draw"))
    search_key = request.POST.get('search[value]')

    order_col = request.POST.get('order[0][column]')
    order_type = request.POST.get('order[0][dir]')
    order_key = order_cols[int(order_col)] if order_type == "asc" else "-" + order_cols[int(order_col)]
        
    condition = None

    col_search_key = request.POST.get('columns[0][search][value]')
    if col_search_key != "":
        condition = condition & Q(pk__icontains=col_search_key) if condition != None else Q(pk__icontains=col_search_key)
    col_search_key = request.POST.get('columns[1][search][value]')
    if col_search_key != "":
        condition = condition & Q(project_no__icontains=col_search_key) if condition != None else Q(project_no__icontains=col_search_key)
    col_search_key = request.POST.get('columns[2][search][value]')
    if col_search_key != "":
        condition = condition & Q(survey_type__icontains=col_search_key) if condition != None else Q(survey_type__icontains=col_search_key)
    col_search_key = request.POST.get('columns[3][search][value]')
    if col_search_key != "":
        condition = condition & Q(client__icontains=col_search_key) if condition != None else Q(client__icontains=col_search_key)
    col_search_key = request.POST.get('columns[4][search][value]')
    if col_search_key != "":
        condition = condition & Q(map_no__icontains=col_search_key) if condition != None else Q(map_no__icontains=col_search_key)
    col_search_key = request.POST.get('columns[5][search][value]')
    if col_search_key != "":
        condition = condition & Q(county__icontains=col_search_key) if condition != None else Q(county__icontains=col_search_key)
    col_search_key = request.POST.get('columns[6][search][value]')
    if col_search_key != "":
        condition = condition & Q(address_street__icontains=col_search_key) if condition != None else Q(address_street__icontains=col_search_key)
    col_search_key = request.POST.get('columns[7][search][value]')
    if col_search_key != "":
        condition = condition & Q(survey__icontains=col_search_key) if condition != None else Q(survey__icontains=col_search_key)
    col_search_key = request.POST.get('columns[8][search][value]')
    if col_search_key != "":
        condition = condition & Q(rural_block__icontains=col_search_key) if condition != None else Q(rural_block__icontains=col_search_key)
    col_search_key = request.POST.get('columns[9][search][value]')
    if col_search_key != "":
        condition = condition & Q(rural_section__icontains=col_search_key) if condition != None else Q(rural_section__icontains=col_search_key)
    col_search_key = request.POST.get('columns[10][search][value]')
    if col_search_key != "":
        condition = condition & Q(subdivision__icontains=col_search_key) if condition != None else Q(subdivision__icontains=col_search_key)
    col_search_key = request.POST.get('columns[11][search][value]')
    if col_search_key != "":
        condition = condition & Q(unit__icontains=col_search_key) if condition != None else Q(unit__icontains=col_search_key)
    col_search_key = request.POST.get('columns[12][search][value]')
    if col_search_key != "":
        condition = condition & Q(sub_block__icontains=col_search_key) if condition != None else Q(sub_block__icontains=col_search_key)
    col_search_key = request.POST.get('columns[13][search][value]')
    if col_search_key != "":
        condition = condition & Q(lot__icontains=col_search_key) if condition != None else Q(lot__icontains=col_search_key)
    col_search_key = request.POST.get('columns[14][search][value]')
    if col_search_key != "":
        condition = condition & Q(meridian__icontains=col_search_key) if condition != None else Q(meridian__icontains=col_search_key)
    col_search_key = request.POST.get('columns[15][search][value]')
    if col_search_key != "":
        condition = condition & Q(t_r__icontains=col_search_key) if condition != None else Q(t_r__icontains=col_search_key)
    col_search_key = request.POST.get('columns[16][search][value]')
    if col_search_key != "":
        condition = condition & Q(plss_section__icontains=col_search_key) if condition != None else Q(plss_section__icontains=col_search_key)
    col_search_key = request.POST.get('columns[17][search][value]')
    if col_search_key != "":
        condition = condition & Q(notes__icontains=col_search_key) if condition != None else Q(notes__icontains=col_search_key)
    col_search_key = request.POST.get('columns[18][search][value]')
    if col_search_key != "":
        condition = condition & Q(aka__icontains=col_search_key) if condition != None else Q(aka__icontains=col_search_key)
    col_search_key = request.POST.get('columns[19][search][value]')
    if col_search_key != "":
        condition = condition & Q(folder_path__icontains=col_search_key) if condition != None else Q(folder_path__icontains=col_search_key)

    if condition == None and (search_key == None or search_key == ""):
        count = FormAll.objects.all().count()
        posts = FormAll.objects.all().order_by(order_key)[start:start+length]
    else:
        if search_key != None and search_key != "":
            condition_global = (Q(pk__icontains=search_key) | Q(project_no__icontains=search_key) | \
                Q(survey_type__icontains=search_key) | Q(client__icontains=search_key) | Q(map_no__icontains=search_key) | \
                Q(county__icontains=search_key) | Q(address_street__icontains=search_key) | \
                Q(survey__icontains=search_key) | Q(rural_block__icontains=search_key) | \
                Q(rural_section__icontains=search_key) | Q(subdivision__icontains=search_key) | \
                Q(unit__icontains=search_key) | Q(sub_block__icontains=search_key) | \
                Q(lot__icontains=search_key) | Q(meridian__icontains=search_key) | \
                Q(t_r__icontains=search_key) | Q(plss_section__icontains=search_key) \
                | Q(notes__icontains=search_key) | Q(aka__icontains=search_key))

            condition = condition & condition_global if condition != None else condition_global

        count = FormAll.objects.filter(condition).count()
        posts = FormAll.objects.filter(condition).order_by(order_key)[start:start+length]

    data = []
    for post in posts:
        if request.user.edit_auth:
            action_buttons = '<a class="btn btn-default" href="/post/'+str(post.pk)+'/edit/"> \
                        <span><i class="fa fa-pencil" style="font-size:24px"></i></span> \
                    </a> <a class="btn btn-default" target="_blank" href="/get_pdf/'+str(post.pk)+'/"> \
                    <span><i class="fa fa-eye" style="font-size:24px"></i></span> \
                </a>'
        else:
            action_buttons = '<a class="btn btn-default" target="_blank" href="/get_pdf/'+str(post.pk)+'/"> \
                    <span><i class="fa fa-eye" style="font-size:24px"></i></span> \
                </a>'

        data.append([post.pk, post.project_no, post.survey_type, \
            post.client, post.map_no, post.county, post.address_street, post.survey, \
            post.rural_block, post.rural_section, post.subdivision, \
            post.unit, post.sub_block, post.lot, post.meridian, post.t_r, \
            post.plss_section, post.notes, post.aka, \
            '<a class="btn btn-default" href="'+str(post.folder_path)+'" target="_blank" title="'+str(post.folder_path)+'"> \
                    <span><i class="fa fa-external-link" style="font-size:24px"></i></span> \
                </a>', action_buttons])
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
    if request.user.edit_auth == False:
        get_object_or_404(FormAll, pk=None)
        
    posts = FormAll.objects.all()
    errors = ""
    if request.method == "POST":
        count = FormAll.objects.filter(project_no=request.POST.get('projectno')).count()
        if count == 0:
            form = PostForm(request.POST)
            if form.is_valid() and count == 0:
                post = form.save(commit=False)
                post.date_entered = timezone.now()
                post.date_needed = None if request.POST.get('date-needed') == "" else request.POST.get('date-needed')
                post.client = request.POST.get('client')
                post.project_no = request.POST.get('projectno')
                post.map_no = request.POST.get('mapno')
                post.contact = request.POST.get('jobcontact')
                post.client_address = request.POST.get('clientaddress')
                post.phone = request.POST.get('phone')
                post.notes = request.POST.get('notes')
                post.certify_to = request.POST.get('certify')
                post.lender = request.POST.get('lender')
                post.gf_no = request.POST.get('gf')
                post.survey_type = request.POST.get('surveytype')
                post.clerksfile = request.POST.get('clerksfile')
                post.requested_by = request.POST.get('requested_by')
                if request.POST.get('surveytype') == "prad":
                    post.county = request.POST.get('county')
                    post.subdivision = request.POST.get('subdivision')
                    post.unit = request.POST.get('unit')
                    post.sub_block = request.POST.get('subblock')
                    post.lot = request.POST.get('lot')
                    post.join_field = "\\".join([post.county, post.subdivision, post.unit, post.sub_block, post.lot])
                elif request.POST.get('surveytype') == "rural":
                    post.county = request.POST.get('county')
                    post.survey = request.POST.get('survey')
                    post.rural_block = request.POST.get('block')
                    post.rural_section = request.POST.get('rural_section')
                    post.join_field = "\\".join([post.county, post.survey, post.rural_block, post.rural_section])
                else:
                    post.county = request.POST.get('county')
                    post.meridian = request.POST.get('meridian')
                    post.t_r = request.POST.get('town_range')
                    post.plss_section = request.POST.get('section')
                    post.join_field = "\\".join([post.county, post.meridian, post.t_r, post.plss_section])
                post.folder_path = request.POST.get('fpath')

                form.save()
                
                return redirect("/post/%d/edit/" % post.pk)
        else:
            errors = "The project number is already exited."

    form = PostForm()
    join_type = MasterGeom.objects.all().distinct('join_type')
    return render(request, 'blog/post_new.html', {'form': form, 'join_types': join_type, 'errors': errors})


def loadCounties(request):
    result_set = []
    counties = MasterGeom.objects.filter(join_type=request.GET.get('join_type')).distinct('county')
    
    for county in counties:
        if county == None:
            continue
        result_set.append(county.county)
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

@login_required
def post_edit(request, pk):
    if request.user.edit_auth == False:
        get_object_or_404(FormAll, pk=None)

    posts = FormAll.objects.all()
    post = get_object_or_404(FormAll, pk=pk)
    errors = ""

    if request.method == "POST":
        count = FormAll.objects.filter(Q(project_no=request.POST.get('projectno')) & ~Q(pk=request.POST.get('post_id'))).count()

        if count == 0:
            form = PostForm(request.POST, instance=post)
            if form.is_valid() and count == 0:
                post.date_entered = timezone.now()
                post.date_needed = None if request.POST.get('date-needed') == "" else request.POST.get('date-needed')
                post.client = request.POST.get('client')
                post.project_no = request.POST.get('projectno')
                post.map_no = request.POST.get('mapno')
                post.contact = request.POST.get('jobcontact')
                post.client_address = request.POST.get('clientaddress')
                post.phone = request.POST.get('phone')
                post.notes = request.POST.get('notes')
                post.certify_to = request.POST.get('certify')
                post.lender = request.POST.get('lender')
                post.gf_no = request.POST.get('gf')
                post.survey_type = request.POST.get('surveytype')
                post.clerksfile = request.POST.get('clerksfile')
                post.requested_by = request.POST.get('requested_by')
                if request.POST.get('surveytype') == "prad":
                    post.county = request.POST.get('county')
                    post.subdivision = request.POST.get('subdivision')
                    post.unit = request.POST.get('unit')
                    post.sub_block = request.POST.get('subblock')
                    post.lot = request.POST.get('lot')
                    post.join_field = "\\".join([post.subdivision, post.unit, post.sub_block, post.lot])
                elif request.POST.get('surveytype') == "rural":
                    post.county = request.POST.get('county')
                    post.survey = request.POST.get('survey')
                    post.rural_block = request.POST.get('block')
                    post.rural_section = request.POST.get('rural_section')
                    post.join_field = "\\".join([post.county, post.survey, post.rural_block, post.rural_section])
                else:
                    post.county = request.POST.get('county')
                    post.meridian = request.POST.get('meridian')
                    post.t_r = request.POST.get('town_range')
                    post.plss_section = request.POST.get('section')
                    post.join_field = "\\".join([post.county, post.meridian, post.t_r, post.plss_section])
                post.folder_path = request.POST.get('fpath')

                form.save()
                return redirect("/post/%d/edit/" % post.pk)
        else:
            errors = "The project number is already exited."

    form = PostForm(instance=post)
    join_types = ['prad', 'plss', 'rural']#MasterGeom.objects.all().distinct('join_type')
    
    counties = MasterGeom.objects.filter(join_type=post.survey_type).distinct('county')
    counties = [tp.county.strip() for tp in counties if tp.county!=None]

    res = MasterGeom.objects.filter(join_type=post.survey_type, county=post.county).distinct('join_field')
    
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
        "level3": level[2], "level4": level[3], 'pk': post.pk, "errors": errors, 'post': post})

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
def update_profile(request, pk):
    if not request.user.pk != pk: 
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
    return render(request, 'registration/update_profile.html', {'user_form': form})


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
    start_y = 640
    line_space = 25
    bgColor = colors.Color(red=(211.0/255),green=(211.0/255),blue=(211.0/255))

    canvas1 = canvas.Canvas(response, pagesize=letter)
    canvas1.setLineWidth(.3)

    canvas1.setFont('Helvetica-Bold', 15)
    canvas1.drawString(start_x+140,start_y+80, clean(post.title))

    canvas1.setFont('Helvetica', 12)
     
    canvas1.drawString(start_x+50,start_y,'Date Created %s' % cleanDate(post.date_entered))

    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,start_y-65,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, start_y-60,'Client Info')

    offsetY = start_y-60
    canvas1.drawString(start_x, offsetY-line_space,'Client')
    lines = drawText(canvas1, clean(post.client), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Contact')
    lines = drawText(canvas1, clean(post.contact), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Client Address')
    lines = drawText(canvas1, clean(post.client_address), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Phone')
    lines = drawText(canvas1, clean(post.phone), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    offsetY = offsetY-lines*line_space - 30
    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,offsetY-5,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, offsetY,'Job Location')

    canvas1.drawString(start_x, offsetY-line_space,'Map No')
    lines = drawText(canvas1, clean(post.map_no), 15, start_x+140, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Address')
    lines = drawText(canvas1, clean(post.address_street), 15, start_x+140, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'City')
    lines = drawText(canvas1, clean(post.city), 15, start_x+140, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'State')
    lines = drawText(canvas1, clean(post.state), 15, start_x+140, offsetY)
    offsetY = offsetY-lines*line_space

    offsetY = offsetY - 30 - lines*line_space
    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,offsetY-5,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, offsetY,'Notes')

    lines = drawText(canvas1, clean(post.notes), 40, start_x, offsetY)
    offsetY = offsetY-lines*line_space-80

    start_x = 310
    canvas1.setFont('Helvetica-Bold', 12)
    canvas1.drawString(start_x+60,start_y,'Survey Work Order')
    canvas1.line(start_x+60,start_y-2,start_x+165,start_y-2)

    offsetY = start_y - 20
    canvas1.setFont('Helvetica', 12)
    canvas1.drawString(start_x+60, offsetY-18,'Project #')
    lines = drawText(canvas1, clean(post.project_no), 17, start_x+150, offsetY, 20)
    offsetY = offsetY-lines*18

    canvas1.drawString(start_x+60, offsetY-18,'Map #')
    lines = drawText(canvas1, clean(post.map_no), 17, start_x+150, offsetY, 20)
    offsetY = offsetY-lines*18

    canvas1.drawString(start_x+60, offsetY-18,'Date Needed')
    lines = drawText(canvas1, clean(post.date_needed), 17, start_x+150, offsetY, 20)
    offsetY = offsetY-lines*18

    canvas1.drawString(start_x+60, offsetY-18,'Requested By')
    lines = drawText(canvas1, clean(post.requested_by), 17, start_x+150, offsetY, 20)
    offsetY = offsetY-lines*18

    offsetY = offsetY - 40
    start_x = start_x + 12
    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,offsetY-5,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, offsetY,'Reference Info')

    canvas1.drawString(start_x, offsetY-line_space,'Certify To')
    lines = drawText(canvas1, clean(post.certify_to), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Lender')
    lines = drawText(canvas1, clean(post.lender), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Gf#')
    lines = drawText(canvas1, clean(post.gf_no), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Clerkfile#')
    lines = drawText(canvas1, clean(post.clerksfile), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Volume')
    lines = drawText(canvas1, clean(post.book), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Page')
    lines = drawText(canvas1, clean(post.page), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Well Name')
    lines = drawText(canvas1, clean(post.well_name), 17, start_x+130, offsetY)
    offsetY = offsetY-lines*line_space

    canvas1.drawString(start_x, offsetY-line_space,'Well Number')
    lines = drawText(canvas1, clean(post.well_number), 17, start_x+130, offsetY)
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


class AuthenticationEmailBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(email=username)
        except Users.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None