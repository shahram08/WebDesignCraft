<?php
// بارگذاری تنظیمات و توابع مورد نیاز
require_once 'includes/config.php';
require_once 'includes/database.php';
require_once 'includes/User.php';

// بررسی وجود پیام فلش
$flash = get_flash_message();
?>
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo SITE_TITLE; ?> - استودیو طراحی وب</title>
    
    <!-- بوت‌استرپ نسخه RTL -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
    
    <!-- فونت‌آیکون -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- فونت وزیر برای متون فارسی -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css">
    
    <!-- استایل سفارشی -->
    <link rel="stylesheet" href="public/assets/css/custom.css">
</head>
<body>
    <!-- منوی ناوبری -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="<?php echo url(); ?>">
                <i class="fas fa-code me-2"></i>استودیو طراحی وب
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="<?php echo url(); ?>">صفحه اصلی</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="<?php echo url('about.php'); ?>">درباره ما</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="<?php echo url('services.php'); ?>">خدمات</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="<?php echo url('portfolio.php'); ?>">نمونه کارها</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="<?php echo url('blog.php'); ?>">وبلاگ</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="<?php echo url('contact.php'); ?>">تماس با ما</a>
                    </li>
                </ul>
                <div class="d-flex">
                    <?php if (is_logged_in()): ?>
                        <?php if (is_admin()): ?>
                        <a href="<?php echo url('admin/'); ?>" class="btn btn-outline-light me-2">پنل مدیریت</a>
                        <?php else: ?>
                        <a href="<?php echo url('dashboard/'); ?>" class="btn btn-outline-light me-2">پنل کاربری</a>
                        <?php endif; ?>
                        <a href="<?php echo url('logout.php'); ?>" class="btn btn-danger">خروج</a>
                    <?php else: ?>
                        <a href="<?php echo url('login.php'); ?>" class="btn btn-outline-light me-2">ورود</a>
                        <a href="<?php echo url('register.php'); ?>" class="btn btn-primary">ثبت‌نام</a>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </nav>

    <!-- نمایش پیام‌های فلش -->
    <?php if ($flash): ?>
    <div class="container mt-5 pt-4">
        <div class="alert alert-<?php echo $flash['type']; ?> alert-dismissible fade show" role="alert">
            <?php echo $flash['message']; ?>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </div>
    <?php endif; ?>

    <!-- بخش قهرمان (Hero) -->
    <header class="hero-section py-5 mt-5">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6 mb-5 mb-lg-0">
                    <h1 class="display-4 fw-bold mb-4">طراحی وب حرفه‌ای برای کسب‌وکار شما</h1>
                    <p class="lead mb-4">ما وب‌سایت‌های سفارشی، واکنش‌گرا و بهینه‌شده برای موتورهای جستجو طراحی می‌کنیم که به رشد کسب‌وکار شما کمک می‌کند.</p>
                    <div class="d-grid gap-2 d-md-flex">
                        <a href="<?php echo url('contact.php'); ?>" class="btn btn-primary btn-lg px-4 me-md-2">درخواست مشاوره رایگان</a>
                        <a href="<?php echo url('portfolio.php'); ?>" class="btn btn-outline-dark btn-lg px-4">مشاهده نمونه کارها</a>
                    </div>
                </div>
                <div class="col-lg-6">
                    <img src="https://images.unsplash.com/photo-1600132806370-bf17e65e942f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80" class="img-fluid rounded shadow-lg" alt="طراحی وب">
                </div>
            </div>
        </div>
    </header>

    <!-- بخش خدمات -->
    <section class="services-section py-5 bg-light">
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="section-title">خدمات ما</h2>
                <p class="section-description">ما طیف گسترده‌ای از خدمات طراحی و توسعه وب ارائه می‌دهیم</p>
            </div>
            
            <div class="row g-4">
                <?php
                // دریافت خدمات از دیتابیس
                try {
                    $db = get_db_connection();
                    $stmt = $db->query("SELECT * FROM services LIMIT 6");
                    $services = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    
                    foreach ($services as $service) {
                        echo '<div class="col-md-6 col-lg-4">';
                        echo '<div class="card h-100 border-0 shadow-sm">';
                        echo '<div class="card-body p-4 text-center">';
                        echo '<div class="service-icon mb-3"><i class="fas ' . $service['icon'] . ' fa-3x text-primary"></i></div>';
                        echo '<h3 class="card-title">' . $service['title'] . '</h3>';
                        echo '<p class="card-text">' . $service['description'] . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                    }
                } catch (PDOException $e) {
                    // نمایش خدمات پیش‌فرض در صورت خطا
                    $default_services = [
                        ['title' => 'طراحی وب', 'description' => 'طراحی سفارشی و واکنش‌گرای وب‌سایت که در تمامی دستگاه‌ها به خوبی نمایش داده می‌شود.', 'icon' => 'fa-desktop'],
                        ['title' => 'توسعه وب', 'description' => 'توسعه کامل وب با استفاده از فناوری‌های مدرن و فریم‌ورک‌های به‌روز.', 'icon' => 'fa-code'],
                        ['title' => 'طراحی UI/UX', 'description' => 'طراحی رابط کاربری و تجربه کاربری با تمرکز بر کاربردپذیری و تبدیل.', 'icon' => 'fa-paint-brush'],
                        ['title' => 'اپلیکیشن موبایل', 'description' => 'توسعه اپلیکیشن‌های موبایل بومی و چندسکویی.', 'icon' => 'fa-mobile-alt'],
                        ['title' => 'راه‌حل‌های فروشگاهی', 'description' => 'راه‌اندازی فروشگاه آنلاین با پردازش امن پرداخت.', 'icon' => 'fa-shopping-cart'],
                        ['title' => 'بازاریابی دیجیتال', 'description' => 'بهینه‌سازی موتورهای جستجو، شبکه‌های اجتماعی و بازاریابی محتوا برای رشد حضور آنلاین شما.', 'icon' => 'fa-chart-line']
                    ];
                    
                    foreach ($default_services as $service) {
                        echo '<div class="col-md-6 col-lg-4">';
                        echo '<div class="card h-100 border-0 shadow-sm">';
                        echo '<div class="card-body p-4 text-center">';
                        echo '<div class="service-icon mb-3"><i class="fas ' . $service['icon'] . ' fa-3x text-primary"></i></div>';
                        echo '<h3 class="card-title">' . $service['title'] . '</h3>';
                        echo '<p class="card-text">' . $service['description'] . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                    }
                }
                ?>
            </div>
            
            <div class="text-center mt-4">
                <a href="<?php echo url('services.php'); ?>" class="btn btn-outline-primary">مشاهده همه خدمات</a>
            </div>
        </div>
    </section>

    <!-- بخش درباره ما -->
    <section class="about-section py-5">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6 mb-4 mb-lg-0">
                    <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80" class="img-fluid rounded shadow-lg" alt="تیم طراحی وب">
                </div>
                <div class="col-lg-6 ps-lg-5">
                    <h2 class="section-title mb-4">درباره ما</h2>
                    <p class="mb-4">استودیو طراحی وب ما یک شرکت طراحی دیجیتال خلاق است که در زمینه طراحی وب، توسعه اپلیکیشن و بازاریابی دیجیتال تخصص دارد. تیم ما متشکل از طراحان، توسعه‌دهندگان و متخصصان بازاریابی با تجربه است که برای ارائه راه‌حل‌های دیجیتال با کیفیت بالا به مشتریان خود متعهد هستند.</p>
                    
                    <div class="row g-4 mb-4">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center">
                                <div class="icon-box me-3 text-primary">
                                    <i class="fas fa-check-circle fa-2x"></i>
                                </div>
                                <div>
                                    <h4 class="mb-1">طراحی واکنش‌گرا</h4>
                                    <p class="mb-0">سازگار با تمامی دستگاه‌ها</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="d-flex align-items-center">
                                <div class="icon-box me-3 text-primary">
                                    <i class="fas fa-check-circle fa-2x"></i>
                                </div>
                                <div>
                                    <h4 class="mb-1">بهینه برای سئو</h4>
                                    <p class="mb-0">افزایش رتبه در گوگل</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <a href="<?php echo url('about.php'); ?>" class="btn btn-primary">بیشتر بدانید</a>
                </div>
            </div>
        </div>
    </section>

    <!-- بخش نمونه کارها -->
    <section class="portfolio-section py-5 bg-light">
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="section-title">نمونه کارهای اخیر</h2>
                <p class="section-description">برخی از پروژه‌های اخیر ما که با افتخار به مشتریان خود ارائه داده‌ایم</p>
            </div>
            
            <div class="row g-4">
                <?php
                // دریافت نمونه کارها از دیتابیس
                try {
                    $db = get_db_connection();
                    $stmt = $db->query("SELECT * FROM portfolio LIMIT 6");
                    $portfolio_items = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    
                    foreach ($portfolio_items as $item) {
                        echo '<div class="col-md-6 col-lg-4">';
                        echo '<div class="card portfolio-item border-0 shadow-sm h-100">';
                        echo '<img src="' . $item['image_url'] . '" class="card-img-top" alt="' . $item['title'] . '">';
                        echo '<div class="card-body">';
                        echo '<h4 class="card-title">' . $item['title'] . '</h4>';
                        echo '<p class="card-text">' . $item['description'] . '</p>';
                        echo '<span class="badge bg-primary">' . $item['category'] . '</span>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                    }
                } catch (PDOException $e) {
                    // اگر دیتابیس در دسترس نبود، نمونه کارهای پیش فرض نمایش داده می‌شوند
                    echo '<div class="col-12 text-center">';
                    echo '<p>لطفاً ابتدا <a href="setup.php">صفحه راه‌اندازی اولیه</a> را اجرا کنید.</p>';
                    echo '</div>';
                }
                ?>
            </div>
            
            <div class="text-center mt-4">
                <a href="<?php echo url('portfolio.php'); ?>" class="btn btn-outline-primary">مشاهده همه نمونه کارها</a>
            </div>
        </div>
    </section>

    <!-- بخش مشتریان -->
    <section class="clients-section py-5">
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="section-title">مشتریان ما</h2>
                <p class="section-description">برخی از شرکت‌ها و سازمان‌هایی که افتخار همکاری با آنها را داشته‌ایم</p>
            </div>
            
            <div class="row row-cols-2 row-cols-md-4 row-cols-lg-6 g-4 justify-content-center">
                <div class="col text-center">
                    <div class="client-logo py-4 px-3 bg-light rounded shadow-sm">
                        <img src="public/assets/img/client-1.svg" alt="لوگوی مشتری 1" class="img-fluid" onerror="this.src='https://via.placeholder.com/150x80?text=Logo+1'">
                    </div>
                </div>
                <div class="col text-center">
                    <div class="client-logo py-4 px-3 bg-light rounded shadow-sm">
                        <img src="public/assets/img/client-2.svg" alt="لوگوی مشتری 2" class="img-fluid" onerror="this.src='https://via.placeholder.com/150x80?text=Logo+2'">
                    </div>
                </div>
                <div class="col text-center">
                    <div class="client-logo py-4 px-3 bg-light rounded shadow-sm">
                        <img src="public/assets/img/client-3.svg" alt="لوگوی مشتری 3" class="img-fluid" onerror="this.src='https://via.placeholder.com/150x80?text=Logo+3'">
                    </div>
                </div>
                <div class="col text-center">
                    <div class="client-logo py-4 px-3 bg-light rounded shadow-sm">
                        <img src="public/assets/img/client-4.svg" alt="لوگوی مشتری 4" class="img-fluid" onerror="this.src='https://via.placeholder.com/150x80?text=Logo+4'">
                    </div>
                </div>
                <div class="col text-center">
                    <div class="client-logo py-4 px-3 bg-light rounded shadow-sm">
                        <img src="public/assets/img/client-5.svg" alt="لوگوی مشتری 5" class="img-fluid" onerror="this.src='https://via.placeholder.com/150x80?text=Logo+5'">
                    </div>
                </div>
                <div class="col text-center">
                    <div class="client-logo py-4 px-3 bg-light rounded shadow-sm">
                        <img src="public/assets/img/client-6.svg" alt="لوگوی مشتری 6" class="img-fluid" onerror="this.src='https://via.placeholder.com/150x80?text=Logo+6'">
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- بخش تماس با ما -->
    <section class="contact-section py-5 bg-light">
        <div class="container">
            <div class="row">
                <div class="col-lg-5 mb-4 mb-lg-0">
                    <h2 class="section-title mb-4">با ما در ارتباط باشید</h2>
                    <p class="mb-4">برای کسب اطلاعات بیشتر درباره خدمات ما یا درخواست مشاوره رایگان با ما تماس بگیرید.</p>
                    
                    <div class="contact-info mb-4">
                        <div class="mb-3 d-flex align-items-center">
                            <div class="icon-box me-3 text-primary">
                                <i class="fas fa-map-marker-alt fa-2x"></i>
                            </div>
                            <div>
                                <h5 class="mb-1">آدرس</h5>
                                <p class="mb-0">تهران، خیابان ولیعصر، کوچه نیلوفر، پلاک ۴۵</p>
                            </div>
                        </div>
                        <div class="mb-3 d-flex align-items-center">
                            <div class="icon-box me-3 text-primary">
                                <i class="fas fa-phone-alt fa-2x"></i>
                            </div>
                            <div>
                                <h5 class="mb-1">تلفن</h5>
                                <p class="mb-0">۰۲۱-۸۸۷۷۶۶۵۵</p>
                            </div>
                        </div>
                        <div class="d-flex align-items-center">
                            <div class="icon-box me-3 text-primary">
                                <i class="fas fa-envelope fa-2x"></i>
                            </div>
                            <div>
                                <h5 class="mb-1">ایمیل</h5>
                                <p class="mb-0">info@webstudio.com</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="social-links">
                        <a href="#" class="btn btn-outline-dark me-2"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="btn btn-outline-dark me-2"><i class="fab fa-telegram"></i></a>
                        <a href="#" class="btn btn-outline-dark me-2"><i class="fab fa-linkedin"></i></a>
                        <a href="#" class="btn btn-outline-dark"><i class="fab fa-twitter"></i></a>
                    </div>
                </div>
                <div class="col-lg-7">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body p-4">
                            <h3 class="card-title mb-4">ارسال پیام</h3>
                            <form action="<?php echo url('contact-process.php'); ?>" method="POST" class="contact-form needs-validation" novalidate>
                                <div class="mb-3">
                                    <label for="name" class="form-label">نام و نام خانوادگی</label>
                                    <input type="text" class="form-control" id="name" name="name" required>
                                    <div class="invalid-feedback">
                                        لطفا نام خود را وارد کنید.
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label for="email" class="form-label">آدرس ایمیل</label>
                                    <input type="email" class="form-control" id="email" name="email" required>
                                    <div class="invalid-feedback">
                                        لطفا یک آدرس ایمیل معتبر وارد کنید.
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label for="subject" class="form-label">موضوع</label>
                                    <input type="text" class="form-control" id="subject" name="subject" required>
                                    <div class="invalid-feedback">
                                        لطفا موضوع پیام خود را وارد کنید.
                                    </div>
                                </div>
                                <div class="mb-4">
                                    <label for="message" class="form-label">پیام</label>
                                    <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
                                    <div class="invalid-feedback">
                                        لطفا پیام خود را وارد کنید.
                                    </div>
                                </div>
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary">ارسال پیام</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- فوتر -->
    <footer class="bg-dark text-light py-5">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-4">
                    <h3 class="mb-4">استودیو طراحی وب</h3>
                    <p>ما یک استودیوی طراحی وب خلاق هستیم که به ارائه راه‌حل‌های دیجیتال سفارشی برای کسب‌وکارها متعهد است.</p>
                    <div class="social-links mt-4">
                        <a href="#" class="text-light me-3"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="text-light me-3"><i class="fab fa-telegram"></i></a>
                        <a href="#" class="text-light me-3"><i class="fab fa-linkedin"></i></a>
                        <a href="#" class="text-light"><i class="fab fa-twitter"></i></a>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4">
                    <h5 class="mb-4">پیوندهای سریع</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2"><a href="<?php echo url(); ?>" class="text-light text-decoration-none">صفحه اصلی</a></li>
                        <li class="mb-2"><a href="<?php echo url('about.php'); ?>" class="text-light text-decoration-none">درباره ما</a></li>
                        <li class="mb-2"><a href="<?php echo url('services.php'); ?>" class="text-light text-decoration-none">خدمات</a></li>
                        <li class="mb-2"><a href="<?php echo url('portfolio.php'); ?>" class="text-light text-decoration-none">نمونه کارها</a></li>
                        <li class="mb-2"><a href="<?php echo url('blog.php'); ?>" class="text-light text-decoration-none">وبلاگ</a></li>
                        <li><a href="<?php echo url('contact.php'); ?>" class="text-light text-decoration-none">تماس با ما</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-4">
                    <h5 class="mb-4">خدمات</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2"><a href="#" class="text-light text-decoration-none">طراحی وب</a></li>
                        <li class="mb-2"><a href="#" class="text-light text-decoration-none">توسعه وب</a></li>
                        <li class="mb-2"><a href="#" class="text-light text-decoration-none">طراحی UI/UX</a></li>
                        <li class="mb-2"><a href="#" class="text-light text-decoration-none">اپلیکیشن موبایل</a></li>
                        <li class="mb-2"><a href="#" class="text-light text-decoration-none">راه‌حل‌های فروشگاهی</a></li>
                        <li><a href="#" class="text-light text-decoration-none">بازاریابی دیجیتال</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-4">
                    <h5 class="mb-4">تماس با ما</h5>
                    <div class="mb-3">
                        <p class="mb-1"><i class="fas fa-map-marker-alt me-2"></i> تهران، خیابان ولیعصر، کوچه نیلوفر، پلاک ۴۵</p>
                    </div>
                    <div class="mb-3">
                        <p class="mb-1"><i class="fas fa-phone-alt me-2"></i> ۰۲۱-۸۸۷۷۶۶۵۵</p>
                    </div>
                    <div>
                        <p class="mb-1"><i class="fas fa-envelope me-2"></i> info@webstudio.com</p>
                    </div>
                </div>
            </div>
            <hr class="my-4 bg-secondary">
            <div class="row">
                <div class="col-md-6">
                    <p class="mb-0">&copy; ۱۴۰۳ استودیو طراحی وب. تمامی حقوق محفوظ است.</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p class="mb-0">
                        <a href="#" class="text-light text-decoration-none me-3">سیاست حریم خصوصی</a>
                        <a href="#" class="text-light text-decoration-none">شرایط استفاده از خدمات</a>
                    </p>
                </div>
            </div>
        </div>
    </footer>

    <!-- جاوااسکریپت بوت‌استرپ -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- جاوااسکریپت سفارشی -->
    <script src="public/assets/js/main.js"></script>
</body>
</html>