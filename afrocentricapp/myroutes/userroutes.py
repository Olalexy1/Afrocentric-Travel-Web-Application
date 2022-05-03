'''This file is the controller that determines the path when the user visits our routes'''
from faulthandler import disable
from locale import currency
import random, requests, urllib3, json, jsonpickle
from json import JSONEncoder
from os import stat_result
from flask import Flask, render_template, request, abort, redirect, flash, make_response, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from afrocentricapp import app, db
from afrocentricapp.mymodels import Admin, Country, CustomRequest, Customer, Destination, Inclusive, Order, OrderDetails, Product, Shipment, State, Subscribers, pkg_inclusions, Tourbooking, Tourpackage, TourpackagePayment, Visa, VisaPayment, Visaprocurement, Contactus, Reviews



@app.route("/")
def home():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    tourdeets = Tourpackage.query.all()
    revdeets = Reviews.query.all()
    destdeets = Destination.query.all()
    if user == None:
        return render_template ('/user/afrocentricext.html', tourdeets=tourdeets, revdeets=revdeets, destdeets = destdeets)
    else:
        return render_template ('/user/afrocentricext.html', userdeets=userdeets, tourdeets=tourdeets, revdeets=revdeets, destdeets = destdeets)
  


@app.route('/register', methods=['GET','POST'])
def register():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    destdeets = Destination.query.all()
    if request.method == 'GET':
        return render_template('/user/afrocentricext.html', userdeets=userdeets, destdeets = destdeets)
    else:
        email = request.form.get('email')
        pswd1 = request.form.get('pswd1')
        pswd2 = request.form.get('pswd2')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        
        userdeets2 = userdeets = Customer.query.filter(Customer.customer_email==email).first()
        
        #validate
        if email == '' or pswd1 == '' or firstname == '' or lastname == '' or pswd2 == '' or gender == '':
            flash('Registration failed, kindly fill the required fields', 'warning')
            return redirect ('/')
        elif userdeets2:
            flash('Email already exists', 'warning')
            return redirect ('/')
        elif pswd1 != pswd2:
            flash('Kindly ensure that the passwords match', 'warning')
            return redirect ('/')
        else:
            formated = generate_password_hash(pswd1)
            flash('Registration successful', 'success')
            profile = Customer(customer_email = email, customer_pword = formated, customer_fname = firstname, customer_lname = lastname, customer_phone = phone, customer_gender = gender)
            db.session.add(profile)
            db.session.commit()
            user = profile.customer_id
            session['loggedin'] = user
            return redirect('/')


@app.route('/login', methods=['GET','POST'])
def login():
    email = request.form.get('email')
    pswd = request.form.get('pswd')

    if email == '' or pswd == '':
        flash('Login failed, kindly fill the required fields', 'warning')
        return redirect('/')
    else:
        userdeets = Customer.query.filter(Customer.customer_email==email).first()
        formated_password =  userdeets.customer_pword
        check_password = check_password_hash(formated_password,pswd)

        if check_password == True:
            session['loggedin'] = userdeets.customer_id
            return redirect ('/')
        else:
            flash('Invalid login credentials', 'warning')
            return redirect ('/')



@app.route('/logout')
def logout():
    user = session.get('loggedin')
    if user == None:
        return redirect ('/')
    else:
        session.pop('loggedin')
        return redirect ('/')


@app.route('/request', methods=['GET','POST'])
def custrequests():
    user = session.get('loggedin')
    userdeets = Customer.query.get(user)
    countrydeets = Country.query.all()
    destdeets = Destination.query.all()
    if request.method == 'GET':
        return render_template('user/custompackage.html', countrydeets=countrydeets, userdeets=userdeets, destdeet = destdeets)
    else:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        country = request.form.get('country')
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        departure = request.form.get('departuredate')
        returndate = request.form.get('returndate')
        information = request.form.get('additional')
        size = request.form.get('inlineRadioOptions')
        if email == '' or phone == '' or firstname == '' or lastname == '' or phone == '' or country == '' or origin == '' or destination == '' or departure == '' or returndate == '':
            flash('Kindly fill in the required fields')
            return redirect('/request')
        else:
            req = CustomRequest(custom_request_fname=firstname, custom_request_lname=lastname, custom_request_email=email, customer_request_phone=phone, custom_request_country=country, custom_request_origin_city=origin, custom_request_destination_city= destination, custom_request_travel_date=departure, custom_request_return_date=returndate, custom_request_additional_info=information, custom_request_group_size=size)
            db.session.add(req)
            db.session.commit()
            flash('Request has been sent. You will get feedback in 48hrs', 'info')
            return redirect('/request')


@app.route('/contact', methods=['GET','POST'])
def contact():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    destdeets = Destination.query.all()
    if request.method == 'GET':
        return render_template ('/user/contactus.html', userdeets=userdeets, destdeets = destdeets)
    else:
        fullname = request.form.get('fullname')
        subject = request.form.get('subject')
        email = request.form.get('email')
        message = request.form.get('message')
        cont = Contactus(contactus_fullname=fullname, contactus_email=email, contactus_subject=subject, contactus_message=message)
        db.session.add(cont)
        db.session.commit()
        flash('Message has been sent. You will get feedback in 48hrs', 'info')
        return redirect('/contact')

@app.route("/about")
def about():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    destdeets = Destination.query.all()
    if user == None:
        return render_template ('/user/aboutus.html')
    else:
        return render_template ('/user/aboutus.html', userdeets=userdeets, destdeets = destdeets)


@app.route("/blog")
def blog():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    destdeets = Destination.query.all()
    if user == None:
        return render_template ('/user/blog.html')
    else:
        return render_template ('/user/blog.html', userdeets=userdeets, destdeets = destdeets)


@app.route('/subscribers', methods=['GET','POST'])
def sub():
    email = request.form.get('email')
    subscribe = Subscribers(subscribers_email=email)
    db.session.add(subscribe)
    db.session.commit()
    flash('You have successfully subscribed to our newsletters', 'success')
    return redirect('/')


@app.route('/tourpackage')
def package():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    tourdeets = Tourpackage.query.all()
    inclusions = Inclusive.query.all()
    destdeets = Destination.query.all()

    if user == None:
        return render_template ('/user/tourpackages.html', tourdeets=tourdeets, inclusions=inclusions, destdeets = destdeets)
    else:
        return render_template ('/user/tourpackages.html', userdeets=userdeets, tourdeets=tourdeets, inclusions=inclusions, destdeets = destdeets)

@app.route('/visa')
def visas():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    visadeets = Visa.query.all()
    destdeets = Destination.query.all()
    if user == None:
        return render_template ('/user/tourpackages.html', visadeets=visadeets, destdeets = destdeets)
    else:
        return render_template ('/user/tourpackages.html', userdeets=userdeets, visadeets=visadeets, destdeets = destdeets)


@app.route("/user")
def user():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    destdeets = Destination.query.all()
    if user == None:
        return render_template ('/user/afrocentricext.html', destdeets = destdeets)
    else:
        return render_template ('/user/userdashboard.html', userdeets=userdeets, destdeets = destdeets)


@app.route('/booktour/<int:id>',methods=['GET','POST'])
def bookings(id):
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    tourdeets = Tourpackage.query.get(id)
    destdeets = Destination.query.all()
    inclusions = Inclusive.query.all()
    if request.method == 'GET':
        return render_template ('/user/booking.html', inclusions = inclusions, tourdeets=tourdeets, userdeets=userdeets, destdeets = destdeets)
    else:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        status = 'Pending'
        email = request.form.get('email')
        tourpackageid = tourdeets.tourpackage_id
        ref = int(random.random() * 1000000000) 
        session['refno'] = ref
        amount = request.form.get('amount')
        if amount == "":
            flash ('Please select an accommodation type', 'warning')
        else:
            booking = Tourbooking(tourbooking_customer_email=email, tourbooking_status=status, tourbooking_fname=firstname, tourbooking_lname=lastname, tourbooking_ref=ref, fk_tourbooking_tourpackageid=tourpackageid, fk_tourbooking_customerid=user, tourbooking_amount=amount)
            db.session.add(booking)
            db.session.commit()
            flash (f'Tour has been booked, your reference number is {ref} and you have 24hrs to confirm this booking by completing payment.', 'info')
            return redirect('/booktour/confirmpayment')


#This route will show all chosen sessions and connect to paystack
@app.route("/booktour/confirmpayment", methods=['GET','POST'])
def confirm():
    user = session.get('loggedin')
    userdeets = Customer.query.get(user)
    destdeets = Destination.query.all()
    ref = session.get('refno')
    if ref== None:
        return redirect('/tourpackage')
    else:
        bookdeets = Tourbooking.query.filter(Tourbooking.tourbooking_ref== ref).first()
        
        if request.method == 'GET':
            return render_template('user/confirmpayment.html', userdeets=userdeets, bookdeets=bookdeets, destdeets = destdeets)
        else:
            data = {"email":bookdeets.tourbooking_customer_email,"amount":bookdeets.tourbooking_amount * 100, "ref":bookdeets.tourbooking_ref}
            headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_dadd9863193a1e432e4c765c77d4386f3e009646"}

            response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))

            rspjson = json.loads(response.text) 
            if rspjson.get("status") == True:
                authurl = rspjson["data"]["authorization_url"]
                return redirect(authurl)
            else:
                flash('Please Try Again', 'warning')
                return render_template ('/user/booking.html', userdeets=userdeets, destdeets = destdeets)


@app.route('/user/paystack')
def paystack():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    reference = request.args.get('reference')
    ref = session.get('refno')
    #update db
    headers = {"content-Type": "application/json","Authorization":"Bearer sk_test_dadd9863193a1e432e4c765c77d4386f3e009646"}

    response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
    rsp=response.json()
    if rsp['data']['status'] == 'success':
        amount = rsp['data']['amount']
        method = rsp['data']['channel']
        currency = rsp['data']['currency']
        refnumber = rsp['data']['reference']

        update = Tourbooking.query.filter(Tourbooking.tourbooking_ref==ref).first()
        update.tourbooking_status = 'Confirmed'
        db.session.commit()

        update.tourbooking_ref
        update.tourbooking_id
        update.fk_tourbooking_tourpackageid
        status = 'Successful'
        payment = TourpackagePayment(tourpackage_payment_amount= amount/100, tourpackage_payment_status = status, tourpackage_payment_method = method, tourpackage_payment_currency = currency, fk_tourpackage_payment_tourpackage_id = update.fk_tourbooking_tourpackageid, fk_tourpackage_payment_tourbooking_id = update.tourbooking_id, tourpackage_booking_ref = update.tourbooking_ref, tourpackage_paystack_ref=reference)
        db.session.add(payment)
        db.session.commit()


        tourdeets = Tourpackage.query.get(update.fk_tourbooking_tourpackageid)
        tourdeets.tourpackage_slot
        bookinfo = db.session.execute(f"SELECT COUNT(tourbooking_status) FROM tourbooking WHERE tourbooking_status='Confirmed' AND fk_tourbooking_tourpackageid = {update.fk_tourbooking_tourpackageid}")

        data = bookinfo.fetchall()
        data2 = data[0]
        data3 = data2[0]

    
        if data3 > 0 or data3 < tourdeets.tourpackage_available:
            db.session.execute(f"UPDATE tourpackage SET tourpackage_slot = (tourpackage_available - {data3}) WHERE tourpackage_id = {update.fk_tourbooking_tourpackageid}")
            db.session.commit()
            info = "Payment successful"
        else:
            pass
        flash('Payment Successful', 'success')
        return render_template('user/successpage.html', data3 = data3, info = info, reference = reference, refnumber = refnumber, update = update, payment = payment, userdeets = userdeets)

    else:
        status = 'Failed'
        payment = TourpackagePayment(tourpackage_payment_amount= amount/100, tourpackage_payment_status = status, tourpackage_payment_method = method, tourpackage_payment_currency = currency, fk_tourpackage_payment_tourpackage_id = update.fk_tourbooking_tourpackageid, fk_tourpackage_payment_tourbooking_id = update.tourbooking_id)

        db.session.add(payment)
        db.session.commit()

        flash('Payment Failed', 'warning')
        return redirect('/booktour/confirmpayment')


# @app.route('/paymentsuccess')
# def paysuccess():
#     user = session.get('loggedin')
#     userdeets =  Customer.query.get(user)


@app.route('/reviews', methods=['GET','POST'])
def reviews():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    destdeets = Destination.query.all()
    if request.method == 'GET':
        return render_template ('/user/reviews.html', userdeets=userdeets, destdeets = destdeets)
    else:
        fullname = request.form.get('fullname')
        ratings = request.form.get('ratings')
        email = request.form.get('email')
        message = request.form.get('message')
        rev = Reviews (r_customer_fullname=fullname, r_customer_email=email, review_ratings=ratings, review_Info=message)
        db.session.add(rev)
        db.session.commit()
        flash('Your review has been received', 'info')
        return redirect('/reviews')


@app.route('/profile')
def profile():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    destdeets = Destination.query.all()
    Male = 'Male'
    if user == None:
        return redirect ('/')
    if request.method == 'GET':
        return render_template('user/profile.html', userdeets = userdeets, Male = Male, destdeets = destdeets)


@app.route('/customer/bookings')
def cust_booking():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    destdeets = Destination.query.all()
    bookdeets = Tourbooking.query.filter(Tourbooking.fk_tourbooking_customerid==user).all()
    if user == None:
        return redirect ('/')
    if request.method == 'GET':
        return render_template('user/custbooking.html', bookdeets=bookdeets, userdeets = userdeets, destdeets = destdeets)
    

# @app.route('/customer/payments')
# def cust_payment():
#     user = session.get('loggedin')
#     userdeets =  Customer.query.get(user)
#     destdeets = Destination.query.all()
    
#     if user == None:
#         return redirect ('/')
#     if request.method == 'GET':
#         return render_template('user/custpayment.html', bookdeets=bookdeets, userdeets = userdeets, destdeets = destdeets)


@app.route('/update', methods=['GET','POST'])
def user_update():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if user == None:
        return redirect ('/')
    if request.method == 'GET':
        return redirect('/profile')
    else:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        pswd1 = request.form.get('pswd1')
        pswd2 = request.form.get('pswd2')
        gender = request.form.get('gender')
        pswd = request.form.get('pswd')

        formated_password =  userdeets.customer_pword
        check_password = check_password_hash(formated_password,pswd)

    
        if check_password != True:
            flash('Kindly enter the correct password', 'warning')
            return redirect ('/profile')
        elif pswd1 != pswd2:
            flash('Kindly ensure that the passwords match', 'warning')
            return redirect ('/profile')
        else:
            if check_password == True:
                formated = generate_password_hash(pswd1)
                userdeets.customer_fname = firstname
                userdeets.customer_lname = lastname
                userdeets.customer_pword = formated
                userdeets.customer_phone = phone
                userdeets.customer_gender = gender
                userdeets.customer_email = email
                db.session.commit()

                return redirect('/user')


@app.route('/search/destination', methods=['GET','POST'])
def searchbar():
    user = session.get('loggedin')
    userdeets = Customer.query.get(user)
    destdeets = Destination.query.all()
    inclusions = Inclusive.query.all()
    
    dest = request.form.get('destination')

    searchdeets = Tourpackage.query.filter(Tourpackage.fk_tourpackage_destination_id == dest).all()

    return render_template ('/user/tourpackagessearch.html', userdeets=userdeets, inclusions=inclusions, destdeets = destdeets, searchdeets = searchdeets, destination=dest)


@app.route('/search/tourpackage', methods=['GET','POST'])
def search():
    user = session.get('loggedin')
    userdeets = Customer.query.get(user)
    destdeets = Destination.query.all()
    inclusions = Inclusive.query.all()

    search = request.form.get('search')
    searched = "%{}%".format(search)

    searchdeets = Tourpackage.query.filter(Tourpackage.tourpackage_name.like(searched)).all()

    return render_template ('/user/tourpackagessearch.html', userdeets=userdeets, inclusions=inclusions, destdeets = destdeets, searchdeets = searchdeets)


# @app.route('/search/tourpackage/new', methods=['POST'])
# def search_cat():
#     user = session.get('loggedin')
#     userdeets = Customer.query.get(user)

#     search = request.form.get('search')
#     searched = "%{}%".format(search)

#     searchdeets = Tourpackage.query.filter(Tourpackage.tourpackage_name.like(searched)).all()

#     if searchdeets:
#         return json.dumps({'searchdeets':searchdeets})
#     return jsonify({'error' : 'Missing data!'})




    












