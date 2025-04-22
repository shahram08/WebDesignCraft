<?php
// بارگذاری تنظیمات و توابع مورد نیاز
require_once 'includes/config.php';
require_once 'includes/database.php';
require_once 'includes/User.php';

// فقط کاربران وارد شده می‌توانند خارج شوند
if(is_logged_in()) {
    $user = new User();
    $user->logout();
    
    // تنظیم پیام موفقیت
    set_flash_message('success', 'شما با موفقیت از حساب کاربری خود خارج شدید.');
}

// هدایت به صفحه اصلی
redirect(url());
?>