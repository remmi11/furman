from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Tickets
from .forms import TicketForm
# Create your views here.

SURVEY_TYPE = ['PRAD', 'RURAL', 'PLSS', 'OTHER ISSUE']

@login_required
def ticket_list(request):
	if not request.user.edit_auth:
		return redirect('/')

	ticktes = Tickets.objects.all().order_by("-pk")
	return render(request, 'ticket/ticket_list.html', 
		{"ticktes": ticktes})

@login_required
def ticket_detail(request, pk):
	if not request.user.edit_auth:
		return redirect('/')
		
	ticket = Tickets.objects.get(pk=pk)
	return render(request, 'ticket/ticket_detail.html',
		{'ticket': ticket})

@login_required
@csrf_exempt
def ticket_edit(request, pk):
	if not request.user.edit_auth:
		return redirect('/')

	join_types = SURVEY_TYPE
	ticket = Tickets.objects.get(pk=pk)
	if request.POST:
		data = request.POST.copy()
		data['status'] = 2 if data['status'] == "on" else 1
		form = TicketForm(data, instance=ticket)
		print (form.is_valid())
		print (form.errors.as_data())
		form.save()
		return redirect("/ticket/%d/" % ticket.id)

	return render(request, 'ticket/ticket_new.html',
		{'join_types': join_types, 'ticket': ticket})

@login_required
@csrf_exempt
def ticket_new(request):
	if not request.user.edit_auth:
		return redirect('/')

	join_types = SURVEY_TYPE

	ticket = Tickets()

	if request.POST:
		values = request.POST.dict()
		del values['id']
		ticket = Tickets.objects.create(**values)
		return redirect("/ticket/%d/" % ticket.id)
	return render(request, 'ticket/ticket_new.html', 
		{'join_types': join_types, 'ticket': ticket})

@login_required
def ticket_remove(request, pk):
	if not request.user.edit_auth:
		return redirect('/')

	ticket = get_object_or_404(Tickets, pk=pk)
	if ticket:
		ticket.delete()

	return redirect("/tickets/")