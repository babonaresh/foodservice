from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import *
from .forms import *
from .forms import UserRegistrationForm
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.views.generic import View
#from .utils import render_to_pdf #created in step 4
from django.template.loader import get_template


# Create your views here.

now = timezone.now()
def home(request):
   return render(request, 'crm/home.html',
                 {'crm': home})

#def post_share(request, post_id):
    # Retrieve post by id
   # post = get_object_or_404(summary, status='published')

    #if request.method == 'POST':
        # Form was submitted
     #   form = EmailPostForm(request.POST)
      #  if form.is_valid():
            # Form fields passed validation
       #     cd = form.cleaned_data
            # ... send email
        #    post_url = request.build_absolute_uri(
         #       post.get_absolute_url())
          #  subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
           # message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            #send_mail(subject, message, 'admin@myblog.com', [cd['to']])
           # sent = True
    #else:
      #  form = EmailPostForm()
    #return render(request, 'crm/share.html', {'post': post,
     #                                               'form': form,'sent': sent})

#class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#       template=get_template('crm/index.html')
 #        context = {
  #           'customer'
#
 #      pdf = render_to_pdf('crm/index.html', )
  #       if pdf:
   #          response = HttpResponse(pdf, content_type='application/pdf')
    #         filename = "Invoice_%s.pdf" %(context)
     #        content = "inline; filename='%s'" % (filename)
      #       download = request.GET.get("download")
       #      if download:
        #         content = "attachment; filename='%s'" % (filename)
         #    response['Content-Disposition'] = content
          #   return response
        # return HttpResponse("Not found")




@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/customer_list.html',
                 {'customers': customer})

@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/customer_list.html',
                         {'customers': customer})
   else:
        # edit
       form = CustomerForm(instance=customer)
       return render(request, 'crm/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('crm:customer_list')

@login_required
def service_list(request):
   services = Service.objects.filter(created_date__lte=timezone.now())
   return render(request, 'crm/service_list.html', {'services': services})

@login_required
def service_new(request):
   if request.method == "POST":
       form = ServiceForm(request.POST)
       if form.is_valid():
           service = form.save(commit=False)
           service.created_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/service_list.html',
                         {'services': services})
   else:
       form = ServiceForm()
       # print("Else")
   return render(request, 'crm/service_new.html', {'form': form})

@login_required
def service_edit(request, pk):
   service = get_object_or_404(Service, pk=pk)
   if request.method == "POST":
       form = ServiceForm(request.POST, instance=service)
       if form.is_valid():
           service = form.save()
           # service.customer = service.id
           service.updated_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/service_list.html', {'services': services})
   else:
       # print("else")
       form = ServiceForm(instance=service)
   return render(request, 'crm/service_edit.html', {'form': form})

@login_required
def service_delete(request, pk):
   service = get_object_or_404(Service, pk=pk)
   service.delete()
   return redirect('crm:service_list')

@login_required
def product_list(request):
   products = Product.objects.filter(created_date__lte=timezone.now())
   return render(request, 'crm/product_list.html', {'products': products})

@login_required
def product_new(request):
   if request.method == "POST":
       form = ProductForm(request.POST)
       if form.is_valid():
           product = form.save(commit=False)
           product.created_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/product_list.html',
                         {'products': products})
   else:
       form = ProductForm()
       # print("Else")
   return render(request, 'crm/product_new.html', {'form': form})

@login_required
def product_edit(request, pk):
   product = get_object_or_404(Product, pk=pk)
   if request.method == "POST":
       form = ProductForm(request.POST, instance=product)
       if form.is_valid():
           product = form.save()
           # service.customer = service.id
           product.updated_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/product_list.html', {'products': products})
   else:
       # print("else")
       form = ProductForm(instance=product)
   return render(request, 'crm/product_edit.html', {'form': form})

@login_required
def product_delete(request, pk):
   product = get_object_or_404(Product, pk=pk)
   product.delete()
   return redirect('crm:product_list')

@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
    return render(request, 'crm/summary.html', {'customers': customers,
                                                    'products': products,
                                                    'services': services,
                                                    'sum_service_charge': sum_service_charge,
                                                    'sum_product_charge': sum_product_charge,})


def password_reset(request):
    return render(request, 'home/password_reset.html',
    {'home': password_reset})


def password_reset_confirm(request):
    return render(request, 'home/password_reset_confirm.html',
    {'home': password_reset_confirm})

def password_reset_email(request):
    return render(request, 'home/password_reset_email.html',
    {'home': password_reset_email})

def password_reset_complete(request):
    return render(request, 'home/password_reset_complete.html',
    {'home': password_reset_complete})
