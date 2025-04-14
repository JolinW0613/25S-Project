from flask import Blueprint, request, jsonify, make_response, current_app, Response
from backend.db_connection import db
import json
from datetime import date, datetime, time, timedelta
from decimal import Decimal

artist_bp = Blueprint('artist_bp', __name__)

# ------------------------------------------------------------
# Custom JSON serializer for unsupported types (datetime, timedelta, Decimal)
def convert_json_safe(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    elif isinstance(obj, timedelta):
        return str(obj)  # Or use obj.total_seconds() if numerical format is needed
    elif isinstance(obj, Decimal):
        return float(obj)  # Or str(obj) to preserve exact value
    raise TypeError(f"Type {type(obj)} not serializable")

# ------------------------------------------------------------
# GET /<int:artist_id>/schedule
# Retrieve upcoming performance schedule for a specific artist
@artist_bp.route('/<int:artist_id>/schedule', methods=['GET'])
def get_artist_schedule(artist_id):
    current_app.logger.info(f'GET /schedule handler for artist_id: {artist_id}')
    query = """
        SELECT p.performance_id,
               p.title,
               p.performance_type,
               p.performance_date,
               p.performance_time,
               p.location
        FROM Performance p
        JOIN Contract c ON p.performance_id = c.performance_id
        WHERE c.artist_id = %s
          AND p.performance_date >= %s
        ORDER BY p.performance_date ASC
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (artist_id, '2024-03-01'))
    schedule = cursor.fetchall()
    response = Response(json.dumps(schedule, default=convert_json_safe), mimetype='application/json')
    response.status_code = 200
    return response

# ------------------------------------------------------------
# GET /<int:artist_id>/payments
# Retrieve payment records (earnings) for the specified artist
@artist_bp.route('/<int:artist_id>/payments', methods=['GET'])
def get_artist_payments(artist_id):
    current_app.logger.info(f'GET /payments handler for artist_id: {artist_id}')
    query = """
        SELECT payment_id,
               payment_date,
               payment_status,
               source,
               amount
        FROM Payment
        WHERE artist_id = %s
        ORDER BY payment_date DESC
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (artist_id,))
    payments = cursor.fetchall()
    response = Response(json.dumps(payments, default=convert_json_safe), mimetype='application/json')
    response.status_code = 200
    return response

# ------------------------------------------------------------
# PUT /<int:artist_id>/payment
# Update payment status for a given payment ID and artist
@artist_bp.route('/<int:artist_id>/payment', methods=['PUT'])
def update_artist_payment(artist_id):
    current_app.logger.info(f'PUT /payment handler for artist_id: {artist_id}')
    payment_info = request.json
    payment_id = payment_info.get('payment_id')
    new_status = payment_info.get('payment_status')

    query = """
        UPDATE Payment
        SET payment_status = %s
        WHERE payment_id = %s AND artist_id = %s
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (new_status, payment_id, artist_id))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Payment updated successfully"}))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# GET /<int:artist_id>/history
# Retrieve past performance history for the artist, including total earnings
@artist_bp.route('/<int:artist_id>/history', methods=['GET'])
def get_artist_history(artist_id):
    current_app.logger.info(f'GET /history handler for artist_id: {artist_id}')
    cutoff_date = request.args.get('cutoff', '2024-03-01')
    query = """
        SELECT p.performance_id,
               p.title,
               p.performance_type,
               p.performance_date,
               (SELECT SUM(amount)
                FROM Payment
                WHERE artist_id = %s AND source = p.title) AS total_earnings
        FROM Performance p
        JOIN Contract c ON p.performance_id = c.performance_id
        WHERE c.artist_id = %s AND p.performance_date < %s
        ORDER BY p.performance_date DESC
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (artist_id, artist_id, cutoff_date))
    history = cursor.fetchall()
    response = Response(json.dumps(history, default=convert_json_safe), mimetype='application/json')
    response.status_code = 200
    return response

# ------------------------------------------------------------
# POST /<int:artist_id>/schedule
# Create a new schedule message/notification for the artist
@artist_bp.route('/<int:artist_id>/schedule', methods=['POST'])
def create_artist_schedule(artist_id):
    current_app.logger.info(f'POST /schedule handler for artist_id: {artist_id}')
    data = request.json
    message = data.get('message')
    schedule_datetime = data.get('schedule_datetime')
    query = """
        INSERT INTO Schedule (message, schedule_datetime, artist_id)
        VALUES (%s, %s, %s)
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (message, schedule_datetime, artist_id))
    db.get_db().commit()
    response = make_response(jsonify({"message": "New schedule notification created"}))
    response.status_code = 201
    return response

# ------------------------------------------------------------
# GET /<int:artist_id>/insights
# Retrieve aggregated insights for a specified artist (grouped by performance type).
@artist_bp.route('/<int:artist_id>/insights', methods=['GET'])
def get_artist_insights(artist_id):
    current_app.logger.info(f'GET /insights handler for artist_id: {artist_id}')
    query = """
        SELECT p.performance_type,
               COUNT(*) AS num_projects,
               SUM(pay.amount) AS total_earnings,
               AVG(pay.amount) AS avg_earnings
        FROM Performance p
        JOIN Contract c ON p.performance_id = c.performance_id
        JOIN Payment pay ON pay.artist_id = c.artist_id AND pay.source = p.title
        WHERE c.artist_id = %s
        GROUP BY p.performance_type
        ORDER BY total_earnings DESC
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (artist_id,))
    insights = cursor.fetchall()
    insights = [serialize_row(row) for row in insights]
    response = make_response(jsonify(insights))
    response.status_code = 200
    return response