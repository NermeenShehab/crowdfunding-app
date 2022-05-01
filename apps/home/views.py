from itertools import count
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.db.models import Avg, Sum

from datetime import date, datetime

from apps.home.models import Category, Comment, Donation, Project,Image, Project_Report, Reply,User,Comment_Report
from apps.home.forms import Project_Form,Report_form,Reply_form,Category_form


@login_required(login_url="/login/")
def index(request):
    # return last 5 project
    all_projects = Project.objects.all()
    last_5_projects = Project.objects.all().order_by('-id')[:5]

    context = {
        'segment': 'index',
        'all_projects': all_projects,
        'count': len(all_projects),
        'last_5_projects': last_5_projects,
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def create_new_project(request):
    my_images = Image.objects.all()
    if request.method == 'GET':

        form = Project_Form()
        return render(request, "home/create-project.html", context={"form": form, 'images': my_images})

    if request.method == "POST":
        form = Project_Form(request.POST,request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            project = form.save()  
            for image in images:
                Image.objects.create(project_id=project.id,images=image)    
            return redirect('home')
    else:
        form = Project_Form()
    return render(request, "home/create-project.html", context={"form": form})


@login_required(login_url="/login/")
def show_project_details(request, project_id):

    context = {}
    try:
        project = Project.objects.get(id=project_id)
        donate = project.donation_set.all().aggregate(Sum("donation"))
        donations = len(project.donation_set.all())
        comments = project.comment_set.all()
        replies= Reply.objects.all()
        
        project_images=project.image_set.all()
        
        
        # handle date
        myFormat = "%Y-%m-%d %H:%M:%S"
        today = datetime.strptime(datetime.now().strftime(myFormat), myFormat)
        start_date = datetime.strptime(project.start_time.strftime(myFormat), myFormat)
        end_date = datetime.strptime(project.end_time.strftime(myFormat), myFormat)
        days_diff = (end_date-today).days
        new_report_form=Report_form()
        reply=Reply_form()
        # relatedProjects = Project.objects.all().filter(category_id=project.category)
        context = {'project': project,
                'donation' : donate["donation__sum"] if donate["donation__sum"] else 0,
                'donations' : donations,
                'days' : days_diff,
                'comments' : comments,
                'num_of_comments' : len(comments),
                'project_images':project_images,
                'replies':replies,

                'report_form':new_report_form,
                'reply_form':reply
                #    'relatedProjects': relatedProjects,
                }
        return render(request, "home/project-details.html", context)
    except Project.DoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def donate(request, project_id):
    if request.method == "POST":
        if request.POST['donate']:
            donation = Donation.objects.create(
                donation=request.POST['donate'],
                project_id=project_id,
                user_id=1
            )
            # handle to return to project details
            return redirect('show_project', project_id)
    return render(request, "home/project-details.html", project_id)


@login_required(login_url="/login/")
def create_comment(request, project_id):
    if request.method == "POST":
        if request.POST['comment']:
            comment = Comment.objects.create(
                comment=request.POST['comment'],
                project_id=project_id,
                user_id=1
            )
            # handle to return to project details
            return redirect('show_project', project_id)
    return render(request, "home/project-details.html", project_id)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def add_report(request, project_id):
    my_project=Project.objects.get(id=project_id)
    if request.method == "POST":
        # myuser_id=request.user.id
        # check=User.objects.get(id=1).project_report_set.all().id
        # print(check)
    

        Project_Report.objects.create(
                report = 'ip',
                project=my_project,
                # user_id = request.user.id
                user_id = 1
            )
        return redirect('show_project',project_id) # handle to return to project details


@login_required(login_url="/login/")
def add_comment_report(request, comment_id):
    my_comment=Comment.objects.get(id=comment_id)
    project=Project.objects.all().filter(comment__id=comment_id)[0]

    if request.method == "POST":
        # myuser_id=request.user.id
        # check=User.objects.get(id=1).project_report_set.all().id
        # print(check)
    

        Comment_Report.objects.create(
                report = 'ip',
                comment=my_comment,
                # user_id = request.user.id
                user_id = 1
            )
        return redirect('show_project',project.id) # handle to return to project details


@login_required(login_url="/login/")
def create_comment_reply(request, comment_id):

    if request.method == "POST":
        if request.POST['reply']:
            project=Project.objects.all().filter(comment__id=comment_id)[0]

            reply = Reply.objects.create(
                reply = request.POST['reply'],
                comment_id = comment_id,
                # user_id = request.user.id
                user_id = 1
            )

            return redirect('show_project',project.id) # handle to return to project details
    return render(request, "home/project-details.html",project.id)


@login_required(login_url="/login/")
def add_category(request):

    categories=Category.objects.all()
    
    if request.method=='GET':
        form=Category_form()
        return render(request,"home/category_form.html",context={'form':form})
    if request.method=='POST':
        form=Category_form(request.POST)

        if form.is_valid():
            new_category=request.POST['name']
            for category in categories:
                if category.name == new_category:
                    
                    error=' not valid'
                    
                    return render(request,"home/category_form.html",context={'form':form,'form_error':error})
                
            form.save()
            return redirect('home')
