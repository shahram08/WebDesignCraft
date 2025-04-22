from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import User, ContactMessage, BlogPost, Service, PortfolioItem
from forms import LoginForm, RegistrationForm, ContactForm, BlogPostForm, ServiceForm, PortfolioItemForm
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash
import re
from sqlalchemy.exc import IntegrityError
import secrets
import string

def generate_slug(title):
    # Replace farsi characters with english equivalents (simplified)
    replacements = {
        'آ': 'a', 'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 'چ': 'ch',
        'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z', 'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's',
        'ش': 'sh', 'ص': 's', 'ض': 'z', 'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f',
        'ق': 'gh', 'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'v', 'ه': 'h',
        'ی': 'y', ' ': '-', '‌': '', '‍': ''
    }
    
    result = ''
    for char in title.lower():
        result += replacements.get(char, char)
    
    # Remove any non-alphanumeric characters and replace spaces with hyphens
    result = re.sub(r'[^\w\s-]', '', result)
    result = re.sub(r'[-\s]+', '-', result).strip('-')
    
    return result

def init_routes(app):
    
    @app.route('/')
    def index():
        # Get featured services for the homepage
        services = Service.query.limit(3).all()
        
        # Get latest blog posts for the homepage
        blog_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(3).all()
        
        # Get portfolio items for the homepage
        portfolio_items = PortfolioItem.query.limit(6).all()
        
        return render_template('index.html', 
                               services=services, 
                               blog_posts=blog_posts,
                               portfolio_items=portfolio_items)
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/services')
    def services():
        all_services = Service.query.all()
        return render_template('services.html', services=all_services)
    
    @app.route('/portfolio')
    def portfolio():
        all_items = PortfolioItem.query.all()
        categories = set(item.category for item in all_items)
        return render_template('portfolio.html', 
                               portfolio_items=all_items, 
                               categories=categories)
    
    @app.route('/blog')
    def blog():
        page = request.args.get('page', 1, type=int)
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=5)
        return render_template('blog.html', posts=posts)
    
    @app.route('/blog/<string:slug>')
    def blog_post(slug):
        post = BlogPost.query.filter_by(slug=slug).first_or_404()
        return render_template('blog_post.html', post=post)
    
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            new_message = ContactMessage(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(new_message)
            try:
                db.session.commit()
                flash('پیام شما با موفقیت ارسال شد!', 'success')
                return redirect(url_for('contact'))
            except Exception as e:
                logging.error(f"Error saving contact message: {e}")
                db.session.rollback()
                flash('خطایی در ارسال پیام رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        
        return render_template('contact.html', form=form)
    
    # Authentication routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f'خوش آمدید {user.username}!', 'success')
                return redirect(next_page if next_page else url_for('index'))
            else:
                flash('ورود ناموفق. لطفا ایمیل و رمز عبور خود را بررسی کنید.', 'danger')
        
        return render_template('login.html', form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            try:
                db.session.commit()
                flash('ثبت نام شما با موفقیت انجام شد! اکنون می‌توانید وارد شوید.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                logging.error(f"Error registering user: {e}")
                db.session.rollback()
                flash('خطایی در ثبت نام رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        
        return render_template('register.html', form=form)
    
    @app.route('/logout')
    def logout():
        logout_user()
        flash('شما با موفقیت خارج شدید.', 'info')
        return redirect(url_for('index'))
    
    # Admin panel routes
    @app.route('/admin')
    @login_required
    def admin():
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        contact_count = ContactMessage.query.filter_by(is_read=False).count()
        blog_count = BlogPost.query.count()
        service_count = Service.query.count()
        portfolio_count = PortfolioItem.query.count()
        
        return render_template('admin/index.html', 
                              contact_count=contact_count,
                              blog_count=blog_count,
                              service_count=service_count,
                              portfolio_count=portfolio_count)
    
    @app.route('/admin/blog')
    @login_required
    def admin_blog():
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
        return render_template('admin/blog.html', posts=posts)
    
    @app.route('/admin/blog/new', methods=['GET', 'POST'])
    @login_required
    def admin_blog_new():
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        form = BlogPostForm()
        if form.validate_on_submit():
            post = BlogPost(
                title=form.title.data,
                slug=form.slug.data,
                summary=form.summary.data,
                content=form.content.data,
                user_id=current_user.id
            )
            db.session.add(post)
            try:
                db.session.commit()
                flash('پست جدید با موفقیت ایجاد شد!', 'success')
                return redirect(url_for('admin_blog'))
            except IntegrityError:
                db.session.rollback()
                flash('این اسلاگ قبلاً استفاده شده است. لطفاً اسلاگ دیگری وارد کنید.', 'danger')
            except Exception as e:
                logging.error(f"Error creating blog post: {e}")
                db.session.rollback()
                flash('خطایی در ایجاد پست رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        
        return render_template('admin/blog_edit.html', form=form, mode='new')
    
    @app.route('/admin/blog/edit/<int:post_id>', methods=['GET', 'POST'])
    @login_required
    def admin_blog_edit(post_id):
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        post = BlogPost.query.get_or_404(post_id)
        form = BlogPostForm()
        
        if form.validate_on_submit():
            post.title = form.title.data
            post.slug = form.slug.data
            post.summary = form.summary.data
            post.content = form.content.data
            
            try:
                db.session.commit()
                flash('پست با موفقیت به‌روزرسانی شد!', 'success')
                return redirect(url_for('admin_blog'))
            except IntegrityError:
                db.session.rollback()
                flash('این اسلاگ قبلاً استفاده شده است. لطفاً اسلاگ دیگری وارد کنید.', 'danger')
            except Exception as e:
                logging.error(f"Error updating blog post: {e}")
                db.session.rollback()
                flash('خطایی در به‌روزرسانی پست رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        elif request.method == 'GET':
            form.title.data = post.title
            form.slug.data = post.slug
            form.summary.data = post.summary
            form.content.data = post.content
        
        return render_template('admin/blog_edit.html', form=form, mode='edit', post=post)
    
    @app.route('/admin/blog/delete/<int:post_id>', methods=['POST'])
    @login_required
    def admin_blog_delete(post_id):
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        
        try:
            db.session.commit()
            flash('پست با موفقیت حذف شد!', 'success')
        except Exception as e:
            logging.error(f"Error deleting blog post: {e}")
            db.session.rollback()
            flash('خطایی در حذف پست رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        
        return redirect(url_for('admin_blog'))
    
    @app.route('/admin/services')
    @login_required
    def admin_services():
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        services = Service.query.all()
        return render_template('admin/services.html', services=services)
    
    @app.route('/admin/services/new', methods=['GET', 'POST'])
    @login_required
    def admin_services_new():
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        form = ServiceForm()
        if form.validate_on_submit():
            service = Service(
                title=form.title.data,
                description=form.description.data,
                icon=form.icon.data
            )
            db.session.add(service)
            try:
                db.session.commit()
                flash('سرویس جدید با موفقیت ایجاد شد!', 'success')
                return redirect(url_for('admin_services'))
            except Exception as e:
                logging.error(f"Error creating service: {e}")
                db.session.rollback()
                flash('خطایی در ایجاد سرویس رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        
        return render_template('admin/service_edit.html', form=form, mode='new')
    
    @app.route('/admin/services/edit/<int:service_id>', methods=['GET', 'POST'])
    @login_required
    def admin_services_edit(service_id):
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        service = Service.query.get_or_404(service_id)
        form = ServiceForm()
        
        if form.validate_on_submit():
            service.title = form.title.data
            service.description = form.description.data
            service.icon = form.icon.data
            
            try:
                db.session.commit()
                flash('سرویس با موفقیت به‌روزرسانی شد!', 'success')
                return redirect(url_for('admin_services'))
            except Exception as e:
                logging.error(f"Error updating service: {e}")
                db.session.rollback()
                flash('خطایی در به‌روزرسانی سرویس رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        elif request.method == 'GET':
            form.title.data = service.title
            form.description.data = service.description
            form.icon.data = service.icon
        
        return render_template('admin/service_edit.html', form=form, mode='edit', service=service)
    
    @app.route('/admin/services/delete/<int:service_id>', methods=['POST'])
    @login_required
    def admin_services_delete(service_id):
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        
        try:
            db.session.commit()
            flash('سرویس با موفقیت حذف شد!', 'success')
        except Exception as e:
            logging.error(f"Error deleting service: {e}")
            db.session.rollback()
            flash('خطایی در حذف سرویس رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        
        return redirect(url_for('admin_services'))
    
    @app.route('/admin/portfolio')
    @login_required
    def admin_portfolio():
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        items = PortfolioItem.query.all()
        return render_template('admin/portfolio.html', items=items)
    
    @app.route('/admin/portfolio/new', methods=['GET', 'POST'])
    @login_required
    def admin_portfolio_new():
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        form = PortfolioItemForm()
        if form.validate_on_submit():
            item = PortfolioItem(
                title=form.title.data,
                description=form.description.data,
                category=form.category.data,
                image_url=form.image_url.data
            )
            db.session.add(item)
            try:
                db.session.commit()
                flash('نمونه کار جدید با موفقیت ایجاد شد!', 'success')
                return redirect(url_for('admin_portfolio'))
            except Exception as e:
                logging.error(f"Error creating portfolio item: {e}")
                db.session.rollback()
                flash('خطایی در ایجاد نمونه کار رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        
        return render_template('admin/portfolio_edit.html', form=form, mode='new')
    
    @app.route('/admin/portfolio/edit/<int:item_id>', methods=['GET', 'POST'])
    @login_required
    def admin_portfolio_edit(item_id):
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        item = PortfolioItem.query.get_or_404(item_id)
        form = PortfolioItemForm()
        
        if form.validate_on_submit():
            item.title = form.title.data
            item.description = form.description.data
            item.category = form.category.data
            item.image_url = form.image_url.data
            
            try:
                db.session.commit()
                flash('نمونه کار با موفقیت به‌روزرسانی شد!', 'success')
                return redirect(url_for('admin_portfolio'))
            except Exception as e:
                logging.error(f"Error updating portfolio item: {e}")
                db.session.rollback()
                flash('خطایی در به‌روزرسانی نمونه کار رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        elif request.method == 'GET':
            form.title.data = item.title
            form.description.data = item.description
            form.category.data = item.category
            form.image_url.data = item.image_url
        
        return render_template('admin/portfolio_edit.html', form=form, mode='edit', item=item)
    
    @app.route('/admin/portfolio/delete/<int:item_id>', methods=['POST'])
    @login_required
    def admin_portfolio_delete(item_id):
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        item = PortfolioItem.query.get_or_404(item_id)
        db.session.delete(item)
        
        try:
            db.session.commit()
            flash('نمونه کار با موفقیت حذف شد!', 'success')
        except Exception as e:
            logging.error(f"Error deleting portfolio item: {e}")
            db.session.rollback()
            flash('خطایی در حذف نمونه کار رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        
        return redirect(url_for('admin_portfolio'))
    
    @app.route('/admin/messages')
    @login_required
    def admin_messages():
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        return render_template('admin/messages.html', messages=messages)
    
    @app.route('/admin/messages/<int:message_id>')
    @login_required
    def admin_messages_view(message_id):
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        message = ContactMessage.query.get_or_404(message_id)
        message.is_read = True
        
        try:
            db.session.commit()
        except Exception as e:
            logging.error(f"Error marking message as read: {e}")
            db.session.rollback()
        
        return render_template('admin/message_view.html', message=message)
    
    @app.route('/admin/messages/delete/<int:message_id>', methods=['POST'])
    @login_required
    def admin_messages_delete(message_id):
        if not current_user.is_admin:
            flash('شما دسترسی به پنل مدیریت را ندارید.', 'danger')
            return redirect(url_for('index'))
        
        message = ContactMessage.query.get_or_404(message_id)
        db.session.delete(message)
        
        try:
            db.session.commit()
            flash('پیام با موفقیت حذف شد!', 'success')
        except Exception as e:
            logging.error(f"Error deleting message: {e}")
            db.session.rollback()
            flash('خطایی در حذف پیام رخ داد. لطفا مجددا تلاش کنید.', 'danger')
        
        return redirect(url_for('admin_messages'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Function to initialize database with some sample data 
    # This is only for demonstration purposes
    @app.cli.command("init-db")
    def init_db():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            is_admin=True
        )
        admin.set_password("adminpassword")
        db.session.add(admin)
        
        # Create services
        services = [
            Service(title="طراحی وب", description="طراحی وب‌سایت سفارشی و ریسپانسیو که در تمام دستگاه‌ها عالی به نظر می‌رسد.", icon="fa-desktop"),
            Service(title="توسعه وب", description="توسعه وب کامل با فناوری‌ها و فریم‌ورک‌های مدرن.", icon="fa-code"),
            Service(title="طراحی UI/UX", description="طراحی رابط کاربری و تجربه کاربری با تمرکز بر قابلیت استفاده و تبدیل.", icon="fa-paint-brush"),
            Service(title="اپلیکیشن‌های موبایل", description="توسعه اپلیکیشن‌های موبایل بومی و چند-پلتفرمی.", icon="fa-mobile-alt"),
            Service(title="راهکارهای فروشگاهی", description="توسعه فروشگاه آنلاین با پردازش پرداخت امن.", icon="fa-shopping-cart"),
            Service(title="بازاریابی دیجیتال", description="سئو، شبکه‌های اجتماعی و بازاریابی محتوا برای رشد حضور آنلاین شما.", icon="fa-chart-line")
        ]
        
        for service in services:
            db.session.add(service)
        
        # Create portfolio items
        portfolio_items = [
            PortfolioItem(
                title="وب‌سایت شرکتی",
                description="یک وب‌سایت مدرن برای یک شرکت خدمات مالی",
                category="طراحی وب",
                image_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
            ),
            PortfolioItem(
                title="پلتفرم فروشگاهی",
                description="یک فروشگاه آنلاین کاملاً ریسپانسیو با یکپارچگی پرداخت",
                category="فروشگاه",
                image_url="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
            ),
            PortfolioItem(
                title="رابط کاربری اپلیکیشن موبایل",
                description="طراحی رابط کاربری برای یک اپلیکیشن پیگیری تناسب اندام",
                category="طراحی UI/UX",
                image_url="https://images.unsplash.com/photo-1551650975-87deedd944c3?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
            ),
            PortfolioItem(
                title="وب‌سایت رستوران",
                description="یک وب‌سایت شیک با سیستم رزرو آنلاین",
                category="طراحی وب",
                image_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
            ),
            PortfolioItem(
                title="وبلاگ سفر",
                description="یک وبلاگ متمرکز بر محتوا با یکپارچگی چندرسانه‌ای",
                category="توسعه وب",
                image_url="https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
            ),
            PortfolioItem(
                title="پورتفولیو عکاسی",
                description="یک وب‌سایت پورتفولیو مینیمالیستی برای یک عکاس حرفه‌ای",
                category="طراحی وب",
                image_url="https://images.unsplash.com/photo-1452587925148-ce544e77e70d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
            )
        ]
        
        for item in portfolio_items:
            db.session.add(item)
        
        # Create blog posts
        blog_posts = [
            BlogPost(
                title="10 روند طراحی وب برای سال 2023",
                slug="web-design-trends-2023",
                content="""
                <p>دنیای طراحی وب به طور مداوم در حال تکامل است. در اینجا 10 روند برتری که در سال 2023 می‌بینیم آورده شده است:</p>
                
                <h3>1. حالت تاریک</h3>
                <p>حالت تاریک محبوبیت فزاینده‌ای پیدا کرده است و به کاربران یک جایگزین جذاب بصری ارائه می‌دهد که فشار چشم را کاهش می‌دهد و عمر باتری را در صفحه‌های OLED صرفه‌جویی می‌کند.</p>
                
                <h3>2. طراحی مینیمالیستی</h3>
                <p>کمتر همچنان بیشتر است در طراحی وب. رویکردهای مینیمالیستی بر عناصر ضروری متمرکز شده، از فضای منفی به طور موثر استفاده می‌کنند تا رابط‌های تمیز و بدون شلوغی ایجاد کنند.</p>
                
                <h3>3. عناصر سه بعدی</h3>
                <p>با بهبود قابلیت‌های مرورگر، ما عناصر سه بعدی تعاملی بیشتری می‌بینیم که کاربران را درگیر کرده و تجربیاتی به یادماندنی ایجاد می‌کنند.</p>
                
                <h3>4. رابط کاربری صوتی</h3>
                <p>بهینه‌سازی جستجوی صوتی ضروری می‌شود زیرا کاربران بیشتری از طریق دستورات صوتی با وب‌سایت‌ها تعامل می‌کنند.</p>
                
                <h3>5. میکرو-تعاملات</h3>
                <p>انیمیشن‌های کوچک و عناصر بازخورد، تجربه کاربر را با ارائه تأیید بصری از اقدامات و افزودن شخصیت بهبود می‌بخشند.</p>
                
                <h3>6. طراحی با اولویت دسترسی‌پذیری</h3>
                <p>طراحی برای همه کاربران نه تنها اخلاقی است بلکه به طور فزاینده‌ای توسط مقررات در سراسر جهان الزامی می‌شود.</p>
                
                <h3>7. تایپوگرافی پررنگ</h3>
                <p>تایپوگرافی بزرگ و بیانگر همچنان غالب است و اغلب به عنوان عنصر بصری اصلی جایگزین تصاویر می‌شود.</p>
                
                <h3>8. اشکال انتزاعی و هندسی</h3>
                <p>اشکال ارگانیک و الگوهای هندسی جذابیت بصری اضافه می‌کنند بدون اینکه محتوا را لبریز کنند.</p>
                
                <h3>9. تجربیات اسکرول غوطه‌ور</h3>
                <p>جلوه‌های پارالاکس و انیمیشن‌های راه‌اندازی شده با اسکرول فرصت‌های داستان‌سرایی جذابی ایجاد می‌کنند.</p>
                
                <h3>10. یکپارچگی واقعیت افزوده</h3>
                <p>ویژگی‌های AR به کاربران اجازه می‌دهد محصولات را در فضای خود قبل از خرید تجسم کنند.</p>
                
                <p>به روز ماندن با این روندها کمک می‌کند تا اطمینان حاصل شود که وب‌سایت شما در منظر دیجیتال امروزی مدرن و رقابتی باقی می‌ماند.</p>
                """,
                summary="روندهای طراحی پیشرفته را که به وب در سال 2023 شکل می‌دهند کشف کنید، از حالت تاریک تا یکپارچگی واقعیت افزوده.",
                user_id=1,
                created_at=datetime(2023, 6, 15)
            ),
            BlogPost(
                title="چرا طراحی ریسپانسیو بیش از همیشه اهمیت دارد",
                slug="responsive-design-importance",
                content="""
                <p>در دنیای چند-دستگاهی امروز، طراحی ریسپانسیو دیگر فقط یک ویژگی خوب نیست—این ضروری است. در اینجا دلیل آن آمده است:</p>
                
                <h3>ترافیک موبایل غالب است</h3>
                <p>بیش از 50٪ از ترافیک وب جهانی اکنون از دستگاه‌های تلفن همراه می‌آید. اگر سایت شما در گوشی‌های هوشمند و تبلت‌ها به خوبی عمل نمی‌کند، شما به طور بالقوه نیمی از مخاطبان خود را دور می‌کنید.</p>
                
                <h3>گوگل سایت‌های دوستدار موبایل را اولویت می‌دهد</h3>
                <p>ایندکس‌گذاری موبایل-اول گوگل به این معنی است که موتور جستجو در درجه اول از نسخه موبایل محتوا برای ایندکس‌گذاری و رتبه‌بندی استفاده می‌کند. سایت‌های غیر ریسپانسیو ممکن است دیده شدن کمتری در نتایج جستجو داشته باشند.</p>
                
                <h3>انتظارات تجربه کاربری</h3>
                <p>کاربران امروزی انتظار تجربیات بی‌درز در تمام دستگاه‌های خود دارند. سایتی که نیاز به نیشگون گرفتن، بزرگنمایی یا اسکرول افقی در موبایل دارد، ناامیدی و نرخ‌های پرش بالا ایجاد می‌کند.</p>
                
                <h3>دسته‌های جدید دستگاه</h3>
                <p>فراتر از تلفن‌ها و تبلت‌ها، کاربران اکنون در ساعت‌های هوشمند، تلویزیون‌های هوشمند و دستگاه‌هایی با صفحه‌های تاشو مرور می‌کنند. طراحی واقعاً ریسپانسیو با هر اندازه یا جهت صفحه نمایش سازگار می‌شود.</p>
                
                <h3>بهینه‌سازی تبدیل</h3>
                <p>مطالعات به طور مداوم نشان می‌دهند که سایت‌های دوستدار موبایل بهتر تبدیل می‌شوند. یک تجربه روان موبایل موانع خرید، ثبت‌نام و سایر اقدامات مطلوب را از بین می‌برد.</p>
                
                <h3>کارآیی هزینه</h3>
                <p>نگهداری یک وب‌سایت ریسپانسیو واحد از نظر هزینه موثرتر از توسعه و به‌روزرسانی نسخه‌های جداگانه دسکتاپ و موبایل است.</p>
                
                <h3>آینده‌پروفی</h3>
                <p>یک سایت ریسپانسیو خوب ساخته شده ذاتاً با دستگاه‌ها و اندازه‌های صفحه‌نمایش آینده که ممکن است ظهور کنند سازگارتر است.</p>
                
                <p>نتیجه: طراحی ریسپانسیو صرفاً در مورد خوب به نظر رسیدن در صفحه‌های مختلف نیست—در مورد اطمینان از این است که سایت شما در اکوسیستم در حال گسترش دستگاه‌های متصل قابل دسترسی، کاربردی و رقابتی باقی می‌ماند.</p>
                """,
                summary="با غالب بودن ترافیک موبایل در وب، طراحی ریسپانسیو برای سئو، تجربه کاربری و موفقیت تجاری بسیار مهم شده است.",
                user_id=1,
                created_at=datetime(2023, 7, 22)
            ),
            BlogPost(
                title="5 اصل ضروری UX که هر طراح باید دنبال کند",
                slug="essential-ux-principles",
                content="""
                <p>طراحی تجربه کاربر (UX) بر ایجاد تجربیات معنی‌دار و مرتبط برای کاربران متمرکز است. این پنج اصل اساسی به هدایت هر پروژه طراحی UX کمک خواهد کرد:</p>
                
                <h3>1. طراحی با محوریت کاربر</h3>
                <p>همیشه با تحقیق کاربر شروع کنید. درک نیازها، رفتارها و نقاط درد کاربران شما باید تصمیمات طراحی را هدایت کند نه ترجیحات زیبایی‌شناختی یا فرضیات. پرسوناهای کاربر ایجاد کنید، مصاحبه‌ها انجام دهید و در طول فرآیند طراحی، نمونه‌های اولیه را با کاربران واقعی آزمایش کنید.</p>
                
                <h3>2. سلسله مراتب و سازماندهی</h3>
                <p>اطلاعات باید به طور منطقی سازماندهی شوند، با اولویت بصری به مهم‌ترین عناصر داده شود. کاربران باید بتوانند به راحتی محتوا را اسکن کنند و اهمیت نسبی عناصر مختلف را درک کنند. از اندازه، رنگ، کنتراست و موقعیت برای ایجاد سلسله مراتب واضح بصری استفاده کنید.</p>
                
                <h3>3. یکنواختی و استانداردها</h3>
                <p>رابط‌های یکنواخت شهودی‌تر و آسان‌تر برای یادگیری هستند. یکنواختی را در الگوهای طراحی، روش‌های تعامل و اصطلاحات در سراسر محصول خود حفظ کنید. از قراردادهای ایجاد شده در صورت مناسب بودن پیروی کنید—کاربران انتظاراتی را از تجربیات دیجیتال دیگر می‌آورند.</p>
                
                <h3>4. دسترسی‌پذیری و فراگیر بودن</h3>
                <p>برای همه کاربران بالقوه طراحی کنید، از جمله کسانی که دارای ناتوانی یا اختلال هستند. عواملی مانند کنتراست رنگ، اندازه متن، ناوبری کیبورد و سازگاری با صفحه‌خوان را در نظر بگیرید. طراحی دسترس‌پذیر اغلب قابلیت استفاده را برای همه بهبود می‌بخشد، نه فقط کاربران با ناتوانی.</p>
                
                <h3>5. بازخورد و پاسخ</h3>
                <p>کاربران باید همیشه بدانند چه اتفاقی در سیستم می‌افتد. بازخورد واضحی برای اقدامات (مانند تغییرات حالت دکمه یا نشانگرهای بارگذاری) ارائه دهید، خطاها را به صورت مفید اطلاع دهید و اطمینان حاصل کنید که زمان‌های پاسخ طبیعی به نظر می‌رسند. بازخورد خوب اضطراب کاربر را کاهش می‌دهد و اعتماد به رابط را ایجاد می‌کند.</p>
                
                <p>این اصول فقط مفاهیم نظری نیستند—آنها تأثیر واقعی بر کسب‌وکار دارند. تحقیقات نشان می‌دهد که هر دلار سرمایه‌گذاری شده در UX 100 دلار بازگشت می‌آورد و 88٪ از مصرف‌کنندگان آنلاین پس از یک تجربه کاربری ضعیف احتمال کمتری دارد که به یک سایت بازگردند.</p>
                
                <p>با اولویت‌بندی این اصول اساسی، طراحان می‌توانند تجربیات دیجیتال شهودی‌تر، کارآمدتر و لذت‌بخش‌تری ایجاد کنند که هم به کاربران و هم به اهداف کسب‌وکار خدمت می‌کنند.</p>
                """,
                summary="اصول اساسی UX را بیاموزید که می‌توانند محصولات دیجیتال شما را متحول کنند.",
                user_id=1,
                created_at=datetime(2023, 8, 10)
            )
        ]
        
        for post in blog_posts:
            db.session.add(post)
        
        try:
            db.session.commit()
            print("Database initialized with sample data")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {e}")