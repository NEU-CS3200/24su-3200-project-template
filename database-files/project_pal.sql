-- Create The project_pal schema
DROP DATABASE IF EXISTS Project_pal;
CREATE DATABASE IF NOT EXISTS Project_pal;
USE Project_pal;

-- Department Table
CREATE TABLE IF NOT EXISTS Department (
    dept_id INT AUTO_INCREMENT,
    deptName VARCHAR(75) NOT NULL,
    PRIMARY KEY (dept_id)
);

-- Professor Table
CREATE TABLE IF NOT EXISTS Professor (
    professor_id INT AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    dept_id INT,
    office_location VARCHAR(100),
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
                                     ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (professor_id)
);

-- Class Table
CREATE TABLE IF NOT EXISTS Class (
    course_id INT AUTO_INCREMENT,
    course_name VARCHAR(55),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
        ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (course_id)
);

-- Section Table (Weak Entity to Class)
CREATE TABLE IF NOT EXISTS Section (
    section_num INT NOT NULL,
    semester_year VARCHAR(25) NOT NULL,
    course_id INT NOT NULL,
    professor_id INT,
    FOREIGN KEY (course_id) REFERENCES Class(course_id)
                                   ON UPDATE restrict ON DELETE restrict,
    FOREIGN KEY (professor_id) REFERENCES Professor(professor_id)
                                   ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (section_num, semester_year, course_id),
    UNIQUE (course_id, semester_year, section_num)
);

-- Project Table
CREATE TABLE IF NOT EXISTS Project (
    project_id INT AUTO_INCREMENT,
    instructions TEXT,
    professor_id INT,
    FOREIGN KEY (professor_id) REFERENCES Professor(professor_id)
        ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (project_id)
);

-- TA Table
CREATE TABLE IF NOT EXISTS TA (
    ta_id INT AUTO_INCREMENT UNIQUE,
    first_name VARCHAR(75) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    email VARCHAR(75),
    section_num INT NOT NULL,
    semester_year varchar(25) NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY(course_id, semester_year, section_num) REFERENCES Section(course_id, semester_year, section_num)
                                   ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (ta_id)
);

-- TA Speciality Table (Multivalued Attribute)
CREATE TABLE IF NOT EXISTS TASpeciality (
    ta_id INT PRIMARY KEY,
    speciality_description VARCHAR(255),
    FOREIGN KEY (ta_id) REFERENCES TA(ta_id) ON UPDATE restrict ON DELETE restrict
);

-- Group Table
CREATE TABLE IF NOT EXISTS `Group` (
    group_id INT AUTO_INCREMENT,
    group_name VARCHAR(100) NOT NULL,
    ta_id INT,
    section_num INT NOT NULL,
    semester_year varchar(25) NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (ta_id) REFERENCES TA(ta_id)
                                   ON UPDATE restrict ON DELETE restrict,
    FOREIGN KEY(course_id, semester_year, section_num) REFERENCES Section(course_id, semester_year, section_num)
                                   ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (group_id)
);

-- Submission Table (Weak Entity to Group)
CREATE TABLE IF NOT EXISTS Submission (
    submission_id INT AUTO_INCREMENT,
    group_id INT,
    submitted_at DATETIME,
    submission_link VARCHAR(100),
    project_id INT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
        ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (submission_id, group_id)
);

-- Student Table
CREATE TABLE IF NOT EXISTS Student (
    student_id INT AUTO_INCREMENT NOT NULL,
    first_name VARCHAR(75) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    email VARCHAR(75) NOT NULL UNIQUE,
    major VARCHAR(75),
    year INT,
    on_campus BOOLEAN,
    group_id INT,
    FOREIGN KEY (group_id) REFERENCES `Group`(group_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    PRIMARY KEY (student_id)
);

-- Student Speciality Table (Multivalued Attribute)
CREATE TABLE IF NOT EXISTS StudentSpeciality (
    student_id INT PRIMARY KEY,
    speciality_description VARCHAR(255),
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
        ON UPDATE restrict ON DELETE restrict
);

-- StudentSection Table (Bridge Table)
CREATE TABLE IF NOT EXISTS StudentSection (
    student_id INT,
    course_id INT,
    semester_year VARCHAR(25),
    section_num INT,
    FOREIGN KEY (course_id, semester_year, section_num)
        REFERENCES Section(course_id, semester_year, section_num)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY (student_id)
        REFERENCES Student(student_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    PRIMARY KEY (student_id, course_id, semester_year, section_num)
);

-- Days Table (Part of Availability Composite Attribute)
CREATE TABLE IF NOT EXISTS Days (
    day_id INT AUTO_INCREMENT PRIMARY KEY,
    day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday') NOT NULL
);

-- Time Table (Part of Availability Composite Attribute)
CREATE TABLE IF NOT EXISTS Time (
    time_id INT AUTO_INCREMENT PRIMARY KEY,
    time ENUM('Morning', 'Afternoon', 'Night') NOT NULL
);

-- Location Table (Part of Availability Composite Attribute)
CREATE TABLE IF NOT EXISTS Location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255) NOT NULL
);

-- Availability Table
CREATE TABLE IF NOT EXISTS Availability (
    availability_id INT AUTO_INCREMENT,
    location_id INT,
    day_id INT NOT NULL,
    time_id INT,
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
        ON UPDATE restrict ON DELETE restrict,
    FOREIGN KEY (day_id) REFERENCES Days(day_id)
        ON UPDATE restrict ON DELETE restrict,
    FOREIGN KEY (time_id) REFERENCES Time(time_id)
        ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (availability_id)
);

-- StudentAvailability Table (Bridge Table)
CREATE TABLE IF NOT EXISTS StudentAvailability (
    availability_id INT NOT NULL,
    student_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
        ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (availability_id, student_id)
);

-- TAAvailability Table (Bridge Table)
CREATE TABLE IF NOT EXISTS TAAvailability (
    availability_id INT NOT NULL,
    ta_id INT NOT NULL,
    FOREIGN KEY (ta_id) REFERENCES TA(ta_id)
        ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (availability_id, ta_id)
);

-- Department Data
INSERT INTO Department (deptName)
VALUES ('Computer Science'),
       ('Finance'),
       ('Chemistry'),
       ('Marketing'),
       ('Public Relations'),
       ('Physics'),
       ('International Business'),
       ('Information Science'),
       ('Bioengineering'),
       ('Chemical Engineering'),
       ('Civil Engineering'),
       ('Industrial Engineering'),
       ('Nursing'),
       ('Hisotry'),
       ('Communications');

-- Professor Data
INSERT INTO Professor(first_name, last_name, email, dept_id, office_location)
VALUES ('Mark', 'Fontenot', 'm.fontenot@northeastern.edu', 1, 'WVH 115'),
       ('Sally', 'Fields', 'fields.sa@northeastern.edu', 2, 'Hayden 302'),
       ('Patrick', 'Thompson', 'pa.thompson@northeastern.edu', 3, 'Mugar 112'),
       ('Sara', 'Klein', 's.klein@northeastern.edu', 3, 'Mugar 223'),
       ('Matt', 'James', 'm.james@northestern.edu', 3, 'Churchill 102'),
       ('Normie', 'Hollyer', 'nhollyer0@paypal.com', 25, 'Adams Building'),
       ('Holt', 'Anderton', 'handerton1@mac.com', 9, 'Dodge Hall'),
       ('Marne', 'Swainsbury', 'mswainsbury2@skype.com', 26, 'Adams Building'),
       ('Brear', 'Roberds', 'broberds3@squidoo.com', 3, 'Dodge Hall'),
       ('Ileana', 'Scarr', 'iscarr4@guardian.co.uk', 1, 'Dodge Hall'),
       ('Nan', 'Tully', 'ntully5@trellian.com', 27, 'Wilson Hall'),
       ('Janeta', 'Banbury', 'jbanbury6@naver.com', 18, 'Parker Center'),
       ('Kippie', 'Redsull', 'kredsull7@flavors.me', 20, 'Wilson Hall'),
       ('Clim', 'Frid', 'cfrid8@blogspot.com', 20, 'Johnson Center'),
       ('Jonas', 'Swigger', 'jswigger9@e-recht24.de', 1, 'Johnson Center'),
       ('Berty', 'Pittle', 'bpittlea@pcworld.com', 27, 'Grant Hall'),
       ('Winifred', 'Comizzoli', 'wcomizzolib@drupal.org', 11, 'Adams Building'),
       ('Michelina', 'Boulton', 'mboultonc@dailymail.co.uk', 18, 'Grant Hall'),
       ('Philippine', 'Binnion', 'pbinniond@nbcnews.com', 27, 'Clark Hall'),
       ('Margo', 'Van Waadenburg', 'mvanwaadenburge@hp.com', 24, 'Smith Building'),
       ('Lorraine', 'Chesterfield', 'lchesterfieldf@marketwatch.com', 2, 'Parker Center'),
       ('Adella', 'Fannin', 'afanning@house.gov', 8, 'Parker Center'),
       ('Yolane', 'Caldero', 'ycalderoh@hhs.gov', 11, 'Forsyth Hall'),
       ('Francyne', 'Wartonby', 'fwartonbyi@ibm.com', 20, 'Johnson Center'),
       ('Izaak', 'Meadowcroft', 'imeadowcroftj@google.it', 15, 'Dodge Hall');

-- Class Data
INSERT INTO Class(course_name, dept_id)
VALUES ('Database Design', 1),
       ('Organic Chemistry', 3),
       ('Investments', 2),
       ('Introduction to Psychology', 1),
       ('Advanced Calculus', 2),
       ('History of Art', 3),
       ('Digital Marketing Strategies', 4),
       ('Creative Writing Workshop', 5),
       ('Environmental Science and Sustainability', 6),
       ('Introduction to Astrophysics', 7),
       ('Fashion Design Fundamentals', 8),
       ('Music Theory and Composition', 9),
       ('Entrepreneurship and Innovation', 10)
;
# --- need to change department ids

-- Section Data
INSERT INTO Section(course_id, semester_year, section_num, professor_id)
VALUES (1, 'Fall 2024', 1, 1),
       (3, 'Spring 2025', 1, 2),
       (2, 'Fall 2024', 1, 3),
       (2, 'Fall 2024', 2, 4),
       (2, 'Spring 2025', 1, 5);

-- Project Data
INSERT INTO Project(instructions, professor_id)
VALUES ('Make a functional data-driven application and be original!', 1),
       ('Get ready for this collaborative lab report,it is worth 50% of your grade', 3),
       ('See the linked instructions doc for the final risk management group project', 2);

-- TA Data
INSERT INTO TA(first_name, last_name, email, section_num, semester_year, course_id)
VALUES ('Timmy', 'Johnson', 'johnson.ti@northeastern,edu', 1, 'Fall 2024', 1),
       ('Charlotte', 'Smith', 'smith.ch@northeastern.edu', 1, 'Fall 2024', 2),
       ('Katie', 'OBrian', 'obrian.kate@northeastern.edu', 1, 'Spring 2025', 3);

-- TA Specialty Data
INSERT INTO TASpeciality(ta_id, speciality_description)
VALUES (1, 'Python, JavaScript, Object-Oriented Design, Data Analysis, React'),
       (2, 'Accounting, Risk management, investments'),
       (3, 'wet lab experience, data analysis, organic chemistry');

-- Group Data
INSERT INTO `Group` (group_name, ta_id, section_num, semester_year, course_id)
VALUES ('Team Green', 1, 1, 'Fall 2024', 1),
       ('WeLoveChem', 3, 1, 'Spring 2025', 3),
       ('FinanceBros', 2, 1, 'Fall 2024', 2);

-- Submission Data
INSERT INTO Submission (group_id, submitted_at, submission_link, project_id)
VALUES (1, '2024-08-16 10:45:28', 'projecturl1.com', 1),
       (2, '2024-08-12 09:18:57', 'finaproject.com', 2);
INSERT INTO Submission (group_id, submitted_at, project_id)
VALUES (3, '2024-09-30 06:22:30', 3);

-- Student Data
INSERT INTO Student(first_name, last_name, email, major, year, on_campus, group_id)
VALUES ('John', 'Doe', 'doe.jo@northeastern.edu', 'Computer Science', 3, True, 1),
       ('Sabrina', 'Williams', 'williams.sab@northeastern.edu', 'Marketing', 2, False, 1),
       ('Tom', 'Williams', 'williams.tom@northeastern.edu', 'Finance', 2, False, 1),
       ('Carrie', 'Smith', 'smith.car@northeastern.edu', 'Accounting', 2, True, 1),
       ('Daryl', 'Candace', 'candace.da@northeatern.edu', 'Neuroscience', 1, True, 2);

-- Student Specialty Data
INSERT INTO StudentSpeciality(student_id, speciality_description)
VALUES (1, 'Python, Java, C++, React, Streamlit, SQL'),
       (2, 'Canva, Figma, Branding'),
       (3, 'Risk management, trading, Excel, financial accounting');

-- Student Section Data
INSERT INTO StudentSection(student_id, section_num, course_id, semester_year)
VALUES (1, 1, 1, 'Fall 2024'),
       (2, 1, 2, 'Fall 2024'),
       (3, 1, 2, 'Fall 2024'),
       (4, 1, 2, 'Fall 2024'),
       (5, 1, 3, 'Spring 2025');

-- Days Data
INSERT INTO Days(day)
VALUES ('Monday'),
       ('Tuesday'),
       ('Wednesday'),
       ('Thursday'),
       ('Friday'),
       ('Saturday'),
       ('Sunday');

-- Time Data
INSERT INTO Time(time)
VALUES ('Morning'),
       ('Afternoon'),
       ('Night');

-- Location Data
INSERT INTO Location(location)
VALUES ('Snell'),
       ('Curry'),
       ('ISEC'),
       ('EXP'),
       ('Law Library'),
       ('Boston Public Library');

-- Availability Data
INSERT INTO Availability(location_id, day_id, time_id)
VALUES (1, 1, 1), -- snell, monday morning
       (1, 5, 3), -- snell friday night
       (3, 2, 2),
       (4, 3, 1),
       (6, 6, 2);
INSERT INTO Availability(day_id, time_id)
VALUES (2, 1), -- location can be null (undecided)
       (3, 2),
       (5, 1);

-- StudentAvailability Data
INSERT INTO StudentAvailability(availability_id, student_id)
VALUES (1, 1),
       (3, 1),
       (2, 2),
       (3, 2),
       (1, 3),
       (5, 3),
       (1, 4),
       (2, 4),
       (2, 5);

-- TAAvailability Data
INSERT INTO TAAvailability(availability_id, ta_id)
VALUES (1, 2),
       (1, 3),
       (5, 1),
       (8, 2),
       (7, 1);

-- example query of getting ta and student emails who are available on the same day, time, & location
SELECT t.ta_id, t.email, s.student_id, s.email
FROM (
    SELECT ta.ta_id, sa.student_id
    FROM TAAvailability ta
    JOIN StudentAvailability sa ON ta.availability_id = sa.availability_id
) AS availability_data
JOIN TA t ON t.ta_id = availability_data.ta_id
JOIN Student s ON s.student_id = availability_data.student_id;

-- find group mates in my section who live on campus
SELECT s.student_id, email AS potential_groupmates
FROM StudentSection ss JOIN Student s ON ss.student_id = s.student_id
WHERE course_id = 2 AND semester_year = 'Fall 2024' AND s.on_campus IS TRUE;
-- As a CS3200 TA, I need to be assigned to students who need help in an area that I specialize in so I can be of the most use to them.
SELECT ss.student_id, s.email FROM Student s JOIN StudentSpeciality ss ON ss.student_id = s.student_id
WHERE ss.speciality_description NOT LIKE '%python%' AND ss.speciality_description NOT LIKE '%SQL%';