#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import FormAll, MasterGeom, County
from .forms import PostForm, newForm, UserForm, UserEditForm
from django.shortcuts import redirect
from django.shortcuts import render
from .models import *
#from django.utils import simplejson
import json
import xlwt

import hashlib
import hmac
import base64
import urllib.parse as urlparse

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
from collections import namedtuple

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from django.db import connection
from django.db.models.functions import Upper
from django.core import serializers

GEOM_LIMIT = 1000
GOOGLE_KEY = "AIzaSyDaAQvr-4aNMcp4DrKOS0HiSl8pmYCMI6g"
SECRET_KEY = "HkT3EqphnEi8aoH6bOkyhucS2kk="

@login_required
def post_list(request):
    join_type = MasterGeom.objects.all().distinct('join_type')
    return render(request, 'blog/post_list.html', {"join_types": join_type})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Form, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def sign_url(input_url=None, secret=None):
    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse.urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, str(url_to_sign).encode('utf-8'), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode("utf-8")

def nametuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

@login_required
@csrf_exempt
def ajaxPagination(request):
    order_cols = ['pk', 'project_no', 'survey_type', 'client', 'map_no', 'county', 'address_street',
                    'survey', 'rural_block', 'rural_section', 'subdivision', 
                    'unit', 'sub_block', 'lot', 'meridian', 't_r', 'plss_section', 'notes', 'aka']

    search_text = dict()

    start = int(request.POST.get("start"))
    length = int(request.POST.get("length"))
    draw = int(request.POST.get("draw"))
    search_key = request.POST.get('search[value]')

    order_col = request.POST.get('order[0][column]')

    order_type = request.POST.get('order[0][dir]')
    if order_col == 0 and order_type == "desc":
        order_key = "-pk"
    else:
        try:
            order_key = order_cols[int(order_col)] if order_type == "asc" else "-" + order_cols[int(order_col)]
        except:
            order_key = "-pk"

    condition = None

    col_search_key = request.POST.get('columns[0][search][value]')
    if col_search_key != "":
        search_text["pk"] = col_search_key
        condition = condition & Q(pk__icontains=col_search_key) if condition != None else Q(pk__icontains=col_search_key)
    col_search_key = request.POST.get('columns[1][search][value]')
    if col_search_key != "":
        search_text["project_no"] = col_search_key
        condition = condition & Q(project_no__icontains=col_search_key) if condition != None else Q(project_no__icontains=col_search_key)
    col_search_key = request.POST.get('columns[2][search][value]')
    if col_search_key != "":
        search_text["survey_type"] = col_search_key
        condition = condition & Q(survey_type__icontains=col_search_key) if condition != None else Q(survey_type__icontains=col_search_key)
    col_search_key = request.POST.get('columns[3][search][value]')
    if col_search_key != "":
        search_text["client"] = col_search_key
        condition = condition & Q(client__icontains=col_search_key) if condition != None else Q(client__icontains=col_search_key)
    col_search_key = request.POST.get('columns[4][search][value]')
    if col_search_key != "":
        search_text["map_no"] = col_search_key
        condition = condition & Q(map_no__icontains=col_search_key) if condition != None else Q(map_no__icontains=col_search_key)
    col_search_key = request.POST.get('columns[5][search][value]')
    if col_search_key != "":
        search_text["county"] = col_search_key
        condition = condition & Q(county__icontains=col_search_key) if condition != None else Q(county__icontains=col_search_key)
    col_search_key = request.POST.get('columns[6][search][value]')
    if col_search_key != "":
        search_text["address_street"] = col_search_key
        condition = condition & Q(address_street__icontains=col_search_key) if condition != None else Q(address_street__icontains=col_search_key)
    col_search_key = request.POST.get('columns[7][search][value]')
    if col_search_key != "":
        search_text["survey"] = col_search_key
        condition = condition & Q(survey__icontains=col_search_key) if condition != None else Q(survey__icontains=col_search_key)
    col_search_key = request.POST.get('columns[8][search][value]')
    if col_search_key != "":
        search_text["rural_block"] = col_search_key
        condition = condition & Q(rural_block__icontains=col_search_key) if condition != None else Q(rural_block__icontains=col_search_key)
    col_search_key = request.POST.get('columns[9][search][value]')
    if col_search_key != "":
        search_text["rural_section"] = col_search_key
        condition = condition & Q(rural_section__icontains=col_search_key) if condition != None else Q(rural_section__icontains=col_search_key)
    col_search_key = request.POST.get('columns[10][search][value]')
    if col_search_key != "":
        search_text["subdivision"] = col_search_key
        condition = condition & Q(subdivision__icontains=col_search_key) if condition != None else Q(subdivision__icontains=col_search_key)
    col_search_key = request.POST.get('columns[11][search][value]')
    if col_search_key != "":
        search_text["unit"] = col_search_key
        condition = condition & Q(unit__icontains=col_search_key) if condition != None else Q(unit__icontains=col_search_key)
    col_search_key = request.POST.get('columns[12][search][value]')
    if col_search_key != "":
        search_text["sub_block"] = col_search_key
        condition = condition & Q(sub_block__icontains=col_search_key) if condition != None else Q(sub_block__icontains=col_search_key)
    col_search_key = request.POST.get('columns[13][search][value]')
    if col_search_key != "":
        search_text["lot"] = col_search_key
        condition = condition & Q(lot__icontains=col_search_key) if condition != None else Q(lot__icontains=col_search_key)
    col_search_key = request.POST.get('columns[14][search][value]')
    if col_search_key != "":
        search_text["meridian"] = col_search_key
        condition = condition & Q(meridian__icontains=col_search_key) if condition != None else Q(meridian__icontains=col_search_key)
    col_search_key = request.POST.get('columns[15][search][value]')
    if col_search_key != "":
        search_text["t_r"] = col_search_key
        condition = condition & Q(t_r__icontains=col_search_key) if condition != None else Q(t_r__icontains=col_search_key)
    col_search_key = request.POST.get('columns[16][search][value]')
    if col_search_key != "":
        search_text["plss_section"] = col_search_key
        condition = condition & Q(plss_section__icontains=col_search_key) if condition != None else Q(plss_section__icontains=col_search_key)
    col_search_key = request.POST.get('columns[17][search][value]')
    if col_search_key != "":
        search_text["notes"] = col_search_key
        condition = condition & Q(notes__icontains=col_search_key) if condition != None else Q(notes__icontains=col_search_key)
    col_search_key = request.POST.get('columns[18][search][value]')
    if col_search_key != "":
        search_text["aka"] = col_search_key
        condition = condition & Q(aka__icontains=col_search_key) if condition != None else Q(aka__icontains=col_search_key)
    col_search_key = request.POST.get('columns[19][search][value]')
    if col_search_key != "":
        search_text["folder_path"] = col_search_key
        condition = condition & Q(folder_path__icontains=col_search_key) if condition != None else Q(folder_path__icontains=col_search_key)

    extra_search = (json.loads(request.POST.get("extra_search")))

    if condition == None and (search_key == None or search_key == ""):
        posts = FormAll.objects.all().order_by(order_key)[start:start+length].query

        join_field = None
    else:
        if search_key != None and search_key != "":
            search_text['search_key'] = search_key
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

        if start == 0:
            join_field = FormAll.objects.filter(condition).values('join_field').query
        else:
            join_field = None

        posts = FormAll.objects.filter(condition).order_by(order_key)[start:start+length].query


    search = None

    if extra_search['xmin'] != None and request.POST.get('reload') != "":
        bounds = True
        search = "geom && ST_MakeEnvelope(%s, %s, %s, %s)" % \
            (extra_search['xmin'], extra_search['ymin'], \
            extra_search['xmax'], extra_search['ymax'])

        posts = str(posts).split("WHERE")
        posts = "%s where %s and %s" % (posts[0], search, posts[1])

    cursor = connection.cursor()

    count_sql = "select count(*) from %s" % (str(posts).split("FROM")[1].split("ORDER BY")[0])
    cursor.execute(count_sql.replace("LIKE UPPER(", "LIKE UPPER('").replace("(%", "('%").replace("%)", "%')"))
    row = cursor.fetchone()
    count = int(row[0])

    cursor.execute(str(posts).replace("LIKE UPPER(", "LIKE UPPER('").replace("(%", "('%").replace("%)", "%')"))
    posts = nametuplefetchall(cursor)

    data = []
    for post in posts:
        if request.user.edit_auth:
            action_buttons = '<a style="padding: 2px;" class="btn btn-default" href="/post/'+str(post.id)+'/edit/"> \
                        <span><i class="fa fa-pencil" style="font-size:24px"></i></span> \
                    </a> <a style="padding: 2px;" class="btn btn-default" target="_blank" href="/get_pdf/'+str(post.id)+'/"> \
                    <span><i class="fa fa-eye" style="font-size:24px"></i></span> \
                </a>'
        else:
            action_buttons = '<a style="padding: 2px;" class="btn btn-default" target="_blank" href="/get_pdf/'+str(post.id)+'/"> \
                    <span><i class="fa fa-eye" style="font-size:24px"></i></span> \
                </a>'

        if post.geom:
            action_buttons += '<a style="padding: 2px;" class="btn btn-default" target="_blank" href="javascript:void(0);" \
                    onClick="openMapWithId(\''+str(post.id)+'\')"> \
                    <span><i class="fa fa-globe" style="font-size:24px"></i></span> \
                </a>'

        data.append([post.id, post.project_no, post.survey_type, \
            post.client, post.map_no, post.county, post.address_street, post.survey, \
            post.rural_block, post.rural_section, post.subdivision, \
            post.unit, post.sub_block, post.lot, post.meridian, post.t_r, \
            post.plss_section, post.notes, post.aka, \
            '<a style="padding: 2px;" class="btn btn-default" href="'+str(post.folder_path)+'" target="_blank" title="'+str(post.folder_path)+'"> \
                    <span><i class="fa fa-external-link" style="font-size:24px"></i></span> \
                </a> ' + action_buttons])

    row = None
    bounds = None
    if join_field == None:
        row = {"type": "FeatureCollection", "features": None}
        row = json.dumps(row)

    if join_field != None and request.POST.get('reload') == "":
        join_field = str(join_field).split("WHERE")[1].strip()
        
        row = getGeoSql(join_field)
        if row['features']:
            for feature in row['features']:
                feature['streetview'] = sign_url("https://maps.googleapis.com/maps/api/streetview?location=%s,%s&size=600x300&key=%s" % (feature['lat'], feature['lon'], GOOGLE_KEY), SECRET_KEY)

        row = json.dumps(row)

    if join_field != None and request.POST.get('reload') != "":
        join_field = str(join_field).split("WHERE")[1].strip()

    posts = {
            "draw": draw,
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": data,
            "geom": row,
            "bounds": bounds,
            "search_text": json.dumps(search_text),
            "condition": join_field
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

                try:
                    post.geom = MasterGeom.objects.filter(join_field__iexact=post.join_field)[0].geom
                except:
                    post.geom = None

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

                try:
                    post.geom = MasterGeom.objects.filter(join_field__iexact=post.join_field)[0].geom
                except:
                    post.geom = None

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

def drawNotes(canvasObj, text, x, y, line_space=15):
    text_list = text.split("\n")
    if text == "":
        return 1

    y -= 10
    length = 0
    for txt in text_list:    
        wraped_text = wrap(txt, 30)
        for index in range(0, len(wraped_text)):
            canvasObj.drawString(x, y-(index+1)*line_space, wraped_text[index])
        length += len(wraped_text)
        y = y-len(wraped_text)*line_space - 5

    return length

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
    # start_y = 640
    start_y = 700
    line_space = 25
    bgColor = colors.Color(red=(211.0/255),green=(211.0/255),blue=(211.0/255))

    canvas1 = canvas.Canvas(response, pagesize=letter)
    canvas1.setLineWidth(.3)

    canvas1.setFont('Helvetica-Bold', 15)
    canvas1.drawString(start_x+140,start_y+40, clean(post.title))

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

    lines = drawNotes(canvas1, clean(post.notes), start_x, offsetY)
    offsetY = offsetY-lines*line_space-80

    start_x = 310
    canvas1.setFont('Helvetica-Bold', 12)
    canvas1.drawString(start_x+60,start_y,'Survey Work Order')
    canvas1.line(start_x+60,start_y-2,start_x+165,start_y-2)

    offsetY = start_y #- 15
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

    canvas1.drawString(start_x, offsetY-line_space,'Clerksfile#')
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

    offsetY = offsetY - 45
    canvas1.setFillColor(bgColor)
    canvas1.rect(start_x-10,offsetY-5,270,20, fill=True, stroke=False)
    canvas1.setFillColor(colors.black)
    canvas1.drawString(start_x, offsetY,'Legal')

    # line_space = 18
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

@login_required
def show_map(request):
    geo_json = ""

    if "form_id" in request.GET:
        join_field = FormAll.objects.filter(pk=request.GET["form_id"]).values('join_field').query
        join_field = str(join_field).split("WHERE")[1].strip()

        geo_json = getGeoSql(join_field)
        if geo_json['features']:
            for feature in geo_json['features']:
                feature['streetview'] = sign_url("https://maps.googleapis.com/maps/api/streetview?location=%s,%s&size=600x300&key=%s" % (feature['lat'], feature['lon'], GOOGLE_KEY), SECRET_KEY)

        geo_json = json.dumps(geo_json)

    # print (geo_json)
    join_type = MasterGeom.objects.all().distinct('join_type')
    return render(request, 'blog/map.html', {'join_types': join_type, 'geo_json': geo_json})

@login_required
@csrf_exempt
def ajax_map_search(request):
    survey_type = request.POST.get('surveytype')

    search_key = []
    if survey_type == "plss":
        search_key = [request.POST.get('county'), 
            request.POST.get('town_range'), request.POST.get('section')]
    elif survey_type == "prad":
        search_key = [request.POST.get('county'), 
            request.POST.get('subdivision'), request.POST.get('unit'), 
            request.POST.get('subblock'), request.POST.get('lot')]
    elif survey_type == "rural":
        search_key = [request.POST.get('county'), 
            request.POST.get('survey'), request.POST.get('block'), 
            request.POST.get('rural_section')]

    search_key = "\\".join([tp.strip() for tp in search_key if tp.strip() != ""])

    if search_key == "":
        join_field = FormAll.objects.all().values('join_field').query
    else:
        join_field = FormAll.objects.filter(join_field__istartswith=search_key).values('join_field').query

    row = None
    if join_field != None:
        join_field = str(join_field).split("WHERE")[1].strip()
        row = getGeoSql(join_field)
        if row['features']:
            for feature in row['features']:
                feature['streetview'] = sign_url("https://maps.googleapis.com/maps/api/streetview?location=%s,%s&size=600x300&key=%s" % (feature['lat'], feature['lon'], GOOGLE_KEY), SECRET_KEY)

    return HttpResponse(json.dumps(row), content_type='application/json')

@login_required
@csrf_exempt
def ajax_map_bound(request):
    search = "geom && ST_MakeEnvelope(%s, %s, %s, %s)" % \
        (request.POST.get("xmin"), request.POST.get("ymin"), \
        request.POST.get("xmax"), request.POST.get("ymax"))

    condition = request.POST.get("condition")
    row = getGeoSql(condition, search)
    if row['features']:
        for feature in row['features']:
            feature['streetview'] = sign_url("https://maps.googleapis.com/maps/api/streetview?location=%s,%s&size=600x300&key=%s" % (feature['lat'], feature['lon'], GOOGLE_KEY), SECRET_KEY)

    return HttpResponse(json.dumps(row), content_type='application/json')

@login_required
@csrf_exempt
def ajax_map_by_formid(request):
    geo_json = ""

    if "form_id" in request.POST:
        join_field = FormAll.objects.filter(pk=request.POST["form_id"]).values('join_field').query
        join_field = str(join_field).split("WHERE")[1].strip()

        geo_json = getGeoSql(join_field)
        if geo_json['features']:
            for feature in geo_json['features']:
                feature['streetview'] = sign_url("https://maps.googleapis.com/maps/api/streetview?location=%s,%s&size=600x300&key=%s" % 
                    (feature['lat'], feature['lon'], GOOGLE_KEY), SECRET_KEY)

    return HttpResponse(json.dumps(geo_json), content_type='application/json')


def export_users_xls(request):
    search = json.loads(request.GET.get("search"))
    extra_search = json.loads(request.GET.get("extra_search"))

    condition = None

    if "pk" in search:
        condition = condition & Q(pk__icontains=search["pk"]) if condition != None else Q(pk__icontains=search["pk"])
    if "project_no" in search:
        condition = condition & Q(project_no__icontains=search["project_no"]) if condition != None else Q(project_no__icontains=search["project_no"])
    if "survey_type" in search:
        condition = condition & Q(survey_type__icontains=search["survey_type"]) if condition != None else Q(survey_type__icontains=search["survey_type"])
    if "client" in search:
        condition = condition & Q(client__icontains=search["client"]) if condition != None else Q(client__icontains=search["client"])
    if "map_no" in search:
        condition = condition & Q(map_no__icontains=search["map_no"]) if condition != None else Q(map_no__icontains=search["map_no"])
    if "county" in search:
        condition = condition & Q(county__icontains=search["county"]) if condition != None else Q(county__icontains=search["county"])
    if "address_street" in search:
        condition = condition & Q(address_street__icontains=search["address_street"]) if condition != None else Q(address_street__icontains=search["address_street"])
    if "survey" in search:
        condition = condition & Q(survey__icontains=search["survey"]) if condition != None else Q(survey__icontains=search["survey"])
    if "rural_block" in search:
        condition = condition & Q(rural_block__icontains=search["rural_block"]) if condition != None else Q(rural_block__icontains=search["rural_block"])
    if "rural_section" in search:
        condition = condition & Q(rural_section__icontains=search["rural_section"]) if condition != None else Q(rural_section__icontains=search["rural_section"])
    if "subdivision" in search:
        condition = condition & Q(subdivision__icontains=search["subdivision"]) if condition != None else Q(subdivision__icontains=search["subdivision"])
    if "unit" in search:
        condition = condition & Q(unit__icontains=search["unit"]) if condition != None else Q(unit__icontains=search["unit"])
    if "sub_block" in search:
        condition = condition & Q(sub_block__icontains=search["sub_block"]) if condition != None else Q(sub_block__icontains=search["sub_block"])
    if "lot" in search:
        condition = condition & Q(lot__icontains=search["lot"]) if condition != None else Q(lot__icontains=search["lot"])
    if "meridian" in search:
        condition = condition & Q(meridian__icontains=search["meridian"]) if condition != None else Q(meridian__icontains=search["meridian"])
    if "t_r" in search:
        condition = condition & Q(t_r__icontains=search["t_r"]) if condition != None else Q(t_r__icontains=search["t_r"])
    if "plss_section" in search:
        condition = condition & Q(plss_section__icontains=search["plss_section"]) if condition != None else Q(plss_section__icontains=search["plss_section"])
    if "notes" in search:
        condition = condition & Q(notes__icontains=search["notes"]) if condition != None else Q(notes__icontains=search["notes"])
    if "aka" in search:
        condition = condition & Q(aka__icontains=search["aka"]) if condition != None else Q(aka__icontains=search["aka"])
    if "folder_path" in search:
        condition = condition & Q(folder_path__icontains=search["folder_path"]) if condition != None else Q(folder_path__icontains=search["folder_path"])

    search_key = None if 'search_key' not in search else search['search_key']
    if condition == None and (search_key == None or search_key == ""):
        posts = FormAll.objects.all().order_by("-project_no").query
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

        posts = FormAll.objects.filter(condition).order_by("-project_no").query

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="furmanrecords.xls"'

    columns = ['pk', 'project_no', 'survey_type', 'client', 'map_no', 'county', 'address_street', 'survey', 'rural_block', 'rural_section', 'subdivision', 'unit', 'sub_block', 'lot', 'meridian', 't_r', 'plss_section', 'notes', 'aka']

    wb = xlwt.Workbook(encoding='utf-8')
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # Sheet header, first row
    row_num = 0

    ws = wb.add_sheet('furmanrecords', cell_overwrite_ok=True)

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    if 'xmin' in extra_search and extra_search['xmin'] != None:
        search = "geom && ST_MakeEnvelope(%s, %s, %s, %s)" % \
            (extra_search['xmin'], extra_search['ymin'], \
            extra_search['xmax'], extra_search['ymax'])

        posts = str(posts).split("WHERE")
        posts = "%s where %s and %s" % (posts[0], search, posts[1])

    cursor = connection.cursor()
    cursor.execute(str(posts).replace("LIKE UPPER(", "LIKE UPPER('").replace("(%", "('%").replace("%)", "%')"))
    columns_tmp = [col[0] for col in cursor.description]
    serialized_rows = [dict(zip(columns_tmp, row)) for row in cursor.fetchall()]

    font_style = xlwt.XFStyle()

    for obj in serialized_rows:
        row_num += 1
        col_num = 0
        ws.write(row_num, col_num, obj['id'], font_style)

        for col_key in columns[1:]:
            col_num += 1
            ws.write(row_num, col_num, obj[col_key], font_style)

    wb.save(response)
    return response

def getGeoSql(join_field, bound=None):
    join_field = "geom!='' and " + join_field
    if bound != None:
        join_field += " and " + bound

    sql = '''SELECT row_to_json(fc)
        FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
        FROM (SELECT 'Feature' As type, 
            ST_AsGeoJSON(form_all.geom)::json As geometry, st_x(form_all.geom) as lon, st_y(form_all.geom) as lat, 
            (
                select row_to_json(t) 
                from (select UPPER(form_all.join_field) As join_field,
                        form_all.project_no as project_no,
                        form_all.date_needed as date,
                        form_all.client as client,
                        form_all.address_street as address_street,
                        form_all.survey_type as survey_type,
                        form_all.folder_path as folder_path) t
            )
        As properties
        FROM form_all WHERE '''+join_field+" limit 1000 ) As f ) As fc;"

    sql = sql.replace("LIKE UPPER(", "LIKE UPPER('").replace("(%", "('%").replace("%)", "%')")

    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()

        row = row[0]
        return row

    return []