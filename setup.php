<?php
// این فایل برای ایجاد جداول دیتابیس و مقداردهی اولیه استفاده می‌شود

// بارگذاری تنظیمات و توابع مورد نیاز
require_once 'includes/config.php';

// تنظیم هدر برای نمایش صحیح کاراکترهای فارسی
header('Content-Type: text/html; charset=utf-8');

echo "<h1>راه‌اندازی پایگاه داده</h1>";

try {
    // اتصال به سرور دیتابیس
    $pdo = new PDO('mysql:host=' . DB_HOST, DB_USER, DB_PASS);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // تنظیم کاراکترست به UTF-8
    $pdo->exec("SET NAMES utf8mb4");
    
    // ایجاد دیتابیس اگر وجود نداشته باشد
    $pdo->exec("CREATE DATABASE IF NOT EXISTS `" . DB_NAME . "` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    echo "<p>دیتابیس با موفقیت ایجاد شد یا از قبل وجود داشت.</p>";
    
    // انتخاب دیتابیس
    $pdo->exec("USE `" . DB_NAME . "`");
    
    // ایجاد جدول کاربران
    $pdo->exec("CREATE TABLE IF NOT EXISTS `users` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(100) NOT NULL,
        `email` varchar(100) NOT NULL,
        `password` varchar(255) NOT NULL,
        `is_admin` tinyint(1) NOT NULL DEFAULT 0,
        `registered_at` datetime NOT NULL,
        `last_login` datetime DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `email` (`email`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
    echo "<p>جدول کاربران با موفقیت ایجاد شد.</p>";
    
    // ایجاد جدول خدمات
    $pdo->exec("CREATE TABLE IF NOT EXISTS `services` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `title` varchar(100) NOT NULL,
        `description` text NOT NULL,
        `icon` varchar(50) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
    echo "<p>جدول خدمات با موفقیت ایجاد شد.</p>";
    
    // ایجاد جدول نمونه کارها
    $pdo->exec("CREATE TABLE IF NOT EXISTS `portfolio` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `title` varchar(100) NOT NULL,
        `description` text NOT NULL,
        `category` varchar(50) NOT NULL,
        `image_url` varchar(200) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
    echo "<p>جدول نمونه کارها با موفقیت ایجاد شد.</p>";
    
    // ایجاد جدول مقالات وبلاگ
    $pdo->exec("CREATE TABLE IF NOT EXISTS `blog_posts` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `title` varchar(200) NOT NULL,
        `slug` varchar(200) NOT NULL,
        `content` text NOT NULL,
        `summary` text NOT NULL,
        `created_at` datetime NOT NULL,
        `updated_at` datetime NOT NULL,
        `user_id` int(11) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `slug` (`slug`),
        KEY `user_id` (`user_id`),
        CONSTRAINT `blog_posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
    echo "<p>جدول مقالات وبلاگ با موفقیت ایجاد شد.</p>";
    
    // ایجاد جدول پیام‌های تماس
    $pdo->exec("CREATE TABLE IF NOT EXISTS `contact_messages` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(100) NOT NULL,
        `email` varchar(120) NOT NULL,
        `subject` varchar(200) NOT NULL,
        `message` text NOT NULL,
        `created_at` datetime NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
    echo "<p>جدول پیام‌های تماس با موفقیت ایجاد شد.</p>";
    
    // درج اطلاعات اولیه
    
    // بررسی وجود کاربر ادمین
    $stmt = $pdo->query("SELECT COUNT(*) FROM `users` WHERE `is_admin` = 1");
    $admin_count = $stmt->fetchColumn();
    
    if ($admin_count == 0) {
        // ایجاد کاربر ادمین
        $admin_password = password_hash('admin123', PASSWORD_DEFAULT, ['cost' => HASH_COST]);
        $pdo->exec("INSERT INTO `users` (`name`, `email`, `password`, `is_admin`, `registered_at`) 
                   VALUES ('مدیر سایت', 'admin@example.com', '$admin_password', 1, NOW())");
        echo "<p>کاربر ادمین با موفقیت ایجاد شد. (ایمیل: admin@example.com، رمز عبور: admin123)</p>";
    } else {
        echo "<p>کاربر ادمین از قبل وجود دارد.</p>";
    }
    
    // بررسی وجود خدمات
    $stmt = $pdo->query("SELECT COUNT(*) FROM `services`");
    $services_count = $stmt->fetchColumn();
    
    if ($services_count == 0) {
        // درج خدمات پیش‌فرض
        $pdo->exec("INSERT INTO `services` (`title`, `description`, `icon`) VALUES
        ('طراحی وب', 'طراحی سفارشی و واکنش‌گرای وب‌سایت که در تمامی دستگاه‌ها به خوبی نمایش داده می‌شود.', 'fa-desktop'),
        ('توسعه وب', 'توسعه کامل وب با استفاده از فناوری‌های مدرن و فریم‌ورک‌های به‌روز.', 'fa-code'),
        ('طراحی UI/UX', 'طراحی رابط کاربری و تجربه کاربری با تمرکز بر کاربردپذیری و تبدیل.', 'fa-paint-brush'),
        ('اپلیکیشن موبایل', 'توسعه اپلیکیشن‌های موبایل بومی و چندسکویی.', 'fa-mobile-alt'),
        ('راه‌حل‌های فروشگاهی', 'راه‌اندازی فروشگاه آنلاین با پردازش امن پرداخت.', 'fa-shopping-cart'),
        ('بازاریابی دیجیتال', 'بهینه‌سازی موتورهای جستجو، شبکه‌های اجتماعی و بازاریابی محتوا برای رشد حضور آنلاین شما.', 'fa-chart-line')");
        echo "<p>خدمات پیش‌فرض با موفقیت اضافه شدند.</p>";
    } else {
        echo "<p>خدمات از قبل وجود دارند.</p>";
    }
    
    // بررسی وجود نمونه کارها
    $stmt = $pdo->query("SELECT COUNT(*) FROM `portfolio`");
    $portfolio_count = $stmt->fetchColumn();
    
    if ($portfolio_count == 0) {
        // درج نمونه کارهای پیش‌فرض
        $pdo->exec("INSERT INTO `portfolio` (`title`, `description`, `category`, `image_url`) VALUES
        ('وب‌سایت شرکتی', 'یک وب‌سایت مدرن برای یک شرکت خدمات مالی', 'طراحی وب', 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'),
        ('پلتفرم فروشگاهی', 'یک فروشگاه آنلاین کاملاً واکنش‌گرا با قابلیت پرداخت آنلاین', 'فروشگاه آنلاین', 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'),
        ('رابط کاربری اپلیکیشن موبایل', 'طراحی رابط کاربری برای یک اپلیکیشن پایش تناسب اندام', 'طراحی UI/UX', 'https://images.unsplash.com/photo-1551650975-87deedd944c3?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'),
        ('وب‌سایت رستوران', 'یک وب‌سایت شیک با سیستم رزرو آنلاین', 'طراحی وب', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'),
        ('وبلاگ سفر', 'یک وبلاگ با محوریت محتوا و یکپارچه‌سازی چندرسانه‌ای', 'توسعه وب', 'https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'),
        ('نمونه کار عکاسی', 'یک وب‌سایت مینیمالیستی برای یک عکاس حرفه‌ای', 'طراحی وب', 'https://images.unsplash.com/photo-1452587925148-ce544e77e70d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80')");
        echo "<p>نمونه کارهای پیش‌فرض با موفقیت اضافه شدند.</p>";
    } else {
        echo "<p>نمونه کارها از قبل وجود دارند.</p>";
    }
    
    // بررسی وجود مقالات وبلاگ
    $user_id = $pdo->query("SELECT `id` FROM `users` WHERE `is_admin` = 1 LIMIT 1")->fetchColumn();
    
    $stmt = $pdo->query("SELECT COUNT(*) FROM `blog_posts`");
    $blog_posts_count = $stmt->fetchColumn();
    
    if ($blog_posts_count == 0 && $user_id) {
        // درج مقالات وبلاگ پیش‌فرض
        $pdo->exec("INSERT INTO `blog_posts` (`title`, `slug`, `content`, `summary`, `created_at`, `updated_at`, `user_id`) VALUES
        ('۱۰ روند طراحی وب برای سال ۱۴۰۳', 'web-design-trends-2023', '<p>دنیای طراحی وب دائماً در حال تکامل است. اینها ۱۰ روند برتری هستند که در سال ۱۴۰۳ می‌بینیم:</p><h3>۱. حالت تاریک</h3><p>حالت تاریک به‌طور فزاینده‌ای محبوب شده است و به کاربران جایگزینی جذاب ارائه می‌دهد که فشار چشم را کاهش می‌دهد و عمر باتری را در صفحه‌نمایش‌های OLED ذخیره می‌کند.</p><h3>۲. طراحی مینیمالیستی</h3><p>کمتر همچنان بیشتر است. رویکردهای مینیمالیستی بر عناصر ضروری تمرکز دارند و از فضای منفی به‌طور مؤثر استفاده می‌کنند تا رابط‌های تمیز و بدون شلوغی ایجاد کنند.</p>', 'روندهای جدید طراحی وب که سال ۱۴۰۳ را شکل می‌دهند، از حالت تاریک تا یکپارچه‌سازی واقعیت افزوده را کشف کنید.', NOW(), NOW(), $user_id),
        ('چرا طراحی واکنش‌گرا مهم‌تر از همیشه است', 'responsive-design-importance', '<p>در دنیای امروز با چندین دستگاه، طراحی واکنش‌گرا فقط یک ویژگی جذاب نیست - ضروری است. دلایل آن در ادامه آمده است:</p><h3>ترافیک موبایل غالب است</h3><p>بیش از ۵۰٪ ترافیک جهانی وب اکنون از دستگاه‌های موبایل می‌آید. اگر سایت شما در تلفن‌های هوشمند و تبلت‌ها عملکرد خوبی نداشته باشد، احتمالاً نیمی از مخاطبان خود را از دست می‌دهید.</p>', 'با تسلط ترافیک موبایل بر وب، طراحی واکنش‌گرا برای سئو، تجربه کاربری و موفقیت کسب‌وکار ضروری شده است.', NOW(), NOW(), $user_id),
        ('۵ اصل UX ضروری که هر طراح باید رعایت کند', 'essential-ux-principles', '<p>طراحی تجربه کاربری (UX) بر ایجاد تجارب معنادار و مرتبط برای کاربران تمرکز دارد. این پنج اصل اساسی به هدایت هر پروژه طراحی UX کمک می‌کنند:</p><h3>۱. طراحی کاربرمحور</h3><p>همیشه با تحقیقات کاربر شروع کنید. نیازها، رفتارها و نقاط درد کاربران شما باید تصمیمات طراحی را هدایت کند، نه ترجیحات زیبایی‌شناختی یا فرضیات.</p>', 'اصول اساسی UX را بیاموزید که می‌توانند محصولات دیجیتال شما را متحول کنند.', NOW(), NOW(), $user_id)");
        echo "<p>مقالات وبلاگ پیش‌فرض با موفقیت اضافه شدند.</p>";
    } else {
        echo "<p>مقالات وبلاگ از قبل وجود دارند یا کاربر ادمین یافت نشد.</p>";
    }
    
    echo "<p style='color: green; font-weight: bold;'>راه‌اندازی پایگاه داده با موفقیت انجام شد!</p>";
    echo "<p><a href='index.php'>بازگشت به صفحه اصلی</a></p>";
    
} catch(PDOException $e) {
    echo "<p style='color: red;'>خطا در راه‌اندازی پایگاه داده: " . $e->getMessage() . "</p>";
    exit;
}
?>