from django.shortcuts import render, get_object_or_404
from django.utils import timezone
# from .models import Form, Form500, MasterGeom, County
from .forms import PostForm, newForm
from django.shortcuts import redirect
from django.shortcuts import render
from .models import *
#from django.utils import simplejson
from django.http import HttpResponse


# def post_list(request):
#     posts = Form.objects.all() #filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})


def post_list(request):
    # filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Form500.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Form, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


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
    return render(request, 'blog/post_new.html', {'form': form})

def loadCounties(request):
    #survey_types = MasterGeom.objects.all().distinct('join_type')
    # county_id = request.GET.get('surveytype')
    # print (county_id)
    counties = MasterGeom.objects.all().distinct('county')
    #counties = MasterGeom.objects.filter(join_type=county_id).order_by('county_code')
    return render(request, 'blog/post_new.html', {'counties': counties })

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

    return HttpResponse(simplejson.dumps(result_set), mimetype='application/json', content_type='application/json')



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
    return render(request, 'blog/post_edit.html', {'form': form})


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
