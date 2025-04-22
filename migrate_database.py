from app import app, db, migrate
from flask import Flask
from flask_migrate import Migrate, MigrateCommand, upgrade
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_and_migrate_database():
    with app.app_context():
        try:
            logger.info("حذف جداول قبلی...")
            db.drop_all()
            logger.info("جداول قبلی با موفقیت حذف شدند.")
            
            logger.info("ایجاد جداول جدید...")
            db.create_all()
            logger.info("جداول جدید با موفقیت ایجاد شدند.")
            
            # اکنون می‌توانیم فایل upgrade_database.py را اجرا کنیم
            logger.info("در حال اجرای اسکریپت upgrade_database.py...")
            import upgrade_database
            upgrade_database.upgrade_database()
            
            logger.info("مایگریشن با موفقیت انجام شد!")
            
        except Exception as e:
            logger.error(f"خطا در مایگریشن دیتابیس: {e}")
            db.session.rollback()

if __name__ == "__main__":
    reset_and_migrate_database()