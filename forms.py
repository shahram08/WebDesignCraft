from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    remember = BooleanField('مرا به خاطر بسپار')
    submit = SubmitField('ورود')

class RegistrationForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('تکرار رمز عبور', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('ثبت نام')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('این نام کاربری قبلاً انتخاب شده است. لطفاً نام کاربری دیگری انتخاب کنید.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('این ایمیل قبلاً ثبت شده است. لطفاً ایمیل دیگری وارد کنید.')

class ContactForm(FlaskForm):
    name = StringField('نام شما', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    subject = StringField('موضوع', validators=[DataRequired(), Length(min=3, max=200)])
    message = TextAreaField('پیام', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('ارسال پیام')

class BlogPostForm(FlaskForm):
    title = StringField('عنوان', validators=[DataRequired(), Length(min=3, max=200)])
    slug = StringField('اسلاگ', validators=[DataRequired(), Length(min=3, max=200)])
    summary = TextAreaField('خلاصه', validators=[DataRequired(), Length(min=10)])
    content = TextAreaField('محتوا', validators=[DataRequired()])
    submit = SubmitField('ذخیره')

class ServiceForm(FlaskForm):
    title = StringField('عنوان', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('توضیحات', validators=[DataRequired()])
    icon = StringField('آیکون', validators=[DataRequired(), Length(min=3, max=50)])
    submit = SubmitField('ذخیره')

class PortfolioItemForm(FlaskForm):
    title = StringField('عنوان', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('توضیحات', validators=[DataRequired()])
    category = StringField('دسته بندی', validators=[DataRequired(), Length(min=2, max=50)])
    image_url = StringField('آدرس تصویر', validators=[DataRequired()])
    submit = SubmitField('ذخیره')