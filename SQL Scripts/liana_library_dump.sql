SET client_min_messages TO WARNING;

--
-- Table structure for table books
--

DROP TABLE IF EXISTS books CASCADE; -- CASCADE ensures dependent objects (like foreign keys) are dropped
CREATE TABLE books (
  ISBN VARCHAR(20) PRIMARY KEY,
  Title VARCHAR(255) NOT NULL,
  Author_FName VARCHAR(255) NOT NULL,
  Author_LName VARCHAR(255) NOT NULL,
  Publisher VARCHAR(255) NOT NULL,
  Publication_Year INT DEFAULT NULL,
  Genre VARCHAR(50) NOT NULL
);

--
-- Table structure for table members
--

DROP TABLE IF EXISTS members CASCADE; -- CASCADE ensures dependent objects are dropped
CREATE TABLE members (
  MemberID SERIAL PRIMARY KEY, -- Converted from INT NOT NULL AUTO_INCREMENT
  Member_FName VARCHAR(100) NOT NULL,
  Member_LName VARCHAR(100) NOT NULL,
  Signup_Date DATE NOT NULL,
  Address VARCHAR(255) NOT NULL,
  Mobile VARCHAR(20) NOT NULL,
  Email VARCHAR(100) NOT NULL,
  Social_Media VARCHAR(255) NOT NULL,
  -- Converted from ENUM to VARCHAR for PostgreSQL compatibility
  Preference VARCHAR(50) NOT NULL, -- e.g., 'Email','Mobile','Address','Social Media'
  Member_Status VARCHAR(20) NOT NULL -- e.g., 'active','inactive','suspended'
);

-- Add UNIQUE constraints for Mobile and Email if they were UNIQUE KEYs in MySQL
ALTER TABLE members ADD CONSTRAINT UQ_members_Mobile UNIQUE (Mobile);
ALTER TABLE members ADD CONSTRAINT UQ_members_Email UNIQUE (Email);


--
-- Table structure for table loans
--

DROP TABLE IF EXISTS loans CASCADE; -- CASCADE ensures dependent objects are dropped
CREATE TABLE loans (
  LoanID SERIAL PRIMARY KEY, -- Converted from INT NOT NULL AUTO_INCREMENT
  MemberID INT NOT NULL,
  ISBN VARCHAR(20) NOT NULL,
  Borrow_date DATE NOT NULL,
  Return_date DATE DEFAULT NULL,
  -- Foreign Key Constraints
  CONSTRAINT fk_loans_member FOREIGN KEY (MemberID) REFERENCES members (MemberID),
  CONSTRAINT fk_loans_book FOREIGN KEY (ISBN) REFERENCES books (ISBN)
);

--
-- Table structure for table users
--

DROP TABLE IF EXISTS users CASCADE; -- CASCADE ensures dependent objects are dropped
CREATE TABLE users (
  UserID SERIAL PRIMARY KEY, -- Converted from INT NOT NULL AUTO_INCREMENT
  Username VARCHAR(50) NOT NULL UNIQUE, -- Added UNIQUE constraint explicitly
  PasswordHash VARCHAR(255) NOT NULL,
  -- Converted from ENUM to VARCHAR for PostgreSQL compatibility
  Role VARCHAR(10) NOT NULL -- e.g., 'admin','user'
);

-- Re-enable notices
RESET client_min_messages;