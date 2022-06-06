from flask import Flask, render_template, jsonify, flash, request, redirect, abort, session
import os
import random
from werkzeug.datastructures import RequestCacheControl
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from sqlalchemy import and_, text
from sqlalchemy.orm import aliased
from datetime import datetime,timezone
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pttikpvvodylzf:95b84b2bda955cee3e116691fbf72bea7ee4d13030d71b3b7ebaacf51207e21e@ec2-3-226-163-72.compute-1.amazonaws.com:5432/d41ggppl8krk3u'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),"static","media")
app.config['MEDIA_URL'] = "/static/media"
app.secret_key = b'_5#y2L"F4Q8z\n0xom]/'
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = "primary"
login_manager.init_app(app)

ALLOWED_IMG_EXT = ["PNG","JPEG","JPG","WEBP","GIF"]

def allowed_extensions(filename,ext=None):
    if ext==None:
        return '.' in filename and filename.rsplit(".",1)[1].upper() in ALLOWED_IMG_EXT
    else:
        ALLOWED_EXT = [ e.upper() for e in ext]
        return '.' in filename and filename.rsplit(".",1)[1].upper() in ALLOWED_EXT

@app.template_filter('datetime')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime('%d %b %Y')
    
# --------------------------------------------------
# Error Pages 
# --------------------------------------------------
@app.errorhandler(403)
def error_403(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(405)
def error_405(e):
    return render_template('errors/405.html'), 405

@app.errorhandler(500)
def error_500(e):
    return render_template('errors/500.html'), 500

@app.errorhandler(503)
def error_503(e):
    return render_template('errors/503.html'), 503

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --------------------------------------------------
# Coming Soon Routes
# --------------------------------------------------

@app.route('/comingsoon')
def coming_soon():
    return render_template("coming-soon.html")

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --------------------------------------------------
# Auth Routes
# --------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))

@app.route("/auth/login", methods=['GET','POST'])
def login():

    if request.method=='GET':
        if current_user.is_authenticated:
            return redirect('/')
        return render_template("auth/login.html")

    email = request.form.get('email')
    password = request.form.get('password')
    user = Users.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash(u'Please check your login details and try again.','warning')
        return redirect('/auth/login')
    if not user.verified:
        flash(u'Account is not verified. Please ask the admin to verify your account.','warning')
        return redirect('/auth/login')
    login_user(user, remember=False)
    flash(u'You were successfully logged in','success')
    return redirect('/')

@app.route("/auth/register", methods=['GET','POST'])
def signup():
    if request.method=="GET":
        return render_template('auth/register.html')

    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    role = 'client'
    firstname = request.form.get('firstname','')
    lastname = request.form.get('lastname','')
    if password!=confirm_password:
        flash(u'Password - Confirm Password Mismatch','danger')
        return redirect('/auth/login')
    user = Users.query.filter_by(email=email).first()
    if user:
        flash(u'Email already registered. Try again with different email address.','danger')
        return redirect('/auth/login')
    user = Users(fname=firstname.capitalize(),lname=lastname.capitalize(),email=email,password=generate_password_hash(password),role=role)
    db.session.add(user)
    db.session.commit()
    flash(u'Credentials created successfully! Please ask the admin to verify your account.','success')
    return redirect('/auth/login')

@app.route("/auth/logout")
@login_required
def logout():
    logout_user()
    flash(u'You were successfully logged out','info')
    return redirect('/auth/login')

@app.route('/auth/forgot-password')
def forgot_password():
    return render_template("auth/forgot-password.html")

@app.route("/reset_password",methods =['GET','POST'])
def reset_request(token):
    return render_template('auth/reset_password.html')
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    # form = RequestResetForm()
    # return render_template('auth-reset-password.html',title = 'Reset Password',form=form)

@app.route("/reset_password/<string:token>",methods =['GET','POST'])
def reset_token(token):

    abort(404)
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # user = user.verify

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --------------------------------------------------
# Index Homepage
# --------------------------------------------------
@app.route("/", methods=['GET'])
@login_required
def index():
    return render_template("index.html")
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --------------------------------------------------
# Ticket Management
# --------------------------------------------------
@app.route("/tickets",methods=["GET"])
@login_required
def tickets():
    users = Users.query.order_by(Users.fname,Users.lname).all()
    return render_template('tickets/list-all-tickets-page.html',users=users)

@app.route("/create/order-ticket",methods=['GET','POST'])
@login_required
def book_order():
    if request.method=="POST":
        pass
    return render_template("tickets/create-new-order-ticket.html")

@app.route("/create/maintenance-ticket",methods=['POST','GET'])
@login_required
def create_maintenance_ticket():

    if request.method=='POST':
        description = request.form.get('description','')
        short_description = request.form.get('short_description')
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        item_id = request.form.get('item_id')
        images=request.files.getlist('images[]')
        if item_id==None:
            flash(u'Error, please select correct Item Id.','danger')
            return redirect('/create/maintenance-ticket')
        else:
            if type(item_id)!=int:
                item_id=int(item_id)

            if item_id<=0:
                flash(u'Error, please select correct Item Id.','danger')
                return redirect('/create/maintenance-ticket')
            else:
                try:
                    item = Inventory.query.get(item_id)
                    if not item:
                        flash(u'Error, please select correct Item Id.','danger')
                        return redirect('/create/maintenance-ticket')
                    if item.status==2:
                        flash(u'Error, selected Item Id is already under maintenance.','danger')
                        return redirect('/create/maintenance-ticket')
                    elif item.status==0:
                        itemIssued = ItemIssued.query.filter(and_(ItemIssued.item_id==item_id,ItemIssued.returned==False)).first()
                        if not itemIssued:
                            flash(u'Server Error, contact the admin.')
                            return redirect('/create/maintenance-ticket')
                        itemIssued.returned = True
                        itemIssued.received_by=current_user.id
                        itemIssued.returned_on = datetime.now()
                    item.status=2
                    ticket = Ticket(title=title,item_id=item_id,due_date=due_date,short_description=short_description,description=description,created_by=current_user.id,status_updated_by=current_user.id)
                    db.session.add(ticket)
                    db.session.commit()
                    for image in images:
                        if image and allowed_extensions(image.filename):
                            name,ext = secure_filename(image.filename).split(".")
                            gname = f"{name}-{uuid.uuid4()}.{ext}"
                            ufilename = os.path.join(app.config["UPLOAD_FOLDER"],"images",gname)
                            image.save(ufilename)
                            filenameUrl = app.config['MEDIA_URL']+"/images/"+gname
                            img = Images(image=filenameUrl,filename=secure_filename(image.filename),external_id=ticket.id,image_of='ticket')
                            db.session.add(img)
                    db.session.commit()
                    flash(f'Success, created maintenance ticket for Item #{item_id} successfully.','success')
                except Exception as e:
                    db.session.rollback()
                    flash(u'Error:: '+str(e),'danger')

    products = db.session.query(Product.id,Product.name).order_by(Product.name).all()
    users = db.session.query(Users).order_by(Users.fname,Users.lname).all()
    return render_template('tickets/create-new-maintenance-ticket.html',products=products,users=users)

@app.route("/items/<int:id>",methods=["GET"])
@login_required
def items(id=None):
    if id==None:
        return jsonify({'data':[]})
    itemList = []
    items = db.session.query(Inventory.id).filter(Inventory.product_id==int(id)).order_by(Inventory.id).all()
    for item in items:
        itemList.append(item[0])
    return jsonify({'data':itemList})

@app.route('/tickets/maintenance/<int:id>',methods=["GET","POST"])
@login_required
def maintenance_ticket(id=None):
    if id==None:
        abort(404)

    if request.method=="POST":
        comment = request.form.get('comment')
        if comment==None or comment=='':
            flash(u'Please enter your reply before posting','warning')
        else:
            try:
                reply = Replies(comment=comment,posted_by=current_user.id,ticket_id=int(id))
                db.session.add(reply)
                db.session.commit()
                flash(u'Your comment posted successfully!','success')
            except Exception as e:
                db.session.rollback()
                print(str(e))
                flash(u'Server Error, occuered try again later.','danger')

    created_by = aliased(Users)
    status_updated_by = aliased(Users)
    closed_by = aliased(Users)

    ticket = db.session.query(Ticket,created_by,status_updated_by,closed_by).filter(Ticket.id==int(id)).join(created_by, created_by.id==Ticket.created_by,isouter=True).join(status_updated_by,status_updated_by.id==Ticket.status_updated_by,isouter=True).join(closed_by,closed_by.id==Ticket.closed_by,isouter=True).first()
    if ticket==None:
        abort(404)
    images = Images.query.filter(and_(Images.image_of=="ticket",Images.external_id==int(id))).order_by(Images.id).all()

    replies = db.session.query(Replies,Users).filter(Replies.ticket_id==int(id)).join(Users,Users.id==Replies.posted_by,isouter=True).order_by(Replies.posted_on).all()

    return render_template('tickets/view-maintenance-ticket-details.html',images=images,maintenance=ticket,replies=replies)

@app.route('/tickets/maintenance/item/<int:id>',methods=['GET','POST'])
@login_required
def item_maintenance(id=None):
    if id==None:
        abort(404)

    created_by = aliased(Users)
    status_updated_by = aliased(Users)
    closed_by = aliased(Users)

    ticket = db.session.query(Ticket,created_by,status_updated_by,closed_by).filter(and_(Ticket.item_id==int(id),Ticket.isclosed==False)).join(created_by, created_by.id==Ticket.created_by,isouter=True).join(status_updated_by,status_updated_by.id==Ticket.status_updated_by,isouter=True).join(closed_by,closed_by.id==Ticket.closed_by,isouter=True).first()
    if ticket==None:
        abort(404)
    
    if request.method=="POST":
        comment = request.form.get('comment')
        if comment==None or comment=='':
            flash(u'Please enter your reply before posting','warning')
        else:
            try:
                reply = Replies(comment=comment,posted_by=current_user.id,ticket_id=ticket[0].id)
                db.session.add(reply)
                db.session.commit()
                flash(u'Your comment posted successfully!','success')
            except Exception as e:
                db.session.rollback()
                print(str(e))
                flash(u'Server Error, occuered try again later.','danger')
    
    images = Images.query.filter(and_(Images.image_of=="ticket",Images.external_id==ticket[0].id)).order_by(Images.id).all()
    replies = db.session.query(Replies,Users).filter(Replies.ticket_id==ticket[0].id).join(Users,Users.id==Replies.posted_by,isouter=True).order_by(Replies.posted_on).all()

    return render_template('tickets/view-maintenance-ticket-details.html',images=images,maintenance=ticket,replies=replies)

@app.route('/update-ticket-status/maintenance/<int:id>',methods=["POST"])
@login_required
def update_maintenance_ticket_status(id=None):
    if id==None:
        print('#326')
        return jsonify({'flag': False})
    
    status = request.form.get('status')
    if status==None or status=='':
        print('#331')
        return jsonify({'flag':False})

    ticket = Ticket.query.get(int(id))
    if not ticket:
        print('#336')
        return jsonify({'flag': False})
    try:
        ticket.status_updated_by = current_user.id
        ticket.status = status
        ticket.status_updated_on = datetime.now()
        db.session.commit()
    except:
        db.session.rollback()
        print('#345')
        return jsonify({'flag': False})

    return jsonify({'flag':True})

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --------------------------------------------------
# User Management
# --------------------------------------------------

@app.route("/user/create",methods=['GET','POST'])
@login_required
def create_user():
    if request.method=="GET":
        return render_template('users/create-a-user.html')
    
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    role = request.form.get('role','client')
    firstname = request.form.get('firstname','')
    lastname = request.form.get('lastname','')
    if password!=confirm_password:
        flash(u'Password - Confirm Password Mismatch','danger')
        return redirect('/user/create')
    user = Users.query.filter_by(email=email).first()
    if user:
        flash(u'Email already registered. Try again with different email address.','danger')
        return redirect('/user/create')
    user = Users(fname=firstname.capitalize(),lname=lastname.capitalize(),email=email,password=generate_password_hash(password),role=role,verified=True)
    db.session.add(user)
    db.session.commit()
    flash(u'Credentials created successfully!','success')
    return redirect('/user/create')

@app.route("/users", methods=['GET'])
@login_required
def users():
    return render_template("users/list-all-users-page.html")

@app.route('/user/<int:id>',methods=["GET"])
@login_required
def user(id=None):
    if id==None:
        abort(404)
    
    user = Users.query.get(int(id))
    if not user:
        abort(404)
    
    return render_template('users/user-details.html',user=user)

@app.route("/profile/edit", methods=["POST"])
@login_required
def edit_profile():
    try:
        fname = request.form.get('fname')
        lname = request.form.get('lname','')
        phone = request.form.get('phone',None)
        password = request.form.get('password','')
        confirm_password = request.form.get('confirm_password','')
        change_password= 'change_password' in request.form
        
        flag = False

        if fname=="" or fname==None:
            flash('Firstname is Required.','danger')
            flag=True

        if lname=="":
            lname=None
        
        if phone!="" and phone!=None and len(phone)!=11:
            flash(u'Enter valid 10 digit phone number with 0 at beginning.','danger')
            flag=True

        if change_password==True:
            if password!="" and password!=None and password!=confirm_password:
                flash(u'Password and confirm password mis-match.','danger')
                flag=True
            elif password=="" or password==None:
                flash(u'Enter valid password with minimum 6 characters.')
                flag=True
            elif flag==False:
                flash(u'Your account password updated successfully.','success')
                current_user.password = generate_password_hash(password)
        
        if flag:
            return redirect('/user/profile')

        current_user.fname = fname.capitalize()
        current_user.lname = '' if lname==None else lname.capitalize()
        current_user.phone = phone
        db.session.commit()
        flash(u'Profile saved successfully.','success')
        return redirect('/user/profile')
    except Exception as e:
        db.session.rollback()
        flash(u'Failed to save profile, try again later.'+str(e),'danger')
        return redirect('/user/profile')

@app.route("/user/profile",methods=['GET'])
def profile():
    return render_template("users/profile-page.html")

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --------------------------------------------------
# Activity Management
# --------------------------------------------------

@app.route("/user/activities",methods=['GET'])
def activities():
    return render_template("coming-soon.html")

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --------------------------------------------------
# Products Management
# --------------------------------------------------

@app.route('/product/category',methods=["POST","GET"])
@login_required
def category_page():
    if request.method=="GET": # SHOW CATEGORIES
        return render_template('products/product-category.html')
    elif request.method=="POST":  # CREATE CATEGORY
        category = request.form.get('category','')
        if category=='':
            flash(u'Enter a product category is required.','warning')
        else:
            category = category.capitalize()
            product_category = ProductCategory.query.filter_by(category=category).first()
            if not product_category:
                product_category = ProductCategory(category=category)
                db.session.add(product_category)
                db.session.commit()
                flash(u'A new product category added successfully.','success')
            else:
                flash(u'Product category '+category+', already exists.','danger')
        return redirect('/product/category')

@app.route('/product/category/<int:id>',methods=["POST","DELETE"])
@login_required
def product_category(id=None):
    if request.method=="POST":  # UPDATE CATEGORY
        if id==None:
            abort(404)
        else:
            category = request.form.get('category','')
        if category=='':
            flash(u'Enter a product category is required.','warning')
            # return redirect('/product/category')
        else:
            category = category.capitalize()
            product_category = ProductCategory.query.get(id)
            if product_category:
                product_category.category=category
                db.session.commit()
                flash(u'Product category updated successfully.','success')
                # return redicted('/product/category')
            else:
                abort(500)
    elif request.method=="DELETE":  # DELETE CATEGORY
        if id==None:
            abort(404)
        else:
            product_category = ProductCategory.query.get(id)
            if product_category:
                db.session.delete(product_category)
                db.session.commit()
                productCategoryList = []
                categories = ProductCategory.query.order_by(ProductCategory.id).all()
                for idx,category in enumerate(categories):
                    productCategoryList.append([
                        idx+1,
                        category.category.capitalize(),
                        f"<span><button data-toggle='tooltip' data-placement='bottom' title='Edit' onclick='editCategory({category.id},\"{category.category}\")' class='btn btn-icon btn-primary btn-sm'><i class='far fa-edit'></i></button>&nbsp;<button onclick='deleteCategory({category.id})' class='btn btn-icon btn-danger btn-sm' data-toggle='tooltip' data-placement='bottom' title='Trash'><i class='la la-trash'></i></button></span>"
                    ])            
                return jsonify({'status':True,'data':productCategoryList})
            else:
                return jsonify({'status':False})

    return redirect('/product/category')

@app.route('/product/create',methods=["POST","GET"])
@login_required
def create_product():
    if request.method=="POST":
        name=request.form.get('name')
        description=request.form.get('description','')
        vendor_name=request.form.get('vendor_name','')
        vendor_email=request.form.get('vendor_email','')
        vendor_phone=request.form.get('vendor_phone','')
        short_description=request.form.get('short_description','')
        posted_by=request.form.get('user')
        category=request.form.get('category')
        images=request.files.getlist('images[]')
        critical_limit = request.form.get('critical_limit',1)
        
        if type(critical_limit)!=int:
            critical_limit=int(critical_limit)

        if critical_limit<1:
            critical_limit=1

        if category:
            category=int(category)
        else:
            flash(u'Select a valid product category.','danger')
            return redirect('/product/create')
        try:
            product = Product(name=name,vendor_name=vendor_name,vendor_phone=vendor_phone,vendor_email=vendor_email,description=description,category=category,posted_by=posted_by,short_description=short_description,critical_limit=critical_limit)
            db.session.add(product)
            db.session.commit()
            for image in images:
                if image and allowed_extensions(image.filename):
                    name,ext = secure_filename(image.filename).split(".")
                    gname = f"{name}-{uuid.uuid4()}.{ext}"
                    ufilename = os.path.join(app.config["UPLOAD_FOLDER"],"product_images",gname)
                    image.save(ufilename)
                    filenameUrl = app.config['MEDIA_URL']+"/product_images/"+gname
                    img = ProductImages(image=filenameUrl,filename=secure_filename(image.filename),product=product)
                    db.session.add(img)
            db.session.commit()
            flash(u'Product details successfully registered.','success')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            flash(u"Server Error! "+str(e),'warning')
    categories = ProductCategory.query.order_by(ProductCategory.id).all()
    return render_template('products/create-new-product.html',categories=categories)

@app.route('/products',methods=["GET"])
@login_required
def products():
    return render_template("products/list-all-products-page.html")

@app.route('/product/<int:id>',methods=["GET"])
@login_required
def product_details(id=None):
    if id==None:
        abort(404)
    
    product = db.session.query(Product, ProductCategory).filter(Product.id==int(id)).join(ProductCategory,Product.category==ProductCategory.id).first()
    if not product:
        abort(404)
    
    images = db.session.query(ProductImages).filter(and_(ProductImages.product_id==int(id),ProductImages.show==True)).all()

    items = db.session.query(Inventory,ItemIssued,Users).filter(Inventory.product_id==int(id)).join(ItemIssued, and_(Inventory.id==ItemIssued.item_id,ItemIssued.returned==False),isouter=True).join(Users,Users.id==ItemIssued.issued_to,isouter=True).order_by(Inventory.id).all()

    users = db.session.query(Users.id,Users.fname+' '+Users.lname).order_by(Users.id).all()

    return render_template('products/details-page.html',product=product,items=items,images=images,users=users)

@app.route('/allocate/item',methods=['POST'])
@login_required
def allocate_item():
    item=None
    item_id = request.form.get('item_id', None)
    location = request.form.get('location')
    assigned_to = request.form.get('assigned_to')
    remarks = request.form.get('remarks',None)
    expected_return = request.form.get('expected_date')
    approved_by = current_user.id
    if item_id==None:
        return jsonify({
            'error':True,
            'type':'error',
            'message': 'Error, please try again.'
        })
    else:
        if type(item_id)!=int:
            item_id=int(item_id)

        item = Inventory.query.get(item_id)
        if item==None:
            return jsonify({
                'error':True,
                'type':'error',
                'message': 'Error, please try again.'
            })
        if item.status==0:
            return jsonify({
                'error': True,
                'type':'error',
                'message': 'The selected item is already allocated to someone.'
            })        
        elif item.status==2:
            return jsonify({
                'error': True,
                'type':'error',
                'message': 'The selected item is currently under maintenance, please check later.'
            })        

        if assigned_to==None or int(assigned_to)<=0:
            return jsonify({
                'error': True,
                'type':'warning',
                'message': 'Selecting one assignee is required!'
            })

        if location==None or location=='':
            return jsonify({
                'error': True,
                'type':'warning',
                'message': 'Enter valid location where this item will be used.'
            })
            
        if expected_return==None or expected_return=='':
            return jsonify({
                'error': True,
                'type':'warning',
                'message': 'Select valid expected date of return.'
            })

        try:
            # print("BEFORE ITEM_ISSUED")
            if remarks=='':
                remarks=None
            item_issued = ItemIssued(item_id=item.id,location=location,issued_to=int(assigned_to),approved_by=approved_by,expected_return=datetime.strptime(expected_return,'%Y-%m-%d'),remarks=remarks)
            db.session.add(item_issued)
            # print("AFTER ITEM_ISSUED")
            item.status=0
            db.session.commit()
            # print("AFTER COMMIT")
            ItemList = []
            items = db.session.query(Inventory,ItemIssued,Users).filter(Inventory.product_id==item.product_id).join(ItemIssued, and_(Inventory.id==ItemIssued.item_id,ItemIssued.returned==False),isouter=True).join(Users,Users.id==ItemIssued.issued_to,isouter=True).order_by(Inventory.id).all()
            for idx,item in enumerate(items):
                status = ''
                action = ''
                if item[0].status==0:
                    status = '<span class="badge badge-warning">In-Use</span>'
                    action = f'<span class="btn btn-info" onclick="transfer(\'{item[0].id}\',\'{item[2].fname} {item[2].lname}\',\'{item[1].issued_to}\',\'{item[1].location}\');">Transfer</span>&nbsp;<span class="btn btn-dark" onclick="markAsReturned(\'{item[0].id}\')">Returned</span>'
                elif item[0].status==2:
                    status = '<span class="badge badge-danger">Under Maintenance</span>'
                    action = f'<span class="btn btn-light" onclick="markAsRepaired(\'{item[0].id}\')">Mark as Repaired</span>&nbsp;<a class="btn btn-secondary" target="_blank" href="{url_for("item_maintenance",id=item[0].id)}">Details</a>'
                else:
                    status = '<span class="badge badge-success">Available</span>'
                    action = f'<span class="btn btn-primary" onclick="allocate(\'{item[0].id}\')">Allocate</span>'
                ItemList.append([
                    idx+1,
                    '#'+str(item[0].id),
                    '' if item[1]==None or item[1].location==None else item[1].location,
                    '' if item[1]==None or item[1].issued_to==None else f'<a target="_blank" href="/user/{item[2].id}"><figure class="avatar mr-2 avatar-sm"><img alt="image" src="/static/img/avatar/avatar-{random.randint(1, 5)}.png" class="rounded-circle" data-toggle="tooltip" title="{item[2].fname} {item[2].lname}"></figure></a>',
                    '' if item[1]==None or item[1].expected_return==None else item[1].expected_return.strftime('%d %b %Y'),
                    status,
                    action
                ])

            return jsonify({
                'error':False,
                'message':f'Wooh! Item #{item_id} allocated successfully.',
                'data': ItemList
                })
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return jsonify({
                'error': True,
                'type':'error',
                'message': ' Server error occured, try again later.'+str(e)
            })

@app.route('/transfer/item',methods=['POST'])
@login_required
def transfer_item():
    item=None
    item_id = request.form.get('item_id', None)
    location = request.form.get('location')
    assigned_to = request.form.get('assigned_to')
    remarks = request.form.get('remarks',None)
    expected_return = request.form.get('expected_date')
    approved_by = current_user.id
    if item_id==None:
        return jsonify({
            'error':True,
            'type':'error',
            'message': 'Error, please try again.'
        })
    else:
        if type(item_id)!=int:
            item_id=int(item_id)

        item = Inventory.query.get(item_id)
        if item==None:
            return jsonify({
                'error':True,
                'type':'error',
                'message': 'Error, please try again.'
            })
        if item.status==1:
            return jsonify({
                'error': True,
                'type':'warning',
                'message': 'The selected item is already available for allocation, no need to transfer.'
            })        
        elif item.status==2:
            return jsonify({
                'error': True,
                'type':'error',
                'message': 'The selected item is currently under maintenance, please check later.'
            })        

        if assigned_to==None or int(assigned_to)<=0:
            return jsonify({
                'error': True,
                'type':'warning',
                'message': 'Selecting one assignee is required!'
            })

        if location==None or location=='':
            return jsonify({
                'error': True,
                'type':'warning',
                'message': 'Enter valid location where this item will be used.'
            })
            
        if expected_return==None or expected_return=='':
            return jsonify({
                'error': True,
                'type':'warning',
                'message': 'Select valid expected date of return.'
            })

        try:
            if remarks=='':
                remarks=None
            prev_issued = ItemIssued.query.filter(and_(ItemIssued.item_id==item.id,ItemIssued.returned==False)).first()
            if not prev_issued:
                return jsonify({
                    'error':True,
                    'type': 'warning',
                    'message': 'The selected item is already available for allocation, no need to transfer.'
                })
            prev_issued.returned=True
            prev_issued.transfered=True
            prev_issued.returned_on=datetime.now()
            prev_issued.received_by=int(assigned_to)
            item_issued = ItemIssued(item_id=item.id,location=location,issued_to=int(assigned_to),approved_by=approved_by,expected_return=datetime.strptime(expected_return,'%Y-%m-%d'),remarks=remarks)
            db.session.add(item_issued)
            db.session.commit()
            ItemList = []
            items = db.session.query(Inventory,ItemIssued,Users).filter(Inventory.product_id==item.product_id).join(ItemIssued, and_(Inventory.id==ItemIssued.item_id,ItemIssued.returned==False),isouter=True).join(Users,Users.id==ItemIssued.issued_to,isouter=True).order_by(Inventory.id).all()
            for idx,item in enumerate(items):
                status = ''
                action = ''
                if item[0].status==0:
                    status = '<span class="badge badge-warning">In-Use</span>'
                    action = f'<span class="btn btn-info" onclick="transfer(\'{item[0].id}\',\'{item[2].fname} {item[2].lname}\',\'{item[1].issued_to}\',\'{item[1].location}\');">Transfer</span>&nbsp;<span class="btn btn-dark" onclick="markAsReturned(\'{item[0].id}\')">Returned</span>'
                elif item[0].status==2:
                    status = '<span class="badge badge-danger">Under Maintenance</span>'
                    action = f'<span class="btn btn-light" onclick="markAsRepaired(\'{item[0].id}\')">Mark as Repaired</span>&nbsp;<a class="btn btn-secondary" target="_blank" href="{url_for("item_maintenance",id=item[0].id)}">Details</a>'
                else:
                    status = '<span class="badge badge-success">Available</span>'
                    action = f'<span class="btn btn-primary" onclick="allocate(\'{item[0].id}\')">Allocate</span>'
                ItemList.append([
                    idx+1,
                    '#'+str(item[0].id),
                    '' if item[1]==None or item[1].location==None else item[1].location,
                    '' if item[1]==None or item[1].issued_to==None else f'<a target="_blank" href="/user/{item[2].id}"><figure class="avatar mr-2 avatar-sm"><img alt="image" src="/static/img/avatar/avatar-{random.randint(1, 5)}.png" class="rounded-circle" data-toggle="tooltip" title="{item[2].fname} {item[2].lname}"></figure><a>',
                    '' if item[1]==None or item[1].expected_return==None else item[1].expected_return.strftime('%d %b %Y'),
                    status,
                    action
                ])

            return jsonify({
                'error':False,
                'message':f'Wooh! Item #{item_id} transfered successfully.',
                'data': ItemList
                })
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return jsonify({
                'error': True,
                'type':'error',
                'message': ' Server error occured, try again later.'+str(e)
            })


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --------------------------------------------------
# APIs
# --------------------------------------------------
@app.route("/verify-user/<int:id>",methods=['POST'])
@login_required
def verify_user(id):
    user =  Users.query.get(id)
    if not user:
        return jsonify({'flag':False})
    user.verified = True
    db.session.commit()
    return jsonify({'flag':True})

@app.route("/fetch-all-product-category",methods=["POST"])
def fetech_all_product_category():
    productCategoryList = []
    categories = ProductCategory.query.order_by(ProductCategory.id).all()
    for idx,category in enumerate(categories):
        productCategoryList.append([
            idx+1,
            category.category.capitalize(),
            f"<span><button data-toggle='tooltip' data-placement='bottom' title='Edit' onclick='editCategory({category.id},\"{category.category}\")' class='btn btn-icon btn-primary btn-sm btn-tooltip'><i class='far fa-edit'></i></button>&nbsp;<button onclick='deleteCategory({category.id})' class='btn btn-icon btn-danger btn-sm btn-tooltip' data-toggle='tooltip' data-placement='bottom' title='Trash'><i class='la la-trash'></i></button></span>"
        ])
    return jsonify({'data':productCategoryList})

@app.route("/fetch-all-products",methods=["POST"])
def fetech_all_products():
    productList = []
    # products = db.session.query(Product, ProductCategory).join(calc_counts,and_(Product.category==ProductCategory.id,calc_counts.c.product_id==Product.id)).all()
    
    raw_query = text("""
        select product.id as product_id,product.name as product_name,product_category.category as product_category,product.critical_limit as critical_limit,x.i as inuse,x.a as available,x.m as maintenance from product left join product_category on product.category=product_category.id 
            left join (
        select product_id, SUM(CASE status WHEN 0 THEN cnt ELSE 0 END) AS i
            , SUM(CASE status WHEN 1 THEN cnt ELSE 0 END) AS a
            , SUM(CASE status WHEN 2 THEN cnt ELSE 0 END) AS m
            from (select product_id,status,count(id) as cnt from inventory group by status,product_id) grp group by product_id order by product_id
        ) x on x.product_id=product.id;
    """)

    results = db.engine.execute(raw_query)

    for idx,result in enumerate(results):
        a = int(result[5]) if result[5]!=None else 0,  # Available
        i = int(result[4]) if result[4]!=None else 0,   # In Use
        u = int(result[6]) if result[6]!=None else 0,   # Under Maintainance 
        limit = int(result[3]) if result[3]!=None else 0,  # Critical Limit
        label = ''
        if a[0] <= 0:
            label = '<span class="badge badge-danger">Out of Stock</span>' 
        elif a[0]<limit[0]:
            label = f'<span class="badge badge-warning" data-toggle="tooltip" title="Critical Limit: {limit[0]}">Critical</span>'
        else:
            label = '<span class="badge badge-success">Available</span>'
        productList.append([
            result[0], # product_id
            idx+1,
            result[1], # product_name
            result[2].capitalize(), # product_category
            a[0],  # Available
            i[0],  # In Use
            u[0],  # Under Maintenance
            a[0]+i[0]+u[0],  # Total
            label  # Label
        ])

    return jsonify({'data':productList})

@app.route('/create-items/<int:id>',methods=["POST"])
@login_required
def create_new_items(id=None):
    if id==None:
        return jsonify({'flag':False,'error': 'Invalid request, try again later!'})
    else:
        qty=request.form['qty']
        qty = int(qty)
        if qty==None or qty<1:
            return jsonify({'flag': False,'error': 'Invalid quantity, enter a valid integer number greater than 0.'})
        try:
            for _ in range(qty):
                item = Inventory(product_id=int(id),status=1)
                db.session.add(item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'flag': False,'error':'Error encountered, try again later!'})
        ItemList = []
        items = db.session.query(Inventory,ItemIssued,Users).filter(Inventory.product_id==int(id)).join(ItemIssued, and_(Inventory.id==ItemIssued.item_id,ItemIssued.returned==False),isouter=True).join(Users,Users.id==ItemIssued.issued_to,isouter=True).order_by(Inventory.id).all()
        for idx,item in enumerate(items):
            status = ''
            action = ''
            if item[0].status==0:
                status = '<span class="badge badge-warning">In-Use</span>'
                action = f'<span class="btn btn-info" onclick="transfer(\'{item[0].id}\',\'{item[2].fname} {item[2].lname}\',\'{item[1].issued_to}\',\'{item[1].location}\');">Transfer</span>&nbsp;<span class="btn btn-dark" onclick="markAsReturned(\'{item[0].id}\')">Returned</span>'
            elif item[0].status==2:
                status = '<span class="badge badge-danger">Under Maintenance</span>'
                action = f'<span class="btn btn-light" onclick="markAsRepaired(\'{item[0].id}\')">Mark as Repaired</span>&nbsp;<a class="btn btn-secondary" target="_blank" href="{url_for("item_maintenance",id=item[0].id)}">Details</a>'
            else:
                status = '<span class="badge badge-success">Available</span>'
                action = f'<span class="btn btn-primary" onclick="allocate(\'{item[0].id}\')">Allocate</span>'
            ItemList.append([
                idx+1,
                '#'+str(item[0].id),
                '' if item[1]==None or item[1].location==None else item[1].location,
                '' if item[1]==None or item[1].issued_to==None else f'<a target="_blank" href="/user/{item[2].id}"><figure class="avatar mr-2 avatar-sm"><img alt="image" src="/static/img/avatar/avatar-{random.randint(1, 5)}.png" class="rounded-circle" data-toggle="tooltip" title="{item[2].fname} {item[2].lname}"></figure></a>',
                '' if item[1]==None or item[1].expected_return==None else item[1].expected_return.strftime('%d %b %Y'),
                status,
                action
            ])
        
        return jsonify({'flag':True, 'data': ItemList})

@app.route("/fetch-all-users", methods=['POST'])
def fetech_all_users():
    usersList = []
    users = Users.query.order_by(Users.id).all()
    for idx, user in enumerate(users):
        name = "" if user.fname == None and user.lname == None else user.fname.capitalize() +" "+ user.lname.capitalize()
        usersList.append([
            user.id,
            idx+1,
            name,
            user.role.capitalize(),
            user.email,
            '<span class="badge badge-success">Verified</span>' if user.verified else f'<span style="cursor: pointer;" class="badge badge-primary" id="user{user.id}" onclick="verifyUser({user.id},\'{name}\');">Verify</span>',
        ])

    return jsonify({'data':usersList})

@app.route('/mark-as-repaired/<int:id>',methods=['POST'])
@login_required
def mark_as_repaired(id=None):

    if id==None or id=='':
        return jsonify({
            'flag': False
        })
    
    item = Inventory.query.get(int(id))
    if not item:
        return jsonify({
            'flag': False
        })
    else:
        try:
            if item.status==2:
                ticket = Ticket.query.filter(and_(Ticket.item_id==item.id,Ticket.isopened==False)).first()
                ticket.isclosed = True
                ticket.status = 'Item Repaired'
                ticket.status_updated_by = current_user.id
                ticket.status_updated_on = datetime.now()
                ticket.closed_on = datetime.now()
                ticket.closed_by = current_user.id
                item.status = 1
                db.session.commit() 
                ItemList = []
                items = db.session.query(Inventory,ItemIssued,Users).filter(Inventory.product_id==item.product_id).join(ItemIssued, and_(Inventory.id==ItemIssued.item_id,ItemIssued.returned==False),isouter=True).join(Users,Users.id==ItemIssued.issued_to,isouter=True).order_by(Inventory.id).all()
                for idx,item in enumerate(items):
                    status = ''
                    action = ''
                    if item[0].status==0:
                        status = '<span class="badge badge-warning">In-Use</span>'
                        action = f'<span class="btn btn-info" onclick="transfer(\'{item[0].id}\',\'{item[2].fname} {item[2].lname}\',\'{item[1].issued_to}\',\'{item[1].location}\');">Transfer</span>&nbsp;<span class="btn btn-dark" onclick="markAsReturned(\'{item[0].id}\')">Returned</span>'
                    elif item[0].status==2:
                        status = '<span class="badge badge-danger">Under Maintenance</span>'
                        action = f'<span class="btn btn-light" onclick="markAsRepaired(\'{item[0].id}\')">Mark as Repaired</span>&nbsp;<a class="btn btn-secondary" target="_blank" href="{url_for("item_maintenance",id=item[0].id)}">Details</a>'
                    else:
                        status = '<span class="badge badge-success">Available</span>'
                        action = f'<span class="btn btn-primary" onclick="allocate(\'{item[0].id}\')">Allocate</span>'
                    ItemList.append([
                        idx+1,
                        '#'+str(item[0].id),
                        '' if item[1]==None or item[1].location==None else item[1].location,
                        '' if item[1]==None or item[1].issued_to==None else f'<a target="_blank" href="/user/{item[2].id}"><figure class="avatar mr-2 avatar-sm"><img alt="image" src="/static/img/avatar/avatar-{random.randint(1, 5)}.png" class="rounded-circle" data-toggle="tooltip" title="{item[2].fname} {item[2].lname}"></figure></a>',
                        '' if item[1]==None or item[1].expected_return==None else item[1].expected_return.strftime('%d %b %Y'),
                        status,
                        action
                    ])  
                return jsonify({'flag':True, 'data': ItemList})
                
            else:
                return jsonify({
                    'flag': False
                })    
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return jsonify({
                'flag': False
            })

@app.route('/mark-as-returned/<int:id>',methods=['POST'])
@login_required
def mark_as_returned(id=None):

    if id==None or id=='':
        return jsonify({
            'flag': False
        })
    
    item = Inventory.query.get(int(id))
    if not item:
        return jsonify({
            'flag': False
        })
    else:
        try:
            if item.status==0:
                item_issued = ItemIssued.query.filter(and_(ItemIssued.item_id==int(id),ItemIssued.returned==False)).first()
                if not item_issued:
                    return jsonify({
                        'flag': True
                    })
                item_issued.received_by = current_user.id
                item_issued.returned_on = datetime.now()
                item_issued.returned = True
                item.status = 1
                db.session.commit()
                ItemList = []
                items = db.session.query(Inventory,ItemIssued,Users).filter(Inventory.product_id==item.product_id).join(ItemIssued, and_(Inventory.id==ItemIssued.item_id,ItemIssued.returned==False),isouter=True).join(Users,Users.id==ItemIssued.issued_to,isouter=True).order_by(Inventory.id).all()
                for idx,item in enumerate(items):
                    status = ''
                    action = ''
                    if item[0].status==0:
                        status = '<span class="badge badge-warning">In-Use</span>'
                        action = f'<span class="btn btn-info" onclick="transfer(\'{item[0].id}\',\'{item[2].fname} {item[2].lname}\',\'{item[1].issued_to}\',\'{item[1].location}\');">Transfer</span>&nbsp;<span class="btn btn-dark" onclick="markAsReturned(\'{item[0].id}\')">Returned</span>'
                    elif item[0].status==2:
                        status = '<span class="badge badge-danger">Under Maintenance</span>'
                        action = f'<span class="btn btn-light" onclick="markAsRepaired(\'{item[0].id}\')">Mark as Repaired</span>&nbsp;<a class="btn btn-secondary" target="_blank" href="{url_for("item_maintenance",id=item[0].id)}">Details</a>'
                    else:
                        status = '<span class="badge badge-success">Available</span>'
                        action = f'<span class="btn btn-primary" onclick="allocate(\'{item[0].id}\')">Allocate</span>'
                    ItemList.append([
                        idx+1,
                        '#'+str(item[0].id),
                        '' if item[1]==None or item[1].location==None else item[1].location,
                        '' if item[1]==None or item[1].issued_to==None else f'<a target="_blank" href="/user/{item[2].id}"><figure class="avatar mr-2 avatar-sm"><img alt="image" src="/static/img/avatar/avatar-{random.randint(1, 5)}.png" class="rounded-circle" data-toggle="tooltip" title="{item[2].fname} {item[2].lname}"></figure></a>',
                        '' if item[1]==None or item[1].expected_return==None else item[1].expected_return.strftime('%d %b %Y'),
                        status,
                        action
                    ])  
                return jsonify({'flag':True, 'data': ItemList})
                
            else:
                return jsonify({
                    'flag': False
                })    
        except Exception as e:
            print("ERROR",str(e))
            db.session.rollback()
            return jsonify({
                'flag': False
            })

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --------------------------------------------------
# My Account
# --------------------------------------------------

@app.route('/my-account/items',methods=["GET"])
@login_required
def my_account_items():
    return render_template("my-account/item-allocated-page.html")

@app.route('/my-account/items/<path:category>',methods=['POST'])
@login_required
def my_account_items_allocated(category="all"):
    id = current_user.id
    if category not in ['all','issued','returned']:
        return jsonify({'error': True})
    elif category=="all":
        itemList = []
        itemIssued = db.session.query(ItemIssued,Product,Users).filter(and_(ItemIssued.issued_to==id)).join(Inventory, Inventory.id==ItemIssued.item_id,isouter=True).join(Product,Product.id==Inventory.product_id,isouter=True).join(Users,Users.id==ItemIssued.approved_by,isouter=True).order_by(ItemIssued.id).all()
        for item in itemIssued:
            itemList.append([
                item[0].id,
                item[0].item_id,
                f'<span class="text-truncate">{item[1].name}</span>',
                '' if item[0].location==None else item[0].location,
                '' if item[2]==None or item[0].approved_by==None else f'<a target="_blank" href="/user/{item[2].id}"><figure class="avatar mr-2 avatar-sm"><img alt="image" src="/static/img/avatar/avatar-{random.randint(1, 5)}.png" class="rounded-circle" data-toggle="tooltip" title="{item[2].fname} {item[2].lname}"></figure></a>',
                '' if item[0]==None or item[0].issued_on==None else item[0].issued_on.strftime('%d %b %Y'),
                '' if item[0]==None or item[0].expected_return==None else item[0].expected_return.strftime('%d %b %Y'),
                '<span class="badge badge-success">Issued</span>' if item[0].returned==False else '<span class="badge badge-danger">Returned</span>'
            ])
        return jsonify({'error': False, 'data':itemList})
    elif category=="issued":
        itemList = []
        itemIssued = db.session.query(ItemIssued,Product,Users).filter(and_(ItemIssued.issued_to==id,ItemIssued.returned==False)).join(Inventory, Inventory.id==ItemIssued.item_id,isouter=True).join(Product,Product.id==Inventory.product_id,isouter=True).join(Users,Users.id==ItemIssued.approved_by,isouter=True).order_by(ItemIssued.id).all()
        for item in itemIssued:
            itemList.append([
                item[0].id,
                item[0].item_id,
                f'<span class="text-truncate">{item[1].name}</span>',
                '' if item[0].location==None else item[0].location,
                '' if item[2]==None or item[0].approved_by==None else f'<a target="_blank" href="/user/{item[2].id}"><figure class="avatar mr-2 avatar-sm"><img alt="image" src="/static/img/avatar/avatar-{random.randint(1, 5)}.png" class="rounded-circle" data-toggle="tooltip" title="{item[2].fname} {item[2].lname}"></figure></a>',
                '' if item[0]==None or item[0].issued_on==None else item[0].issued_on.strftime('%d %b %Y'),
                '' if item[0]==None or item[0].expected_return==None else item[0].expected_return.strftime('%d %b %Y')
            ])
        return jsonify({'error': False, 'data':itemList})
    elif category=="returned":
        itemList = []
        approved_by = aliased(Users)
        received_by = aliased(Users)
        itemIssued = db.session.query(ItemIssued,Product,approved_by,received_by).filter(and_(ItemIssued.issued_to==id,ItemIssued.returned==True)).join(Inventory, Inventory.id==ItemIssued.item_id,isouter=True).join(Product,Product.id==Inventory.product_id,isouter=True).join(approved_by,approved_by.id==ItemIssued.approved_by,isouter=True).join(received_by,received_by.id==ItemIssued.received_by,isouter=True).order_by(ItemIssued.id).all()
        for item in itemIssued:
            itemList.append([
                item[0].id,
                item[0].item_id,
                f'<span class="text-truncate">{item[1].name}</span>',
                '' if item[0].location==None else item[0].location,
                '' if item[2]==None or item[0].approved_by==None else f'<a target="_blank" href="/user/{item[2].id}"><figure class="avatar mr-2 avatar-sm"><img alt="image" src="/static/img/avatar/avatar-{random.randint(1, 5)}.png" class="rounded-circle" data-toggle="tooltip" title="{item[2].fname} {item[2].lname}"></figure></a>',
                '' if item[0]==None or item[0].issued_on==None else item[0].issued_on.strftime('%d %b %Y'),
                '' if item[3]==None or item[0].received_by==None else f'<a target="_blank" href="/user/{item[3].id}"><figure class="avatar mr-2 avatar-sm"><img alt="image" src="/static/img/avatar/avatar-{random.randint(1, 5)}.png" class="rounded-circle" data-toggle="tooltip" title="{item[3].fname} {item[3].lname}"></figure></a>',
                '' if item[0]==None or item[0].returned_on==None else item[0].returned_on.strftime('%d %b %Y')
            ])
        return jsonify({'error': False, 'data':itemList})

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
