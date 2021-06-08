CREATE TABLE `h1queries` (
  `queryid` int(11) NOT NULL AUTO_INCREMENT,
  `patientid` int(11) NOT NULL,
  `datequery` datetime NOT NULL DEFAULT current_timestamp(),
  `result` float NOT NULL,
  `age` int(11) NOT NULL,
  `sex` int(11) NOT NULL,
  `cp` int(11) NOT NULL,
  `trestbps` int(11) NOT NULL,
  `chol` int(11) NOT NULL,
  `fbs` tinyint(4) NOT NULL,
  `restecg` int(11) NOT NULL,
  `thalach` int(11) NOT NULL,
  `exang` tinyint(4) NOT NULL,
  `oldpeak` float NOT NULL,
  `slope` int(11) NOT NULL,
  `ca` int(11) NOT NULL,
  `thal` int(11) NOT NULL,
  PRIMARY KEY (`queryid`),
  KEY `patientid_idx` (`patientid`),
  CONSTRAINT `patientid` FOREIGN KEY (`patientid`) REFERENCES `patients` (`patientid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `patients` (
  `patientid` int(11) NOT NULL AUTO_INCREMENT,
  `patientname` varchar(255) NOT NULL,
  `userid` int(11) NOT NULL,
  PRIMARY KEY (`patientid`),
  KEY `userid_idx` (`userid`),
  CONSTRAINT `userid` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `users` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `role` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
