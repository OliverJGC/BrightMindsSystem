from flask import (
    Blueprint, render_template
)

bp = Blueprint('main', __name__)

#Main Index
#Only shows the main.
@bp.route('/')
def index():
    return render_template('main/index.html')

#Contact Us
#Users will send questions to the BrightMinds email.
@bp.route('/contact_us', methods=['GET','POST'])
def contact_us():
    return render_template('main/contact_us.html')

#Sitemap
#Only shows the sitemap.
@bp.route('/sitemap', methods=['GET', 'POST'])
def sitemap():
    return render_template('main/sitemap.html')

#Covid
#Only shows the covid section.
@bp.route('/covid', methods=['GET', 'POST'])
def covid():
    return render_template('main/covid.html')