from flask.ext.codemirror.fields import CodeMirrorField
from flask.ext.wtf import Form
from wtforms.fields import SubmitField


class MyForm(Form):
    source_code = CodeMirrorField(
        language='python',
        config={'lineNumbers' : 'true'}
    )
    submit = SubmitField('Submit')
