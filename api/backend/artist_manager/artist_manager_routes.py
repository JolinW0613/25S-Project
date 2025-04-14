from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

artist_manager = Blueprint('artist_manager', __name__)

# ------------------------------
# GET /artist_schedule
@artist_manager.route('/artist_schedule', methods=['GET'])
def get_artist_schedule():
    cursor = db.get_db().cursor()
    query = '''
        SELECT * FROM ArtPlatformDB.schedule
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(data)
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# ------------------------------
# GET /artist_contact_info
@artist_manager.route('/artist_contact_info', methods=['GET'])
def get_artist_contact_info():
    cursor = db.get_db().cursor()
    query = '''
        SELECT artist_id, contact_info FROM Artist
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(data)
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# ------------------------------
# GET /artist_information
@artist_manager.route('/artist_information', methods=['GET'])
def get_artist_information():
    cursor = db.get_db().cursor()
    query = '''
        SELECT * FROM Artist
        JOIN Contract C ON Artist.artist_id = C.artist_id
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(data)
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# ------------------------------
# GET /artist_revenue
@artist_manager.route('/artist_revenue', methods=['GET'])
def get_artist_revenue():
    cursor = db.get_db().cursor()
    query = '''
        SELECT Payment.*, A.name AS artist_name
        FROM Payment
        JOIN Artist A ON A.artist_id = Payment.artist_id
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(data)
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# ------------------------------
# GET /artist_teams
@artist_manager.route('/artist_teams', methods=['GET'])
def get_artist_teams():
    cursor = db.get_db().cursor()
    query = '''
        SELECT T.*, Artist.artist_id, Artist.name
        FROM Artist
        JOIN Team T ON Artist.team_id = T.team_id
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(data)
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# ------------------------------
# Delete /artist
@artist_manager.route('/artist/<Artist_ID>', methods=['Delete'])
def delete_artist(artistID):
    cursor = db.get_db().cursor()
    current_app.logger.info('DELETED/artist/<artistID> route')
    cursor.execute('DELETE FROM Artist WHERE artist_id = %s',(artistID,))
    db.get_db().commit()
    response = make_response('Artist Deleted!')
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# ------------------------------
# Delete /schedule
@artist_manager.route('/artist/<Schedule_ID>', methods=['Delete'])
def delete_schedule(schedule_ID):
    cursor = db.get_db().cursor()
    current_app.logger.info('DELETED/Schedule/<scheduleID> route')
    cursor.execute('DELETE FROM Schedule WHERE schedule = %s',(schedule_ID,))
    db.get_db().commit()
    response = make_response('Schedule Deleted!')
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# ------------------------------
# Delete /payment
@artist_manager.route('/artist/<Payment_ID>', methods=['Delete'])
def delete_payment(payment_ID):
    cursor = db.get_db().cursor()
    current_app.logger.info('DELETED/Payment/<paymentID> route')
    cursor.execute('DELETE FROM Schedule WHERE schedule = %s',(payment_ID,))
    db.get_db().commit()
    response = make_response('Payment/Revenue Deleted!')
    response.status_code = 200
    response.mimetype = 'application/json'
    return response



# ------------------------------
#Post /revenue
@artist_manager.route('/artist/Payment_ID>', methods=['POST'])
def add_payment():
    current_app.logger.info('POST/ artist_manager route')
    payment_info = request.json
    payment_id = payment_info['payment_id']
    payment_date = payment_info['payment_date']
    payment_status = payment_info['payment_status']
    source = payment_info['source']
    amount = payment_info['amount']
    artist_id = payment_info['artist_id']

    query = 'Insert into Payment (payment_id, payment_date, payment_status, source, amount, artist_id) Values (%s, %s, %s, %s, %s, %s)'
    data = (payment_id, payment_date, payment_status, source, amount)
    cursor = db.get_db().cursor()
    r = cursor.execute(query,data)
    db.get_db().commit()
    response = make_response('Payment/Revenue Deleted!')
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# ------------------------------
#Update an artist_manager
@artist_manager.route('/artist_manager', methods = ['PUT'])
def update_artist_manager():
    current_app.logger.info('PUT /artist_manager route')
    artist_manager_info = request.json
    artist_manager_id = artist_manager_info['artist_manager_id']
    name = artist_manager_info['name']
    contact_info = artist_manager_info['contact_info']
    team_id = artist_manager_info['team_id']
    
    query = 'Update artist_manager Set artist_manager_info = %s, artist_manager_id = %s, name = %s, contact_info = %s, team_id = %s'
    data = (artist_manager_id, name, contact_info, team_id)
    
    cursor = db.get_db().cursor()
    r = cursor.execute(query,data)
    db.get_db().commit()
    return 'Artist Manager Updated!'