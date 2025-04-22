from app import app, db
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin_user():
    """
    ایجاد کاربر ادمین با دسترسی‌های کامل
    """
    # بررسی وجود کاربر ادمین
    admin = User.query.filter_by(email="admin@webstudio.com").first()
    
    if not admin:
        print("در حال ایجاد کاربر ادمین...")
        
        # ایجاد کاربر جدید
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
        
        # ذخیره در دیتابیس
        db.session.add(admin)
        db.session.commit()
        
        print(f"کاربر ادمین با موفقیت ایجاد شد.")
        print(f"ایمیل: admin@webstudio.com")
        print(f"رمز عبور: Admin123!")
    else:
        print("کاربر ادمین از قبل وجود دارد.")
        
if __name__ == "__main__":
    with app.app_context():
        create_admin_user()