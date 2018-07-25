from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Form, Form500, MasterGeom, County
from .forms import PostForm, newForm, UserForm, UserEditForm
from django.shortcuts import redirect
from django.shortcuts import render
from .models import *
#from django.utils import simplejson
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
    return render(request, 'blog/post_new.html', {'form': form})

def loadCounties(request):
    #survey_types = MasterGeom.objects.all().distinct('join_type')
    # county_id = request.GET.get('surveytype')
    # print (county_id)
    counties = MasterGeom.objects.all().distinct('county')
    #counties = MasterGeom.objects.filter(join_type=county_id).order_by('county_code')
    return render(request, 'blog/post_new.html', {'counties': counties })

@login_required
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
        print (form.errors)
        if form.is_valid():
            user = form.save(commit=False)

            print (request.POST.get('new_password'))
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