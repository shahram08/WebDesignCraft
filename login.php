<?php
// بارگذاری تنظیمات و توابع مورد نیاز
require_once 'includes/config.php';
require_once 'includes/database.php';
require_once 'includes/User.php';

// اگر کاربر قبلاً وارد شده است، به صفحه اصلی هدایت می‌شود
if(is_logged_in()) {
    redirect(url());
}

// متغیرهای خطا و اعلان
$errors = [];
$email = '';

// بررسی ارسال فرم
if($_SERVER['REQUEST_METHOD'] == 'POST') {
    // دریافت و تمیز کردن داده‌های ورودی
    $email = clean_input($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    
    // اعتبارسنجی داده‌های ورودی
    if(empty($email)) {
        $errors[] = 'لطفا آدرس ایمیل خود را وارد کنید.';
    } elseif(!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'لطفا یک آدرس ایمیل معتبر وارد کنید.';
    }
    
    if(empty($password)) {
        $errors[] = 'لطفا رمز عبور خود را وارد کنید.';
    }
    
    // اگر خطایی وجود نداشت، تلاش برای ورود
    if(empty($errors)) {
        $user = new User();
        $result = $user->login($email, $password);
        
        if($result['success']) {
            // تنظیم پیام موفقیت
            set_flash_message('success', 'خوش آمدید ' . $_SESSION['user_name'] . '!');
            
            // هدایت به صفحه مناسب
            if(is_admin()) {
                redirect(url('admin/'));
            } else {
                redirect(url('dashboard/'));
            }
        } else {
            $errors[] = $result['message'];
        }
    }
}

// بررسی وجود پیام فلش
$flash = get_flash_message();
?>
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ورود به سایت - <?php echo SITE_TITLE; ?></title>
    
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
                        <a class="nav-link" href="<?php echo url(); ?>">صفحه اصلی</a>
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
                    <a href="<?php echo url('login.php'); ?>" class="btn btn-outline-light me-2 active">ورود</a>
                    <a href="<?php echo url('register.php'); ?>" class="btn btn-primary">ثبت‌نام</a>
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

    <!-- بخش اصلی - فرم ورود -->
    <section class="py-5 mt-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body p-5">
                            <h1 class="card-title text-center mb-4">ورود به حساب کاربری</h1>
                            
                            <?php if (!empty($errors)): ?>
                            <div class="alert alert-danger" role="alert">
                                <ul class="mb-0">
                                    <?php foreach ($errors as $error): ?>
                                    <li><?php echo $error; ?></li>
                                    <?php endforeach; ?>
                                </ul>
                            </div>
                            <?php endif; ?>
                            
                            <form id="loginForm" method="POST" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" class="needs-validation" novalidate>
                                <div class="mb-3">
                                    <label for="email" class="form-label">آدرس ایمیل</label>
                                    <input type="email" class="form-control" id="email" name="email" value="<?php echo $email; ?>" required>
                                    <div class="invalid-feedback">
                                        لطفا یک آدرس ایمیل معتبر وارد کنید.
                                    </div>
                                </div>
                                <div class="mb-4">
                                    <label for="password" class="form-label">رمز عبور</label>
                                    <input type="password" class="form-control" id="password" name="password" required>
                                    <div class="invalid-feedback">
                                        لطفا رمز عبور خود را وارد کنید.
                                    </div>
                                </div>
                                <div class="d-grid gap-2">
                                    <button type="submit" class="btn btn-primary btn-lg">ورود</button>
                                </div>
                            </form>
                            
                            <div class="text-center mt-4">
                                <p>حساب کاربری ندارید؟ <a href="<?php echo url('register.php'); ?>">ثبت‌نام کنید</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- فوتر -->
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6 mb-3 mb-md-0">
                    <p class="mb-0">&copy; ۱۴۰۳ استودیو طراحی وب. تمامی حقوق محفوظ است.</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p class="mb-0">
                        <a href="#" class="text-decoration-none me-3">سیاست حریم خصوصی</a>
                        <a href="#" class="text-decoration-none">شرایط استفاده از خدمات</a>
                    </p>
                </div>
            </div>
        </div>
    </footer>

    <!-- جاوااسکریپت بوت‌استرپ -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- جاوااسکریپت سفارشی -->
    <script src="public/assets/js/form-validation.js"></script>
</body>
</html>