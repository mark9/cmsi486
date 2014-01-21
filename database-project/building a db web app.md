mongoDB & certificate
40 problems
problems 1-3 on practice problems
web app


Part 1 Intro to Databases
(1) Problem 2.14: If you were designing a Web-based system to make airline reservations and sell airline tickets, which DBMS architecture would you choose from Section 2.5? Why? Why would the other architectures not be a good choice? -- The options are centralized DBMSs, basic client/server architecture, two-tier, and three plus tier architectures. A three or more tier architecture would be the most reasonable because of the complexity of the task of booking a flight. The significant difference between theese architectures is the need for intermediary application programs between the GUI and the DB. One example for this need is that a customer should be allowed a few minutes to think about and choose their options without losing the seat to someone else doing a similar DB transaction. The intermediary applications should allow this buffer time by temporarily reserving a spot on the DB. After a person inputs their flight information including credit card payment information, an application program should check validity of the card/payment before immediately booking the seat.

Part 2 The Relational Data Model & SQL
	CRUD
	Joins

(2) Problem 3.10 (page 81): What is a transaction? How does it differ from an Update operation? -- A transaction refers to any type of operation or execution on the DB, such as querying, inserting, deleting, or updating. Updating is just one type of transaction on a database, which entails modifying usually just a single field of a specific record.

(3) Problem 3.12 (page 81): Consider the AIRLINE relational database schema shown in Figure 3.8, which describes a database for airline flight information. Each FLIGHT is identified by a Flight_number, and consists of one or more FLIGHT_LEGs with Leg_numbers 1, 2, 3, and so on. Each FLIGHT_LEG has scheduled arrival and departure times, airports, and one or more LEG_INSTANCEs—one for each Date on which the flight travels. FAREs are kept for each FLIGHT. For each FLIGHT_LEG instance, SEAT_RESERVATIONs are kept, as are the AIRPLANE used on the leg and the actual arrival and departure times and airports. An AIRPLANE is identified by an Airplane_id and is of a particular AIRPLANE_TYPE. CAN_LAND relates AIRPLANE_TYPEs to the AIRPORTs at which they can land. An AIRPORT is identified by an Airport_code. Consider an update for the AIRLINE database to enter a reservation on a particular flight or flight leg on a given date.
 

a. Give the operations for this update. -- First check if the flight is full by accessing the Number_of_available_seats field in the LEG_INSTANCE table. If there is value is greater than zero, update it with the value decreased by one. Then insert a new record in the SEAT_RESERVATION table.

b. What types of constraints would you expect to check? --

Key constraints are requirements that no two records are exactly the same across all fields. An entity integrity constraint says that no primary key value can be null. A referential integrity constraint is one which requires that a tuple in one relation that refers to another relation must refer to a tuple in that relation that is existing. 

There are a lot of constraints. First of all, obviously all primary keys must be unique and not null. Another common constraint in this database is the need for Flight_number and Leg_number in the SEAT_RESERVATION relation to be matching with the respective tuples in the LEG_INSTANCE relation, and likewise, these two fields must be matching with the fields in the FLIGHT_LEG relation. All constraints must be checked.

c. Which of these constraints are key, entity integrity, and referential integrity constraints, and which are not? -- The requirement for all primary keys to no be null would be considered an entity integrity constraint. The Flight_number and Leg_number constraint across the SEAT_RESERVATION, LEG_INSTANCE, and FLIGHT_LEG relations are referential integrity constraints because they are should all be referring to/matching eachother. Key restraints should also follow suit in this scenario if everything is running smoothly, because even if a passenger is repeating a flight, the Flight_number, Leg_number, etc. should be unique anyway.

d. Specify all the referential integrity constraints that hold on the schema shown in Figure 3.8.
•	AIRPORT.Airport_code=CAN_LAND.Airport_code=FLIGHT_LEG.Departure_airport_code
•	AIRPORT.Airport_code=CAN_LAND.Airport_code=FLIGHT_LEG.Arrival_airport_code
•	FLIGHT.Flight_number=FLIGHT_LEG.Flight_number=LEG_INSTANCE.Flight_number=FARE.Flight_number=SEAT_RESERVATION.Flight_number
•	FLIGHT_LEG.Leg_number=LEG_INSTANCE.Leg_number=FARE.Leg_number=SEAT_RESERVATION.Leg_number
•	FLIGHT_LEG.Scheduled_departure_time=LEG_INSTANCE.Departure_time
•	FLIGHT_LEG.Scheduled_arrival_time=LEG_INSTANCE.Arrival_time
•	LEG_INSTANCE.Date=SEAT_RESERVATION.Date
•	LEG_INSTANCE.Number_of_available_seats=AIRPLANE_TYPE.Max_seats - the sum of SEAT_RESERVATION related tuples

(4) Problem 3.16 (page 83) Consider the following relations for a database that keeps track of student enrollment in courses and the books adopted for each course:

STUDENT(Ssn, Name, Major, Bdate)
COURSE(Course#, Cname, Dept)
ENROLL(Ssn, Course#, Quarter, Grade)
BOOK_ADOPTION(Course#, Quarter, Book_isbn)
TEXT(Book_isbn, Book_title, Publisher, Author)

Specify the foreign keys for this schema, stating any assumptions you make.

•	ENROLL.Ssn: assuming STUDENT has the primary
•	ENROLL.Course# and BOOK_ADOPTION.Course#: assuming COURSE has the primary
•	BOOK_ADOPTION.Quarter: assuming ENROLL has the primary
•	BOOK_ADOPTION.Book_isbn: assuming TEXT has the primary


(5) Problem 4.5 (page 112) Consider the database shown in Figure 1.2, whose schema is shown in Figure 2.1. What are the referential integrity constraints that should hold on the schema? Write appropriate SQL DDL statements to define the database.
  
Referential Integrity Constraints:
•	GRADE_REPORT.Student_number references STUDENT.Student_number, STUDENT.Student_number is not null
•	PREREQUISITE.Course_number and SECTION.Course_number both reference COURSE.Course_number, COURSE.Course_number is not null
•	GRADE_REPORT.Section_identifier references SECTION.Section_identifier, SECTION.Section_identifier is not null

SQL DDL Statements:
•	create table STUDENT (
•	Name varchar(50),
•	Student_number int not null auto_increment primary key,
•	Class varchar(10),
•	Major varchar(20)
•	);
•	create table COURSE (
•	Course_name varchar(50)
•	Course_number int not null auto_increment primary key,
•	Credit_hours int,
•	Department varchar(50)
•	);
•	create table PREREQUISITE (
•	Course_number int,
•	foreign key (Course_number) references COURSE(Course_number),
•	Prerequisite_number int
•	);
•	create table SECTION (
•	Section_identifier int not null auto_increment primary key,
•	Course_number int,
•	foreign key (Course_number) references COURSE(Course_number),
•	Semester varchar(6),
•	Year int,
•	Instructor varchar(50)
•	);
•	create table GRADE_REPORT (
•	Student_number int,
•	foreign key (Student_number) references STUDENT(Student_number),
•	Section_identifier int,
•	foreign key (Section_identifier) references SECTION(Section_identifier),
•	Grade varchar(2)
•	);

(6) Problem 4.7 (page 112) Consider the LIBRARY relational database schema shown in Figure 4.6. Choose the appropriate action (reject, cascade, set to NULL, set to default) for each referential integrity constraint, both for the deletion of a referenced tuple and for the update of a primary key attribute value in a referenced tuple. Justify your choices.

Reject: occurs when an attempted update operation is passed that would cause an integrity violation. This is the default action
Cascading (page 96)
Set to null
Set to default
How can the schema be changed in an active database?

Appropriate actions for referential integrity constraints:

Upon deletion of a referenced tuple:

BOOK.Publisher_name=PUBLISHER.Name:
BOOK_AUTHORS.Book_id=BOOK.Book_id
BOOK_COPIES.Book_id=BOOK.Book_id
BOOK_COPIES.Branch_id=LIBRARY_BRANCH.Branch_id
BOOK_LOANS.Book_id=BOOK.Book_id
BOOK_LOANS.Branch_id=LIBRARY_BRANCH.Branch_id
BOOK_LOANS.Card_no=BORROWER.Card_no

Upon update of a primary key attribute value in a referenced tuple:

BOOK.Publisher_name=PUBLISHER.Name
BOOK_AUTHORS.Book_id=BOOK.Book_id
BOOK_COPIES.Book_id=BOOK.Book_id
BOOK_COPIES.Branch_id=LIBRARY_BRANCH.Branch_id
BOOK_LOANS.Book_id=BOOK.Book_id
BOOK_LOANS.Branch_id=LIBRARY_BRANCH.Branch_id
BOOK_LOANS.Card_no=BORROWER.Card_no

 


Problem 4.9 (page 112) How can the key and foreign key constraints be enforced by the DBMS? Is the enforcement technique you suggest difficult to implement? Can the constraint checks be executed efficiently when updates are applied to the database? -- 


Part 3 Conceptual Modeling & Database Design

Part 4 Object, Object-Reational, XML
Part 5 Database Programming Techniques
	PHP
	Stored Procedures - look up google’s uses
Part 6 Database Design Theory
Part 7 File Structures, Indexing, Hashing
Part 8 Query Processing, & Optimization
Part 9 Transaction Processing, Concurrency Control, Recovery
	the worst part of databases
Part 10 Security & Distribution
	SQL Injection
Part 11 Advanced Models, Systems, & Applications
	Data Mining
