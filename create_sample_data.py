from app import app, db
from models import (User, ContactMessage, Tag, Category, BlogPost, 
                  Comment, Like, PostVisit, ActivityType, UserActivity, 
                  Service, PortfolioItem, SiteSettings, Statistics, post_tag, portfolio_tag)
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random
import json

def create_sample_data():
    """
    ایجاد داده‌های نمونه برای نمایش امکانات سایت
    """
    print("در حال ایجاد داده‌های نمونه...")
    
    # بررسی داده‌های موجود
    if User.query.count() > 0:
        print("داده‌های نمونه قبلاً ایجاد شده‌اند.")
        return
    
    # ایجاد انواع فعالیت‌ها
    activity_types = [
        ActivityType(name="ورود", description="ورود کاربر به سیستم"),
        ActivityType(name="ثبت نام", description="ثبت نام کاربر جدید"),
        ActivityType(name="ارسال نظر", description="ارسال نظر برای پست"),
        ActivityType(name="ارسال پیام", description="ارسال پیام از طریق فرم تماس"),
        ActivityType(name="لایک", description="لایک کردن پست"),
        ActivityType(name="ویرایش پروفایل", description="ویرایش اطلاعات پروفایل")
    ]
    db.session.add_all(activity_types)
    db.session.commit()
    
    # ایجاد تنظیمات سایت
    site_settings = SiteSettings(
        site_name="استودیو طراحی وب مدرن",
        site_description="طراحی و توسعه وب‌سایت‌های مدرن و واکنش‌گرا",
        contact_email="info@webstudio.com",
        contact_phone="+98123456789",
        contact_address="تهران، خیابان ولیعصر",
        social_facebook="https://facebook.com/webstudio",
        social_twitter="https://twitter.com/webstudio",
        social_instagram="https://instagram.com/webstudio",
        social_linkedin="https://linkedin.com/company/webstudio",
        footer_text="تمامی حقوق برای استودیو طراحی وب مدرن محفوظ است.",
        maintenance_mode=False
    )
    db.session.add(site_settings)
    db.session.commit()
    
    # ایجاد کاربر ادمین
    admin = User(
        username="admin",
        email="admin@webstudio.com",
        password_hash=generate_password_hash("Admin123!"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_admin=True,
        is_active=True,
        bio="مدیر کل سایت و طراح وب",
        last_login=datetime.utcnow()
    )
    db.session.add(admin)
    
    # ایجاد کاربر عادی
    user = User(
        username="user",
        email="user@example.com",
        password_hash=generate_password_hash("User123!"),
        created_at=datetime.utcnow() - timedelta(days=7),
        updated_at=datetime.utcnow() - timedelta(days=7),
        is_admin=False,
        is_active=True,
        bio="یک کاربر عادی",
        last_login=datetime.utcnow() - timedelta(days=1)
    )
    db.session.add(user)
    db.session.commit()
    
    # ایجاد دسته‌بندی‌ها
    categories = [
        Category(name="طراحی وب", slug="web-design", description="مقالات مرتبط با طراحی وب"),
        Category(name="برنامه‌نویسی", slug="programming", description="مقالات آموزشی برنامه‌نویسی"),
        Category(name="تجربه کاربری", slug="ux", description="اصول تجربه کاربری و رابط کاربری"),
        Category(name="بازاریابی دیجیتال", slug="digital-marketing", description="بازاریابی آنلاین و تبلیغات")
    ]
    db.session.add_all(categories)
    db.session.commit()
    
    # ایجاد تگ‌ها
    tags = [
        Tag(name="HTML", slug="html"),
        Tag(name="CSS", slug="css"),
        Tag(name="JavaScript", slug="javascript"),
        Tag(name="Python", slug="python"),
        Tag(name="React", slug="react"),
        Tag(name="فلسک", slug="flask"),
        Tag(name="دیزاین", slug="design"),
        Tag(name="موبایل", slug="mobile"),
        Tag(name="ریسپانسیو", slug="responsive"),
        Tag(name="SEO", slug="seo")
    ]
    db.session.add_all(tags)
    db.session.commit()
    
    # ایجاد خدمات
    services = [
        Service(
            title="طراحی وب‌سایت",
            description="طراحی وب‌سایت‌های مدرن و زیبا با استفاده از آخرین تکنولوژی‌های روز دنیا",
            icon="fa-laptop-code",
            featured=True,
            order=1
        ),
        Service(
            title="توسعه وب اپلیکیشن",
            description="ایجاد وب اپلیکیشن‌های پیشرفته و کاربردی برای کسب و کارهای مختلف",
            icon="fa-code",
            featured=True,
            order=2
        ),
        Service(
            title="طراحی رابط کاربری",
            description="طراحی رابط کاربری زیبا، کاربرپسند و مطابق با استانداردهای روز",
            icon="fa-palette",
            featured=True,
            order=3
        ),
        Service(
            title="بهینه‌سازی موتورهای جستجو",
            description="افزایش رتبه وب‌سایت شما در موتورهای جستجو با تکنیک‌های پیشرفته سئو",
            icon="fa-search",
            featured=False,
            order=4
        ),
        Service(
            title="پشتیبانی و نگهداری",
            description="خدمات پشتیبانی و نگهداری وب‌سایت‌ها به صورت ۲۴/۷",
            icon="fa-headset",
            featured=False,
            order=5
        )
    ]
    db.session.add_all(services)
    db.session.commit()
    
    # ایجاد نمونه کارها
    portfolio_items = [
        PortfolioItem(
            title="فروشگاه آنلاین مد و پوشاک",
            description="طراحی و پیاده‌سازی یک فروشگاه آنلاین مدرن برای فروش پوشاک",
            category="وب‌سایت",
            image_url="https://placehold.co/600x400?text=Fashion+Store",
            project_url="https://example.com/fashion",
            client_name="گروه مد ایرانیان",
            completed_date=datetime.utcnow() - timedelta(days=60),
            featured=True
        ),
        PortfolioItem(
            title="اپلیکیشن مدیریت پروژه",
            description="طراحی و پیاده‌سازی یک اپلیکیشن تحت وب برای مدیریت پروژه‌ها",
            category="وب اپلیکیشن",
            image_url="https://placehold.co/600x400?text=Project+Manager",
            project_url="https://example.com/pm",
            client_name="شرکت فناوری آرین",
            completed_date=datetime.utcnow() - timedelta(days=90),
            featured=True
        ),
        PortfolioItem(
            title="پرتال آموزشی آنلاین",
            description="پلتفرم آموزش آنلاین با امکان برگزاری کلاس‌های مجازی",
            category="وب‌سایت",
            image_url="https://placehold.co/600x400?text=Education+Portal",
            project_url="https://example.com/edu",
            client_name="موسسه آموزشی پیشگام",
            completed_date=datetime.utcnow() - timedelta(days=120),
            featured=True
        ),
        PortfolioItem(
            title="اپلیکیشن رزرو رستوران",
            description="اپلیکیشن تحت وب برای رزرو میز و سفارش آنلاین غذا",
            category="وب اپلیکیشن",
            image_url="https://placehold.co/600x400?text=Restaurant+App",
            project_url="https://example.com/restaurant",
            client_name="گروه رستوران‌های زنجیره‌ای نیاوران",
            completed_date=datetime.utcnow() - timedelta(days=180),
            featured=False
        )
    ]
    db.session.add_all(portfolio_items)
    db.session.commit()
    
    # ارتباط نمونه کارها با تگ‌ها
    portfolio_item_tags = [
        {"portfolio": 0, "tags": [0, 1, 2, 8]},
        {"portfolio": 1, "tags": [2, 3, 4, 5]},
        {"portfolio": 2, "tags": [0, 1, 2, 5, 9]},
        {"portfolio": 3, "tags": [2, 4, 7, 8]}
    ]
    
    for pt in portfolio_item_tags:
        for tag_idx in pt["tags"]:
            db.session.execute(portfolio_tag.insert().values(
                portfolio_id=portfolio_items[pt["portfolio"]].id,
                tag_id=tags[tag_idx].id
            ))
    db.session.commit()
    
    # ایجاد پست‌های وبلاگ
    blog_posts = [
        BlogPost(
            title="اصول طراحی وب‌سایت‌های مدرن در سال ۲۰۲۵",
            slug="modern-web-design-principles-2025",
            content="""
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد.</p>
            
            <h2>۱. طراحی مینیمال و هدفمند</h2>
            <p>کتابهای زیادی در شصت و سه درصد گذشته، حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی و فرهنگ پیشرو در زبان فارسی ایجاد کرد.</p>
            
            <h2>۲. استفاده از تایپوگرافی قوی</h2>
            <p>در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها و شرایط سخت تایپ به پایان رسد وزمان مورد نیاز شامل حروفچینی دستاوردهای اصلی و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد.</p>
            
            <h2>۳. طراحی با تفکر موبایل اول</h2>
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است.</p>
            """,
            summary="آشنایی با مهمترین اصول و ترندهای طراحی وب‌سایت‌های مدرن در سال ۲۰۲۵ برای ساخت وب‌سایت‌های جذاب و کاربرپسند",
            created_at=datetime.utcnow() - timedelta(days=10),
            updated_at=datetime.utcnow() - timedelta(days=10),
            published=True,
            featured_image="https://placehold.co/1200x630?text=Web+Design+2025",
            user_id=admin.id,
            category_id=categories[0].id
        ),
        BlogPost(
            title="مقایسه فریم‌ورک‌های جاوا اسکریپت در سال ۲۰۲۵",
            slug="javascript-frameworks-comparison-2025",
            content="""
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد.</p>
            
            <h2>React.js</h2>
            <p>کتابهای زیادی در شصت و سه درصد گذشته، حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی و فرهنگ پیشرو در زبان فارسی ایجاد کرد.</p>
            
            <h2>Vue.js</h2>
            <p>در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها و شرایط سخت تایپ به پایان رسد وزمان مورد نیاز شامل حروفچینی دستاوردهای اصلی و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد.</p>
            
            <h2>Angular</h2>
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است.</p>
            
            <h2>Svelte</h2>
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است.</p>
            """,
            summary="بررسی و مقایسه فریم‌ورک‌های محبوب جاوا اسکریپت در سال ۲۰۲۵ و کاربردهای هر کدام",
            created_at=datetime.utcnow() - timedelta(days=5),
            updated_at=datetime.utcnow() - timedelta(days=5),
            published=True,
            featured_image="https://placehold.co/1200x630?text=JS+Frameworks",
            user_id=admin.id,
            category_id=categories[1].id
        ),
        BlogPost(
            title="اصول طراحی رابط کاربری برای افزایش نرخ تبدیل",
            slug="ui-design-principles-conversion-rate",
            content="""
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد.</p>
            
            <h2>اصل اول: سادگی و وضوح</h2>
            <p>کتابهای زیادی در شصت و سه درصد گذشته، حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی و فرهنگ پیشرو در زبان فارسی ایجاد کرد.</p>
            
            <h2>اصل دوم: تاکید بصری</h2>
            <p>در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها و شرایط سخت تایپ به پایان رسد وزمان مورد نیاز شامل حروفچینی دستاوردهای اصلی و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد.</p>
            
            <h2>اصل سوم: طراحی فراخوان به عمل</h2>
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است.</p>
            """,
            summary="آشنایی با اصول طراحی رابط کاربری موثر برای افزایش نرخ تبدیل در وب‌سایت‌ها و اپلیکیشن‌ها",
            created_at=datetime.utcnow() - timedelta(days=15),
            updated_at=datetime.utcnow() - timedelta(days=15),
            published=True,
            featured_image="https://placehold.co/1200x630?text=UI+Design",
            user_id=admin.id,
            category_id=categories[2].id
        ),
        BlogPost(
            title="استراتژی‌های بازاریابی محتوا برای کسب و کارهای کوچک",
            slug="content-marketing-strategies-small-businesses",
            content="""
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد.</p>
            
            <h2>استراتژی اول: تولید محتوای با کیفیت و هدفمند</h2>
            <p>کتابهای زیادی در شصت و سه درصد گذشته، حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی و فرهنگ پیشرو در زبان فارسی ایجاد کرد.</p>
            
            <h2>استراتژی دوم: بهینه‌سازی برای موتورهای جستجو</h2>
            <p>در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها و شرایط سخت تایپ به پایان رسد وزمان مورد نیاز شامل حروفچینی دستاوردهای اصلی و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد.</p>
            
            <h2>استراتژی سوم: استفاده از شبکه‌های اجتماعی</h2>
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است.</p>
            """,
            summary="آشنایی با استراتژی‌های موثر بازاریابی محتوا برای کسب و کارهای کوچک و متوسط",
            created_at=datetime.utcnow() - timedelta(days=20),
            updated_at=datetime.utcnow() - timedelta(days=20),
            published=True,
            featured_image="https://placehold.co/1200x630?text=Content+Marketing",
            user_id=admin.id,
            category_id=categories[3].id
        ),
        BlogPost(
            title="آموزش پایتون برای طراحان وب",
            slug="python-for-web-designers",
            content="""
            <p>لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد.</p>
            
            <h2>بخش اول: آشنایی با پایتون</h2>
            <p>کتابهای زیادی در شصت و سه درصد گذشته، حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی و فرهنگ پیشرو در زبان فارسی ایجاد کرد.</p>
            
            <pre><code>
            # یک مثال ساده از کد پایتون
            def hello_world():
                print("Hello, World!")
                
            hello_world()
            </code></pre>
            
            <h2>بخش دوم: کار با فریم‌ورک فلسک</h2>
            <p>در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها و شرایط سخت تایپ به پایان رسد وزمان مورد نیاز شامل حروفچینی دستاوردهای اصلی و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد.</p>
            
            <pre><code>
            # یک مثال ساده از کد فلسک
            from flask import Flask
            app = Flask(__name__)
            
            @app.route('/')
            def home():
                return 'Welcome to Flask!'
                
            if __name__ == '__main__':
                app.run(debug=True)
            </code></pre>
            """,
            summary="آموزش پایتون برای طراحان وب: از مفاهیم پایه تا استفاده از فریم‌ورک فلسک برای توسعه وب",
            created_at=datetime.utcnow() - timedelta(days=25),
            updated_at=datetime.utcnow() - timedelta(days=25),
            published=True,
            featured_image="https://placehold.co/1200x630?text=Python+for+Web",
            user_id=admin.id,
            category_id=categories[1].id
        )
    ]
    db.session.add_all(blog_posts)
    db.session.commit()
    
    # ارتباط پست‌ها با تگ‌ها
    post_tags = [
        {"post": 0, "tags": [0, 1, 6, 8, 9]},
        {"post": 1, "tags": [2, 4]},
        {"post": 2, "tags": [6, 7, 8]},
        {"post": 3, "tags": [9]},
        {"post": 4, "tags": [3, 5]}
    ]
    
    for pt in post_tags:
        for tag_idx in pt["tags"]:
            db.session.execute(post_tag.insert().values(
                post_id=blog_posts[pt["post"]].id,
                tag_id=tags[tag_idx].id
            ))
    db.session.commit()
    
    # ایجاد نظرات
    comments = [
        Comment(
            content="مقاله بسیار مفیدی بود. ممنون از اشتراک‌گذاری این اطلاعات ارزشمند.",
            created_at=datetime.utcnow() - timedelta(days=9),
            approved=True,
            post_id=blog_posts[0].id,
            user_id=user.id
        ),
        Comment(
            content="من به تازگی شروع به یادگیری React کردم و این مقاله به من خیلی کمک کرد. آیا ممکن است در مورد Next.js هم مطلبی منتشر کنید؟",
            created_at=datetime.utcnow() - timedelta(days=4),
            approved=True,
            post_id=blog_posts[1].id,
            user_id=user.id
        ),
        Comment(
            content="این نکات خیلی کاربردی بودند. من از این اصول در طراحی وب‌سایت جدیدم استفاده کردم و نتایج عالی بود.",
            created_at=datetime.utcnow() - timedelta(days=14),
            approved=True,
            post_id=blog_posts[2].id,
            user_id=user.id
        )
    ]
    db.session.add_all(comments)
    db.session.commit()
    
    # ایجاد پاسخ به نظرات
    replies = [
        Comment(
            content="خیلی ممنون از نظر مثبت شما. خوشحالم که مقاله برایتان مفید بوده است.",
            created_at=datetime.utcnow() - timedelta(days=8),
            approved=True,
            post_id=blog_posts[0].id,
            user_id=admin.id,
            parent_id=comments[0].id
        ),
        Comment(
            content="بله حتما! در آینده نزدیک مقاله‌ای در مورد Next.js منتشر خواهیم کرد. ممنون از پیشنهاد شما.",
            created_at=datetime.utcnow() - timedelta(days=3),
            approved=True,
            post_id=blog_posts[1].id,
            user_id=admin.id,
            parent_id=comments[1].id
        )
    ]
    db.session.add_all(replies)
    db.session.commit()
    
    # ایجاد لایک‌ها
    likes = [
        Like(
            created_at=datetime.utcnow() - timedelta(days=8),
            post_id=blog_posts[0].id,
            user_id=user.id
        ),
        Like(
            created_at=datetime.utcnow() - timedelta(days=3),
            post_id=blog_posts[1].id,
            user_id=user.id
        ),
        Like(
            created_at=datetime.utcnow() - timedelta(days=13),
            post_id=blog_posts[2].id,
            user_id=user.id
        ),
        Like(
            created_at=datetime.utcnow() - timedelta(days=18),
            post_id=blog_posts[3].id,
            user_id=user.id
        )
    ]
    db.session.add_all(likes)
    db.session.commit()
    
    # ایجاد بازدیدها
    for post in blog_posts:
        # تعداد بازدیدهای تصادفی برای هر پست
        visit_count = random.randint(30, 200)
        
        for i in range(visit_count):
            # زمان بازدید تصادفی از زمان انتشار پست تا کنون
            days_ago = random.randint(0, (datetime.utcnow() - post.created_at).days)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            
            visit_date = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # گاهی بازدید توسط کاربر ثبت شده
            user_id = None
            if random.random() < 0.2:  # 20% احتمال
                user_id = random.choice([admin.id, user.id])
            
            visit = PostVisit(
                visit_date=visit_date,
                ip_address=f"192.168.1.{random.randint(1, 255)}",
                user_agent=f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/{random.randint(80, 100)}.0.{random.randint(1000, 9999)}.{random.randint(10, 200)}",
                post_id=post.id,
                user_id=user_id
            )
            db.session.add(visit)
    
    db.session.commit()
    
    # ایجاد فعالیت‌های کاربر
    user_activities = [
        UserActivity(
            description="ورود به سیستم",
            created_at=datetime.utcnow() - timedelta(days=7),
            ip_address="192.168.1.100",
            user_id=admin.id,
            data=json.dumps({"browser": "Chrome", "device": "Desktop"})
        ),
        UserActivity(
            description="ارسال نظر جدید",
            created_at=datetime.utcnow() - timedelta(days=8),
            ip_address="192.168.1.100",
            user_id=admin.id,
            data=json.dumps({"post_id": blog_posts[0].id, "comment_id": replies[0].id})
        ),
        UserActivity(
            description="ورود به سیستم",
            created_at=datetime.utcnow() - timedelta(days=1),
            ip_address="192.168.1.101",
            user_id=user.id,
            data=json.dumps({"browser": "Firefox", "device": "Mobile"})
        ),
        UserActivity(
            description="ارسال نظر جدید",
            created_at=datetime.utcnow() - timedelta(days=4),
            ip_address="192.168.1.101",
            user_id=user.id,
            data=json.dumps({"post_id": blog_posts[1].id, "comment_id": comments[1].id})
        ),
        UserActivity(
            description="لایک کردن پست",
            created_at=datetime.utcnow() - timedelta(days=3),
            ip_address="192.168.1.101",
            user_id=user.id,
            data=json.dumps({"post_id": blog_posts[1].id})
        )
    ]
    db.session.add_all(user_activities)
    db.session.commit()
    
    # ارتباط فعالیت‌ها با نوع فعالیت
    activity_type_relations = [
        {"activity": 0, "type": 0},  # ورود به سیستم
        {"activity": 1, "type": 2},  # ارسال نظر
        {"activity": 2, "type": 0},  # ورود به سیستم
        {"activity": 3, "type": 2},  # ارسال نظر
        {"activity": 4, "type": 4}   # لایک
    ]
    
    for relation in activity_type_relations:
        user_activities[relation["activity"]].types.append(activity_types[relation["type"]])
    db.session.commit()
    
    # ایجاد پیام‌های تماس
    contact_messages = [
        ContactMessage(
            name="علی محمدی",
            email="ali@example.com",
            subject="درخواست مشاوره",
            message="سلام، من می‌خواهم برای کسب و کارم یک وب‌سایت طراحی کنم. آیا می‌توانید به من مشاوره دهید؟",
            created_at=datetime.utcnow() - timedelta(days=3),
            is_read=True,
            reply_sent=True,
            reply_text="سلام علی عزیز، بله حتما. لطفاً با شماره تماس ما تماس بگیرید تا جلسه مشاوره رایگان برای شما ترتیب دهیم.",
            reply_date=datetime.utcnow() - timedelta(days=2),
            ip_address="192.168.1.120"
        ),
        ContactMessage(
            name="فاطمه رضایی",
            email="fateme@example.com",
            subject="قیمت طراحی فروشگاه آنلاین",
            message="سلام، می‌خواستم بدانم هزینه طراحی یک فروشگاه آنلاین با امکانات پرداخت آنلاین و مدیریت محصولات چقدر است؟",
            created_at=datetime.utcnow() - timedelta(days=1),
            is_read=True,
            reply_sent=False,
            ip_address="192.168.1.130"
        ),
        ContactMessage(
            name="محمد حسینی",
            email="mohammad@example.com",
            subject="همکاری به عنوان طراح",
            message="با سلام، من در زمینه طراحی UI/UX فعالیت می‌کنم و مایل به همکاری با شرکت شما هستم. آیا موقعیت کاری در این زمینه دارید؟",
            created_at=datetime.utcnow() - timedelta(hours=6),
            is_read=False,
            reply_sent=False,
            ip_address="192.168.1.140"
        )
    ]
    db.session.add_all(contact_messages)
    db.session.commit()
    
    # ایجاد آمار روزانه
    today = datetime.utcnow().date()
    for i in range(30):
        date = today - timedelta(days=i)
        visits = random.randint(50, 500)
        unique_visitors = int(visits * random.uniform(0.4, 0.8))
        page_views = int(visits * random.uniform(1.5, 3.0))
        
        # محاسبه محبوب‌ترین پست هر روز
        popular_post_id = None
        if blog_posts:
            popular_post_id = random.choice(blog_posts).id
        
        data = {
            "browser_stats": {
                "Chrome": random.uniform(0.4, 0.6),
                "Firefox": random.uniform(0.1, 0.2),
                "Safari": random.uniform(0.1, 0.2),
                "Edge": random.uniform(0.05, 0.1),
                "Other": random.uniform(0.01, 0.05)
            },
            "device_stats": {
                "Desktop": random.uniform(0.4, 0.7),
                "Mobile": random.uniform(0.2, 0.5),
                "Tablet": random.uniform(0.05, 0.15)
            },
            "traffic_sources": {
                "Direct": random.uniform(0.2, 0.4),
                "Search": random.uniform(0.3, 0.5),
                "Social": random.uniform(0.1, 0.2),
                "Referral": random.uniform(0.05, 0.15),
                "Email": random.uniform(0.02, 0.08)
            }
        }
        
        stat = Statistics(
            date=date,
            visits=visits,
            unique_visitors=unique_visitors,
            page_views=page_views,
            most_visited_page="/blog" if random.random() < 0.6 else "/",
            most_visited_post_id=popular_post_id,
            data=json.dumps(data)
        )
        db.session.add(stat)
    
    db.session.commit()
    
    # به‌روزرسانی شمارنده‌های پست
    for post in blog_posts:
        post.update_counts()
    db.session.commit()
    
    print("داده‌های نمونه با موفقیت ایجاد شدند!")
    
if __name__ == "__main__":
    with app.app_context():
        create_sample_data()