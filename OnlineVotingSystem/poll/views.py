from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .forms import RegistrationForm, OTPForm, ChangeForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Candidate, ControlVote, Position
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random

def homeView(request):
    return render(request, "poll/home.html")

def registrationView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['confirm_password']:
                # Generate 6-digit OTP
                otp = str(random.randint(100000, 999999))
                
                # Save registration data and OTP in the session
                request.session['registration_data'] = {
                    'username': cd['username'],
                    'first_name': cd['first_name'],
                    'last_name': cd['last_name'],
                    'email': cd['email'],
                    'password': cd['password'],
                }
                request.session['otp'] = otp
                
                # Send the OTP via email
                try:
                    send_mail(
                        subject='Your Online Voting System Registration OTP',
                        message=f'Hello {cd["first_name"] or cd["username"]},\n\nYour One-Time Password (OTP) for registering with the Online Voting System is: {otp}\n\nThis OTP is valid for this session only.\n\nThank you!',
                        from_email=None,
                        recipient_list=[cd['email']],
                        fail_silently=False,
                    )
                    messages.success(request, f'An OTP has been sent to {cd["email"]}. Please verify it below.')
                    return redirect('verify_otp')
                except Exception as e:
                    messages.error(request, f'Failed to send OTP email: {str(e)}')
                    return render(request, "poll/registration.html", {'form': form})
            else:
                return render(request, "poll/registration.html", {'form':form,'note':'password must match'})
    else:
        form = RegistrationForm()

    return render(request, "poll/registration.html", {'form':form})

def verifyOTPView(request):
    if 'registration_data' not in request.session or 'otp' not in request.session:
        messages.error(request, 'No active registration session found. Please register first.')
        return redirect('registration')
        
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            saved_otp = request.session.get('otp')
            
            if entered_otp == saved_otp:
                # Correct OTP! Create the user account
                data = request.session['registration_data']
                try:
                    user = User.objects.create_user(
                        username=data['username'],
                        email=data['email'],
                        password=data['password'],
                        first_name=data['first_name'],
                        last_name=data['last_name']
                    )
                    user.save()
                    
                    # Log the user in
                    login(request, user)
                    
                    # Clear session data
                    del request.session['registration_data']
                    del request.session['otp']
                    
                    messages.success(request, 'Verification successful! You are now registered and logged in.')
                    return redirect('dashboard')
                except Exception as e:
                    messages.error(request, f'Error creating user: {str(e)}')
                    return redirect('registration')
            else:
                messages.error(request, 'Invalid OTP. Please enter the correct code.')
    else:
        form = OTPForm()
        
    return render(request, "poll/verify_otp.html", {'form': form, 'email': request.session['registration_data']['email']})

def loginView(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.success(request, 'Invalid username or password!')
            return render(request, "poll/login.html")
    else:
        return render(request, "poll/login.html")

@login_required
def logoutView(request):
    logout(request)
    return redirect('home')
@login_required
def dashboardView(request):
    return render(request, "poll/dashboard.html")

@login_required
def positionView(request):

    obj = Position.objects.all()
    return render(request, "poll/position.html", {'obj':obj})
@login_required
def candidateView(request, pos):
    obj = get_object_or_404(Position, pk = pos)
    if request.method == "POST":
        temp = ControlVote.objects.get_or_create(user=request.user, position=obj)[0]
        if temp.status == False:
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            return HttpResponseRedirect('/position/')
        else:
            messages.success(request, 'you have already been voted this position.')
            return render(request, 'poll/candidate.html', {'obj':obj})
    else:
        return render(request, 'poll/candidate.html', {'obj':obj})
@login_required
def resultView(request):
    obj = Candidate.objects.all().order_by('position','-total_vote')
    return render(request, "poll/result.html", {'obj':obj})

@login_required
def candidateDetailView(request, id):

    obj = get_object_or_404(Candidate, pk=id)
    return render(request, "poll/candidate_detail.html", {'obj':obj})
@login_required
def changePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "poll/password.html", {'form':form})
@login_required
def editProfileView(request):

    if request.method == "POST":
        form = ChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ChangeForm(instance=request.user)
    return render(request, "poll/edit_profile.html", {'form':form})

