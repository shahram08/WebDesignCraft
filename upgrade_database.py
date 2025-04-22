from app import app, db
from models import (
    User, ContactMessage, BlogPost, Service, PortfolioItem, 
    Tag, Category, Comment, Like, PostVisit, ActivityType, 
    UserActivity, SiteSettings, Statistics
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upgrade_database():
    with app.app_context():
        try:
            logger.info("آغاز به‌روزرسانی پایگاه داده...")
            
            # ایجاد جداول جدید
            db.create_all()
            logger.info("جداول جدید ایجاد شدند.")
            
            # بررسی و ایجاد تنظیمات سایت
            site_settings = SiteSettings.query.first()
            if not site_settings:
                logger.info("ایجاد تنظیمات پیش‌فرض برای سایت...")
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
                    footer_text="تمامی حقوق برای استودیو طراحی وب مدرن محفوظ است."
                )
                db.session.add(site_settings)
                db.session.commit()
                logger.info("تنظیمات سایت با موفقیت ایجاد شدند.")
            
            # ایجاد دسته‌بندی‌های پیش‌فرض برای بلاگ
            default_categories = ["طراحی وب", "توسعه وب", "سئو", "بازاریابی دیجیتال", "تجربه کاربری"]
            for category_name in default_categories:
                slug = category_name.replace(" ", "-").lower()
                existing_category = Category.query.filter_by(slug=slug).first()
                if not existing_category:
                    category = Category(
                        name=category_name,
                        slug=slug,
                        description=f"مقالات مرتبط با {category_name}"
                    )
                    db.session.add(category)
            db.session.commit()
            logger.info("دسته‌بندی‌های پیش‌فرض با موفقیت ایجاد شدند.")
            
            # ایجاد برچسب‌های پیش‌فرض
            default_tags = ["طراحی وب", "برنامه‌نویسی", "سئو", "وردپرس", "رسپانسیو", 
                           "جاوااسکریپت", "HTML", "CSS", "PHP", "پایتون"]
            for tag_name in default_tags:
                slug = tag_name.replace(" ", "-").lower()
                existing_tag = Tag.query.filter_by(slug=slug).first()
                if not existing_tag:
                    tag = Tag(
                        name=tag_name,
                        slug=slug
                    )
                    db.session.add(tag)
            db.session.commit()
            logger.info("برچسب‌های پیش‌فرض با موفقیت ایجاد شدند.")
            
            # ایجاد انواع فعالیت پیش‌فرض
            default_activity_types = [
                {"name": "ورود", "description": "ورود کاربر به سیستم"},
                {"name": "ثبت نام", "description": "ثبت نام کاربر جدید"},
                {"name": "ارسال نظر", "description": "ارسال نظر برای پست"},
                {"name": "ارسال پیام", "description": "ارسال پیام از طریق فرم تماس"},
                {"name": "لایک", "description": "لایک کردن پست"},
                {"name": "ویرایش پروفایل", "description": "ویرایش اطلاعات پروفایل"}
            ]
            for activity_type in default_activity_types:
                existing_type = ActivityType.query.filter_by(name=activity_type["name"]).first()
                if not existing_type:
                    new_type = ActivityType(
                        name=activity_type["name"],
                        description=activity_type["description"]
                    )
                    db.session.add(new_type)
            db.session.commit()
            logger.info("انواع فعالیت‌های پیش‌فرض با موفقیت ایجاد شدند.")
            
            # به‌روزرسانی پست‌های موجود
            existing_posts = BlogPost.query.all()
            for post in existing_posts:
                if post.category_id is None:
                    # اختصاص دسته‌بندی پیش‌فرض
                    default_category = Category.query.first()
                    if default_category:
                        post.category_id = default_category.id
                
                # افزودن برچسب‌ها به پست
                if not post.tags.count():
                    tags = Tag.query.limit(3).all()  # افزودن ۳ برچسب اول
                    for tag in tags:
                        post.tags.append(tag)
            db.session.commit()
            logger.info("پست‌های موجود با موفقیت به‌روزرسانی شدند.")
            
            # به‌روزرسانی سرویس‌ها
            existing_services = Service.query.all()
            for i, service in enumerate(existing_services):
                service.order = i
                if i < 2:  # دو سرویس اول را ویژه می‌کنیم
                    service.featured = True
            db.session.commit()
            logger.info("سرویس‌های موجود با موفقیت به‌روزرسانی شدند.")
            
            # به‌روزرسانی آمار
            today_stats = Statistics.get_or_create_today()
            logger.info("آمار امروز با موفقیت ایجاد شد.")
            
            logger.info("به‌روزرسانی پایگاه داده با موفقیت انجام شد!")
            
        except Exception as e:
            logger.error(f"خطا در به‌روزرسانی پایگاه داده: {e}")
            db.session.rollback()

if __name__ == "__main__":
    upgrade_database()