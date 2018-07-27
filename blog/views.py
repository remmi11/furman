from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Form, Form500, MasterGeom, County
from .forms import PostForm, newForm, UserForm, UserEditForm
from django.shortcuts import redirect
from django.shortcuts import render
from .models import *
#from django.utils import simplejson
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# def post_list(request):
#     posts = Form.objects.all() #filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_list(request):
    # filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Form500.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Form, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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
    posts = Form500.objects.all()
    post = get_object_or_404(Form500, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            post.date_entered = timezone.now()
            post.date_needed = request.POST.get('date-needed')
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
            post.county = request.POST.get('county')
            post.subdivision = request.POST.get('subdivision')
            post.unit = request.POST.get('unit')
            post.sub_block = request.POST.get('subblock')
            post.lot = request.POST.get('lot')
            post.survey = request.POST.get('survey')
            post.rural_block = request.POST.get('block')
            post.rural_section = request.POST.get('rural_section')
            post.meridian = request.POST.get('meridian')
            post.t_r = request.POST.get('town_range')
            post.plss_section = request.POST.get('section')
            post.folder_path = request.POST.get('fpath')

            form.save()
            return render(request, 'blog/post_list.html', {'posts': posts})
            # return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        join_types = MasterGeom.objects.all().distinct('join_type')
        counties = MasterGeom.objects.filter(join_type=post.survey_type).distinct('county')
        counties = [tp.county.strip() for tp in counties if tp.county!=None]

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

        print (level)
        print (keys)

    return render(request, 'blog/post_edit.html', {'form': form, "join_types": join_types, \
        'counties': counties, "level1": level[0], "level2": level[1], \
        "level3": level[2], "level4": level[3]})

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