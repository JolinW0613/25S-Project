########################################################
# Sample investment_counsellors blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


investment_counsellor_bp = Blueprint('investment_counsellor', __name__)

@investment_counsellor_bp.route('/projects/opportunities', methods=['GET'])
def get_investment_opportunities():
    current_app.logger.info('GET /investment counsello route')
    query = """
        SELECT project_id, name, project_type, start_date, approve_status
        FROM Project
        WHERE approve_status IN ('Pending', 'Approved');
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    response = make_response(jsonify(results))
    response.status_code = 200
    return response

@investment_counsellor_bp.route('/invests/<int:investment_id>/performance', methods=['GET'])
def get_investment_performance(investment_id):
    query = """
        SELECT 
            p.project_id, p.name, p.revenue, p.budget, p.ROI, p.audience_rating,
            i.amount, i.expected_return_date, i.actual_return_date
        FROM Invests i
        JOIN Project p ON i.project_id = p.project_id
        WHERE i.investor_id = %s
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (investment_id,))
    results = cursor.fetchall()

    response = make_response(jsonify(results))
    response.status_code = 200
    return response


@investment_counsellor_bp.route('/alerts', methods=['POST'])
def create_alert():
    data = request.get_json()
    alert_time = data.get('alert_time')
    alert_type = data.get('alert_type')
    is_resolved = data.get('is_resolved', False)
    project_id = data.get('project_id')

    cursor = db.get_db().cursor()
    cursor.execute("""
        INSERT INTO Alert (alert_time, alert_type, is_resolved, project_id)
        VALUES (%s, %s, %s, %s)
    """, (alert_time, alert_type, is_resolved, project_id))
    db.get_db().commit()
    alert_id = cursor.lastrowid

    response = make_response(jsonify({'message': 'Alert created', 'alert_id': alert_id}))
    response.status_code = 201
    return response


@investment_counsellor_bp.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    data = request.get_json()
    is_resolved = data.get('is_resolved')

    if is_resolved is None:
        response = make_response(jsonify({'error': 'Missing is_resolved value'}))
        response.status_code = 400
        return response

    cursor = db.get_db().cursor()
    cursor.execute("""
        UPDATE Alert
        SET is_resolved = %s
        WHERE alert_id = %s
    """, (is_resolved, alert_id))
    db.get_db().commit()

    response = make_response(jsonify({'message': 'Alert updated'}))
    response.status_code = 200
    return response



@investment_counsellor_bp.route('/alerts/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM Alert WHERE alert_id = %s", (alert_id,))
    db.get_db().commit()

    response = make_response(jsonify({'message': 'Alert deleted'}))
    response.status_code = 200
    return response



@investment_counsellor_bp.route('/invests/<int:investor_id>/comparisons', methods=['GET'])
def compare_investment_with_industry(investor_id):
    query = """
        SELECT 
            p.project_id,
            p.name,
            p.ROI AS project_roi,
            p.revenue AS project_revenue,
            p.audience_rating AS project_audience_rating,
            b.avg_dci,
            b.audience_rate_avg,
            b.revenue_avg
        FROM Invests i
        JOIN Project p ON i.project_id = p.project_id
        LEFT JOIN Benchmark b ON p.project_id = b.project_id
        WHERE i.investor_id = %s
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (investor_id,))
    results = cursor.fetchall()

    response = make_response(jsonify(results))
    response.status_code = 200
    return response