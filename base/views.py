# import djnago shortcuts methods
from django.shortcuts import render, redirect
# Import django messages for display pop up messages to the user.
from django.contrib import messages

# Import login_required decorator
from django.contrib.auth.decorators import login_required


# For authenticating and login user import these 2 methods
from django.contrib.auth import login, authenticate, logout







# Import Custom Models
from .models import User, Event, Submission


# Import Custom Forms
from .forms import SubmissionForm
from .forms import CustomUserCreationForm



# Login Page, the basic concept is here to login the user.
def login_page(request):
    # Check where the user is already logged in.
    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'You have already logged in!')
        return redirect('home_page')
    context = {
        'page': 'login'
    }
    
    
    # First of all, Check if the form submit method is "POST" method
    if request.method == "POST":
        # Now, let's grap the email value from the submitted form
        email = request.POST.get('email')
        # Also, gram the password from the form
        password = request.POST.get('password')

        # Before to login the user, let's verify if the user is authenticated user or not.
        user = authenticate(email=email, password=password)
        
        
        # Check if the user is authenticated then login the user
        if user is not None:
            # Use django built in method to login user, pass the request object along with authenticated user object.
            login(request, user)
            
            # after the user is logged in, now redirect user to the user account page.
            return redirect('user_account')
        
    return render(request, 'authentications/login_register.html', context)




# Register Page
def register_page(request):
    # Check if the user is already registered. restriect the logged user from this page to see again
    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'You have already registered!')
        return redirect('home_page')
    
    
    
    form = CustomUserCreationForm()
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)

            return redirect('user_account')
    
    context = {
        'form': form,
        'page': 'register'
    }
    return render(request, 'authentications/login_register.html', context)




# Logout Page
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login_page')

    messages.add_message(request, messages.WARNING, "You haven't logged in yet!")
    return redirect('home_page')


def home_page(request):
    # retriewe the users and events
    users = User.objects.filter(is_participants=True)
    events = Event.objects.all()
  
    # pass users and events to the context object
    context = {
        'users': users,
        'events': events,
       
        }
    
    # render the home page
    return render(request, 'home.html', context)




@login_required(login_url='login_page')
def user_page(reqeust, id):
    # find out the specific user
    user = User.objects.get(id=id)
    # pass user to the context object
    context = {'user': user}
    # render the userProfilePage
    return render(reqeust, 'userProfile.html', context)





@login_required(login_url='login_page')
def user_account_page(request):
    # find out the user.
    user = request.user
    context = {'user': user}
    return render(request, 'userAccount.html', context)





def event_page(request, id):
    # let's target the specific event by its ID
    event = Event.objects.get(id=id)
    
    
    # use (Try Except) block to check for the event and submission if already a user is registered for and submitted the event
    try: 
        # check if a user is already registered for an event
        registered = request.user.event_set.filter(id=event.id).exists()
        
        # Check if the event is submitted 
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()
    except:
        registered = False
        submitted = False
        
    
 
   
    context = {
            'event': event,
            'registered': registered, 
            'submitted': submitted
            }
    return render(request, 'event.html', context)



@login_required(login_url='login_page')
def event_registration(request, id):
    # grap the specific event
    event = Event.objects.get(id=id)
    context = {'event': event}
    
    
    # check if the method is post method
    if request.method == 'POST':
        # add user to the event_participants table
        event.participants.add(request.user)
        
        # show message to the user
        messages.add_message(request, messages.SUCCESS, 'You have Registered for the event successfully.')
        # redirect user to the event page with specific event
        return redirect('event_page', event.id)
    
    return render(request, 'event_confirmation.html', context)





@login_required(login_url='login_page')
def project_submission(request, id):
    
    # first grap the event
    event = Event.objects.get(id=id)
    
    form = SubmissionForm()
    
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        
        
        # Check the Form Validation
        if form.is_valid():
            
            # Here we initiate an instance of the of the submission form before to save it to the db
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            
            # Save it to the DB
            submission.save()
            # Redirect the User back to the Account Page.
            return redirect('user_account')
            
    context = {'event': event, 'form': form}
    return render(request, 'submit_form.html', context)




@login_required(login_url='login_page')
def update_submission(request,id):
    # First of all, let's grap the specific submission
    submission = Submission.objects.get(id=id)
    
    
    if request.user != submission.participant:
        messages.add_message(request, messages.WARNING, "You are restricted from this action!")
        return redirect('home_page')
    # Lets grap the even
    event = submission.event
    form = SubmissionForm(instance=submission)
    
    
    if request.method == "POST":
        form = SubmissionForm(request.POST, instance=submission)
        
        if form.is_valid():
            form.save()
            return redirect('user_account')
    
    context = {
        'form': form,
        }
    return render(request, 'submit_form.html', context)
    
    
    