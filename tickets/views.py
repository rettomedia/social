from django.shortcuts import get_object_or_404, redirect, render
from tickets.forms import TicketForm
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False) 
            ticket.author = request.user  
            ticket.save()
            return redirect('help_center')
    else:
        form = TicketForm()
    
    return render(request, 'tickets/create-ticket.jinja', {'form': form})


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(author=request.user) 
    return render(request, 'tickets/my-tickets.jinja', {'tickets': tickets})


@login_required
def delete_ticket(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    if ticket.author == request.user:
        ticket.delete()
        return redirect('my_tickets')
    else:
        return redirect('my_tickets')