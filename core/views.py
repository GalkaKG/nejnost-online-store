from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse


def about_us(request):
    return render(request, 'core/about-us.html')


def contact_us(request):
    return render(request, 'core/contact-us.html')


def contact_submit(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        # Add other form fields as needed

        # Send email or save the contact details
        send_mail(
            'New Contact Us Message',
            f'Name: {name}\nEmail: {email}',
            'from@example.com',  # Sender email
            ['admin@example.com'],  # Admin email
        )
        return HttpResponse('Thank you for contacting us!')
    return redirect('contact_us')  # Redirect back to the contact page if not POST