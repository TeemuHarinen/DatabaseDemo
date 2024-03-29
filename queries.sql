/*
CREATE TABLE Character (
    PlayerID int NOT NULL,
    name varchar(255) NOT NULL UNIQUE,
    health int NOT NULL DEFAULT 100 CHECK(health > 0),
    isSelected int DEFAULT 1,
    PRIMARY KEY (PlayerID),
    FOREIGN KEY (isSelected) REFERENCES Weapon(WeaponID) ON DELETE SET DEFAULT
);


CREATE TABLE Inventory (
    PlayerID int NOT NULL,
    WeaponID int NOT NULL,
    FOREIGN KEY (WeaponID) REFERENCES Weapon(WeaponID) ON DELETE CASCADE,
    FOREIGN KEY (PlayerID) REFERENCES Character(PlayerID) ON DELETE CASCADE
);

CREATE TABLE FriendList (
    PlayerID int NOT NULL,
    FriendID int NOT NULL,
    FOREIGN KEY (PlayerID) REFERENCES Character(PlayerID) ON DELETE CASCADE,
    FOREIGN KEY (FriendID) REFERENCES Friend(PlayerID) ON DELETE CASCADE
);

CREATE TABLE Friend (
    PlayerID int NOT NULL,
    name varchar(255) NOT NULL,
    health int NOT NULL,
    PRIMARY KEY (PlayerID)
);

CREATE TABLE Weapon (
    WeaponID int NOT NULL,
    Power int NOT NULL,
    name varchar(255) NOT NULL,
    PRIMARY KEY (WeaponID)
);

CREATE TABLE AttackType (
    WeaponID int NOT NULL,
    AttackType varchar(255) NOT NULL,
    AttackMultiplier int NOT NULL,
    FOREIGN KEY (WeaponID) REFERENCES Weapon(isSelected) ON DELETE CASCADE
);
*/

/*
INSERT INTO Character (PlayerID, name, isSelected) VALUES (1, 'Player1', 1);
INSERT INTO Character (PlayerID, name, health, isSelected) VALUES (2, 'Player2', 200, 1);
INSERT INTO Character (PlayerID, name, health, isSelected) VALUES (3, 'Player3', 100, 1);
INSERT INTO Character (PlayerID, name, health, isSelected) VALUES (4, 'Player4', 250, 1);
INSERT INTO Character (PlayerID, name, health, isSelected) VALUES (5, 'Player5', 100, 1);
INSERT INTO Character (PlayerID, name, health, isSelected) VALUES (6, 'Player6', 300, 1);

INSERT INTO Inventory (PlayerID, WeaponID) VALUES (1, 1);
INSERT INTO Inventory (PlayerID, WeaponID) VALUES (1, 2);
INSERT INTO Inventory (PlayerID, WeaponID) VALUES (1, 3);
INSERT INTO Inventory (PlayerID, WeaponID) VALUES (1, 4);
INSERT INTO Inventory (PlayerID, WeaponID) VALUES (1, 5);
INSERT INTO Inventory (PlayerID, WeaponID) VALUES (2, 1);
INSERT INTO Inventory (PlayerID, WeaponID) VALUES (3, 1);
INSERT INTO Inventory (PlayerID, WeaponID) VALUES (4, 1);
INSERT INTO Inventory (PlayerID, WeaponID) VALUES (5, 1);
INSERT INTO Inventory (PlayerID, WeaponID) VALUES (6, 1);

INSERT INTO FriendList (PlayerID, FriendID) VALUES (1, 2);
INSERT INTO FriendList (PlayerID, FriendID) VALUES (1, 3);
INSERT INTO FriendList (PlayerID, FriendID) VALUES (1, 4);
INSERT INTO FriendList (PlayerID, FriendID) VALUES (1, 5);
INSERT INTO FriendList (PlayerID, FriendID) VALUES (1, 6);

INSERT INTO Friend (PlayerID, name, health) VALUES (2, 'Player2', 100);
INSERT INTO Friend (PlayerID, name, health) VALUES (3, 'Player3', 100);
INSERT INTO Friend (PlayerID, name, health) VALUES (4, 'Player4', 100);
INSERT INTO Friend (PlayerID, name, health) VALUES (5, 'Player5', 100);
INSERT INTO Friend (PlayerID, name, health) VALUES (6, 'Player6', 100);

INSERT INTO Weapon (WeaponID, Power, name) VALUES (1, 10, 'Sword');
INSERT INTO Weapon (WeaponID, Power, name) VALUES (2, 20, 'Axe');
INSERT INTO Weapon (WeaponID, Power, name) VALUES (3, 15, 'Bow');
INSERT INTO Weapon (WeaponID, Power, name) VALUES (4, 25, 'Spear');
INSERT INTO Weapon (WeaponID, Power, name) VALUES (5, 30, 'Staff');

INSERT INTO AttackType (WeaponID, AttackType, AttackMultiplier) VALUES (1, 'Slash', 1);
INSERT INTO AttackType (WeaponID, AttackType, AttackMultiplier) VALUES (1, 'HeavyAttack', 2);
INSERT INTO AttackType (WeaponID, AttackType, AttackMultiplier) VALUES (1, 'ComboAttack', 3);
INSERT INTO AttackType (WeaponID, AttackType, AttackMultiplier) VALUES (2, 'Slash', 1);
INSERT INTO AttackType (WeaponID, AttackType, AttackMultiplier) VALUES (2, 'HeavyAttack', 2);
INSERT INTO AttackType (WeaponID, AttackType, AttackMultiplier) VALUES (2, 'ComboAttack', 3);
*/

/*
-- DROP TABLES SHORTCUT FOR TESTING PURPOSES ONLY!
DROP TABLE Character;
DROP TABLE Inventory;
DROP TABLE FriendList;
DROP TABLE Friend;
DROP TABLE Weapon;
DROP TABLE AttackType;
*/


-- Player 1 st
SELECT * FROM Character;
-- Player 1 weapons
SELECT * FROM Inventory WHERE PlayerID = 1;
-- Player 1 weapons and their stats
SELECT * FROM Weapon INNER JOIN Inventory ON Weapon.WeaponID = Inventory.WeaponID;
-- Player friends
SELECT * FROM FriendList INNER JOIN Friend ON FriendList.FriendID = Friend.PlayerID WHERE FriendList.PlayerID = 1;
-- Weapon stats and corresponding attack types
SELECT * FROM Weapon INNER JOIN AttackType ON Weapon.WeaponID = AttackType.WeaponID WHERE AttackType.AttackMultiplier > 1;

-- Indexes to speed up queries

/*
CREATE INDEX PlayerID ON Character(PlayerID);
CREATE INDEX WeaponID ON Weapon(WeaponID);
*/




