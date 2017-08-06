from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
#from django.template import loader

from .models import Choice, Question

# Create your views here.
# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	#template = loader.get_template('polls/index.html')
# 	#shortcut
# 	context = {'latest_question_list': latest_question_list}
# 	return render(request, 'polls/index.html',context)
# 	#output = ','.join([q.question_text for q in latest_question_list])
# 	#return HttpResponse(template.render(context, request))
# 	#return HttpResponse("<h1>Hello World!, you are at the poll index.</h1>")

class IndexView(generic.ListView):
	"""class for index(index.html) of the polls app"""
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Returns last five published questions"""
		#return Question.objects.order_by('-pub_date')[:5]
		"""Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset containing
		 Questions whose pub_date is less than or equal to - 
		 that is, earlier than or equal to - timezone.now."""
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]



# def results(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/results.html', {'question':question})

# 	#response = "You're looking at the results of question %s."
# 	#return HttpResponse(response % question_id)

class ResultsView(generic.DetailView):
	"""\class for showing results of vote"""
	model = Question
	template_name = 'polls/results.html'





def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		#Redisplay the question voting form
		return render(request,'polls/detail.html',{'question':question,'error_message':"You didn't select a choice.", })
	else:
		selected_choice.votes += 1
		selected_choice.save()
		 # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
	#return HttpResponse("You're voting on question %s." % question_id)

# def detail(request, question_id):
# 	# try:
# 	# 	question = Question.objects.get(pk=question_id)
# 	# except Question.DoesNotExist:
# 	# 	raise Http404("Question does not exist")

# 	#shortcut
# 	question = get_object_or_404(Question,pk=question_id)	
# 	return render(request,'polls/detail.html',{'question':question})
# 	#return HttpResponse("You're looking at question %s." % question_id)

class DetailView(generic.DetailView):
	"""\class for showing details of question"""
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())