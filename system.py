from flask import (
    Blueprint, g, redirect, render_template, flash, request, url_for
)
from main.auth import login_required
from main.db import get_db

bp = Blueprint('system', __name__)

#Enroll Index Parents.
#Main section where parents can see their kids data.
@bp.route('/enroll', methods=['GET', 'POST'])
@login_required
def index_enroll():
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, u.username, k.id_parent, k.all_forms_status '
        'from kids k join user u on k.id_parent = u.id where k.id_parent = %s',
        (g.user['id'],)
    )
    kids = c.fetchall()

    return render_template('system/index_system.html', kids=kids)

#Online Registration
@bp.route('/online_registration/<int:id>', methods=['GET', 'POST'])
@login_required
def online_registration(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent, k.all_forms_status '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    c.execute(
        'SELECT * FROM forms WHERE kids_id = %s', (id,)
    )
    forms = c.fetchall()
    if request.method == 'POST':
        c.execute(
            "UPDATE kids SET all_forms_status = %s WHERE id = %s", (True, id)
        )
        db.commit()
        flash("Congratulations! You Have Uploaded The Forms. In Few Days We Will Send You An Email Of Your Child Status.")
        return redirect(url_for('system.online_registration', id=id))

    return render_template('system/online_registration.html', kids=kids, forms=forms)

@bp.route('/upload_vaccine_card/<int:id>', methods=['POST'])
@login_required
def upload_vaccine_card(id):
    if request.method == 'POST':
        file = request.files['vaccine_card']
        newFile = file.read()
        db, c = get_db()
        c.execute(
            'insert into vaccine_card (vaccine_card, kids_id)'
            ' values (%s, %s)',
            (newFile, id)
        )
        c.execute(
            "UPDATE forms SET vaccine_information_s = %s WHERE id = %s", (True, id)
        )
        db.commit()
        flash("You Have Uploaded The Vaccine Card!")
        return redirect(url_for('system.online_registration', id=id))

@bp.route('/upload_physical_test/<int:id>', methods=['POST'])
@login_required
def upload_physical_test(id):
    file = request.files['physical_test']
    newFile = file.read()
    db, c = get_db()
    c.execute(
        'insert into physical_test (physical_test, kids_id)'
        ' values (%s, %s)',
        (newFile, id)
    )
    c.execute(
        "UPDATE forms SET physical_test_s = %s WHERE id = %s", (True, id)
    )
    db.commit()
    flash("You Have Uploaded The Physical Test!")
    return redirect(url_for('system.online_registration', id=id))

#Profile
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, u.username, k.id_parent, k.all_forms_status, k.all_forms_date '
        'from kids k join user u on k.id_parent = u.id where k.id_parent = %s',
        (g.user['id'],)
    )
    kids = c.fetchall()
    c.execute(
        'select p.id, p.firstname_parent, p.middlename_parent, p.lastname_parent, p.email_parent, p.phone_parent, u.username, u.password '
        'from parents p join user u on p.id = %s',
        (g.user['id'],)
    )
    parents = c.fetchall()
    return render_template('system/profile.html', kids=kids, parents=parents)

#Announcements
@bp.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():
    return render_template('system/announcements.html')

#Form2935 1 (DONE)
#(DONE)
#(DONE)
#(DONE)

@bp.route('/form2935/part1/<int:id>', methods=['GET', 'POST'])
@login_required
def general_information(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    db.commit()
    if request.method == 'POST':
        child_lastname = request.form['child_lastname']
        child_middlename = request.form['child_middlename']
        child_firstname = request.form['child_firstname']
        date_birth = request.form['date_birth']
        child_lives_with = request.form['child_lives_with']
        child_home_address = request.form['child_home_address']
        date_admission = request.form['date_admission']
        name_completing_form = request.form['name_completing_form']
        address_parent = request.form['address_parent']
        parent1_phone = request.form['parent1_phone']
        parent2_phone = request.form['parent2_phone']
        guardian_phone = request.form['guardian_phone']
        custody_documents = request.form['custody_documents']
        emergency_fullname = request.form['emergency_fullname']
        emergency_phone = request.form['emergency_phone']
        emergency_address = request.form['emergency_address']
        emergency_relationship = request.form['emergency_relationship']
        release_fullname1 = request.form['release_fullname1']
        release_fullname2 = request.form['release_fullname2']
        release_fullname3 = request.form['release_fullname3']
        release_phone1 = request.form['release_phone1']
        release_phone2 = request.form['release_phone2']
        release_phone3 = request.form['release_phone3']
        sign = request.form['sign']
        db, c = get_db()
        c.execute(
            'insert into general_information (child_lastname, child_middlename, child_firstname, date_birth, child_lives_with, child_home_address, date_admission, '
            'name_completing_form, address_parent, parent1_phone, parent2_phone, guardian_phone, custody_documents, emergency_fullname, emergency_phone, emergency_address, emergency_relationship, '
            'release_fullname1, release_fullname2, release_fullname3, release_phone1, release_phone2, release_phone3, sign, kids_id)'
            ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (child_lastname, child_middlename, child_firstname, date_birth, child_lives_with, child_home_address, date_admission,
            name_completing_form, address_parent, parent1_phone, parent2_phone, guardian_phone, custody_documents, emergency_fullname, emergency_phone, emergency_address, emergency_relationship,
            release_fullname1, release_fullname2, release_fullname3, release_phone1, release_phone2, release_phone3, sign, id)
        )
        c.execute(
            "UPDATE forms SET general_information_s = %s WHERE kids_id = %s", (True, id)
        )
        db.commit()
        flash("The Form Has Been Submitted Succesfuly!")
        return redirect(url_for('system.online_registration', id=id))
    return render_template('system/forms/general_information.html', kids=kids)

#Form2935 2 (DONE)
#(DONE)
#(DONE)
#(DONE)

@bp.route('/form2935/part2/<int:id>', methods=['GET', 'POST'])
@login_required
def consent_information(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    if request.method == 'POST':
        for_emergency_care = request.form['for_emergency_care']
        on_field_trips = request.form['on_field_trips']
        to_and_from_home = request.form['to_and_from_home']
        to_and_from_school = request.form['to_and_from_school']
        consent_field_trips = request.form['consent_field_trips']
        water_table_play = request.form['water_table_play']
        sprinkler_play = request.form['sprinkler_play']
        splashing_wading_pools = request.form['splashing_wading_pools']
        swimming_pools = request.form['swimming_pools']
        aquatic_playgrounds = request.form['aquatic_playgrounds']
        discipline_guidance = request.form['discipline_guidance']
        suspension_expulsion = request.form['suspension_expulsion']
        emergency_plans = request.form['emergency_plans']
        procedures_conducting_health = request.form['procedures_conducting_health']
        safe_sleep = request.form['safe_sleep']
        procedures_parents_discuss = request.form['procedures_parents_discuss']
        procedures_parents_activities = request.form['procedures_parents_activities']
        procedures_release_children = request.form['procedures_release_children']
        illness_exclusion = request.form['illness_exclusion']
        procedures_dispensing_medications = request.form['procedures_dispensing_medications']
        immunization_requirements = request.form['immunization_requirements']
        meals_food_service_practices = request.form['meals_food_service_practices']
        procedures_visit_without_securing = request.form['procedures_visit_without_securing']
        procedures_parent_child = request.form['procedures_parent_child']
        meals_none = request.form['meals_none']
        meals_breakfast = request.form['meals_breakfast']
        meals_morning_snack = request.form['meals_morning_snack']
        meals_lunch = request.form['meals_lunch']
        meals_afternoon_snack = request.form['meals_afternoon_snack']
        meals_supper = request.form['meals_supper']
        meals_evening_snack = request.form['meals_evening_snack']
        monday_am = request.form['monday_am']
        monday_pm = request.form['monday_pm']
        tuesday_am = request.form['tuesday_am']
        tuesday_pm = request.form['tuesday_pm']
        wednesday_am = request.form['wednesday_am']
        wednesday_pm = request.form['wednesday_pm']
        thursday_am = request.form['thursday_am']
        thursday_pm = request.form['thursday_pm']
        friday_am = request.form['friday_am']
        friday_pm = request.form['friday_pm']
        saturday_am = request.form['saturday_am']
        saturday_pm = request.form['saturday_pm']
        sunday_am = request.form['sunday_am']
        sunday_pm = request.form['sunday_pm']
        sign = request.form['sign']
        c.execute(
            'INSERT INTO consent_information (for_emergency_care, on_field_trips, to_and_from_home, to_and_from_school, consent_field_trips, water_table_play, '
            'sprinkler_play, splashing_wading_pools, swimming_pools, aquatic_playgrounds, discipline_guidance, suspension_expulsion, emergency_plans, procedures_conducting_health, safe_sleep, '
            'procedures_parents_discuss, procedures_parents_activities, procedures_release_children, illness_exclusion, procedures_dispensing_medications, immunization_requirements, meals_food_service_practices, procedures_visit_without_securing, '
            'procedures_parent_child, meals_none, meals_breakfast, meals_morning_snack, meals_lunch, meals_afternoon_snack, meals_supper, meals_evening_snack, sign, kids_id)'
            ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (for_emergency_care, on_field_trips, to_and_from_home, to_and_from_school, consent_field_trips, water_table_play, sprinkler_play, splashing_wading_pools, swimming_pools,
            aquatic_playgrounds, discipline_guidance, suspension_expulsion, emergency_plans, procedures_conducting_health, safe_sleep, procedures_parents_discuss, procedures_parents_activities, procedures_release_children, illness_exclusion, procedures_dispensing_medications,
            immunization_requirements, meals_food_service_practices, procedures_visit_without_securing, procedures_parent_child, meals_none, meals_breakfast, meals_morning_snack, meals_lunch, meals_afternoon_snack, meals_supper, meals_evening_snack, sign, id)
        )
        c.execute(
            'INSERT INTO consent_information_hours (monday_am, monday_pm, tuesday_am, tuesday_pm, wednesday_am, wednesday_pm, thursday_am, thursday_pm, friday_am, friday_pm, saturday_am, saturday_pm, '
            'sunday_am, sunday_pm, sign, kids_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (monday_am, monday_pm, tuesday_am, tuesday_pm, wednesday_am, wednesday_pm, thursday_am, thursday_pm, friday_am, friday_pm, saturday_am, saturday_pm,
            sunday_am, sunday_pm, sign, id)
        )
        c.execute(
            "UPDATE forms SET consent_information_s = %s WHERE kids_id = %s", (True, id)
        )
        db.commit()
        flash("The Form Has Been Submitted Succesfuly!")
        return redirect(url_for('system.online_registration', id=id))
    return render_template('system/forms/consent_information.html', kids=kids)

#Form 2935 3 (DONE)
#(DONE)
#(DONE)
#(DONE)

@bp.route('/form2935/part3/<int:id>', methods=['GET', 'POST'])
@login_required
def medical_school_information(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    if request.method == 'POST':
        name_physician = request.form['name_physician']
        address_physician = request.form['address_physician']
        phone_physician = request.form['phone_physician']
        name_emergency_care_facility = request.form['name_emergency_care_facility']
        address_emergency_care_facility = request.form['address_emergency_care_facility']
        phone_emergency_care_facility = request.form['phone_emergency_care_facility']
        give_consent_facility = request.form['give_consent_facility']
        child_diagnosed_food_allergies = request.form['child_diagnosed_food_allergies']
        name_of_school = request.form['name_of_school']
        school_phone_number = request.form['school_phone_number']
        authorized_locations = request.form['authorized_locations']
        walk_from_school_home = request.form['walk_from_school_home']
        ride_a_bus = request.form['ride_a_bus']
        sign = request.form['sign']
        released_care_sibling_under_18 = request.form['released_care_sibling_under_18']
        c.execute(
            'INSERT INTO medical_school_information (name_physician, address_physician, phone_physician, name_emergency_care_facility, address_emergency_care_facility, phone_emergency_care_facility, give_consent_facility, '
            'child_diagnosed_food_allergies, name_of_school, school_phone_number, authorized_locations, walk_from_school_home, ride_a_bus, released_care_sibling_under_18, sign, kids_id)'
            ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (name_physician, address_physician, phone_physician, name_emergency_care_facility, address_emergency_care_facility, phone_emergency_care_facility, give_consent_facility,
            child_diagnosed_food_allergies, name_of_school, school_phone_number, authorized_locations, walk_from_school_home, ride_a_bus, released_care_sibling_under_18, sign, id)
        )
        c.execute(
            "UPDATE forms SET medical_school_s = %s WHERE kids_id = %s", (True, id)
        )
        db.commit()
        flash("The Form Has Been Submitted Succesfuly!")
        return redirect(url_for('system.online_registration', id=id))
    return render_template('system/forms/medical_school_information.html', kids=kids)

#NOT ENABLED
#NOT ENABLED
#NOT ENABLED

@bp.route('/form2935/part4/<int:id>', methods=['GET', 'POST'])
@login_required
def vision_hearing_results(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    if request.method == 'POST':
        vision_right = request.form['vision_right']
        vision_left = request.form['vision_left']
        pass_fail = request.form['pass_fail']
        right_1000hz = request.form['right_1000hz']
        right_2000hz = request.form['right_2000hz']
        right_4000hz = request.form['right_4000hz']
        right_pass_fail = request.form['right_pass_fail']
        left_1000hz = request.form['left_1000hz']
        left_2000hz = request.form['left_2000hz']
        left_4000hz = request.form['left_4000hz']
        left_pass_fail = request.form['left_pass_fail']
        sign = request.form['sign']
        c.execute(
            'INSERT INTO vision_exam_results (vision_right, vision_left, pass_fail, sign, kids_id) values (%s, %s, %s, %s, %s)'
            (vision_right, vision_left, pass_fail, sign, id)
        )
        c.execute(
            'INSERT INTO hearing_exam_results (vision_right, vision_left, pass_fail, sign, kids_id) values (%s, %s, %s, %s, %s)'
            (vision_right, vision_left, pass_fail, sign, id)
        )
    return render_template('forms/form2935_4.html', kids=kids)

#Form2935 5 (DONE)
#(DONE)
#(DONE)
#(DONE)

@bp.route('/form2935/part5/<int:id>', methods=['GET', 'POST'])
@login_required
def vaccine_information(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    if request.method == 'POST':
        hepatitisB_first_dose = request.form['hepatitisB_first_dose']
        hepatitisB_second_dose = request.form['hepatitisB_second_dose']
        hepatitisB_third_dose = request.form['hepatitisB_third_dose']
        rotavirus_first_dose = request.form['rotavirus_first_dose']
        rotavirus_second_dose = request.form['rotavirus_second_dose']
        rotavirus_third_dose = request.form['rotavirus_third_dose']
        DTP_first_dose = request.form['DTP_first_dose']
        DTP_second_dose = request.form['DTP_second_dose']
        DTP_third_dose = request.form['DTP_third_dose']
        DTP_fourth_dose = request.form['DTP_fourth_dose']
        DTP_fifth_dose = request.form['DTP_fifth_dose']
        haemophilus_first_dose = request.form['haemophilus_first_dose']
        haemophilus_second_dose = request.form['haemophilus_second_dose']
        haemophilus_third_dose = request.form['haemophilus_third_dose']
        haemophilus_fourth_dose = request.form['haemophilus_fourth_dose']
        pneumococcal_first_dose = request.form['pneumococcal_first_dose']
        pneumococcal_second_dose = request.form['pneumococcal_second_dose']
        pneumococcal_third_dose = request.form['pneumococcal_third_dose']
        pneumococcal_fourth_dose = request.form['pneumococcal_fourth_dose']
        inactivedPoliovirus_first_dose = request.form['inactivedPoliovirus_first_dose']
        inactivedPoliovirus_second_dose = request.form['inactivedPoliovirus_second_dose']
        inactivedPoliovirus_third_dose = request.form['inactivedPoliovirus_third_dose']
        inactivedPoliovirus_fourth_dose = request.form['inactivedPoliovirus_fourth_dose']
        influenza_date = request.form['influenza_date']
        MMR_first_dose = request.form['MMR_first_dose']
        MMR_second_dose = request.form['MMR_second_dose']
        varicella_first_dose = request.form['varicella_first_dose']
        varicella_second_dose = request.form['varicella_second_dose']
        hepatitisA_first_dose = request.form['hepatitisA_first_dose']
        hepatitisA_second_dose = request.form['hepatitisA_second_dose']
        sign = request.form['sign']
        c.execute(
            'INSERT INTO vaccine_information (hepatitisB_first_dose, hepatitisB_second_dose, hepatitisB_third_dose, rotavirus_first_dose, rotavirus_second_dose, rotavirus_third_dose, DTP_first_dose, '
            'DTP_second_dose, DTP_third_dose, DTP_fourth_dose, DTP_fifth_dose, haemophilus_first_dose, haemophilus_second_dose, haemophilus_third_dose, haemophilus_fourth_dose, pneumococcal_first_dose, pneumococcal_second_dose, '
            'pneumococcal_third_dose, pneumococcal_fourth_dose, inactivedPoliovirus_first_dose, inactivedPoliovirus_second_dose, inactivedPoliovirus_third_dose, inactivedPoliovirus_fourth_dose, influenza_date, '
            'MMR_first_dose, MMR_second_dose, varicella_first_dose, varicella_second_dose, hepatitisA_first_dose, hepatitisA_second_dose, sign, kids_id)'
            ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            (hepatitisB_first_dose, hepatitisB_second_dose, hepatitisB_third_dose, rotavirus_first_dose, rotavirus_second_dose, rotavirus_third_dose, DTP_first_dose,
            DTP_second_dose, DTP_third_dose, DTP_fourth_dose, DTP_fifth_dose, haemophilus_first_dose, haemophilus_second_dose, haemophilus_third_dose, haemophilus_fourth_dose, pneumococcal_first_dose, pneumococcal_second_dose,
            pneumococcal_third_dose, pneumococcal_fourth_dose, inactivedPoliovirus_first_dose, inactivedPoliovirus_second_dose, inactivedPoliovirus_third_dose, inactivedPoliovirus_fourth_dose, influenza_date,
            MMR_first_dose, MMR_second_dose, varicella_first_dose, varicella_second_dose, hepatitisA_first_dose, hepatitisA_second_dose, sign, id)
        )
        c.execute(
            "UPDATE forms SET vaccine_information_s = %s WHERE kids_id = %s", (True, id)
        )
        db.commit()
        flash("The Form Has Been Submitted Succesfuly!")
        return redirect(url_for('system.online_registration', id=id))
    return render_template('system/forms/vaccine_information.html', kids=kids)

#Form2935 6 (DONE)
#(DONE)
#(DONE)
#(DONE)

@bp.route('/form2935/part6/<int:id>', methods=['GET', 'POST'])
@login_required
def signatures(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    if request.method == 'POST':
        health_personnel_signature = request.form['health_personnel_signature']
        varicella_signature = request.form['varicella_signature']
        tb_test = request.form['tb_test']
        parent_guardian_signature = request.form['parent_guardian_signature']
        sign = request.form['sign']
        c.execute(
                'insert into signatures (health_personnel_signature, varicella_signature, tb_test, parent_guardian_signature, sign, kids_id) values (%s, %s, %s, %s, %s, %s)',
                (health_personnel_signature, varicella_signature, tb_test, parent_guardian_signature, sign, id)
            )
        c.execute(
            "UPDATE forms SET signatures_s = %s WHERE kids_id = %s", (True, id)
        )
        db.commit()
        flash("The Form Has Been Submitted Succesfuly!")
        return redirect(url_for('system.online_registration', id=id))
    return render_template('system/forms/signatures.html', kids=kids)

#Medical Authorization (DONE)
#(DONE)
#(DONE)
#(DONE)

@bp.route('/medical_authorization/<int:id>', methods=['GET', 'POST'])
@login_required
def medical_authorization(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    if request.method == 'POST':
        children_authorization = request.form['children_authorization']
        immunizations_up_to_date = request.form['immunizations_up_to_date']
        allergies = request.form['allergies']
        any_medical_informaiton = request.form['any_medical_informaiton']
        medications_child_takes = request.form['medications_child_takes']
        sign = request.form['sign']
        c.execute(
                'insert into medical_authorization (children_authorization, immunizations_up_to_date, allergies, any_medical_informaiton, medications_child_takes, '
                'sign, kids_id) values (%s, %s, %s, %s, %s, %s, %s)',
                (children_authorization, immunizations_up_to_date, allergies, any_medical_informaiton, medications_child_takes, sign, id)
            )
        c.execute(
            "UPDATE forms SET medical_authorization_s = %s WHERE kids_id = %s", (True, id)
        )
        db.commit()
        flash("The Form Has Been Submitted Succesfuly!")
        return redirect(url_for('system.online_registration', id=id))
    return render_template('system/forms/medical_authorization.html', kids=kids)

#Children Risk TB (DONE)
#(DONE)
#(DONE)
#(DONE)

@bp.route('/children_risk_tb/<int:id>', methods=['GET', 'POST'])
@login_required
def children_risk_tb(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    if request.method == 'POST':
        tbquestion1_subq1 = request.form['tbquestion1_subq1']
        tbquestion1_subq2 = request.form['tbquestion1_subq2']
        tbquestion1_subq3 = request.form['tbquestion1_subq3']
        tbquestion2_subq1 = request.form['tbquestion2_subq1']
        tbquestion2_subq2 = request.form['tbquestion2_subq2']
        tbquestion2_subq3 = request.form['tbquestion2_subq3']
        tbquestion2_subq4 = request.form['tbquestion2_subq4']
        tbquestion3_subq1 = request.form['tbquestion3_subq1']
        tbquestion3_subq2 = request.form['tbquestion3_subq2']
        tbquestion3_subq3 = request.form['tbquestion3_subq3']
        tbquestion3_subq1_date = request.form['tbquestion3_subq1_date']
        tbquestion3_subq2_date = request.form['tbquestion3_subq2_date']
        tbquestion3_subq3_date = request.form['tbquestion3_subq3_date']
        sign = request.form['sign']
        c.execute(
            'insert into children_risk_tb (tbquestion1_subq1, tbquestion1_subq2, tbquestion1_subq3, tbquestion2_subq1, tbquestion2_subq2, tbquestion2_subq3, tbquestion2_subq4, tbquestion3_subq1, tbquestion3_subq2, tbquestion3_subq3, '
            'tbquestion3_subq1_date, tbquestion3_subq2_date, tbquestion3_subq3_date, sign, kids_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (tbquestion1_subq1, tbquestion1_subq2, tbquestion1_subq3, tbquestion2_subq1, tbquestion2_subq2, tbquestion2_subq3, tbquestion2_subq4, tbquestion3_subq1, tbquestion3_subq2, tbquestion3_subq3,
            tbquestion3_subq1_date, tbquestion3_subq2_date, tbquestion3_subq3_date, sign, id)
        )
        c.execute(
            "UPDATE forms SET children_risk_s = %s WHERE kids_id = %s", (True, id)
        )
        db.commit()
        flash("The Form Has Been Submitted Succesfuly!")
        return redirect(url_for('system.online_registration', id=id))
    return render_template('system/forms/children_risk_tb.html', kids=kids)

#Account Agreement (DONE)
#(DONE)
#(DONE)
#(DONE)

@bp.route('/account_agreement/<int:id>', methods=['GET', 'POST'])
@login_required
def account_agreement(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    if request.method == 'POST':
        who_is_filling = request.form['who_is_filling']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        cell_phone = request.form['cell_phone']
        home_phone = request.form['home_phone']
        social_security_4digit = request.form['social_security_4digit']
        drivers_license = request.form['drivers_license']
        email = request.form['email']
        present_address = request.form['present_address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        employer = request.form['employer']
        address_employer = request.form['address_employer']
        business_phone = request.form['business_phone']
        sign = request.form['sign']
        db, c = get_db()
        c.execute(
            'insert into account_agreement (who_is_filling, lastname, firstname, middlename, cell_phone, home_phone, social_security_4digit, drivers_license, email, present_address, '
            'city, state, zip, employer, address_employer, business_phone, sign, kids_id)'
            ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (who_is_filling, lastname, firstname, middlename, cell_phone, home_phone, social_security_4digit, drivers_license, email, present_address,
            city, state, zip, employer, address_employer, business_phone, sign, id)
        )
        c.execute(
            "UPDATE forms SET account_agreement_s = %s WHERE kids_id = %s", (True, id)
        )
        db.commit()
        flash("The Form Has Been Submitted Succesfuly!")
        return redirect(url_for('system.online_registration', id=id))
    return render_template('system/forms/account_agreement.html', kids=kids)

#Infant Care (DONE)
#(DONE)
#(DONE)
#(DONE)

@bp.route('/infant_care/<int:id>', methods=['GET', 'POST'])
@login_required
def infant_care(id):
    db, c = get_db()
    c.execute(
        'select k.id, k.firstname_kid, k.middlename_kid, k.lastname_kid, k.id_parent '
        'from kids k join parents p on k.id_parent = p.id where k.id_parent = %s and k.id = %s',
        (g.user['id'], id)
    )
    kids = c.fetchall()
    if request.method == 'POST':
        formula = request.form['formula']
        milk = request.form['milk']
        meats = request.form['meats']
        cereal = request.form['cereal']
        vegetables = request.form['vegetables']
        fruits = request.form['fruits']
        warmer = request.form['warmer']
        pacifier = request.form['pacifier']
        food = request.form['food']
        skin = request.form['skin']
        other = request.form['other']
        symptoms_produced_allergies = request.form['symptoms_produced_allergies']
        skin_care_ointment = request.form['skin_care_ointment']
        on_stomach = request.form['on_stomach']
        on_back = request.form['on_back']
        on_slide = request.form['on_slide']
        sign = request.form['sign']
        db, c = get_db()
        c.execute(
            'insert into infant_care (formula, milk, meats, cereal, vegetables, fruits, warmer, pacifier, food, skin, '
            'other, symptoms_produced_allergies, skin_care_ointment, on_stomach, on_back, on_slide, sign, kids_id)'
            ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (formula, milk, meats, cereal, vegetables, fruits, warmer, pacifier, food, skin,
            other, symptoms_produced_allergies, skin_care_ointment, on_stomach, on_back, on_slide, sign, id)
        )
        c.execute(
            "UPDATE forms SET infant_care_s = %s WHERE kids_id = %s", (True, id)
        )
        db.commit()
        flash("The Form Has Been Submitted Succesfuly!")
        return redirect(url_for('system.online_registration', id=id))
    return render_template('system/forms/infant_care.html', kids=kids)



