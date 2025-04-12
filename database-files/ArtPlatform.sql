SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `ArtPlatformDB` ;
CREATE SCHEMA IF NOT EXISTS `ArtPlatformDB` DEFAULT CHARACTER SET latin1 ;
USE `ArtPlatformDB` ;

CREATE TABLE Team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(200),
    team_type VARCHAR(50),
    team_lead_id INT
);

CREATE TABLE Artist (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(200),
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE ArtistManager (
    artist_manager_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


CREATE TABLE Project (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    project_type VARCHAR(50),
    ROI DECIMAL(10, 2),
    revenue DECIMAL(10, 2),
    budget DECIMAL(10, 2),
    is_saved BOOLEAN,
    audience_rating DECIMAL(3, 1),
    approve_status VARCHAR(50)
);

CREATE TABLE Performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100),
    title VARCHAR(100),
    performance_type VARCHAR(50),
    description TEXT,
    performance_time TIME,
    performance_date DATE,
    project_id INT,
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Contract (
    contract_id INT AUTO_INCREMENT PRIMARY KEY,
    contract_type VARCHAR(50),
    contract_terms TEXT,
    start_date DATE,
    end_date DATE,
    revenue_share DECIMAL(5,2),
    artist_id INT,
    performance_id INT,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (performance_id) REFERENCES Performance(performance_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    payment_date DATE,
    payment_status VARCHAR(50),
    source VARCHAR(100),
    amount DECIMAL(10,2),
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE Investor (
    investor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE Invests (
    investor_id INT,
    project_id INT,
    amount DECIMAL(10,2),
    expected_return_date DATE,
    actual_return_date DATE,
    PRIMARY KEY (investor_id, project_id),
    FOREIGN KEY (investor_id) REFERENCES Investor(investor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Alert (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    alert_time DATETIME,
    alert_type VARCHAR(50),
    is_resolved BOOLEAN,
    project_id INT,
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Schedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(200),
    schedule_datetime DATETIME,
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Benchmark (
    benchmark_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    avg_dci DECIMAL(10,2),
    audience_rate_avg DECIMAL(5,2),
    revenue_avg DECIMAL(10,2),
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE PlatformManager (
    platform_manager_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20)
);

ALTER TABLE Project
ADD COLUMN platform_manager_id INT,
ADD CONSTRAINT fk_project_platmng
    FOREIGN KEY (platform_manager_id) REFERENCES PlatformManager(platform_manager_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

INSERT INTO ArtistManager (name, email, phone)
VALUES
    ('Alice', 'alice@manager.com', '123-456-7890'),
    ('Bob',   'bob@manager.com',   '234-567-8901');

INSERT INTO Team (name, contact_info, team_type, team_lead_id)
VALUES
    ('Team Alpha', 'alpha@example.com', 'Music', 1),
    ('Team Beta',  'beta@example.com',  'Dance', 2);

INSERT INTO PlatformManager (name, email, phone)
VALUES
    ('Alice Johnson', 'alice.johnson@example.com', '123-456-7890'),
    ('Bob Smith', 'bob.smith@example.com', '234-567-8901');

INSERT INTO Project (
    name,
    start_date,
    end_date,
    project_type,
    ROI,
    revenue,
    budget,
    is_saved,
    audience_rating,
    approve_status
)
VALUES
    (
      'Project Phoenix',
      '2025-01-01',
      '2025-06-30',
      'Film',
      1.25,
      100000.00,
      80000.00,
      TRUE,
      8.5,
      'Approved'
    ),
    (
      'Project Mercury',
      '2025-03-15',
      '2025-09-15',
      'Concert',
      1.10,
      50000.00,
      40000.00,
      FALSE,
      7.8,
      'Pending'
    );

INSERT INTO Artist (name, contact_info, team_id)
VALUES
    ('John Doe', 'john@example.com', 1),
    ('Jane Smith', 'jane@example.com', 2);


INSERT INTO Performance (
    location,
    title,
    performance_type,
    description,
    performance_time,
    performance_date,
    project_id
)
VALUES
    (
      'New York Theater',
      'Broadway Showcase',
      'Theater',
      'A special Broadway performance.',
      '19:30:00',
      '2025-04-10',
      1
    ),
    (
      'LA Concert Hall',
      'Pop Music Night',
      'Music Concert',
      'Featuring various pop artists.',
      '20:00:00',
      '2025-05-01',
      2
    );

INSERT INTO Contract (
    contract_type,
    contract_terms,
    start_date,
    end_date,
    revenue_share,
    artist_id,
    performance_id
)
VALUES
    (
      'Exclusive',
      'Term: 6 months, includes X% revenue share.',
      '2025-01-15',
      '2025-07-15',
      15.00,
      1,
      1
    ),
    (
      'Non-Exclusive',
      'Term: 3 months, includes Y% revenue share.',
      '2025-02-01',
      '2025-05-01',
      10.00,
      2,
      2
    );

INSERT INTO Payment (
    payment_date,
    payment_status,
    source,
    amount,
    artist_id
)
VALUES
    (
      '2025-03-01',
      'Completed',
      'Box Office',
      5000.00,
      1
    ),
    (
      '2025-03-15',
      'Pending',
      'Sponsor',
      3000.00,
      2
    );

INSERT INTO Investor (name, email, phone)
VALUES
    ('InvestCorp', 'corp@example.com', '987-654-3210'),
    ('PrivateAngel', 'angel@example.com', '876-543-2109');

INSERT INTO Invests (
    investor_id,
    project_id,
    amount,
    expected_return_date,
    actual_return_date
)
VALUES
    (
      1,
      1,
      20000.00,
      '2025-08-01',
      NULL
    ),
    (
      2,
      2,
      15000.00,
      '2025-10-01',
      NULL
    );

INSERT INTO Alert (
    alert_time,
    alert_type,
    is_resolved,
    project_id
)
VALUES
    (
      '2025-04-01 10:00:00',
      'BudgetOverrun',
      FALSE,
      1
    ),
    (
      '2025-04-15 15:30:00',
      'DelayedSchedule',
      FALSE,
      2
    );

INSERT INTO Schedule (
    message,
    schedule_datetime,
    artist_id
)
VALUES
    (
      'Rehearsal for the Broadway Showcase',
      '2025-04-08 14:00:00',
      1
    ),
    (
      'Sound check for the Pop Music Night',
      '2025-04-30 18:00:00',
      2
    );

INSERT INTO Benchmark (
    project_id,
    avg_dci,
    audience_rate_avg,
    revenue_avg
)
VALUES
    (
      1,
      75.50,
      8.0,
      90000.00
    ),
    (
      2,
      65.20,
      7.5,
      45000.00
    );


-- Queries for Investment Counsellor
# 1.1 This query will help investors to check what kind of projects are in the market so far, including their prject name
# start_date, end_date, project_type, and approve_status.
SELECT project_id, name, start_date, end_date, project_type, approve_status
FROM Project
WHERE approve_status IN ('Approved', 'Pending');

# 1.2 CREATE: Insert a new project (Project Z) into the Project table
INSERT INTO Project (name, start_date, end_date, project_type, ROI, revenue, budget, is_saved, audience_rating, approve_status)
VALUES ('Project Q', '2025-04-01', '2025-12-31', 'Technology', 15.50, 500000.00, 350000.00, TRUE, 8.5, 'Pending');


# 2. This query will help investors check the project they have already invested, including project ROI, audience rating
SELECT p.project_id, p.name, p.budget, p.revenue, p.audience_rating, p.ROI
FROM Project p
JOIN Invests i ON p.project_id = i.project_id
WHERE i.investor_id = 1;



# 3. Track artist performance, audience engagement and market demand in real time.
SELECT a.artist_id, a.name, pe.title, pe.performance_date, pe.location, pe.performance_type
FROM Performance pe
JOIN Contract c ON pe.performance_id = c.performance_id
JOIN Artist a ON c.artist_id = a.artist_id;


# 4.1 This query will help investor check if any projects are running over
# budget by comparing the actual revenue to the budget and calculating the return on investment (ROI).
SELECT
    distinct p.name AS Project_Name,
    p.budget AS Budget,
    p.revenue AS Revenue,
    ROUND((p.revenue - p.budget) / p.budget * 100, 2) AS Budget_Overrun_Percentage,
    p.ROI AS ROI
FROM
    Project p
WHERE
    p.revenue > p.budget;

# 4.2 This query will allow investor to track the audience reception by comparing the
# actual audience ratings with the project’s expected benchmarks.
SELECT
    distinct p.name AS Project_Name,
    p.audience_rating AS Audience_Rating,
    b.audience_rate_avg AS Benchmark_Audience_Rating,
    ROUND(p.audience_rating - b.audience_rate_avg, 2) AS Rating_Difference
FROM
    Project p
JOIN
    Benchmark b ON p.project_id = b.project_id
WHERE
    p.audience_rating < b.audience_rate_avg;

# 4.3 This query allows investors to compare the performance of their current investment with similar projects in the industry
# to assess trends, profitability, and investment decisions.
SELECT
    distinct p.name AS Project_Name,
    p.revenue AS Revenue,
    p.budget AS Budget,
    b.revenue_avg AS Industry_Avg_Revenue,
    b.avg_dci AS Industry_Avg_DCI,
    ROUND((p.revenue - b.revenue_avg) / b.revenue_avg * 100, 2) AS Performance_Comparison_Percentage
FROM
    Project p
JOIN
    Benchmark b ON p.project_id = b.project_id
WHERE
    p.revenue > b.revenue_avg;


# 5. Compare the performance of investors' investment projects with similar projects in the industry
SELECT p.project_id, p.name, p.revenue, p.audience_rating, b.revenue_avg, b.audience_rate_avg
FROM Project p
JOIN Invests i ON p.project_id = i.project_id
JOIN Benchmark b ON p.project_id = b.project_id
WHERE i.investor_id = 2;

# 6. Automatically alert investors to key events (production delays, award nominations, changes in audience engagement)
SELECT alert_id, alert_time, alert_type, is_resolved, project_id
FROM Alert
WHERE project_id IN (SELECT project_id FROM Invests WHERE investor_id = 3)
AND is_resolved = FALSE;


-- Queries for Artist
# 1. View Upcoming Schedule in Real-Time
-- This query retrieves all future performance commitments for Artist 1 by joining the Performance and Contract tables
-- Assume today's date is 2024-03-01'.
SELECT p.performance_id,
       p.title,
       p.performance_type,
       p.performance_date,
       p.performance_time,
       p.location
FROM Performance p
JOIN Contract c ON p.performance_id = c.performance_id
WHERE c.artist_id = 1
  AND p.performance_date >= '2024-03-01'
ORDER BY p.performance_date ASC;

# 2. Receive Immediate Notifications
-- This query selects notifications (stored in the Schedule table) for Artist 1.
-- These records serve as schedule update alerts.
SELECT schedule_id,
       message,
       schedule_datetime
FROM Schedule
WHERE artist_id = 1
ORDER BY schedule_datetime DESC;
-- CREATE: Insert a new schedule notification for Artist 1
INSERT INTO Schedule (message, schedule_datetime, artist_id)
VALUES ('New rehearsal scheduled for tomorrow at 10:00 AM. Please check your calendar.', '2024-03-02 10:00:00', 1);
-- Test whether insert successfully
SELECT *
FROM Schedule
WHERE artist_id = 1;

# 3. See Detailed Breakdown of Earnings per Project
-- This query lists payment records for Artist 1 from the Payment table,
-- showing when each payment was made, its status, source, and amount.
SELECT payment_id,
       payment_date,
       payment_status,
       source,
       amount
FROM Payment
WHERE artist_id = 1
ORDER BY payment_date DESC;

# 4. UPDATE Payment
-- For example, if Artist 1 wants to confirm a payment record
-- this query sets the payment status to 'CONFIRMED' for a given payment (here, payment_id = 1)
UPDATE Payment
SET payment_status = 'CONFIRMED'
WHERE payment_id = 1
  AND artist_id = 1;

# 5. Access Historical Data on Past Projects
-- This query retrieves past performances (with dates before '2025-04-01') for Artist 1.
-- It includes a subquery that calculates total earnings (if any) for each performance by summing amounts from the Payment table.
-- (If no matching payment exists, the result will be NULL.)
SELECT p.performance_id,
       p.title,
       p.performance_type,
       p.performance_date,
       (SELECT SUM(amount)
        FROM Payment
        WHERE artist_id = 1
          AND source = p.title) AS total_earnings
FROM Performance p
JOIN Contract c ON p.performance_id = c.performance_id
WHERE c.artist_id = 1
  AND p.performance_date < '2025-04-01'
ORDER BY p.performance_date DESC;

# 6. Personalized Insights & Recommendations
-- This aggregation query groups performances by type for Artist 1.
-- It counts the number of projects and calculates the sum and average of payment amounts.
-- (If no payments exist for a group, SUM and AVG will return NULL.)
SELECT p.performance_type,
       COUNT(*) AS num_projects,
       SUM(pay.amount) AS total_earnings,
       AVG(pay.amount) AS avg_earnings
FROM Performance p
JOIN Contract c ON p.performance_id = c.performance_id
LEFT JOIN Payment pay ON pay.artist_id = c.artist_id
                      AND pay.source = p.title
WHERE c.artist_id = 1
GROUP BY p.performance_type
ORDER BY total_earnings DESC;
