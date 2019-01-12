#coding=utf-8
from flask_wtf import FlaskForm
from ..leotool.leoform.formcore import StringField,HiddenField,SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
photos = UploadSet('photos', IMAGES)

class fromtest(FlaskForm):
    id = StringField('id', validators=[DataRequired(), Length(1, 36)])
    mhname = StringField('mhname',render_kw={"id":"pwd", "placeholder":"请输入密码"}, validators=[DataRequired(), Length(1, 64)])
    email = StringField('email',render_kw={"id":"email", "class":"form-control","type":"text"})
    hidden_pic_url = HiddenField("pic_url",default="")
    submit = SubmitField('提交')

