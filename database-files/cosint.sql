Create DATABASE cosint;
USE cosint;

CREATE TABLE IF NOT EXISTS companies
(
  name varchar(30),
  registeredAt DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  id int AUTO_INCREMENT,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS users
(
  name varchar(150),
  firstName varchar(50) NOT NULL,
  middleName varchar(50),
  lastName varchar(50) NOT NULL,
  preferredName varchar(50),
  pronouns varchar(10),
  major varchar(50),
  year varchar(15),
  birthday date,
  profilePic varchar(1000),
  role varchar(50),
  studentId varchar(15) UNIQUE,
  mobile varchar(50),
  email varchar(40) NOT NULL,
  passwordHash varchar(128) NOT NULL, 
  profile text,
  advisorId int, 
  companyId int,
  lastLogin DATETIME ON UPDATE CURRENT_TIMESTAMP, 
  active boolean DEFAULT 1,
  registeredAt DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
  updatedAt datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
  id int AUTO_INCREMENT,
  PRIMARY KEY(id),
  UNIQUE INDEX uq_idx_mobile (mobile),
  UNIQUE INDEX uq_idx_email (email),
  CONSTRAINT fk_01 FOREIGN KEY (advisorId) REFERENCES users (id) ON UPDATE CASCADE, 
  CONSTRAINT fk_02 FOREIGN KEY (companyId) REFERENCES companies (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS user_references
(
  name varchar(150),
  firstName varchar(50) NOT NULL,
  middleName varchar(50),
  lastName varchar(50) NOT NULL,
  mobile varchar(15),
  email varchar(40) NOT NULL,
  referral text,
  userId int NOT NULL,
  registeredAt datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY(userId),
  UNIQUE INDEX uq_idx_mobile (mobile),
  UNIQUE INDEX uq_idx_email (email),
  CONSTRAINT fk_03 FOREIGN KEY (userId) REFERENCES users (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS tickets
(
  userId int NOT NULL,
  helperId int,
  summary text NOT NULL,
  completed boolean NOT NULL DEFAULT 0,
  viewedAt datetime,
  updatedAt datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  registeredAt datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  id int AUTO_INCREMENT,
  PRIMARY KEY(id),
  CONSTRAINT fk_04 FOREIGN KEY (userId) REFERENCES users (id) ON UPDATE CASCADE,
  CONSTRAINT fk_05 FOREIGN KEY (helperId) REFERENCES users (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS positions
(
  registeredAt datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  companyId int NOT NULL,
  applicantQuestions text,
  summary text,
  country varchar(15) NOT NULL,
  city varchar(15) NOT NULL,
  address varchar(60) NOT NULL,
  filled boolean NOT NULL DEFAULT 0,
  expectedSalary int,
  viewedAt datetime,
  updatedAt datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  id int AUTO_INCREMENT,
  PRIMARY KEY(id),
  CONSTRAINT fk_11 FOREIGN KEY (companyId) REFERENCES companies (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS applications
(
  registeredAt datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  questionResponse text,
  summary text,
  GPA decimal(3,2),
  submittedAt datetime,
  accepted boolean NOT NULL DEFAULT 0,
  viewedAt datetime,
  updatedAt datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  id int AUTO_INCREMENT,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS related_coursework
(
  applicationId int NOT NULL,
  name varchar(30) NOT NULL,
  summary text,
  PRIMARY KEY (applicationId, name),
  CONSTRAINT fk_08 FOREIGN KEY (applicationId) REFERENCES applications (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS notable_skills
(
  applicationId int NOT NULL,
  name varchar(30) NOT NULL,
  summary text,
  PRIMARY KEY (applicationId, name),
  CONSTRAINT fk_09 FOREIGN KEY (applicationId) REFERENCES applications (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS work_experience 
(
  applicationId int NOT NULL,
  name varchar(30) NOT NULL,
  summary text,
  PRIMARY KEY (applicationId, name),
  CONSTRAINT fk_10 FOREIGN KEY (applicationId) REFERENCES applications (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS position_user_bookmark
(
  positionId int, 
  userId int, 
  PRIMARY KEY (positionId, userId),
  CONSTRAINT fk_12 FOREIGN KEY (positionId) REFERENCES positions (id) ON UPDATE CASCADE,
  CONSTRAINT fk_13 FOREIGN KEY (userId) REFERENCES users (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS application_bookmark
(
  applicationId int,
  userId int,
  PRIMARY KEY (applicationId, userId),
  CONSTRAINT fk_14 FOREIGN KEY (applicationId) REFERENCES applications (id) ON UPDATE CASCADE,
  CONSTRAINT fk_15 FOREIGN KEY (userId) REFERENCES users (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS position_application_bookmark
(
  positionId int,
  applicationId int,
  PRIMARY KEY (positionId, applicationId),
  CONSTRAINT fk_16 FOREIGN KEY (positionId) REFERENCES positions (id) ON UPDATE CASCADE,
  CONSTRAINT fk_17 FOREIGN KEY (applicationId) REFERENCES applications (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS company_user_bookmark
( 
  companyId int, 
  userId int, 
  PRIMARY KEY (companyId, userId),
  CONSTRAINT fk_18 FOREIGN KEY (companyId) REFERENCES companies (id) ON UPDATE CASCADE,
  CONSTRAINT fk_19 FOREIGN KEY (userId) REFERENCES users (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS offer_list
(
  positionId int,
  userId int,
  PRIMARY KEY (positionId, userId),
  CONSTRAINT fk_20 FOREIGN KEY (positionId) REFERENCES positions (id) ON UPDATE CASCADE,
  CONSTRAINT fk_21 FOREIGN KEY (userId) REFERENCES users (id) ON UPDATE CASCADE
);