from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Poll, Choice, Vote

def poll_details(request, poll_id):
  poll = get_object_or_404(Poll, pk=poll_id)
  user_voted = False

  if request.user.is_authenticated:
      current_user = request.user.username
      if Vote.objects.filter(user=current_user, choice__poll=poll).exists():
          user_voted = True
  
  context = {
      'poll': poll,
      'user_voted': user_voted
  }  
  return render(request, 'polls/poll.html', context)

@login_required
def poll_list(request):
  polls = Poll.objects.all()
  return render(request, 'polls/polls.html', {'polls': polls})

def search_polls(request):
  query = request.GET.get('query')
  results = []

  if query:
    cursor = connection.cursor()

    # Fix for A03:2021 SQL Injection
    # sql = f"SELECT * FROM polls_poll WHERE question LIKE ?"
    # cursor.execute(sql, ['%' + query + '%])

    sql = f"SELECT * FROM polls_poll WHERE question LIKE '%{query}%'"
    cursor.execute(sql)

    print(results)
    rows = cursor.fetchall()

    for row in rows:
      poll = Poll(id=row[0], question=row[1], creator=row[2])
      results.append(poll)

  return render(request, 'polls/search.html', {'results': results, 'made_query': query})

@login_required
def delete_poll(request, poll_id):
  poll = get_object_or_404(Poll, pk=poll_id)

  # Fix for A01:2021 Broken Access Control
  # if poll.creator != request.user:
    # return HttpResponseForbidden("Cannot delete polls created by others!")

  poll.delete()
  return redirect('poll_list')

@login_required
def create_poll(request):
  if request.method == 'POST':
    question = request.POST.get('question')
    choices = request.POST.get('choices')
    creator = request.POST.get('creator')

    # Fix for A04:2021 Insecure Design
    # creator = request.user

    poll = Poll.objects.create(question=question, creator=creator)

    for choice in choices.splitlines():
      Choice.objects.create(poll=poll, text=choice)

    return redirect('poll_list')
  
  return render(request, 'polls/create.html')

@login_required
def vote(request, poll_id):
  poll = get_object_or_404(Poll, pk=poll_id)
  currrent_user = request.user.username

  if Vote.objects.filter(user=currrent_user, choice__poll=poll).exists():
    return redirect('poll_details', poll_id=poll.id)
  
  if request.method == 'POST':
    choice_id = request.POST.get('choice')

    if not choice_id:
      return redirect('poll_details', poll_id=poll.id)
        
    choice = get_object_or_404(Choice, pk=choice_id, poll=poll)

    choice.votes += 1
    choice.save()

    Vote.objects.create(user=currrent_user, choice=choice)

    return redirect('poll_details', poll_id=poll.id)
  
  return redirect('poll_list')

