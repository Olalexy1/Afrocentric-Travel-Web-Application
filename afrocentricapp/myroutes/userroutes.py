'''This file is the controller that determines the path when the user visits our routes'''
from faulthandler import disable
from locale import currency
import random, requests, urllib3, json
from os import stat_result
from flask import render_template, request, abort, redirect, flash, make_response, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from afrocentricapp import app, db
from afrocentricapp.mymodels import Admin, Country, CustomRequest, Customer, Destination, Inclusive, Order, OrderDetails, Product, Shipment, State, Subscribers, pkg_inclusions, Tourbooking, Tourpackage, TourpackagePayment, Visa, VisaPayment, Visaprocurement, Contactus, Reviews

@app.route("/")
def home():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    tourdeets = Tourpackage.query.all()
    revdeets = Reviews.query.all()
    if user == None:
        return render_template ('/user/afrocentricext.html', tourdeets=tourdeets, revdeets=revdeets)
    else:
        return render_template ('/user/afrocentricext.html', userdeets=userdeets, tourdeets=tourdeets, revdeets=revdeets)
  


@app.route('/register', methods=['GET','POST'])
def register():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if request.method == 'GET':
        return render_template('/user/afrocentricext.html', userdeets=userdeets)
    else:
        email = request.form.get('email')
        pswd1 = request.form.get('pswd1')
        pswd2 = request.form.get('pswd2')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        #validate
        if email == '' or pswd1 == '' or firstname == '' or lastname == '' or pswd2 == '' or gender == '':
            flash('Registration failed, kindly fill the reqiured fields', 'warning')
            return redirect ('/')
        elif pswd1 != pswd2:
            flash('Kindly ensure that the passwords match', 'warning')
            return redirect ('/')
        else:
            formated = generate_password_hash(pswd1)
            flash('Registration sucessful')
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
        flash('Login failed, kindly fill the reqiured fields', 'warning')
        return redirect('/')
    else:
        userdeets = Customer.query.filter(Customer.customer_email==email).first()
        formated_password =  userdeets.customer_pword
        check_password = check_password_hash(formated_password,pswd)

        if check_password == True:
            session['loggedin'] = userdeets.customer_id
            return redirect ('/')
        else:
            flash('Invalid Credentials')
            return redirect ('/')



@app.route('/logout')
def logout():
    session.pop('loggedin')
    return redirect ('/')


@app.route('/request', methods=['GET','POST'])
def custrequests():
    user = session.get('loggedin')
    userdeets = Customer.query.get(user)
    countrydeets = Country.query.all()
    if request.method == 'GET':
        return render_template('user/custompackage.html', countrydeets=countrydeets, userdeets=userdeets)
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
            flash('Kindly fill in the reuired fields')
            return redirect('/request')
        else:
            req = CustomRequest(custom_request_fname=firstname, custom_request_lname=lastname, custom_request_email=email, customer_request_phone=phone, custom_request_country=country, custom_request_origin_city=origin, custom_request_destination_city= destination, custom_request_travel_date=departure, custom_request_return_date=returndate, custom_request_additional_info=information, custom_request_group_size=size)
            db.session.add(req)
            db.session.commit()
            flash('Request has been sent. You will get feedback in 48hrs')
            return redirect('/request')


@app.route('/contact', methods=['GET','POST'])
def contact():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if request.method == 'GET':
        return render_template ('/user/contactus.html', userdeets=userdeets)
    else:
        fullname = request.form.get('fullname')
        subject = request.form.get('subject')
        email = request.form.get('email')
        message = request.form.get('message')
        cont = Contactus(contactus_fullname=fullname, contactus_email=email, contactus_subject=subject, contactus_message=message)
        db.session.add(cont)
        db.session.commit()
        flash('Request has been sent. You will get feedback in 48hrs')
        return redirect('/contact')

@app.route("/about")
def about():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if user == None:
        return render_template ('/user/aboutus.html')
    else:
        return render_template ('/user/aboutus.html', userdeets=userdeets)


@app.route("/blog")
def blog():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if user == None:
        return render_template ('/user/blog.html')
    else:
        return render_template ('/user/blog.html', userdeets=userdeets)


@app.route('/subscribers', methods=['GET','POST'])
def sub():
    email = request.form.get('email')
    subscribe = Subscribers(subscribers_email=email)
    db.session.add(subscribe)
    db.session.commit()
    flash('You have successfully subscribed to our newsletters')
    return redirect('/')


@app.route('/tourpackage')
def package():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    tourdeets = Tourpackage.query.all()
    inclusions = Inclusive.query.all()
    tourinclude = db.session.query(pkg_inclusions).join(Tourpackage).join(Inclusive).filter(Tourpackage.tourpackage_id == Inclusive.inclusive_id )

    if user == None:
        return render_template ('/user/tourpackages.html', tourdeets=tourdeets, inclusions=inclusions, tourinclude = tourinclude)
    else:
        return render_template ('/user/tourpackages.html', userdeets=userdeets, tourdeets=tourdeets, inclusions=inclusions, tourinclude=tourinclude)

@app.route('/visa')
def visas():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    visadeets = Visa.query.all()
    if user == None:
        return render_template ('/user/tourpackages.html', visadeets=visadeets)
    else:
        return render_template ('/user/tourpackages.html', userdeets=userdeets, visadeets=visadeets)


@app.route("/user")
def user():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if user == None:
        return render_template ('/user/afrocentricext.html')
    else:
        return render_template ('/user/userdashboard.html', userdeets=userdeets)


@app.route('/booktour/<int:id>',methods=['GET','POST'])
def bookings(id):
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    tourdeets = Tourpackage.query.get(id)
    if request.method == 'GET':
        return render_template ('/user/booking.html', tourdeets=tourdeets, userdeets=userdeets)
    else:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        status = 'Pending'
        email = request.form.get('email')
        tourpackageid = tourdeets.tourpackage_id
        ref = int(random.random() * 1000000000) 
        session['refno'] = ref
        amount = request.form.get('amount')
        booking = Tourbooking(tourbooking_customer_email=email, tourbooking_status=status, tourbooking_fname=firstname, tourbooking_lname=lastname, tourbooking_ref=ref, fk_tourbooking_tourpackageid=tourpackageid, fk_tourbooking_customerid=user, tourbooking_amount=amount)
        db.session.add(booking)
        db.session.commit()
        flash('Tour has been booked, you have 24hrs to confirm this booking by completing payment')
        return redirect('/booktour/confirmpayment')


#This route will show all chosen sessions and connect to paystack
@app.route("/booktour/confirmpayment", methods=['GET','POST'])
def confirm():
    user = session.get('loggedin')
    userdeets = Customer.query.get(user)
    ref = session.get('refno')
    if ref== None:
        return redirect('/tourpackage')
    else:
        bookdeets = Tourbooking.query.filter(Tourbooking.tourbooking_ref== ref).first()
        
        if request.method == 'GET':
            return render_template('user/confirmpayment.html', userdeets=userdeets, bookdeets=bookdeets)
        else:
            data = {"email":bookdeets.tourbooking_customer_email,"amount":bookdeets.tourbooking_amount*100, "ref":bookdeets.tourbooking_ref}
            headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_dadd9863193a1e432e4c765c77d4386f3e009646"}

            response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))

            rspjson = json.loads(response.text) 
            if rspjson.get("status") == True:
                authurl = rspjson["data"]["authorization_url"]
                return redirect(authurl)
            else:
                return "Please try again"


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
        payment = TourpackagePayment(tourpackage_payment_amount= amount, tourpackage_payment_status = status, tourpackage_payment_method = method, tourpackage_payment_currency = currency, fk_tourpackage_payment_tourpackage_id = update.fk_tourbooking_tourpackageid, fk_tourpackage_payment_tourbooking_id = update.tourbooking_id, tourpackage_payment_ref = update.tourbooking_ref)
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
        return render_template('user/blog.html', data3 = data3, info = info, reference = reference, refnumber = refnumber)

    else:
        status = 'Failed'
        payment = TourpackagePayment(tourpackage_payment_amount= amount, tourpackage_payment_status = status, tourpackage_payment_method = method, tourpackage_payment_currency = currency, fk_tourpackage_payment_tourpackage_id = update.fk_tourbooking_tourpackageid, fk_tourpackage_payment_tourbooking_id = update.tourbooking_id)

        db.session.add(payment)
        db.session.commit()

        return "Payment Failed"


@app.route('/reviews', methods=['GET','POST'])
def reviews():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if request.method == 'GET':
        return render_template ('/user/reviews.html', userdeets=userdeets)
    else:
        fullname = request.form.get('fullname')
        ratings = request.form.get('ratings')
        email = request.form.get('email')
        message = request.form.get('message')
        rev = Reviews (r_customer_fullname=fullname, r_customer_email=email, review_ratings=ratings, review_Info=message)
        db.session.add(rev)
        db.session.commit()
        flash('Your review is well received')
        return redirect('/reviews')


@app.route('/profile')
def profile():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    Male = 'Male'
    if user == None:
        return redirect ('/')
    if request.method == 'GET':
        return render_template('user/profile.html', userdeets = userdeets, Male = Male)


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

        if pswd1 != pswd2:
            flash('Kindly ensure that the passwords match')
            return redirect ('/profile')

        else:
            formated = generate_password_hash(pswd1)

            userdeets.customer_fname = firstname
            userdeets.customer_lname = lastname
            userdeets.customer_pword = formated
            userdeets.customer_phone = phone
            userdeets.customer_gender = gender
            userdeets.customer_email = email
            db.session.commit()

            return redirect('/user')



            