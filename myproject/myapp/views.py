from django.http import HttpResponse
from myapp.models import *
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseForbidden
from .forms import RegisterForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import os
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from num2words import num2words
import qrcode
from .forms import *
import json
from datetime import datetime,timedelta








    ############05-09-2024############################
    
# views.py



@never_cache
def dashboard_view(request):
    # Check if user is logged in by looking for 'username' in session
    # if 'username' not in request.session:
    #     message = "You need to be logged in to access this page."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})

    # # Get role from session
    # user_role = request.session.get('role', None)

    # # Debugging: Print user role
    # print("User Role from session:", user_role)

    # # Check if role is 'admin'
    # if user_role != 'admin':
    #     message = "You do not have permission to access this page. Redirecting to the dashboard."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})

    # If everything is okay, load the dashboard
    data = {
        'active_users': 500,
        'sales': 2000,
        'reports': 10,
    }

    return render(request, 'myapp/dashboard.html', data)

@never_cache
def vendor_master(request):
    if request.method == 'POST':
        form = vendor_data(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            company_address=form.cleaned_data['company_address']
            gst=form.cleaned_data['gst']
            phone_number=form.cleaned_data['phone_number']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            pincode=form.cleaned_data['pincode']
            created_on = datetime.now()
            
            add_vendor_details=vendor_master_data(sno=vendor_master_data.objects.count()+1,company_code="VEN{:002d}".format(vendor_master_data.objects.count()+1),
                                             company_name=company_name,company_address=company_address,gst=gst,phone_number=phone_number,city=city,state=state,pincode=pincode,created_on=created_on).save()
            messages.success(request, 'Book added successfully!')
            return redirect('vendor_list')
        return render(request, 'myapp/vendor_master.html', {'form': form, 'add_vendor_details': add_vendor_details})
    else:
        form = searech_book_data()
        books = None

    return render(request, 'myapp/vendor_master.html', {'form': form, 'books': books})

@never_cache
def vendor_list(request):
    author_books = vendor_master_data.objects.filter(status='A')
    paginator = Paginator(author_books, 10)  # Create an instance of Paginator, show 10 records per page

    page_number = request.GET.get('page', 1)  # Get the current page number from URL
    page_obj = paginator.get_page(page_number)  # Call get_page() on the paginator instance
    # return render(request, 'your_template.html', {'page_obj': page_obj})  # Filters records by author
    return render(request, 'myapp/vendor_list.html', {'page_obj': page_obj})
from django.shortcuts import redirect, get_object_or_404
from bson import ObjectId 
from mongoengine import DoesNotExist 
from django.http import JsonResponse
@never_cache
def toggle_vendor_status(request, vendor_id):
    #  # Check if user is logged in by looking for 'username' in session
    # if 'username' not in request.session:
    #     message = "You need to be logged in to access this page."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})

    # # Get role from session
    # user_role = request.session.get('role', None)

    # # Debugging: Print user role
    # print("User Role from session:", user_role)

    # # Check if role is 'admin'
    # if user_role != 'admin':
    #     message = "You do not have permission to access this page. Redirecting to the dashboard."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})
    if request.method == 'POST':
        try:
            vendor_id = ObjectId(vendor_id)
            vendor = vendor_master_data.objects.get(id=vendor_id)
            new_status = 'Inactive' if vendor.status == 'A' else 'A'
            vendor_master_data.objects(id=vendor_id).update(set__status=new_status)

            return JsonResponse({'new_status': new_status})
        except DoesNotExist:
            return JsonResponse({'error': 'Vendor not found.'}, status=404)
def generate_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)

    # Ensure the 'pdfs' directory exists
    pdf_dir = os.path.join(settings.BASE_DIR, 'pdfs')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Save PDF to the 'pdfs' directory
    file_name = f"invoice_{context_dict['invoice_number']}.pdf"
    file_path = os.path.join(pdf_dir, file_name)

    with open(file_path, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(html, dest=result_file)
    
    if pisa_status.err:
        return None  # Return None in case of an error
    
    return file_name  # Return the file name for redirection


def view_pdf(request, pdf_file_name):
    # Construct the full file path
    file_path = os.path.join(settings.BASE_DIR, 'pdfs', pdf_file_name)
    if os.path.exists(file_path):
        # Serve the PDF file in the browser
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        return HttpResponse('File not found', status=404)
    

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

import os
from django.conf import settings
from django.http import FileResponse
@never_cache
def bill_generate(request):
    #  # Check if user is logged in by looking for 'username' in session
    # if 'username' not in request.session:
    #     message = "You need to be logged in to access this page."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})

    # # Get role from session
    # user_role = request.session.get('role', None)

    # # Debugging: Print user role
    # print("User Role from session:", user_role)

    # # Check if role is 'admin'
    # if user_role != 'admin':
    #     message = "You do not have permission to access this page. Redirecting to the dashboard."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})
    form = search_unit_address(request.POST or None)
    unit_name = None
    selected_unit = None
    products = []

    if request.method == 'POST':
        # Handling the selected unit from search results
        if 'selected_unit' in request.POST:
            selected_unit_name = request.POST.get('selected_unit')
            if selected_unit_name:
                try:
                    selected_unit = vendor_master_data.objects.get(company_name=selected_unit_name)
                except vendor_master_data.DoesNotExist:
                    messages.error(request, "Unit not found.")
                    selected_unit = None

        # Handling the bill generation process
        elif 'bill_generate' in request.POST:
            company_name = request.POST.get('company_name')
            billing_address = request.POST.get('billing_address')
            shipping_address = request.POST.get('shipping_address')
            eway_number = request.POST.get('eway_number')
            purchase_number = request.POST.get('purchase_number')
            purchase_date = request.POST.get('purchase_date')
            gst_number = request.POST.get('gst_number')
            vechine_number = request.POST.get('vechine_number')

            product_name_list = request.POST.getlist('product_name[]')
            Hsn_list = request.POST.getlist('Hsn[]')
            Quantity_list = request.POST.getlist('Quantity[]')
            UOM_data_list = request.POST.getlist('UOM_data[]')
            price_list = request.POST.getlist('price[]')
            total_list=request.POST.getlist('totalAmount[]')
            

            total_amount = request.POST.get('totalAmountInput')
            sgst = request.POST.get('sgstInput')
            cgst = request.POST.get('cgstInput')
            igst=  request.POST.get('igstInput')
            total_amount_after_tax = request.POST.get('totalAmountAfterTaxInput')
            for_in_words=num2words(total_amount_after_tax, lang='en').capitalize()

            # Generate invoice number
            invoice_number = "INV{:002d}".format(generate_bill.objects.count() + 1)
            created_on = datetime.now()
            only_date=datetime.now().date

            # Storing data into the generate_bill table
            store_date_in_table = generate_bill(
                sno=generate_bill.objects.count() + 1,
                invoice_no=invoice_number,
                company_name=company_name,
                billing_address=billing_address,
                shipping_address=shipping_address,
                eway_number=eway_number,
                purchase_number=purchase_number,
                purchase_date=purchase_date,
                created_on=created_on,
                created_by="Admin",
                status='A'


            )
            store_date_in_table.save()

           
            for i in range(len(product_name_list)):
                try:
                    product_name = product_name_list[i]
                    Hsn = Hsn_list[i]
                    quantity = float(Quantity_list[i])
                    uom = UOM_data_list[i]
                    price = float(price_list[i])
                    Amount=float(total_list[i])

                    # Store the product details
                    product_details.objects.create(
                        sno=product_details.objects.count() + 1,
                        product_name=product_name,
                        inv_bill=invoice_number,
                        Hsn=Hsn,
                        Quantity=quantity,
                        UOM_data=uom,
                        price=price,
                        Amount=Amount,
                        created_on=created_on,
                        created_by="Admin",
                        status='A'
                    ).save()

                    products.append({
                        'product_name': product_name,
                        'Hsn': Hsn,
                        'Quantity': quantity,
                        'UOM_data': uom,
                        'price': price,
                        'Amount':Amount
                    })

                except ValueError as e:
                    print(f"Error processing row {i}: {e}")
            # Generate the QR code
            qr_data = f"Invoice No: {invoice_number}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=3,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_image = qr.make_image(fill='black', back_color='white')

            # Save the QR code as an image file
            qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
            if not os.path.exists(qr_dir):
                os.makedirs(qr_dir)  # Create the directory if it doesn't exist

            qr_file_name = f"qr_code_invoice_{invoice_number}.png"
            qr_file_path = os.path.join(qr_dir, qr_file_name)
            qr_image.save(qr_file_path)  # Save the QR code image

            # Debugging: Print the full file path to ensure it is being saved correctly
            print(f"QR code saved at: {qr_file_path}")
            # Generate PDF and return file name
            context = {
                'invoice_number': invoice_number,
                'company_name': company_name,
                'billing_address': billing_address,
                'shipping_address': shipping_address,
                'gst_number': gst_number,
                'vechine_number': vechine_number,
                'products': products,
                'total_amount': total_amount,
                'sgst': sgst,
                'cgst': cgst,
                'igst':igst,
                'total_amount_after_tax': total_amount_after_tax,
                'purchase_number':purchase_number,
                'purchase_date':purchase_date,
                'eway_number':eway_number,
                'word_data':for_in_words,
                'qr_code_url':qr_file_path,
                'bill_date':only_date
            }
            
            pdf_file_name = generate_pdf('myapp/invoice_template.html', context)
            path_of_pdf="http://127.0.0.1:8000/view_pdf/"+pdf_file_name
            bill_details_store=bill_details(sno=bill_details.objects.count()+1,
                                            company_name=company_name,
                                            bill_id=invoice_number,
                                            total_amount=total_amount,
                                            sgst=sgst,
                                            cgst=cgst,
                                            total_amount_after_tax=total_amount_after_tax,
                                            created_on=created_on,
                                            created_by="Admin",
                                            status='A',
                                            file_path=path_of_pdf
                                            ).save()

            # Redirect to the PDF file for viewing
            # return redirect(f'/view_pdf/{pdf_file_name}')
            return redirect('get_bill_list')
        elif 'search_unit_form' in request.POST:
            if form.is_valid():
                search_query = form.cleaned_data['unit_name']
                unit_name = vendor_master_data.objects.filter(company_name__icontains=search_query,status='A')

    return render(request, 'myapp/bill_generate.html', {
        'form': form,
        'books': unit_name,
        'selected_unit': selected_unit
    })


############################################################
###############Quatation#####################################

def generate_pdf_qua(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)

    # Ensure the 'pdfs' directory exists
    pdf_dir = os.path.join(settings.BASE_DIR, 'pdfs/quatations')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Save PDF to the 'pdfs' directory
    file_name = f"invoice_{context_dict['invoice_number']}.pdf"
    file_path = os.path.join(pdf_dir, file_name)

    with open(file_path, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(html, dest=result_file)
    
    if pisa_status.err:
        return None  # Return None in case of an error
    
    return file_name  # Return the file name for redirection

def view_pdf_qua(request, pdf_file_name):
    # Construct the full file path
    file_path = os.path.join(settings.BASE_DIR, 'pdfs', 'quatations', pdf_file_name)
    print(f"Looking for file at: {file_path}")  # Debugging: Print the file path
    
    if os.path.exists(file_path):
        # Serve the PDF file in the browser
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        return HttpResponse('File not found', status=404)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'pdfs')

import os
from django.conf import settings
from django.http import FileResponse
@never_cache
def bill_generate_qua(request):
    #  # Check if user is logged in by looking for 'username' in session
    # if 'username' not in request.session:
    #     message = "You need to be logged in to access this page."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})

    # # Get role from session
    # user_role = request.session.get('role', None)

    # # Debugging: Print user role
    # print("User Role from session:", user_role)

    # # Check if role is 'admin'
    # if user_role != 'admin':
    #     message = "You do not have permission to access this page. Redirecting to the dashboard."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})
    form = search_unit_address(request.POST or None)
    unit_name = None
    selected_unit = None
    products = []

    if request.method == 'POST':
        # Handling the selected unit from search results
        if 'selected_unit' in request.POST:
            selected_unit_name = request.POST.get('selected_unit')
            if selected_unit_name:
                try:
                    selected_unit = vendor_master_data.objects.get(company_name=selected_unit_name)
                except vendor_master_data.DoesNotExist:
                    messages.error(request, "Unit not found.")
                    selected_unit = None

        # Handling the bill generation process
        elif 'bill_generate_qua' in request.POST:
            company_name = request.POST.get('company_name')
            billing_address = request.POST.get('billing_address')
            gst_number = request.POST.get('gst_number')
            city=request.POST.get('city')
            state=request.POST.get('state')
            pincode=request.POST.get('pincode')
            product_name_list = request.POST.getlist('product_name[]')
            Quantity_list = request.POST.getlist('Quantity[]')
            UOM_data_list = request.POST.getlist('UOM_data[]')
            price_list = request.POST.getlist('price[]')
            total_list=request.POST.getlist('totalAmount[]')
            print(total_list)

            total_amount = request.POST.get('totalAmountInput')
            sgst = request.POST.get('sgstInput')
            cgst = request.POST.get('cgstInput')
            igst=  request.POST.get('igstInput')
            total_amount_after_tax = request.POST.get('totalAmountAfterTaxInput')
            for_in_words=num2words(total_amount_after_tax, lang='en').capitalize()

            # Generate invoice number
            invoice_number = "QUA{:002d}".format(generate_bill_qua.objects.count() + 1)
            created_on=datetime.now()
            only_date=datetime.now().date

            # Storing data into the generate_bill table
            store_date_in_table = generate_bill_qua(
                sno=generate_bill_qua.objects.count() + 1,
                invoice_no=invoice_number,
                company_name=company_name,
                billing_address=billing_address,
                created_on=created_on,
                created_by="Admin",
                status='A',
            )
            store_date_in_table.save()

           
            for i in range(len(product_name_list)):
                try:
                    product_name = product_name_list[i]
                    quantity = float(Quantity_list[i])
                    uom = UOM_data_list[i]
                    price = float(price_list[i])
                    Amount=float(total_list[i])

                    # Store the product details
                    product_details_qua.objects.create(
                        sno=product_details_qua.objects.count() + 1,
                        product_name=product_name,
                        inv_bill=invoice_number,
                        Quantity=quantity,
                        UOM_data=uom,
                        price=price,
                        Amount=Amount,
                        created_on=created_on,
                        created_by="Admin",
                        status='A',
                    ).save()

                    products.append({
                        'product_name': product_name,
                        'Quantity': quantity,
                        'UOM_data': uom,
                        'price': price,
                        'Amount':Amount
                    })

                except ValueError as e:
                    print(f"Error processing row {i}: {e}")

            context = {
                'invoice_number': invoice_number,
                'company_name': company_name,
                'billing_address': billing_address,
                'city':city,
                'state':state,
                'pincode':pincode,
                'gst_number': gst_number,
                'products': products,
                'total_amount': total_amount,
                'sgst': sgst,
                'cgst': cgst,
                'igst':igst,
                'total_amount_after_tax': total_amount_after_tax,
                'word_data':for_in_words,
                'qua_date':only_date
            }
            
            pdf_file_name = generate_pdf_qua('myapp/invoice_template_qua.html', context)
            path_of_pdf="http://127.0.0.1:8000/view_pdf_qua/"+pdf_file_name
            bill_details_store=bill_details_qua(sno=bill_details_qua.objects.count()+1,
                                            company_name=company_name,
                                            bill_id=invoice_number,
                                            total_amount=total_amount,
                                            sgst=sgst,
                                            cgst=cgst,
                                            total_amount_after_tax=total_amount_after_tax,
                                            created_on=created_on,
                                            created_by="Admin",
                                            status='A',
                                            file_path=path_of_pdf
                                            ).save()

            # Redirect to the PDF file for viewing
            # return redirect(f'/view_pdf/{pdf_file_name}')
            return redirect('get_bill_list_qua')
        elif 'search_unit_form' in request.POST:
            if form.is_valid():
                search_query = form.cleaned_data['unit_name']
                unit_name = vendor_master_data.objects.filter(company_name__icontains=search_query,status='A')

    return render(request, 'myapp/bill_generate_qua.html', {
        'form': form,
        'books': unit_name,
        'selected_unit': selected_unit
    })

###############################################################
def view_pdf(request, pdf_file_name):
    file_path = os.path.join('pdfs', pdf_file_name)
    if os.path.exists(file_path):
        # Serve the PDF file in the browser
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        return HttpResponse('File not found', status=404)

@never_cache
def get_bill_list(request):
    #  # Check if user is logged in by looking for 'username' in session
    # if 'username' not in request.session:
    #     message = "You need to be logged in to access this page."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})

    # # Get role from session
    # user_role = request.session.get('role', None)

    # # Debugging: Print user role
    # print("User Role from session:", user_role)

    # # Check if role is 'admin'
    # if user_role != 'admin':
    #     message = "You do not have permission to access this page. Redirecting to the dashboard."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})
    bill_data = bill_details.objects.filter(status='A').order_by("-bill_id")
    
    if request.method == 'POST' and 'get_bill_list' in request.POST:
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        if from_date and to_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()+ timedelta(days=1)
            # Filter bill data between from_date and to_date
           
            bill_data = bill_data.filter(created_on__gte=from_date, created_on__lt=to_date)

    # Pagination: Show 10 records per page
    paginator = Paginator(bill_data, 10)
    page_number = request.GET.get('page', 1)
    bill_obj = paginator.get_page(page_number)

    return render(request, 'myapp/get_bill_list.html', {'page_obj': bill_obj})

def check_role(user, role):
    return user.role == role  

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.core.paginator import Paginator


def get_bill_list_qua(request):
    # # Get role from session
    # user_role = request.session.get('role', None)

    # # Debugging: Print user role
    # print("User Role from session:", user_role)

    # # Check if role is 'admin'
    # if user_role != 'admin':
    #     message = "You do not have permission to access this page. Redirecting to the dashboard."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/dashboard/'})

    # Fetch bill data
    bill_data = bill_details_qua.objects.filter(status='A').order_by("-bill_id")
    
    if request.method == 'POST' and 'get_bill_list' in request.POST:
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        if from_date and to_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date() + timedelta(days=1)
            # Filter bill data between from_date and to_date
            bill_data = bill_data.filter(created_on__gte=from_date, created_on__lte=to_date)

    paginator = Paginator(bill_data, 10)
    page_number = request.GET.get('page', 1)
    bill_obj = paginator.get_page(page_number)

    return render(request, 'myapp/get_bill_list_qua.html', {'page_obj': bill_obj})




# Register view
@never_cache
def register_and_list_view(request):
    # Check if user is logged in by looking for 'username' in session
    # if 'username' not in request.session:
    #     message = "You need to be logged in to access this page."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/login/'})

    # # Get role from session
    # user_role = request.session.get('role', None)

    # # Debugging: Print user role
    # print("User Role from session:", user_role)

    # # Check if role is 'admin'
    # if user_role != 'admin':
    #     message = "You do not have permission to access this page. Redirecting to the dashboard."
    #     return render(request, 'myapp/message_page.html', {'message': message, 'redirect_url': '/vendor_list/'})

    # If the user is an admin and authenticated, continue with form handling
    if request.method == 'POST' and 'register_view' in request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        # Check if username or email already exists
        if User.objects(username=username) or User.objects(email=email):
            return HttpResponse("Username or email already exists.")

        # Check if passwords match
        if password != confirm_password:
            return HttpResponse("Passwords do not match.")

        # Create and save the new user
        user = User(username=username, email=email, role=role, status='A')
        user.set_password(password)
        user.save()

        return redirect('register')  # Redirect after successful registration

    # Get the list of users for display
    users = User.objects.filter(status='A')  # Adjust query as needed

    # Render the template with both the form and user list
    return render(request, 'myapp/register.html', {'page_obj': users})

# Login view

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        if not username or not password:
            return HttpResponse("Please enter both username and password.")

        try:
            # Check if user exists by username
            user = User.objects.get(username=username)

            # Check password manually (since authenticate is not working with MongoEngine)
            if user.check_password(password):  # Ensure you have a method to check password
                
                # If password is correct, set session variables
                request.session['username'] = user.username
                request.session['role'] = user.role
                print(user.role)

                # Redirect based on user role
                if user.role == 'admin':
                    return redirect('dashboard')  # Redirect to admin dashboard
                elif user.role == 'user':
                    return redirect('vendor_list')  # Redirect to vendor list for regular users
                else:
                    return HttpResponseForbidden("You do not have permission to access this page.")
            else:
                return HttpResponse("Invalid credentials.")
        
        except User.DoesNotExist:
            return HttpResponse("User does not exist.")
    
    return render(request, 'myapp/login.html')



@login_required
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')  # Redirect to the URL pattern named 'login'




# Home view (role-based access control)

@login_required
@never_cache
def home_view(request):
    role = request.session.get('role', None)
    if role == 'admin':
        return render(request, 'myapp/dashboard.html')
    elif role == 'user':
        return render(request, 'myapp/vendor_list.html')
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")
    
