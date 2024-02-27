from flask import Flask, render_template, request, redirect, url_for, Blueprint
from .document_manager import sections, append_to_section

app = Flask(__name__)
main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    """Handle the index route."""
    if request.method == 'POST':
        section_key = request.form['section']
        content = request.form['content']
        append_to_section(section_key, content)
        return redirect(url_for('main.index'))
    return render_template('index.html', sections=sections.keys())

def create_app():
    """Create and configure an instance of the Flask application."""
    app.register_blueprint(main)
    return app

