-- ایجاد دیتابیس اصلی
-- CREATE DATABASE web_studio_db;
-- \c web_studio_db;

-- جدول کاربران
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_admin BOOLEAN DEFAULT FALSE,
    profile_picture VARCHAR(200),
    bio TEXT,
    phone VARCHAR(20),
    last_login TIMESTAMP WITHOUT TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_user_username ON "user" (username);
CREATE INDEX idx_user_email ON "user" (email);

-- جدول تگ‌ها
CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE
);

-- جدول دسته‌بندی‌ها
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- جدول پست‌های وبلاگ
CREATE TABLE blog_post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    published BOOLEAN DEFAULT TRUE,
    featured_image VARCHAR(200),
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES category(id) ON DELETE SET NULL
);

CREATE INDEX idx_blog_post_slug ON blog_post (slug);
CREATE INDEX idx_blog_post_user_id ON blog_post (user_id);
CREATE INDEX idx_blog_post_category_id ON blog_post (category_id);

-- جدول ارتباطی پست و تگ
CREATE TABLE post_tag (
    post_id INTEGER NOT NULL REFERENCES blog_post(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- جدول نظرات
CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    approved BOOLEAN DEFAULT FALSE,
    post_id INTEGER NOT NULL REFERENCES blog_post(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES comment(id) ON DELETE CASCADE
);

CREATE INDEX idx_comment_post_id ON comment (post_id);
CREATE INDEX idx_comment_user_id ON comment (user_id);
CREATE INDEX idx_comment_parent_id ON comment (parent_id);

-- جدول لایک‌ها
CREATE TABLE "like" (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    post_id INTEGER NOT NULL REFERENCES blog_post(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    UNIQUE (post_id, user_id)
);

CREATE INDEX idx_like_post_id ON "like" (post_id);
CREATE INDEX idx_like_user_id ON "like" (user_id);

-- جدول بازدیدها
CREATE TABLE post_visit (
    id SERIAL PRIMARY KEY,
    visit_date TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    ip_address VARCHAR(45),
    user_agent VARCHAR(200),
    post_id INTEGER NOT NULL REFERENCES blog_post(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES "user"(id) ON DELETE SET NULL
);

CREATE INDEX idx_post_visit_post_id ON post_visit (post_id);
CREATE INDEX idx_post_visit_visit_date ON post_visit (visit_date);
CREATE INDEX idx_post_visit_user_id ON post_visit (user_id);

-- جدول انواع فعالیت‌ها
CREATE TABLE activity_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200)
);

-- جدول فعالیت‌های کاربران
CREATE TABLE user_activity (
    id SERIAL PRIMARY KEY,
    description VARCHAR(200) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    ip_address VARCHAR(45),
    data TEXT, -- برای ذخیره داده‌های JSON
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_activity_user_id ON user_activity (user_id);
CREATE INDEX idx_user_activity_created_at ON user_activity (created_at);

-- جدول ارتباطی فعالیت کاربر و نوع فعالیت
CREATE TABLE user_activity_type (
    activity_id INTEGER NOT NULL REFERENCES user_activity(id) ON DELETE CASCADE,
    type_id INTEGER NOT NULL REFERENCES activity_type(id) ON DELETE CASCADE,
    PRIMARY KEY (activity_id, type_id)
);

-- جدول خدمات
CREATE TABLE service (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(50) NOT NULL,
    featured BOOLEAN DEFAULT FALSE,
    "order" INTEGER DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- جدول نمونه کارها
CREATE TABLE portfolio_item (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    image_url VARCHAR(200) NOT NULL,
    project_url VARCHAR(200),
    client_name VARCHAR(100),
    completed_date DATE,
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- جدول ارتباطی نمونه کار و تگ
CREATE TABLE portfolio_tag (
    portfolio_id INTEGER NOT NULL REFERENCES portfolio_item(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
    PRIMARY KEY (portfolio_id, tag_id)
);

-- جدول پیام‌های تماس
CREATE TABLE contact_message (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_read BOOLEAN DEFAULT FALSE,
    reply_sent BOOLEAN DEFAULT FALSE,
    reply_text TEXT,
    reply_date TIMESTAMP WITHOUT TIME ZONE,
    ip_address VARCHAR(45)
);

CREATE INDEX idx_contact_message_created_at ON contact_message (created_at);
CREATE INDEX idx_contact_message_is_read ON contact_message (is_read);

-- جدول تنظیمات سایت
CREATE TABLE site_settings (
    id SERIAL PRIMARY KEY,
    site_name VARCHAR(100) NOT NULL,
    site_description TEXT,
    site_logo VARCHAR(200),
    contact_email VARCHAR(120),
    contact_phone VARCHAR(20),
    contact_address TEXT,
    social_facebook VARCHAR(200),
    social_twitter VARCHAR(200),
    social_instagram VARCHAR(200),
    social_linkedin VARCHAR(200),
    footer_text TEXT,
    analytics_code TEXT,
    maintenance_mode BOOLEAN DEFAULT FALSE
);

-- جدول آمار
CREATE TABLE statistics (
    id SERIAL PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE UNIQUE,
    visits INTEGER DEFAULT 0,
    unique_visitors INTEGER DEFAULT 0,
    page_views INTEGER DEFAULT 0,
    most_visited_page VARCHAR(200),
    most_visited_post_id INTEGER REFERENCES blog_post(id) ON DELETE SET NULL,
    data TEXT -- برای ذخیره داده‌های JSON
);

CREATE INDEX idx_statistics_date ON statistics (date);

-- بخش ایجاد ویوها برای گزارش‌گیری بهتر

-- ویو بازدیدهای روزانه
CREATE VIEW daily_visits_view AS
SELECT 
    CAST(visit_date AS DATE) AS visit_day,
    COUNT(*) AS total_visits,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(DISTINCT ip_address) AS unique_ips
FROM 
    post_visit
GROUP BY 
    CAST(visit_date AS DATE)
ORDER BY 
    visit_day DESC;

-- ویو محبوب‌ترین پست‌ها
CREATE VIEW popular_posts_view AS
SELECT 
    bp.id,
    bp.title,
    bp.slug,
    bp.views_count,
    bp.likes_count,
    bp.comments_count,
    u.username AS author_name,
    c.name AS category_name,
    COUNT(pv.id) AS recent_visits
FROM 
    blog_post bp
LEFT JOIN 
    "user" u ON bp.user_id = u.id
LEFT JOIN 
    category c ON bp.category_id = c.id
LEFT JOIN 
    post_visit pv ON bp.id = pv.post_id AND pv.visit_date > NOW() - INTERVAL '30 days'
GROUP BY 
    bp.id, u.username, c.name
ORDER BY 
    recent_visits DESC, bp.views_count DESC;

-- ویو فعالیت‌های اخیر کاربران
CREATE VIEW recent_user_activities_view AS
SELECT 
    ua.id,
    ua.description,
    ua.created_at,
    ua.ip_address,
    u.username,
    u.email,
    string_agg(at.name, ', ') AS activity_types
FROM 
    user_activity ua
JOIN 
    "user" u ON ua.user_id = u.id
LEFT JOIN 
    user_activity_type uat ON ua.id = uat.activity_id
LEFT JOIN 
    activity_type at ON uat.type_id = at.id
GROUP BY 
    ua.id, u.username, u.email
ORDER BY 
    ua.created_at DESC;

-- ویو آمار کلی سایت
CREATE VIEW site_statistics_view AS
SELECT 
    (SELECT COUNT(*) FROM "user") AS total_users,
    (SELECT COUNT(*) FROM blog_post) AS total_posts,
    (SELECT COUNT(*) FROM comment) AS total_comments,
    (SELECT COUNT(*) FROM "like") AS total_likes,
    (SELECT COUNT(*) FROM post_visit) AS total_visits,
    (SELECT COUNT(*) FROM contact_message) AS total_messages,
    (SELECT COUNT(*) FROM portfolio_item) AS total_portfolio_items,
    (SELECT COUNT(*) FROM service) AS total_services,
    (SELECT COUNT(*) FROM tag) AS total_tags,
    (SELECT COUNT(*) FROM category) AS total_categories;

-- ویو خلاصه وضعیت پیام‌های تماس
CREATE VIEW contact_messages_summary_view AS
SELECT 
    COUNT(*) AS total_messages,
    COUNT(CASE WHEN is_read = FALSE THEN 1 END) AS unread_messages,
    COUNT(CASE WHEN reply_sent = TRUE THEN 1 END) AS replied_messages,
    MAX(created_at) AS latest_message_date
FROM 
    contact_message;

-- ویو برای نمایش کامنت‌های منتظر تایید
CREATE VIEW pending_comments_view AS
SELECT 
    c.id,
    c.content,
    c.created_at,
    u.username AS author_name,
    bp.title AS post_title,
    bp.slug AS post_slug
FROM 
    comment c
JOIN 
    "user" u ON c.user_id = u.id
JOIN 
    blog_post bp ON c.post_id = bp.id
WHERE 
    c.approved = FALSE
ORDER BY 
    c.created_at DESC;

-- داده‌های اولیه برای انواع فعالیت
INSERT INTO activity_type (name, description) VALUES
('ورود', 'ورود کاربر به سیستم'),
('ثبت نام', 'ثبت نام کاربر جدید'),
('ارسال نظر', 'ارسال نظر برای پست'),
('ارسال پیام', 'ارسال پیام از طریق فرم تماس'),
('لایک', 'لایک کردن پست'),
('ویرایش پروفایل', 'ویرایش اطلاعات پروفایل');

-- تنظیمات پیش‌فرض سایت
INSERT INTO site_settings (
    site_name, 
    site_description, 
    contact_email, 
    contact_phone, 
    contact_address, 
    footer_text
) VALUES (
    'استودیو طراحی وب مدرن',
    'طراحی و توسعه وب‌سایت‌های مدرن و واکنش‌گرا',
    'info@webstudio.com',
    '+98123456789',
    'تهران، خیابان ولیعصر',
    'تمامی حقوق برای استودیو طراحی وب مدرن محفوظ است.'
);

-- ایجاد فانکشن برای به‌روزرسانی تاریخ آپدیت
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- تریگرها برای به‌روزرسانی خودکار فیلد updated_at
CREATE TRIGGER update_user_updated_at
    BEFORE UPDATE ON "user"
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_blog_post_updated_at
    BEFORE UPDATE ON blog_post
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_service_updated_at
    BEFORE UPDATE ON service
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_portfolio_item_updated_at
    BEFORE UPDATE ON portfolio_item
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- فانکشن برای به‌روزرسانی شمارنده‌های پست
CREATE OR REPLACE FUNCTION update_post_comment_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE blog_post SET comments_count = comments_count + 1 WHERE id = NEW.post_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE blog_post SET comments_count = comments_count - 1 WHERE id = OLD.post_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_comment_change
    AFTER INSERT OR DELETE ON comment
    FOR EACH ROW
    EXECUTE FUNCTION update_post_comment_count();

-- فانکشن برای به‌روزرسانی شمارنده لایک‌ها
CREATE OR REPLACE FUNCTION update_post_like_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE blog_post SET likes_count = likes_count + 1 WHERE id = NEW.post_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE blog_post SET likes_count = likes_count - 1 WHERE id = OLD.post_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_like_change
    AFTER INSERT OR DELETE ON "like"
    FOR EACH ROW
    EXECUTE FUNCTION update_post_like_count();

-- فانکشن برای به‌روزرسانی شمارنده بازدیدها
CREATE OR REPLACE FUNCTION update_post_view_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE blog_post SET views_count = views_count + 1 WHERE id = NEW.post_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_visit_insert
    AFTER INSERT ON post_visit
    FOR EACH ROW
    EXECUTE FUNCTION update_post_view_count();

-- فانکشن برای ثبت فعالیت‌های کاربر
CREATE OR REPLACE FUNCTION log_user_activity(
    user_id INTEGER,
    activity_description TEXT,
    activity_type_name TEXT,
    ip_address TEXT DEFAULT NULL,
    activity_data TEXT DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    activity_id INTEGER;
    type_id INTEGER;
BEGIN
    -- ایجاد فعالیت جدید
    INSERT INTO user_activity (user_id, description, ip_address, data)
    VALUES (user_id, activity_description, ip_address, activity_data)
    RETURNING id INTO activity_id;
    
    -- یافتن نوع فعالیت
    SELECT id INTO type_id FROM activity_type WHERE name = activity_type_name;
    
    -- ارتباط فعالیت با نوع آن
    IF type_id IS NOT NULL THEN
        INSERT INTO user_activity_type (activity_id, type_id)
        VALUES (activity_id, type_id);
    END IF;
    
    RETURN activity_id;
END;
$$ LANGUAGE plpgsql;