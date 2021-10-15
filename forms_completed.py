from flask import (
    Blueprint, g, redirect, render_template, flash, request, url_for
)
from main.auth import login_required
from main.db import get_db

bp = Blueprint('forms_completed', __name__)

#Form2935 1
@bp.route('/form2935/part1/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def general_information_c(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'select * from general_information where kids_id = %s', (id,)
    )
    general_information = c.fetchall()
    db.commit()
    return render_template('system/forms_completed/general_information_c.html', kids=kids, general_information=general_information)

#Form2935 2
@bp.route('/form2935/part2/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def consent_information_c(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'select * from consent_information where kids_id = %s', (id,)
    )
    consent_information = c.fetchall()
    c.execute(
        'select * from consent_information_hours where kids_id = %s', (id,)
    )
    consent_information_hours = c.fetchall()
    db.commit()
    return render_template('system/forms_completed/consent_information_c.html', kids=kids, consent_information=consent_information, consent_information_hours=consent_information_hours)

#Form2935 3
@bp.route('/form2935/part3/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def medical_school_information_c(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'select * from medical_school_information where kids_id = %s', (id,)
    )
    medical_school_information = c.fetchall()
    db.commit()
    return render_template('system/forms_completed/medical_school_information_c.html', kids=kids, medical_school_information=medical_school_information)

#Form2935 5
@bp.route('/form2935/part5/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def vaccine_information_c(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'select * from vaccine_information where kids_id = %s', (id,)
    )
    vaccine_information = c.fetchall()
    db.commit()
    return render_template('system/forms_completed/vaccine_information_c.html', kids=kids, vaccine_information=vaccine_information)

#Form2935 6
@bp.route('/form2935/part6/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def signatures_c(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'select * from signatures where kids_id = %s', (id,)
    )
    signatures = c.fetchall()
    db.commit()
    return render_template('system/forms_completed/signatures_c.html', kids=kids, signatures=signatures)

#Medical Authorization
@bp.route('/medical_authorization/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def medical_authorization_c(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'select * from medical_authorization where kids_id = %s', (id,)
    )
    medical_authorization = c.fetchall()
    db.commit()
    return render_template('system/forms_completed/medical_authorization_c.html', kids=kids, medical_authorization=medical_authorization)

#Children Risk TB
@bp.route('/children_risk_tb/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def children_risk_tb_c(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'select * from children_risk_tb where kids_id = %s', (id,)
    )
    children_risk_tb = c.fetchall()
    db.commit()
    return render_template('system/forms_completed/children_risk_tb_c.html', kids=kids, children_risk_tb=children_risk_tb)

#Account Agreement
@bp.route('/account_agreement/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def account_agreement_c(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'select * from account_agreement where kids_id = %s', (id,)
    )
    account_agreement = c.fetchall()
    db.commit()
    return render_template('system/forms_completed/account_agreement_c.html', kids=kids, account_agreement=account_agreement)

#Infant Care
@bp.route('/infant_care/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def infant_care_c(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'select * from infant_care where kids_id = %s', (id,)
    )
    infant_care = c.fetchall()
    db.commit()
    return render_template('system/forms_completed/infant_care_c.html', kids=kids, infant_care=infant_care)



