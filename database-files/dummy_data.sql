USE cosint

-- Insert into companies
INSERT INTO companies (name)
VALUES
    ('TechCorp'),
    ('Innovate Inc'),
    ('Healthify Solutions'),
    ('EduVenture'),
    ('Cosint'),
    ('Greip');

-- Insert into users
INSERT INTO users (name, firstName, middleName, lastName, mobile, email, passwordHash, profile, companyId, lastLogin, preferredName, pronouns, major, year, birthday, profilePic, role)
VALUES
    ('John Doe', 'John', 'A', 'Doe', '1234567890', 'johndoe@example.com', MD5('password123'), 'Senior Engineer at TechCorp', 1, NOW(), 'Jack', 'He/Him', 'Computer Science', 'Senior', '1990-01-01', 'https://example.com/johndoe.jpg', 'Student'),
    ('Jane Smith', 'Jane', 'B', 'Smith', '1234567891', 'janesmith@example.com', MD5('securepass'), 'Manager at Innovate Inc', 2, NOW(), 'Jenny', 'She/Her', 'Business Administration', 'Junior', '1991-02-02', 'https://example.com/janesmith.jpg', 'Admin'),
    ('Samuel Green', 'Samuel', 'C', 'Green', '1234567892', 'samuelgreen@example.com', MD5('mypassword'), 'Data Scientist at Healthify Solutions', 3, NOW(), 'Sam', 'He/They', 'Data Science', 'Senior', '1992-03-03', 'https://images.sidearmdev.com/convert?url=https%3a%2f%2fdxbhsrqyrr690.cloudfront.net%2fsidearm.nextgen.sites%2funco.sidearmsports.com%2fimages%2f2024%2f8%2f29%2fGreen_Sam_Cropped_HS.png&type=webp', 'Advisor'),
    ('Emily White', 'Emily', 'D', 'White', '1234567893', 'emilywhite@example.com', MD5('whitepass'), 'CTO at EduVenture', 4, NOW(), 'Em', 'She/Her', 'Computer Engineering', 'Senior', '1993-04-04', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_1lcAVOaA1Vx5AnY7QZiLb2ZxV8Nwf0EVXw&s', 'Employer'),
    ('Mark Fontenot', 'Mark', 'N', 'Fontenot', '1234567894', 'markfont@example.com', MD5('database'), 'Junior at NEU', NULL, NOW(), 'Mark', 'He/Him', 'Computer Science', 'Junior', '2000-05-01', 'https://media.licdn.com/dms/image/v2/C4E03AQGToUqmxXqtSA/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1516305759672?e=1738800000&v=beta&t=CNVHwddh5MAMs_DqfJ6A7fbAv59jVp7zvrzHSzg_ij8', 'Student'),
    ('Jordan Michael', 'Jordan', 'O', 'Michael', '1234567895', 'joming@example.com', MD5('basketball'), 'Admin at Consint', 5, NOW(), 'Jordan', 'He/Him', NULL, NULL, '1989-01-01', 'https://preview.redd.it/michael-jordan-wizards-jersey-legit-or-no-v0-55t5fffppadd1.jpeg?width=976&format=pjpg&auto=webp&s=b29da956bd4f759cbedb9b95c70172e154371491', 'Admin'),
    ('Joe Montana', 'Joe', 'P', 'Montana', '1234567896', 'jmontana@example.com', MD5('hannah'), 'Advisor at NEU', NULL, NOW(), 'Joe', 'He/Him', NULL, NULL, '1985-02-28', 'https://static.www.nfl.com/image/private/t_headshot_desktop/league/ueq3x4ldeixk2h5wq3n7', 'Advisor'),
    ('Peter Burke', 'Peter', 'S', 'Burke', '1234567897', 'peterb@example.com', MD5('whitecollar'), 'CEO at Greip', 6, NOW(), 'Pete', 'He/Him', NULL, NULL, '1987-05-11', 'https://funkymbti.com/wp-content/uploads/2024/05/peter2.jpg', 'Employer');

UPDATE users SET studentId = 12345678, advisorId = 7 WHERE id = 5;

-- Insert into user_references
INSERT INTO user_references (name, firstName, middleName, lastName, mobile, email, referral, userId) 
VALUES
    ('Mark Taylor', 'Mark', 'E', 'Taylor', '1234567894', 'marktaylor@example.com', 'Referred for engineering role', 1),
    ('Lucy Brown', 'Lucy', 'F', 'Brown', '1234567895', 'lucybrown@example.com', 'Recommended for a data position', 5);

-- Insert into tickets
INSERT INTO tickets (userId, helperId, summary, completed, viewedAt)
VALUES
    (1, 2, 'System upgrade issue', 0, NULL),
    (3, 4, 'Database optimization task', 1, NOW());

-- Insert into positions
INSERT INTO positions (companyId, applicantQuestions, summary, country, city, address, expectedSalary)
VALUES
    (1, 'What is your experience in backend development?', 'Backend Developer Role', 'USA', 'New York', '123 Tech Street', 75000),
    (6, 'Describe your approach to team management.', 'Team Manager Role', 'Canada', 'Toronto', '456 Innovate Lane', 85000);

-- Insert into applications
INSERT INTO applications (questionResponse, summary, GPA, submittedAt)
VALUES
    ('I have 5 years of experience in backend development and microservices architecture.',
    'Application for Backend Developer', 3.8, NOW()),
    ('I have 10 years of experience in management and have successfully led teams.',
    'Application for Manager Role', 3.5, NOW());

-- Insert into related_coursework
INSERT INTO related_coursework (applicationId, name, summary)
VALUES
    (1, 'Advanced Database Systems', 'Focus on relational databases and optimization techniques'),
    (2, 'Leadership in Organizations', 'Explored management theories and practices');

-- Insert into notable_skills
INSERT INTO notable_skills (applicationId, name, summary)
VALUES
    (1, 'Microservices Architecture', 'Designed and implemented scalable backend services'),
    (2, 'Team Leadership', 'Led diverse teams across multiple projects');

-- Insert into work_experience
INSERT INTO work_experience (applicationId, name, summary)
VALUES
    (1, 'Software Engineer at ABC Corp', 'Developed backend systems using Node.js and PostgreSQL'),
    (2, 'Manager at XYZ Ltd.', 'Managed a team of 15 engineers and achieved project milestones.');

-- Insert into position_user_bookmark
INSERT INTO position_user_bookmark (positionId, userId)
VALUES
    (1, 1),
    (2, 2);

-- Insert into position_application_bookmark
INSERT INTO position_application_bookmark (positionId, applicationId)
VALUES
    (1, 1),
    (2, 2);

-- Insert into application_bookmark
INSERT INTO application_bookmark (applicationId, userId)
VALUES
    (1, 2),
    (2, 5);

-- Insert into company_user_bookmark
INSERT INTO company_user_bookmark (companyId, userId)
VALUES
    (1, 1);