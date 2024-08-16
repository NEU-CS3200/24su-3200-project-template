-- Create The project_pal schema
DROP DATABASE IF EXISTS Project_pal;
CREATE DATABASE IF NOT EXISTS Project_pal;
USE Project_pal;

-- Department Table
CREATE TABLE IF NOT EXISTS Department (
    dept_id INT AUTO_INCREMENT,
    deptName VARCHAR(75) NOT NULL UNIQUE,
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
    course_name VARCHAR(55) UNIQUE,
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
    email VARCHAR(75) UNIQUE,
    section_num INT NOT NULL,
    semester_year varchar(25) NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY(course_id, semester_year, section_num) REFERENCES Section(course_id, semester_year, section_num)
                                   ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (ta_id)
);

-- Speciality Table
CREATE TABLE IF NOT EXISTS Speciality (
    specialty_id INT AUTO_INCREMENT PRIMARY KEY,
    speciality VARCHAR(25)
);

-- TASpecialty Table
CREATE TABLE IF NOT EXISTS TASpecialty(
    ta_id INT,
    specialty_id INT,
    FOREIGN KEY (ta_id) REFERENCES TA(ta_id) ON UPDATE restrict ON DELETE restrict,
    FOREIGN KEY (specialty_id) REFERENCES Speciality(specialty_id) ON UPDATE restrict ON DELETE restrict
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
    submission_link VARCHAR(100) NOT NULL,
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
    student_id INT,
    specialty_id INT,
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON UPDATE restrict ON DELETE restrict,
    FOREIGN KEY (specialty_id) REFERENCES Speciality(specialty_id) ON UPDATE restrict ON DELETE restrict
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

-- Availability Table
CREATE TABLE IF NOT EXISTS Availability (
    availability_id INT AUTO_INCREMENT,
    day_id INT NOT NULL,
    time_id INT,
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
    FOREIGN KEY (availability_id) REFERENCES Student(student_id) ON UPDATE restrict ON DELETE restrict,
    FOREIGN KEY (availability_id) REFERENCES Availability(availability_id) ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (availability_id, student_id)
);

-- TAAvailability Table (Bridge Table)
CREATE TABLE IF NOT EXISTS TAAvailability (
    availability_id INT NOT NULL,
    ta_id INT NOT NULL,
    FOREIGN KEY (ta_id) REFERENCES TA(ta_id) ON UPDATE restrict ON DELETE restrict,
    FOREIGN KEY (availability_id) REFERENCES Availability(availability_id) ON UPDATE restrict ON DELETE restrict,
    PRIMARY KEY (availability_id, ta_id)
);

-- Department Data
INSERT INTO Department (deptName)
VALUES ('Computer Science'), ('Mathematics'), ('Biology'),
       ('Chemistry'), ('Physics'), ('Economics'),
       ('Psychology'), ('Political Science'), ('Sociology'),
       ('Anthropology'), ('History'), ('English Literature'),
       ('Philosophy'), ('Art History'), ('Business Administration'),
       ('Environmental Science'), ('Mechanical Engineering'),
       ('Electrical Engineering'), ('Communication Studies'), ('Linguistics');

-- Professor Data
INSERT INTO Professor (first_name, last_name, email, dept_id, office_location)
VALUES ('Mark', 'Fontenot', 'm.fontenot@northeastern.edu', 1, 'Mugar Hall'),
       ('Pietra', 'Ramsey', 'pramsey0@wunderground.com', 15, 'Forsyth Hall'),
       ('Nikola', 'Pock', 'npock1@wiley.com', 4, 'Adams Building'),
       ('Sacha', 'Winnister', 'swinnister2@rambler.ru', 6, 'Adams Building'),
       ('Burke', 'Goforth', 'bgoforth3@google.ru', 4, 'Dodge Hall'),
       ('Win', 'Sparshatt', 'wsparshatt4@youtube.com', 8, 'Adams Building'),
       ('Debra', 'Piniur', 'dpiniur5@sfgate.com', 5, 'Wilson Hall'),
       ('Yanaton', 'Pescud', 'ypescud6@digg.com', 10, 'Parker Center'),
       ('Eada', 'Carrington', 'ecarrington7@1688.com', 17, 'Wilson Hall'),
       ('Bettine', 'Southerton', 'bsoutherton8@ocn.ne.jp', 3, 'Dodge Hall'),
       ('Griz', 'Pusill', 'gpusill9@latimes.com', 17, 'Clark Hall'),
       ('Serge', 'Kitchaside', 'skitchasidea@comsenz.com', 8, 'Forsyth Hall'),
       ('Veronike', 'Meletti', 'vmelettib@wikimedia.org', 4, 'Smith Building'),
       ('Renato', 'Mellor', 'rmellorc@disqus.com', 10, 'Grant Hall'),
       ('Zoe', 'Vayro', 'zvayrod@wordpress.com', 9, 'Forsyth Hall'),
       ('Octavia', 'Terzo', 'oterzoe@loc.gov', 5, 'Taylor Hall'),
       ('Dorthy', 'Shelbourne', 'dshelbournef@hibu.com', 14, 'Adams Building'),
       ('Adey', 'Postles', 'apostlesg@clickbank.net', 12, 'Taylor Hall'),
       ('Laurie', 'Daines', 'ldainesh@hp.com', 4, 'Johnson Center'),
       ('Adriane', 'Genn', 'agenni@noaa.gov', 4, 'Taylor Hall'),
       ('Amabelle', 'Durie', 'aduriej@jugem.jp', 15, 'Clark Hall'),
       ('Natty', 'Bellelli', 'nbellellik@webs.com', 14, 'Parker Center'),
       ('Noelyn', 'Kildahl', 'nkildahll@twitter.com', 13, 'Forsyth Hall'),
       ('Currey', 'Tideswell', 'ctideswellm@slate.com', 9, 'Adams Building'),
       ('Keelby', 'Eymor', 'keymorn@xrea.com', 5, 'Grant Hall'),
       ('Klara', 'Poutress', 'kpoutresso@paginegialle.it', 6, 'Taylor Hall'),
       ('Loren', 'Brandino', 'lbrandinop@shinystat.com', 19, 'Taylor Hall'),
       ('Sampson', 'Ellissen', 'sellissenq@craigslist.org', 8, 'Taylor Hall'),
       ('Burlie', 'Laytham', 'blaythamr@paginegialle.it', 4, 'Forsyth Hall'),
       ('Elinore', 'Nelle', 'enelles@about.com', 9, 'Clark Hall'),
       ('Agnella', 'Keppy', 'akeppyt@ucsd.edu', 9, 'Adams Building');

-- Class Data
INSERT INTO Class (course_name, dept_id) VALUES
('Introduction to Cultural Anthropology', 10),
('Human Evolution', 10),
('Introduction to Art History', 14),
('Renaissance Art', 14),
('General Biology', 3),
('Genetics', 3),
('Principles of Management', 15),
('Marketing Fundamentals', 15),
('General Chemistry', 4),
('Organic Chemistry', 4),
('Public Speaking', 19),
('Interpersonal Communication', 19),
('Introduction to Programming', 1),
('Data Structures and Algorithms', 1),
('Microeconomics', 6),
('Macroeconomics', 6),
('Circuit Analysis', 17),
('Electromagnetics', 17),
('British Literature', 12),
('American Fiction', 12),
('Introduction to Environmental Science', 16),
('Environmental Policy', 16),
('World History', 11),
('American History', 11),
('Introduction to Linguistics', 20),
('Phonetics and Phonology', 20),
('Calculus I', 2),
('Linear Algebra', 2),
('Dynamics', 2),
('Thermodynamics', 2);

-- Section Data
INSERT INTO Section (section_num, semester_year, professor_id, course_id)
VALUES
       (1, 'Spring 2025', 14, 3),
       (2, 'Spring 2025', 10, 6),
       (2, 'Fall 2024', 15, 7),
       (2, 'Spring 2025', 24, 9),
       (2, 'Fall 2024', 7, 5),
       (1, 'Spring 2025', 9, 18),
       (3, 'Spring 2025', 26, 26),
       (2, 'Fall 2024', 23, 24),
       (1, 'Spring 2025', 5, 9),
       (2, 'Fall 2024', 28, 28),
       (2, 'Fall 2024', 25, 25),
       (1, 'Spring 2025', 27, 27),
       (2, 'Spring 2025', 22, 22),
       (3, 'Fall 2024', 11, 17),
       (3, 'Spring 2025', 2, 7),
       (2, 'Spring 2025', 19, 11),
       (1, 'Fall 2024', NULL, 11),
       (2, 'Spring 2025', 30, 30),
       (3, 'Fall 2024', 10, 6),
       (3, 'Fall 2024', 25, 25),
       (3, 'Spring 2025', 8, 2),
       (1, 'Fall 2024', 20, 25),
       (2, 'Spring 2025', 4, 16),
       (2, 'Spring 2025', 29, 29),
       (1, 'Fall 2024', 1, 13); -- MODEL DATA, taught by Prof Mark: DON'T DELETE!

-- Project Data
INSERT INTO Project(instructions, professor_id)
VALUES ('Make a functional data-driven application and be original!', 1),
       ('Get ready for this collaborative lab report,it is worth 50% of your grade', 3),
       ('See the linked instructions doc for the final risk management group project', 2);

-- TA Data
INSERT INTO TA(first_name, last_name, email, section_num, semester_year, course_id)
VALUES
    ('Timmy', 'Johnson', 'john.timmy@northeastern.edu', 2, 'Spring 2025', 29),
    ('Merle', 'Cheeld', 'mcheeld0@weather.com', 1, 'Spring 2025', 3),
    ('Vally', 'Lambdin', 'vlambdin1@wunderground.com', 2, 'Spring 2025', 6),
    ('Ennis', 'Eake', 'eeake2@ihg.com', 2, 'Fall 2024', 7),
    ('Turner', 'Lafflin', 'tlafflin3@thetimes.co.uk', 2, 'Spring 2025', 9),
    ('Donni', 'Champneys', 'dchampneys4@google.pl', 2, 'Fall 2024', 5),
    -- TA's for Prof Mark class: DON'T DELETE!
    ('John', 'Cain', 'john.cain@northeastern.edu', 1, 'Fall 2024', 13),
    ('Grace', 'Martin', 'martin.grace@northeastern.edu', 1, 'Fall 2024', 13),
    ('Kate', 'Harold', 'harold.ka@northeastern.edu', 1, 'Fall 2024', 13);
# ----- data from mockaroo
INSERT INTO TA (first_name, last_name, email, section_num, semester_year, course_id)
VALUES
    ('Opalina', 'La Grange', 'olagrange0@nasa.gov', 1, 'Spring 2025', 3),
    ('Phil', 'Tirrey', 'ptirrey1@sun.com', 2, 'Spring 2025', 6),
    ('Lynnell', 'Bourke', 'lbourke2@upenn.edu', 2, 'Fall 2024', 7),
    ('Elisabetta', 'Rimes', 'erimes3@google.com.br', 2, 'Spring 2025', 9),
    ('Hadlee', 'Levet', 'hlevet4@nba.com', 2, 'Fall 2024', 5),
    ('Thornton', 'Verlinde', 'tverlinde5@vinaora.com', 3, 'Fall 2024', 17),
    ('Hedy', 'Reeday', 'hreeday6@ucla.edu', 1, 'Spring 2025', 18);

INSERT INTO Speciality(speciality)
VALUES ('Python'),
       ('JavaScript'),
       ('Object-Oriented Design'),
       ('Accounting'),
       ('Risk management'),
       ('investments'),
       ('wet lab experience'),
       ('data analysis'),
       ('organic chemistry'),
       ('Figma'),
       ('illustrator');

-- TA Specialty Data
INSERT INTO TASpecialty(ta_id, specialty_id)
VALUES (1, 1),
       (1, 2),
       (1, 3),
       (2, 4),
       (2, 5),
       (2, 6),
       (3, 7),
       (3, 8),
       (3, 9);

-- Group Data
-- (1, 'Fall 2024', 13)
INSERT INTO `Group` (group_name, ta_id, section_num, semester_year, course_id)
VALUES ('Team Green', 1, 2, 'Spring 2025', 29),
       ('WeLoveChem', 3, 2, 'Spring 2025', 6),
       ('FinanceBros', 2, 1, 'Spring 2025', 3),
       ('Group1', 8, 1, 'Fall 2024', 13),
       -- These are groups in Prof Mark's section
       ('Group2', NULL, 1, 'Fall 2024', 13),
       ('Group3', 7, 1, 'Fall 2024', 13),
       ('Group4', 9, 1, 'Fall 2024', 13),
       ('Group5', NULL, 1, 'Fall 2024', 13);

-- Submission Data
INSERT INTO Submission (group_id, submitted_at, submission_link, project_id)
VALUES (1, '2024-08-16 10:45:28', 'projecturl1.com', 1),
       (2, '2024-08-12 09:18:57', 'finaproject.com', 2);
INSERT INTO Submission (group_id, submitted_at, submission_link, project_id)
VALUES (3, '2024-09-30 06:22:30', 'https://example.com/submit4',  3),
-- submissions from professor mark's section
       (4, '2024-08-12 09:18:57', 'https://example.com/submit5', 1),
       (5, '2024-08-08 10:30:45', 'https://example.com/submit4', 1),
       (6, '2024-08-10 08:15:22', 'https://example.com/submit7', 1);

-- Student Data
INSERT INTO Student(first_name, last_name, email, major, year, on_campus, group_id)
VALUES ('John', 'Doe', 'doe.jo@northeastern.edu', 'Computer Science', 3, True, 1),
       ('Sabrina', 'Williams', 'williams.sab@northeastern.edu', 'Marketing', 2, False, 1),
       ('Tom', 'Williams', 'williams.tom@northeastern.edu', 'Finance', 2, False, 1),
       ('Carrie', 'Smith', 'smith.car@northeastern.edu', 'Accounting', 2, True, 1),
       ('Daryl', 'Candace', 'candace.da@northeatern.edu', 'Neuroscience', 1, True, 2);
INSERT INTO Student (first_name, last_name, email, major, year, on_campus, group_id)
VALUES ('Nanette', 'Aronovitz', 'naronovitz0@state.tx.us', 'Theatre', 5, true, 4),
       ('Luigi', 'Langlais', 'llanglais1@prnewswire.com', 'Biology', 5, true, 6),
       ('Gardener', 'Studdeard', 'gstuddeard2@mit.edu', 'Accounting', 5, false, 4),
       ('Tremaine', 'Byre', 'tbyre3@upenn.edu', 'Political Science', 3, true, 1),
       ('Joanna', 'Muncey', 'jmuncey4@berkeley.edu', 'Data Science', 5, false, 1),
       ('Cleveland', 'Arend', 'carend5@aol.com', 'Biology', 1, true, 2),
       ('Julietta', 'Kennedy', 'jkennedy6@umich.edu', 'Data Science', 4, true, 6),
       ('Nonnah', 'Maton', 'nmaton7@is.gd', 'Theatre', 4, true, 4),
       ('Wynny', 'Ledamun', 'wledamun8@hao123.com', 'Theatre', 3, false, 3),
       ('Timothee', 'Laidel', 'tlaidel9@apple.com', 'Industrial Engineering', 5, false, 4),
       ('Caresse', 'Mackley', 'cmackleya@imageshack.us', 'Industrial Engineering', 5, false, 4),
       ('Micki', 'Woodrooffe', 'mwoodrooffeb@apache.org', 'Biomedical Engineering', 3, true, 3),
       ('Portie', 'Boram', 'pboramc@canalblog.com', 'Architecture', 4, true, 6),
       ('Norrie', 'Immings', 'nimmingsd@bbb.org', 'Neuroscience', 2, false, 5),
       ('Gizela', 'Jedrychowski', 'gjedrychowskie@ustream.tv', 'Dance', 2, false, 3),
       ('Calhoun', 'Lievesley', 'clievesleyf@parallels.com', 'Neuroscience', 5, true, 5),
       ('Florida', 'Coster', 'fcosterg@mail.ru', 'Neuroscience', 3, true, 5),
       ('Weidar', 'Van den Oord', 'wvandenoordh@kickstarter.com', 'International Business', 1, false, 3),
       ('Lebbie', 'Balls', 'lballsi@example.com', 'Industrial Engineering', 1, false, 5),
       ('Eduardo', 'Lintin', 'elintinj@ezinearticles.com', 'Political Science', 1, false, Null),
       ('Aubree', 'Djurdjevic', 'adjurdjevick@tinyurl.com', 'Chemistry', 1, false, 5),
       ('Shaina', 'Mant', 'smantl@gov.uk', 'Neuroscience', 5, false, Null),
       ('Andra', 'Yu', 'ayum@etsy.com', 'Theatre', 4, true, Null),
       ('Jobie', 'Worland', 'jworlandn@bravesites.com', 'Accounting', 4, true, Null),
       ('Christiano', 'Foxall', 'cfoxallo@feedburner.com', 'Fashion', 3, true, 3),
       ('Oliviero', 'Spawton', 'ospawtonp@cloudflare.com', 'Criminal Justice', 1, false, 3),
       ('Philippine', 'Marusyak', 'pmarusyakq@blinklist.com', 'International Business', 5, false, 2),
       ('Boone', 'Morde', 'bmorder@craigslist.org', 'Computer Engineering', 1, true, 1),
       ('Julee', 'Mulryan', 'jmulryans@senate.gov', 'Data Science', 5, true, 2),
       ('Renaldo', 'Brabban', 'rbrabbant@de.vu', 'Mechanical Engineering', 4, true, 1),
       ('Allx', 'Greene', 'agreeneu@wufoo.com', 'Criminal Justice', 4, true, 4),
       ('Farah', 'Nulty', 'fnultyv@jalbum.net', 'Accounting', 5, false, 4),
       ('Cassius', 'Piscot', 'cpiscotw@amazon.com', 'Dance', 4, false, 1),
       ('Marga', 'Bernardino', 'mbernardinox@arstechnica.com', 'International Business', 2, false, 4),
       ('Tallulah', 'Corbie', 'tcorbiey@addtoany.com', 'Accounting', 3, true, 5),
       ('Hieronymus', 'Daly', 'hdalyz@tumblr.com', 'Theatre', 2, false, 4),
       ('Patrica', 'Goadsby', 'pgoadsby10@goo.gl', 'Chemistry', 4, false, 5),
       ('Alina', 'Couche', 'acouche11@stanford.edu', 'Fashion', 2, false, 6),
       ('Becka', 'Croneen', 'bcroneen12@guardian.co.uk', 'International Business', 1, false, 6),
       ('Wenda', 'Ghidini', 'wghidini13@house.gov', 'Computer Engineering', 4, false, 6);

-- Student Specialty Data
INSERT INTO StudentSpeciality(student_id, specialty_id)
VALUES (1, 1),
       (1, 2),
       (2, 9),
       (2, 10),
       (2, 1),
       (3, 7),
       (3, 8);

-- Student Section Data
INSERT INTO StudentSection(student_id, section_num, semester_year, course_id)
VALUES (1, 2, 'Spring 2025', 29), -- keep this value!
       (2, 2, 'Spring 2025', 29), -- keep this value!
       (1, 1, 'Spring 2025', 3),
       (2, 1, 'Spring 2025', 3),
       (3, 1, 'Spring 2025', 3),
       (4, 1, 'Spring 2025', 3),
       (5, 2,'Spring 2025', 6),
       -- Students in Prof Mark's class
       (11, 1, 'Fall 2024', 13),
       (12, 1, 'Fall 2024', 13),
       (15, 1, 'Fall 2024', 13),
       (20, 1, 'Fall 2024', 13),
       (21, 1, 'Fall 2024', 13),
       (30, 1, 'Fall 2024', 13),
       (31, 1, 'Fall 2024', 13),
       (40, 1, 'Fall 2024', 13),
       (1, 1, 'Fall 2024', 13),
       (18, 1, 'Fall 2024', 13);
# ----- need to fix mockoroo data file

-- Days Data
-- data exhaustive, can't insert anymore data bc there are only 7 days in a week
INSERT INTO Days(day)
VALUES ('Monday'),
       ('Tuesday'),
       ('Wednesday'),
       ('Thursday'),
       ('Friday'),
       ('Saturday'),
       ('Sunday');

-- Time Data
-- data exhaustive, can't insert anymore data bc only 3 time options
INSERT INTO Time(time)
VALUES ('Morning'),
       ('Afternoon'),
       ('Night');

-- Availability Data
INSERT INTO Availability (time_id, day_id)
VALUES (1, 1), (2, 2), (3, 3),
       (1, 4), (2, 5),(3, 6),
       (1, 7), (2, 1),(3, 2),
       (1, 3), (2, 4), (3, 5),
       (1, 6), (2, 7), (3, 1),
       (1, 2),(2, 3), (3, 4),
       (1, 5),(2, 6),(3, 7);

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
       (2, 5),
       (5, 1);

-- TAAvailability Data
INSERT INTO TAAvailability(availability_id, ta_id)
VALUES (1, 2),
       (1, 3),
       (5, 1),
       (8, 2),
       (7, 1);

-- DEMO QUERIES

-- USE this query for UPDATE MAJOR - PUT request
-- STUDENT USER
SELECT first_name, last_name, email, major AS Student_John
FROM Student
WHERE student_id=1;

-- USE this query for UPDATE & DELETE TA AVAILABILITY - POST & DELETE request
-- TA USER
SELECT ta.ta_id, first_name, last_name, day, time AS TA_Timmy
FROM TA ta JOIN TAAvailability t on ta.ta_id = t.ta_id
JOIN Availability a on t.availability_id = a.availability_id
JOIN Days d on a.day_id = d.day_id
JOIN Time ti on a.time_id = ti.time_id
WHERE ta.ta_id=1;