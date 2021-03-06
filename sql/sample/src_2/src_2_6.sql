--- src_2_6


DELETE FROM employee WHERE 1;
DELETE FROM department WHERE 1;
DELETE FROM jobrole WHERE 1;

INSERT INTO `jobrole` (`id`, `name`) VALUES
(1, 'Clerk'),
(2, 'Developer'),
(3, 'IT Administrator'),
(4, 'Architect'),
(5, 'Software Engineer'),
(6, 'System Engineer'),
(7, 'Test Engineer'),
(8, 'Account Manager'),
(9, 'Project Manager'),
(10, 'Head of'),
(11, 'Designer');

INSERT INTO `department` (`id`, `name`, `did`) VALUES
(1, 'Administration', NULL),
(2, 'HR', 1),
(3, 'Finance', 1),
(4, 'Production', NULL),
(5, 'Architecture', 4),
(6, 'Development', 4),
(7, 'Core', 6),
(8, 'Server', 6),
(9, 'Client', 6),
(10, 'Operations', 4),
(11, 'Industrialization', 4),
(12, 'Project Management', 4),
(13, 'Sales', NULL),
(14, 'IT Facilities', 1),
(15, 'QA', 4),
(16, 'Design', 4);

INSERT INTO `employee` (`id`, `name`, `address`, `salary`, `manager`, `did`, `jid`, `gender`, `dob`) VALUES
(0, 'Bernd Grotius', 'Testadresse 845234', 78900, 1, 10, 3, 'MALE', '1970-07-18'),
(84, 'Jan Breuer', 'Testadresse 324345', 64700, 0, 2, 1, 'MALE', '1962-04-24'),
(85, 'Rita Fischer', 'Testadresse 86753', 60400, 0, 2, 1, 'FEMALE', '1960-07-27'),
(86, 'Roman Müller', 'Testadresse 834423', 56000, 0, 3, 1, 'MALE', '1970-03-02'),
(87, 'Karl Breitner', 'Testadresse 7435432', 70000, 0, 14, 3, 'MALE', '1968-06-03'),
(88, 'Hans Ritter', 'Testadresse 8324345', 90400, 1, 4, 10, 'MALE', '1963-05-28'),
(89, 'Janina Loss', 'Testadresse 832432', 62400, 1, 5, 4, 'MALE', '1976-05-15'),
(90, 'Peter Winnen', 'Testadresse 93265432', 65200, 0, 6, 2, 'MALE', '1977-02-22'),
(91, 'Dieter Radtke', 'Testadresse 7324346', 59800, 0, 7, 2, 'MALE', '1979-11-29'),
(92, 'Tina Huth', 'Testadresse 3271233', 48000, 0, 7, 2, 'FEMALE', '1980-01-04'),
(93, 'Florian Zoellner', 'Testadresse 8324234', 55200, 0, 7, 2, 'MALE', '1979-08-14'),
(94, 'Simon Boeffgen', 'Testadresse 123834', 64900, 0, 8, 2, 'MALE', '1973-05-11'),
(95, 'Petra Wirt', 'Testadresse 0943252', 59000, 0, 8, 2, 'FEMALE', '1969-04-01'),
(96, 'Jan Klarenbach', 'Testadresse 732442', 48000, 0, 8, 2, 'MALE', '1981-12-29'),
(97, 'Heiko Sommer', 'Testadresse 832423', 58800, 0, 9, 2, 'MALE', '1964-05-11'),
(98, 'Alexandra Roth', 'Testadresse 832432', 52000, 0, 9, 2, 'FEMALE', '1975-03-11'),
(99, 'Bjoern Sommerscheidt', 'Testadresse 8324234', 56400, 0, 10, 3, 'MALE', '1969-04-23'),
(101, 'Sebastien Becker', 'Testadresse 5684324', 70000, 0, 11, 6, 'MALE', '1962-04-09'),
(102, 'Rainer Zufall', 'Testadresse 8435423', 69000, 0, 12, 9, 'MALE', '1968-02-27'),
(103, 'Thomas Heinz', 'Testadresse 4313480', 71800, 0, 12, 9, 'MALE', '1963-09-09'),
(104, 'Jochen Berger', 'Testadresse 83425', 52000, 0, 13, 8, 'MALE', '1979-08-25'),
(105, 'Luise Mueller', 'Testadresse 286345', 54200, 0, 13, 8, 'FEMALE', '1974-05-18'),
(106, 'Britt Fischer', 'Testadresse 932623', 45800, 0, 14, 2, 'FEMALE', '1968-03-12'),
(107, 'Christoph Dahmen', 'Testadresse 7234324', 84200, 1, 15, 10, 'MALE', '1962-04-09'),
(108, 'Frank Jaeger', 'testadresse 680534', 57800, 0, 15, 7, 'MALE', '1971-11-11'),
(109, 'Fiona Schmidt', 'Testadresse 65932', 54800, 0, 15, 7, 'FEMALE', '1974-06-28'),
(110, 'Berta Brecht', 'Testadresse 12953', 64200, 0, 16, 10, 'FEMALE', '1967-03-09'),
(111, 'Peter Goenner', 'Testadresse 84565', 85200, 1, 2, 10, 'MALE', '1966-09-29'),
(112, 'Hannah Reebe', 'Testadresse 843563', 90400, 1, 1, 10, 'FEMALE', '1962-07-02'),
(113, 'Achim Breuer', 'Testadresse 845324', 80000, 1, 13, 10, 'MALE', '1972-05-07'),
(114, 'Ute Heymann', 'Testadresse 8563234', 78000, 1, 7, 10, 'FEMALE', '1967-11-14'),
(115, 'Lars Weber', 'Testadresse 743534', 58600, 0, 5, 4, 'MALE', '1972-05-28'),
(116, 'Patrick Schlemmer', 'Testadresse 7343424', 54800, 0, 9, 2, 'MALE', '1970-06-03'),
(117, 'Laura Stern', 'Testadresse 734543', 49200, 0, 9, 2, 'FEMALE', '1969-07-28'),
(118, 'Johann Gueter', 'Testadresse 745345', 59800, 0, 16, 6, 'MALE', '1959-11-23');
