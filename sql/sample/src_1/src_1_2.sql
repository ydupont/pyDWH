--- src_1_2

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
(10, 'Head of');

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
(15, 'QA', 4);


INSERT INTO `employee` (`id`, `name`, `address`, `salary`, `manager`, `did`, `jid`, `gender`, `dob`) VALUES
(1, 'Franz Schmitt', 'Testadresse 433', 55000, 0, 2, 1, 'MALE', '1954-07-02'),
(2, 'Andrea Müller', 'Testadresse 985', 42000, 0, 2, 1, 'FEMALE', '1972-08-05'),
(3, 'Josef Hardt', 'Testadresse 7453', 62000, 0, 3, 1, 'MALE', '1964-02-01'),
(4, 'Franzsika Reiter', 'Testadresse 7435', 44000, 0, 3, 1, 'FEMALE', '1967-06-01'),
(5, 'Bruno Karlsen', 'Testadresse 4546', 39000, 0, 14, 3, 'MALE', '1978-04-21'),
(6, 'Peter Merck', 'Testadresse 75463', 41000, 0, 14, 3, 'MALE', '1972-03-23'),
(7, 'Johann Schlechtenberg', 'Testadresse 8563', 56000, 1, 14, 3, 'MALE', '1968-12-28'),
(8, 'Paula Drews', 'Testadresse 46756', 38000, 0, 14, 3, 'FEMALE', '1980-03-14'),
(9, 'Wolfgang Kreutz', 'Testadresse 435456', 64000, 1, 4, 5, 'MALE', '1974-05-05'),
(10, 'Anna Kwecnzik', 'Testadresse 96563', 56000, 1, 4, 5, 'FEMALE', '1971-08-17'),
(11, 'Jan Ost', 'Testadresse 8435435', 52500, 0, 7, 4, 'MALE', '1966-09-04'),
(12, 'Karl Retter', 'Testadresse 854645764', 58400, 0, 7, 4, 'MALE', '1972-10-03'),
(13, 'Jana Müller', 'Testadresse 9435456', 54200, 0, 7, 4, 'FEMALE', '1969-01-19'),
(14, 'Hans Wurst', 'Testadresse 984345', 41000, 0, 7, 2, 'MALE', '1979-09-06'),
(15, 'Lara Paulsen', 'Testadresse 7435435', 32000, 0, 7, 2, 'FEMALE', '1981-04-11'),
(16, 'Andreas Becker', 'Testadresse 84353', 38000, 0, 7, 2, 'MALE', '1964-09-08'),
(17, 'Klaus Jungblut', 'Testadresse 85454', 36400, 0, 7, 2, 'MALE', '1974-03-05'),
(18, 'Björn Roth', 'Testadresse 84353', 41000, 0, 8, 4, 'MALE', '1972-05-07'),
(19, 'Karla Roth', 'Testadresse 84354', 34000, 0, 8, 4, 'FEMALE', '1977-09-01'),
(20, 'Roland Koch', 'Testadresse 835434', 31000, 0, 8, 4, 'MALE', '1981-02-23'),
(21, 'Friedrich Ranke', 'Testadresse 745343', 39800, 0, 8, 4, 'MALE', '1971-03-11'),
(22, 'Hans-Josef Schleier', 'Testadresse 734354', 42000, 0, 9, 4, 'MALE', '1963-05-28'),
(23, 'Kevin Mittler', 'Testadresse 21435', 34000, 0, 9, 4, 'MALE', '1973-08-11'),
(24, 'Hannah Merz', 'Testadresse 63242', 32400, 0, 9, 4, 'FEMALE', '1974-07-07'),
(25, 'Petra Pomp', 'Testadresse 98324', 28000, 0, 9, 4, 'FEMALE', '1978-04-27'),
(26, 'Fritz Lohnert', 'Testaddresse 99833', 54500, 1, 10, 3, 'MALE', '1969-03-02'),
(27, 'Fiona Schmitz', 'Testadresse 34645', 29800, 0, 10, 3, 'FEMALE', '1978-12-11'),
(28, 'Alexander Klein', 'Testadresse 46334', 47200, 0, 11, 5, 'MALE', '1969-06-06'),
(29, 'Robert Janzen', 'Testadresse 64334', 54000, 0, 11, 9, 'MALE', '1959-09-04'),
(30, 'Helena Gerber', 'Testadresse 74543', 46000, 0, 11, 5, 'FEMALE', '1968-11-14'),
(31, 'Frank Frisch', 'Testadresse 84563', 57000, 0, 12, 9, 'MALE', '1965-07-14'),
(32, 'Jana Mess', 'Testadresse 7435435', 51000, 0, 12, 9, 'FEMALE', '1968-04-27'),
(33, 'Anne Siebert', 'Testadresse 76435433', 42000, 0, 12, 8, 'FEMALE', '1973-02-11'),
(34, 'Renate Weiler', 'Testadresse 843543', 46000, 0, 12, 8, 'FEMALE', '1969-05-18'),
(35, 'Werner Riedel', 'Testadresse 832432', 54000, 1, 13, 8, 'MALE', '1963-06-23'),
(36, 'Sebastien Schmied', 'Testadresse 83234', 41500, 0, 13, 8, 'MALE', '1979-12-02'),
(37, 'Bernd Kütter', 'Testadresse 32434523', 78000, 1, 13, 10, 'MALE', '1972-04-02'),
(38, 'Angelika Klassen', 'Testadresse 34234', 72000, 1, 1, 10, 'FEMALE', '1968-11-13'),
(39, 'Ingo Strater', 'Testadresse 435435', 72000, 1, 4, 10, 'MALE', '1970-03-03'),
(40, 'Herbert Feiler', 'Testadresse 75342', 41400, 0, 4, 7, 'MALE', '1962-04-24'),
(41, 'Inge Helfer', 'Testadresse 324324', 42000, 0, 4, 7, 'FEMALE', '1971-08-26');


