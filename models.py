from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from sqlalchemy.sql import func
import json

# Association tables
post_tag = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

portfolio_tag = db.Table('portfolio_tag',
    db.Column('portfolio_id', db.Integer, db.ForeignKey('portfolio_item.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

user_activity_type = db.Table('user_activity_type',
    db.Column('activity_id', db.Integer, db.ForeignKey('user_activity.id'), primary_key=True),
    db.Column('type_id', db.Integer, db.ForeignKey('activity_type.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(200))
    bio = db.Column(db.Text)
    phone = db.Column(db.String(20))
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relations
    posts = db.relationship('BlogPost', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    activities = db.relationship('UserActivity', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    visits = db.relationship('PostVisit', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def record_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def get_activity_count(self):
        return UserActivity.query.filter_by(user_id=self.id).count()
    
    def __repr__(self):
        return f'<User {self.username}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    reply_sent = db.Column(db.Boolean, default=False)
    reply_text = db.Column(db.Text)
    reply_date = db.Column(db.DateTime)
    ip_address = db.Column(db.String(45))
    
    def __repr__(self):
        return f'<ContactMessage {self.subject}>'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    
    # Many-to-many relationships
    posts = db.relationship('BlogPost', secondary=post_tag, backref=db.backref('tags', lazy='dynamic'))
    portfolio_items = db.relationship('PortfolioItem', secondary=portfolio_tag, backref=db.backref('tags', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Relationships
    posts = db.relationship('BlogPost', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.Boolean, default=True)
    featured_image = db.Column(db.String(200))
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('Like', backref='post', lazy=True, cascade="all, delete-orphan")
    visits = db.relationship('PostVisit', backref='post', lazy=True, cascade="all, delete-orphan")
    
    def increment_view(self):
        self.views_count += 1
        db.session.commit()
    
    def update_counts(self):
        self.comments_count = Comment.query.filter_by(post_id=self.id).count()
        self.likes_count = Like.query.filter_by(post_id=self.id).count()
        db.session.commit()
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)
    
    # Foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    
    # Self-referential relationship for comment replies
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]),
                             lazy='dynamic')
    
    def __repr__(self):
        return f'<Comment {self.id}>'

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Unique constraint to prevent duplicate likes
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_user_like'),)
    
    def __repr__(self):
        return f'<Like {self.id}>'

class PostVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visit_date = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    
    # Foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # nullable for anonymous users
    
    def __repr__(self):
        return f'<PostVisit {self.id}>'

class ActivityType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    
    # Relationships
    activities = db.relationship('UserActivity', secondary=user_activity_type, 
                               backref=db.backref('types', lazy=True))
    
    def __repr__(self):
        return f'<ActivityType {self.name}>'

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    data = db.Column(db.Text)  # JSON data
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def set_data(self, data_dict):
        self.data = json.dumps(data_dict)
    
    def get_data(self):
        if self.data:
            return json.loads(self.data)
        return {}
    
    def __repr__(self):
        return f'<UserActivity {self.id}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=False)  # Font Awesome icon name
    featured = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Service {self.title}>'

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    project_url = db.Column(db.String(200))
    client_name = db.Column(db.String(100))
    completed_date = db.Column(db.Date)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PortfolioItem {self.title}>'

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=False)
    site_description = db.Column(db.Text)
    site_logo = db.Column(db.String(200))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    contact_address = db.Column(db.Text)
    social_facebook = db.Column(db.String(200))
    social_twitter = db.Column(db.String(200))
    social_instagram = db.Column(db.String(200))
    social_linkedin = db.Column(db.String(200))
    footer_text = db.Column(db.Text)
    analytics_code = db.Column(db.Text)
    maintenance_mode = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<SiteSettings {self.site_name}>'

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow().date, unique=True)
    visits = db.Column(db.Integer, default=0)
    unique_visitors = db.Column(db.Integer, default=0)
    page_views = db.Column(db.Integer, default=0)
    most_visited_page = db.Column(db.String(200))
    most_visited_post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))
    data = db.Column(db.Text)  # JSON for additional data
    
    def set_data(self, data_dict):
        self.data = json.dumps(data_dict)
    
    def get_data(self):
        if self.data:
            return json.loads(self.data)
        return {}
    
    @classmethod
    def get_or_create_today(cls):
        today = datetime.utcnow().date()
        stats = cls.query.filter_by(date=today).first()
        if not stats:
            stats = cls(date=today)
            db.session.add(stats)
            db.session.commit()
        return stats
    
    def increment_visit(self):
        self.visits += 1
        db.session.commit()
    
    def increment_page_view(self):
        self.page_views += 1
        db.session.commit()
    
    def __repr__(self):
        return f'<Statistics {self.date}>'