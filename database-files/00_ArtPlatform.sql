DROP DATABASE IF EXISTS ArtPlatformDB;
CREATE DATABASE IF NOT EXISTS ArtPlatformDB;
USE ArtPlatformDB;

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

CREATE TABLE PlatformManager (
    platform_manager_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20)
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
    approve_status VARCHAR(50),
    platform_manager_id INT,
    FOREIGN KEY (platform_manager_id) REFERENCES PlatformManager(platform_manager_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
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

