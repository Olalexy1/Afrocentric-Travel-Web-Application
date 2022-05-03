'''This file is the controller that determines the path when the user visits our routes'''
from ast import Sub
import math, random, os, datetime
from unicodedata import category

from flask import render_template, request, abort, redirect, flash, make_response, session, url_for
from pkg_resources import Requirement

from sqlalchemy import or_, desc


from werkzeug.security import generate_password_hash, check_password_hash

from afrocentricapp import app, db 
from afrocentricapp.mymodels import Admin, Country, CustomRequest, Customer, Destination, Inclusive, Order, OrderDetails, Product, Shipment, State, pkg_inclusions, Tourbooking, Tourpackage, TourpackagePayment, Visa, VisaPayment, Visaprocurement, Subscribers, Reviews, Contactus




@app.route('/admin/login')
def adminlogin():
    admin = session.get('admin')
    if admin == None:
        return render_template('admin/adminlogin.html')
    else:
        return redirect ('/admin/dashboard')



@app.route("/admin/submit/login", methods=['GET','POST'])
def submit_adminlogin():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email == '' or password == '':
        flash('Login failed, kindly fill the required fields', 'warning')
        return redirect ('/admin/login')
    else:
        admindeets = Admin.query.filter(Admin.admin_email == email).first()
        formated_password =  admindeets.admin_password
        check_password = check_password_hash(formated_password,password)
        
        if check_password == True:
            admin = admindeets.admin_id
            session['admin'] = admin
            return redirect(url_for('adminpage'))
        else:
            flash('Invalid login credentials', 'warning')
            return redirect(url_for('adminlogin'))



@app.route('/admin/dashboard')
def adminpage():
    admin = session.get('admin')
    if admin == None:
        return redirect(url_for('adminlogin'))
    else:
        admindeets = Admin.query.get(admin)
        return render_template('admin/admindashboardext.html', admindeets = admindeets)


@app.route('/admin/logout')
def admin_logout():
    admin = session.get('admin')
    if admin == None:
        return redirect(url_for('adminlogin'))
    else:
        session.pop('admin')
        return redirect ('/admin/login')
    

@app.route('/admin/register', methods=['GET','POST'])
def admin_register():
    admin = session.get('admin')
    admindeets = Admin.query.all()
    if request.method == 'GET':
        return render_template('admin/adminregistration.html', admindeets= admindeets)
    else:
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        admindeets = db.session.query(Admin).filter(Admin.admin_email == email).first()

        if email == '' or firstname == '' or lastname == '' or password1 == '' or password2 == '':
            flash('Registration failed, kindly fill the required fields', 'warning')
            return redirect (url_for('admin_register'))
        elif admindeets:
            flash("Email already exists", 'warning')
            return redirect (url_for('admin_register'))
        elif password1 != password2:
            flash("The two passwords do not match", 'warning')
            return redirect (url_for('admin_register'))
        else:
            formated = generate_password_hash(password1)
            regdeets = Admin(admin_fname = firstname, admin_lname = lastname, admin_email = email, admin_password = formated)
            db.session.add(regdeets)
            db.session.commit()
            flash('Admin Registration successful', 'success')
            admin = regdeets.admin_id
            session['admin'] = admin
            return redirect('/admin/login')
            


           
@app.route('/admin/tourpackage')
def tourpackage():
    admin = session.get('admin')
    if admin == None:
        return redirect('/admin/login')
    else:
        admindeets = Admin.query.get(admin)
        tourdeets = Tourpackage.query.all()
        return render_template('admin/tourpackageext.html', tourdeets = tourdeets, admindeets = admindeets)




@app.route('/admin/addtourpackage', methods=['GET','POST'])
def addtourpackage():
    destdeets = Destination.query.all()
    admin = session.get('admin')
    if admin == None:
        return redirect('/admin/login')
    else:
        admindeets = Admin.query.get(admin)
        if request.method =='GET':
            inclusions = Inclusive.query.all()
            return render_template('admin/addtourext.html', inclusions= inclusions, admindeets = admindeets, destdeets = destdeets)
        else:
            tourname = request.form.get('tourname')
            price_share = request.form.get('price_share')
            price_single = request.form.get('price_single')
            tourdesc = request.form.get('tourdesc')
            departuredate = request.form.get('departuredate')
            returndate = request.form.get('returndate')
            slot = request.form.get('slot')
            inclusives =request.form.getlist('inclusive')
            destname = request.form.get('destination')

           
            pic_object = request.files.get('tourimage')
            original_file =  pic_object.filename
            if tourname =='' or price_share =='' or tourdesc =='' or price_single == '' or departuredate == '' or returndate =='' or slot =='':
                flash("Kindly fill all required field", 'warning')
                return redirect('/admin/addtourpackage')

            if original_file !='': 
                extension = os.path.splitext(original_file)
                if extension[1].lower() in ['.jpg','.png']:
                    fn = math.ceil(random.random() * 100000000)  
                    save_as = str(fn)+extension[1] 
                    pic_object.save(f"afrocentricapp/static/assets/img/tourpackages/{save_as}")
                    
                    tour = Tourpackage(tourpackage_name=tourname, tourpackage_price_sharing=price_share, tourpackage_pics=save_as, tourpackage_price_single=price_single, tourpackage_desc=tourdesc, tourpackage_dept_date=departuredate, tourpackage_rtn_date= returndate, tourpackage_available=slot, fk_tourpackage_destination_id = destname)
                    db.session.add(tour)
                    db.session.commit()

                    for i in inclusives:
                        include = pkg_inclusions.insert().values(fk_pkg_inclusive_tourpackage_id=tour.tourpackage_id,fk_pkg_inclusive_id=i)
                        db.session.execute(include)
                        db.session.commit()
                        flash('Tour Package Added', 'success')         
                    return redirect("/admin/tourpackage")
                else:
                    flash('File Not Allowed', 'success')
                    return redirect("/admin/addtourpackage")

            else:
                save_as = ""
                flash('Upload a file', 'success')
                return redirect("/admin/addtourpackage")




@app.route('/admin/tourpackage/delete/<int:id>')
def admin_delete(id):
    admin = session.get('admin')
    if admin == None:
        return redirect('/admin/login')
    else:
        tourdeets = db.session.query(Tourpackage).get(id)
        db.session.delete(tourdeets)
        db.session.commit()
        flash(f'Tour package {id} deleted', 'warning')
        return redirect('/admin/tourpackage')




@app.route('/admin/tourpackage/modify/<int:id>', methods=['GET','POST'])
def admin_modify(id):
    admin = session.get('admin')
    tourdeets = Tourpackage.query.get(id)
    destdeets = Destination.query.all()
    if admin == None:
        return redirect('/admin/login')
    else:
        if request.method == 'GET':
            admindeets = Admin.query.get(admin)
            inclusions = Inclusive.query.all()
            tourdeets = Tourpackage.query.get(id)
            return render_template('admin/edittourext.html',tourdeets=tourdeets, inclusions=inclusions, admindeets=admindeets, destdeets = destdeets)
        
        else:
            
            tourname = request.form.get('tourname')
            price_share = request.form.get('price_share')
            price_single = request.form.get('price_single')
            tourdesc = request.form.get('tourdesc')
            departuredate = request.form.get('departuredate')
            returndate = request.form.get('returndate')
            slots = request.form.get('slot')
            pic_object = request.files.get('tourimage')
            inclusives = request.form.getlist('inclusive')
            destname = request.form.get('destination')

            original_file =  pic_object.filename

            if original_file !='': 
                extension = os.path.splitext(original_file)
                if extension[1].lower() in ['.jpg','.png']:
                    fn = math.ceil(random.random() * 100000000)  
                    save_as = str(fn)+extension[1] 
                    pic_object.save(f"afrocentricapp/static/assets/img/tourpackages/{save_as}")

                    tourdeets.tourpackage_name = tourname
                    tourdeets.price_share = price_share
                    tourdeets.price_single = price_single
                    tourdeets.tourdesc = tourdesc
                    tourdeets.departuredate = departuredate
                    tourdeets.returndate = returndate
                    tourdeets.slots = slots
                    tourdeets.tourpackage_pics = save_as
                    tourdeets.fk_tourpackage_destination_id = destname
                    db.session.commit()

                    for i in inclusives:
                        include = pkg_inclusions.insert().values(fk_pkg_inclusive_tourpackage_id=tourdeets.tourpackage_id,fk_pkg_inclusive_id=i)
                        db.session.execute(include)
                        db.session.commit()
                        flash('Tour package successfully updated', 'success')
                else:
                    flash('File Type Not Allowed', 'warning')
                    return redirect("/admin/addtourpackage")

            elif original_file == "":

                tourdeets = Tourpackage.query.get(id)

                tourdeets.tourpackage_name = tourname
                tourdeets.tourpackage_price_sharing = price_share
                tourdeets.tourpackage_price_single = price_single
                tourdeets.tourpackage_desc = tourdesc
                tourdeets.tourpackage_dept_date = departuredate
                tourdeets.tourpackage_rtn_date = returndate
                tourdeets.tourpackage_available = slots
                tourdeets.fk_tourpackage_destination_id = destname
                db.session.commit()


                bookinfo = db.session.execute(f"SELECT COUNT(tourbooking_status) FROM tourbooking WHERE tourbooking_status='Confirmed' AND fk_tourbooking_tourpackageid = {tourdeets.tourpackage_id}")

                data = bookinfo.fetchall()
                data2 = data[0]
                data3 = data2[0]

    
                if data3 < tourdeets.tourpackage_available:
                    db.session.execute(f"UPDATE tourpackage SET tourpackage_slot = (tourpackage_available - {data3}) WHERE tourpackage_id = {tourdeets.tourpackage_id}")
                    db.session.commit()

                for i in inclusives:
                    include = pkg_inclusions.insert().values(fk_pkg_inclusive_tourpackage_id=tourdeets.tourpackage_id,fk_pkg_inclusive_id=i)
                    db.session.execute(include)
                    db.session.commit()
                    flash('Tour package successfully updated', 'success')
                return redirect ('/admin/tourpackage')    





@app.route('/admin/customers')
def admin_customers():
    admin = session.get('admin')
    if admin == None:
        return redirect('/admin/login')
    else:
        admindeets = Admin.query.get(admin)
        custdeets = Customer.query.all()
        return render_template ('admin/customerext.html', custdeets = custdeets, admindeets = admindeets)




@app.route('/admin/customrequests')
def admin_requests():
    admin = session.get('admin')
    if admin == None:
        return redirect('/admin/login')
    else:
        admindeets = Admin.query.get(admin)
        reqdeets = CustomRequest.query.all()
        return render_template ('admin/custreqext.html', reqdeets = reqdeets, admindeets = admindeets)




@app.route('/admin/customer/reviews')
def admin_reviews():
    admin = session.get('admin')
    if admin == None:
        return redirect('/admin/login')
    else:
        admindeets = Admin.query.get(admin)
        reviewdeets = Reviews.query.all()
        return render_template ('admin/revext.html', reviewdeets = reviewdeets, admindeets = admindeets)




@app.route('/admin/customer/subscribers')
def admin_sub():
    admin = session.get('admin')
    if admin == None:
        return redirect('/admin/login')
    else:
        admindeets = Admin.query.get(admin)
        subdeets = Subscribers.query.all()
        return render_template ('admin/subext.html', subdeets = subdeets, admindeets = admindeets)




@app.route('/admin/visa')
def visa():
    admin = session.get('admin')
    if admin == None:
        return redirect('/admin/login')
    else:
        admindeets = Admin.query.get(admin)
        visadeets = Visa.query.all()
        return render_template('admin/visaext.html', visadeets= visadeets, admindeets= admindeets)




@app.route('/admin/addvisa', methods=['GET','POST'])
def addvisa():
    admin = session.get('admin')
    if admin == None:
        return redirect('/admin/login')
    else:
        admindeets = Admin.query.get(admin)
        countrydeets = Country.query.all()
        if request.method =='GET':
            return render_template('admin/addvisaext.html', admindeets = admindeets, countrydeets = countrydeets)
        else:

            visaname = request.form.get('visaname')
            category = request.form.get('category')
            requirement = request.form.get('requirements')
            price = request.form.get('price')
            duration = request.form.get('duration')
            country = request.form.get('country')

            pic_object2 = request.files.get('visaimage')
            original_file =  pic_object2.filename

            if visaname == '' or category =='' or requirement =='' or price == '' or duration == '' or country == '':
                flash("Kindly fill all required field", 'warning')
                return redirect('/admin/addtourpackage')

            if original_file !='': 
                extension = os.path.splitext(original_file)
                if extension[1].lower() in ['.jpg','.png']:
                    fn = math.ceil(random.random() * 100000000)  
                    save_as = str(fn)+extension[1] 
                    pic_object2.save(f"afrocentricapp/static/assets/img/visaflyers/{save_as}")
                    
                    visa = Visa(visa_name=visaname,Visa_category=category, visa_requirement=requirement, visa_pics=save_as, visa_price=price, visa_duration=duration, fk_visa_country=country)
                    db.session.add(visa)
                    db.session.commit()            
                    return redirect("/admin/visa")
                else:
                    flash('File Not Allowed', 'warning')
                    return redirect("/admin/addvisa")

            else:
                save_as = ""
                flash('Upload a file', 'warning')
                return redirect("/admin/addvisa")




@app.route('/admin/bookings')
def admin_bookings():
    admin = session.get('admin')
    if admin == None:
        return redirect('admin/login')
    else:
        admindeets = Admin.query.get(admin)
        bookdeets = Tourbooking.query.all()
        return render_template('/admin/bookingsext.html', bookdeets = bookdeets, admindeets=admindeets)




@app.route('/admin/visaprocurement')
def admin_procurement():
    admin = session.get('admin')
    if admin == None:
        return redirect('admin/login')
    else:
        admindeets = Admin.query.get(admin)
        procuredeets = Visaprocurement.query.all()
        return render_template('/admin/procurementext.html', procuredeets = procuredeets, admindeets=admindeets)




@app.route('/admin/tourbooking/payment')
def admin_tourpayment():
    admin = session.get('admin')
    if admin == None:
        return redirect('admin/login')
    else:
        admindeets = Admin.query.get(admin)
        tourpaydeets = TourpackagePayment.query.all()
        return render_template('/admin/tourpaymentext.html', tourpaydeets = tourpaydeets, admindeets=admindeets)



@app.route('/admin/visa/payment')
def admin_visapayment():
    admin = session.get('admin')
    if admin == None:
        return redirect('admin/login')
    else:
        admindeets = Admin.query.get(admin)
        visapaydeets = VisaPayment.query.all()
        return render_template('/admin/visapaymentext.html', visapaydeets = visapaydeets, admindeets = admindeets)



@app.route('/admin/tourbooking/pending')
def booked_pending():
    admin = session.get('admin')
    if admin == None:
        return redirect('admin/login')
    else:
        admindeets = Admin.query.get(admin)
        query = db.session.execute(f"SELECT * FROM tourbooking WHERE tourbooking_status='Pending'")
        data = query.fetchall()
        return render_template('/admin/bookingsext.html', bookdeets = data, admindeets=admindeets)



@app.route('/admin/tourbooking/confirmed')
def booked_confirmed():
    admin = session.get('admin')
    if admin == None:
        return redirect('admin/login')
    else:
        admindeets = Admin.query.get(admin)
        query = db.session.execute(f"SELECT * FROM tourbooking WHERE tourbooking_status='Confirmed'")
        data = query.fetchall()
        return render_template('/admin/bookingsext.html', bookdeets = data, admindeets=admindeets)



@app.route('/admin/add/destinations', methods=['GET','POST'])
def add_destination():
    admin = session.get('admin')
    if admin == None:
        return redirect('admin/login')
    else:
        admindeets = Admin.query.get(admin)
        countrydeets = Country.query.all()
        if request.method =='GET':
            return render_template('admin/adddestination.html', admindeets = admindeets, countrydeets = countrydeets)
        else:

            destination = request.form.get('destination')
            country = request.form.get('country')
            state = request.form.get('state')

            countdeets = Country.query.filter(Country.country_id==country).first()

            con = countdeets.country_id
            

            if destination == "":
                flash('Please enter destination', 'success')
                return redirect('/admin/add/destinations')

            else:
                desdeets = Destination(destination_location = destination, fk_destination_state = state, fk_destination_country = con)
                db.session.add(desdeets)
                db.session.commit()
                flash('Destination Added Successfully', 'success')
                return redirect('/admin/destinations')  



@app.route('/admin/destinations')
def destination():
    admin = session.get('admin')
    if admin == None:
        return redirect('admin/login')
    else:
        admindeets = Admin.query.get(admin)
        destdeets = Destination.query.all()
        return render_template('admin/destination.html', admindeets = admindeets, destdeets = destdeets)

       
