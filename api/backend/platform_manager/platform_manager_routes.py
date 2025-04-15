########################################################
#contains 12 routes, 6 GETS (SQL Queries), 2 POSTS, 2 PUTS, 2 DELETES
########################################################

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of
# routes.
pManager = Blueprint('pManager', __name__)

#When adding to the api backend
#create a folder, platformManager
#and create platformManager.py

#or something whatever works


#routes 1-6 correspond to the SQL queries



#route 1 GET
#------------------------------------------------------------
#Purpose: To provide a comprehensive view of artist
# data (ID, name, contact info) along with their team
# and manager details, enabling the platform manager
# to verify that personal information is securely
# stored and linked to authorized personnel
@pManager.route('/artists', methods=['GET'])
def get_test1():
    query = '''
        SELECT
    a.artist_id,
    a.name AS artist_name,
    a.contact_info,
    t.name AS team_name,
    am.name AS manager_name,
    am.email AS manager_email
FROM
    Artist a
LEFT JOIN
    Team t ON a.team_id = t.team_id
LEFT JOIN
    ArtistManager am ON a.artist_id = am.artist_id
ORDER BY
    a.artist_id
    '''
   
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response


#route 2 GET
#Purpose: To list upcoming performances with their
# details (title, location, type, date/time) and
# associated project information, allowing the
# platform manager to anticipate high-traffic
# events (e.g., concerts) and ensure system
# stability by monitoring performance schedules
# in real-time.

@pManager.route('/performances', methods=['GET'])
def get_test2():
    query = '''
        SELECT
    p.performance_id,
    p.title AS performance_title,
    p.location,
    p.performance_type,
    p.description,
    p.performance_date,
    TIME_FORMAT(p.performance_time, '%H:%i:%s') AS performance_time,  -- Convert TIME to string
    pr.name AS project_name,
    pr.project_type,
    CONCAT(p.performance_date, ' ', p.performance_time) AS performance_datetime
FROM
    Performance p
INNER JOIN
    Project pr ON p.project_id = pr.project_id
WHERE
    p.performance_date >= CURDATE()
ORDER BY
    p.performance_date, p.performance_time
    '''
   
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response


#route 3 GET

#Purpose: To integrate project financials
# (revenue, budget, ROI), benchmarks
# (DCI, audience rating, revenue),
# and investment data into a real-time analytics
# report, comparing performance against industry
# standards, enabling the platform manager to
# provide users with accurate decision-making insights.


@pManager.route('/projects', methods=['GET'])
def get_test3():
    query = '''
        SELECT
    p.project_id,
    p.name AS project_name,
    p.project_type,
    p.revenue,
    p.budget,
    p.ROI,
    b.avg_dci AS benchmark_dci,
    b.audience_rate_avg AS benchmark_audience_rating,
    b.revenue_avg AS benchmark_revenue,
    SUM(i.amount) AS total_investment,
    COUNT(i.investor_id) AS investor_count,
    p.audience_rating AS current_audience_rating
FROM
    Project p
LEFT JOIN
    Benchmark b ON p.project_id = b.project_id
LEFT JOIN
    Invests i ON p.project_id = i.project_id
GROUP BY
    p.project_id, p.name, p.project_type, p.revenue, p.budget, p.ROI,
    b.avg_dci, b.audience_rate_avg, b.revenue_avg, p.audience_rating
HAVING
    p.revenue IS NOT NULL
ORDER BY
    p.revenue DESC
    '''
   
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response


#route 4 GET
#Purpose: To summarize artist details
# (name, team, manager) and their active contract count

@pManager.route('/artist_contract', methods=['GET'])
def get_test4():
    query = '''
        SELECT
    a.artist_id,
    a.name AS artist_name,
    t.name AS team_name,
    t.team_type,
    am.name AS manager_name,
    am.email AS manager_email,
    COUNT(c.contract_id) AS active_contracts
FROM
    Artist a
LEFT JOIN
    Team t ON a.team_id = t.team_id
LEFT JOIN
    ArtistManager am ON a.artist_id = am.artist_id
LEFT JOIN
    Contract c ON a.artist_id = c.artist_id
        AND c.end_date >= CURDATE()
GROUP BY
    a.artist_id, a.name, t.name, t.team_type, am.name, am.email
ORDER BY
    a.artist_id
    '''
   
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response


#route 5 GET
#Purpose: To retrieve a detailed list of projects
# (name, type, budget, revenue, ROI, status) needing
# approval, including profitability assessments and
# responsible manager details, enabling the platform
# manager to review and approve projects based on
# compliance with platform policies and financial
# viability.

@pManager.route('/project_roi', methods=['GET'])
def get_test5():
    query = '''
        SELECT
    p.project_id,
    p.name AS project_name,
    p.project_type,
    p.budget,
    p.revenue,
    p.ROI,
    p.approve_status,
    p.start_date,
    p.end_date,
    pm.name AS platform_manager_name
FROM
    Project p
LEFT JOIN
    PlatformManager pm ON p.platform_manager_id = pm.platform_manager_id
WHERE
    p.approve_status IN ('Pending', 'Under Review')
    OR p.approve_status IS NULL
ORDER BY
    p.start_date DESC
    '''
   
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response


#route 6 GET
#Purpose: To display unresolved alerts with their type,
# associated project details, time unresolved,
# allowing the platform manager to
# quickly identify and address technical issues
# reported by users, ensuring a responsive support system.

@pManager.route('/alerts', methods=['GET'])
def get_test6():
    query = '''
        SELECT
    a.alert_id,
    a.alert_time,
    a.alert_type,
    a.is_resolved,
    p.name AS project_name,
    p.project_type,
    p.approve_status,
    DATEDIFF(CURDATE(), a.alert_time) AS days_unresolved
FROM
    Alert a
INNER JOIN
    Project p ON a.project_id = p.project_id
WHERE
    a.is_resolved = FALSE
ORDER BY
    a.alert_time ASC
    '''
   
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response



#route 7 POST
#creates an Alert
@pManager.route('/alert', methods=['POST'])
def create_alert():
    """
    Create a new alert in the Alert table.
    Expects JSON body with: alert_time (required), alert_type (required), is_resolved (optional, defaults to False),
    project_id (required, must reference a valid Project).
    Returns the ID of the newly created alert.
    """
    try:
        data = request.json
        if not data or 'alert_time' not in data or 'alert_type' not in data or 'project_id' not in data:
            return make_response(jsonify({"error": "Missing required fields: alert_time, alert_type, and project_id are required"}), 400)

        alert_time = data['alert_time']
        alert_type = data['alert_type']
        is_resolved = data.get('is_resolved', False)  # Default to False if not provided
        project_id = data['project_id']

        # Validate project_id
        cursor = db.get_db().cursor()
        cursor.execute("SELECT project_id FROM Project WHERE project_id = %s", (project_id,))
        if not cursor.fetchone():
            return make_response(jsonify({"error": "Invalid project_id: Project does not exist"}), 400)

        query = '''
            INSERT INTO Alert (alert_time, alert_type, is_resolved, project_id)
            VALUES (%s, %s, %s, %s)
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (alert_time, alert_type, is_resolved, project_id))
        db.get_db().commit()

        alert_id = cursor.lastrowid
        response = make_response(jsonify({"message": "Alert created successfully", "alert_id": alert_id}))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error creating alert: {str(e)}")
        return make_response(jsonify({"error": "Failed to create alert"}), 500)

#route 8 PUT
#updates an Alert
@pManager.route('/alert/<id>', methods=['PUT'])
def update_alert(id):
    """
    Update an existing alert in the Alert table.
    Expects JSON body with: alert_time, alert_type, is_resolved, project_id (all optional, at least one required).
    """
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT alert_id FROM Alert WHERE alert_id = %s", (id,))
        if not cursor.fetchone():
            return make_response(jsonify({"error": "Alert not found"}), 404)

        data = request.json
        if not data:
            return make_response(jsonify({"error": "No update data provided"}), 400)

        alert_time = data.get('alert_time')
        alert_type = data.get('alert_type')
        is_resolved = data.get('is_resolved')
        project_id = data.get('project_id')

        # Validate project_id if provided
        if project_id is not None:
            cursor.execute("SELECT project_id FROM Project WHERE project_id = %s", (project_id,))
            if not cursor.fetchone():
                return make_response(jsonify({"error": "Invalid project_id: Project does not exist"}), 400)

        updates = []
        params = []
        if alert_time is not None:
            updates.append("alert_time = %s")
            params.append(alert_time)
        if alert_type is not None:
            updates.append("alert_type = %s")
            params.append(alert_type)
        if is_resolved is not None:
            updates.append("is_resolved = %s")
            params.append(is_resolved)
        if project_id is not None:
            updates.append("project_id = %s")
            params.append(project_id)

        if not updates:
            return make_response(jsonify({"error": "No fields to update"}), 400)

        params.append(id)
        query = f"UPDATE Alert SET {', '.join(updates)} WHERE alert_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()

        response = make_response(jsonify({"message": "Alert updated successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error updating alert: {str(e)}")
        return make_response(jsonify({"error": "Failed to update alert"}), 500)



#route 9 DELETE
#deletes an Alert
@pManager.route('/alert/<id>', methods=['DELETE'])
def delete_alert(id):
    """
    Delete an alert from the Alert table.
    """
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT alert_id FROM Alert WHERE alert_id = %s", (id,))
        if not cursor.fetchone():
            return make_response(jsonify({"error": "Alert not found"}), 404)

        query = "DELETE FROM Alert WHERE alert_id = %s"
        cursor.execute(query, (id,))
        db.get_db().commit()

        response = make_response(jsonify({"message": "Alert deleted successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error deleting alert: {str(e)}")
        return make_response(jsonify({"error": "Failed to delete alert"}), 500)



#Route 10 POST
#creates a project

@pManager.route('/project', methods=['POST'])
def create_project():
    try:
        data = request.json
        if not data or 'name' not in data:
            return make_response(jsonify({"error": "Missing required field: name"}), 400)

        name = data['name']
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        project_type = data.get('project_type')
        ROI = data.get('ROI')
        revenue = data.get('revenue')
        budget = data.get('budget')
        is_saved = data.get('is_saved', False)
        audience_rating = data.get('audience_rating')
        approve_status = data.get('approve_status')
        platform_manager_id = data.get('platform_manager_id')

        if platform_manager_id is not None:
            cursor = db.get_db().cursor()
            cursor.execute("SELECT platform_manager_id FROM PlatformManager WHERE platform_manager_id = %s", (platform_manager_id,))
            if not cursor.fetchone():
                return make_response(jsonify({"error": "Invalid platform_manager_id: Platform Manager does not exist"}), 400)

        query = '''
            INSERT INTO Project (name, start_date, end_date, project_type, ROI, revenue, budget,
                                is_saved, audience_rating, approve_status, platform_manager_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (name, start_date, end_date, project_type, ROI, revenue, budget,
                               is_saved, audience_rating, approve_status, platform_manager_id))
        db.get_db().commit()

        project_id = cursor.lastrowid
        response = make_response(jsonify({"message": "Project created successfully", "project_id": project_id}))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error creating project: {str(e)}")
        return make_response(jsonify({"error": "Failed to create project"}), 500)


#Route 11 PUT
#updates project

@pManager.route('/project/<id>', methods=['PUT'])
def update_project(id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT project_id FROM Project WHERE project_id = %s", (id,))
        if not cursor.fetchone():
            return make_response(jsonify({"error": "Project not found"}), 404)

        data = request.json
        if not data:
            return make_response(jsonify({"error": "No update data provided"}), 400)

        name = data.get('name')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        project_type = data.get('project_type')
        ROI = data.get('ROI')
        revenue = data.get('revenue')
        budget = data.get('budget')
        is_saved = data.get('is_saved')
        audience_rating = data.get('audience_rating')
        approve_status = data.get('approve_status')
        platform_manager_id = data.get('platform_manager_id')

        if platform_manager_id is not None:
            cursor.execute("SELECT platform_manager_id FROM PlatformManager WHERE platform_manager_id = %s", (platform_manager_id,))
            if not cursor.fetchone():
                return make_response(jsonify({"error": "Invalid platform_manager_id: Platform Manager does not exist"}), 400)

        updates = []
        params = []
        if name is not None:
            updates.append("name = %s")
            params.append(name)
        if start_date is not None:
            updates.append("start_date = %s")
            params.append(start_date)
        if end_date is not None:
            updates.append("end_date = %s")
            params.append(end_date)
        if project_type is not None:
            updates.append("project_type = %s")
            params.append(project_type)
        if ROI is not None:
            updates.append("ROI = %s")
            params.append(ROI)
        if revenue is not None:
            updates.append("revenue = %s")
            params.append(revenue)
        if budget is not None:
            updates.append("budget = %s")
            params.append(budget)
        if is_saved is not None:
            updates.append("is_saved = %s")
            params.append(is_saved)
        if audience_rating is not None:
            updates.append("audience_rating = %s")
            params.append(audience_rating)
        if approve_status is not None:
            updates.append("approve_status = %s")
            params.append(approve_status)
        if platform_manager_id is not None:
            updates.append("platform_manager_id = %s")
            params.append(platform_manager_id)

        if not updates:
            return make_response(jsonify({"error": "No fields to update"}), 400)

        params.append(id)
        query = f"UPDATE Project SET {', '.join(updates)} WHERE project_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()

        response = make_response(jsonify({"message": "Project updated successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error updating project: {str(e)}")
        return make_response(jsonify({"error": "Failed to update project"}), 500)


##Route 12 DELETE
#Deletes a project
@pManager.route('/project/<id>', methods=['DELETE'])
def delete_project(id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT project_id FROM Project WHERE project_id = %s", (id,))
        if not cursor.fetchone():
            return make_response(jsonify({"error": "Project not found"}), 404)

        query = "DELETE FROM Project WHERE project_id = %s"
        cursor.execute(query, (id,))
        db.get_db().commit()

        response = make_response(jsonify({"message": "Project deleted successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error deleting project: {str(e)}")
        return make_response(jsonify({"error": "Failed to delete project"}), 500)