from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    
    name ={'username':'root'}

    posts = [
        {
            'author': {'username':'root'},
            'body':"Hi I am a root"
        },
        {
            'author': {'username':'test'},
            'body':"Hi I am a test"
        },
        {
            'author': {'username':'test2'},
            'body':"Hi I am a test2"
        }
    ]
    return render_template('index.html',name=name, posts =posts)


if __name__ == '__main__':
    app.run()
