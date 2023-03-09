import sqlite3
db = sqlite3.connect('database.db')
db.executescript("PRAGMA foreign_keys=ON")
cur = db.cursor()

def main():
    userInput = -1
    #Menu
    while(userInput != "0"):
        print("\nMenu options:")
        print("1: Add character")
        print("2: Update character")
        print("3: Delete character")
        print("4: Search inventory")
        print("5: Print example queries")
        print("0: Quit")
        userInput = input("What do you want to do: ")
        if int(userInput) < 0 or int(userInput) > 5:
            print("Invalid input")
            continue
        if userInput == "1":
            insertCharacter()
        if userInput == "2":
            updateCharacter()
        if userInput == "3":
            deleteCharacter()
        if userInput == "4":
            searchInventory()
        if userInput == "5":
            printQueries()
        if userInput == "0":
            print("Shutting down...")
            break
    db.close()        
    return

#Add character to database
def insertCharacter():
    playerName = input("Add characher name: ")
    #Check if name is empty
    if playerName == "":
        print("Invalid name")
        return
    selectedWeapon = int(input("Select weapon for you character: \n 1) Sword, 2) Axe, 3) Bow, 4), Spear, 5) Staff: "))
    #Check if weapon choice is valid
    if selectedWeapon < 1 or selectedWeapon > 5:
        print("Invalid weapon selection")
        return
    if selectedWeapon == 1:
        weaponName = "Sword"
    elif selectedWeapon == 2:
        weaponName = "Axe"
    elif selectedWeapon == 3:
        weaponName = "Bow"
    elif selectedWeapon == 4:
        weaponName = "Spear"
    elif selectedWeapon == 5:
        weaponName = "Staff"
    health = int(input("Add health (10 - 1 000): "))
    #Check if health is valid
    if health < 10 or health > 1000:
        print("Invalid health selection")
        return
    try:
        #Add character to database
        cur.execute("SELECT PlayerID FROM Character ORDER BY PlayerID DESC LIMIT 1;")
        playerID = cur.fetchone()[0]
        playerID = int(playerID) + 1
        cur.execute("INSERT INTO Character (PlayerID, name, health, isSelected) VALUES (?, ?, ?, ?);", (playerID, playerName, health, selectedWeapon))
        #Add weapon to inventory
        cur.execute("INSERT INTO Inventory (PlayerID, WeaponID) VALUES (?, ?);", (playerID, selectedWeapon))
        db.commit()
    #Raise error if name already exists
    except sqlite3.IntegrityError:
        print("Name already exists. Choose different name.")
        db.rollback()
        return
    #Raise error if database error      
    except db.Error:
        print("Error!")
        db.rollback()
        return
    print("Character added: \n PlayerID:", playerID, " \n Name: ", playerName, " \n Weapon: ", weaponName, " \n Health: ", health)
    return

#Update character in database
def updateCharacter():
    characterID = input("What is the character's ID: ")
    try:
        #Select character from database and print name and current weapon and health
        cur.execute("SELECT * FROM Character WHERE PlayerID = ?;", (characterID,))
        data = cur.fetchall()
        cur.execute("SELECT name FROM Weapon WHERE WeaponID = ?;", (data[0][3],))
        weaponSelected = cur.fetchone()[0]
        print("Character selected: ", data[0][1])
        print("Your character's current weapon is: ", weaponSelected)
        print("Your character's current health is: ", data[0][2])
        #Select all weapons from inventory and add them to a list if there are any
        cur.execute("SELECT WeaponID FROM Inventory WHERE PlayerID = ?;", (characterID,))
        weaponID = cur.fetchall()
        cur.execute("SELECT name FROM Weapon WHERE WeaponID = ?;", (weaponID[0][0],))
        weaponName = cur.fetchone()
        cur.execute("SELECT WeaponID FROM Inventory WHERE PlayerID = ?;", (characterID,))
        weaponID = cur.fetchall()
        listOfWeapons = []
        for i in range(len(weaponID)):
            cur.execute("SELECT name FROM Weapon WHERE WeaponID = ?;", (weaponID[i][0],))
            weaponName = cur.fetchone()[0]
            listOfWeapons.append(weaponName)
        print()
        #If there are no weapons in inventory, print error message and ask for new health
        if len(listOfWeapons) == 0:
            print("Your inventory is empty. Cannot change weapon.")
            health = int(input("Add new health (10 - 1 000): "))
            if health < 10 or health > 1000:
                print("Invalid health selection")
                return
            #Update health
            cur.execute("UPDATE Character SET health = ? WHERE PlayerID = ?;", (health, characterID,))
            db.commit()
            print("Character updated: \n New health: ", health)
            return
        #If there are weapons in inventory, print them and ask for new weapon and health
        else:
            print("Select new weapon from your inventory:")
            for i in range(len(listOfWeapons)):
                print(i+1, ")", listOfWeapons[i])
            selectedWeapon = int(input("Select weapon: "))
            if selectedWeapon < 1 or selectedWeapon > len(listOfWeapons):
                print("Invalid weapon selection")
                return
            weaponName = listOfWeapons[selectedWeapon-1]
            if weaponName == "Sword":
                weaponID = 1
            elif weaponName == "Axe":
                weaponID = 2
            elif weaponName == "Bow":
                weaponID = 3
            elif weaponName == "Spear":
                weaponID = 4
            elif weaponName == "Staff":
                weaponID = 5
            health = int(input("Add new health (10 - 1 000): "))
            if health < 10 or health > 1000:
                print("Invalid health selection")
                return
            #Update weapon and health
            cur.execute("UPDATE Character SET isSelected = ?, health = ? WHERE PlayerID = ?;", (weaponID, health, characterID,))
            db.commit()
            cur.execute("SELECT name FROM Weapon WHERE WeaponID = ?;", (weaponID,))
            newWeaponName = cur.fetchone()[0]
            print("Character updated: \n New weapon: ", newWeaponName, " \n New health: ", health)
            return
    #Raise error if character does not exist
    except IndexError:
        print("Player with PlayerID '{}' does not exist".format(characterID))
        return
    #Raise error if database error
    except db.Error:
        print("Error!")
        db.rollback()
        return

#Delete character from database
def deleteCharacter():
    characterID = input("What is the player's PlayerID you want to delete: ")
    try:
        #Delete character from database
        cur.execute("SELECT name FROM Character WHERE PlayerID = ?;", (characterID,))
        name = cur.fetchone()[0]
        cur.execute("DELETE FROM Character WHERE PlayerID = ?;", (characterID,))
        db.commit()
    #Raise error if character does not exist
    except TypeError:
        print("Player with PlayerID '{}' does not exist".format(characterID))
        return
    #Raise error if database error
    except db.Error:
        print("Error!")
        db.rollback()
        return
    print("Character '{}' deleted".format(name))
    return

#Search for character's inventory
def searchInventory():
    characterID = input("What PlayerID's inventory you want to search: ")
    try:    
        #Select character and inventory from database and print them
        cur.execute("SELECT name FROM Character WHERE PlayerID = ?;", (characterID,))
        playerName = cur.fetchone()[0]
        cur.execute("SELECT WeaponID FROM Inventory WHERE PlayerID = ?;", (characterID,))
        weaponID = cur.fetchall()
        if len(weaponID) == 0:
            print("'{}' inventory is empty".format(playerName))
            return
        print("'{}' Inventory: ".format(playerName))
        print("Weapons:")
        for i in range(len(weaponID)):
            cur.execute("SELECT name FROM Weapon WHERE WeaponID = ?;", (weaponID[i][0],))
            weaponName = cur.fetchone()[0]
            print(weaponName)
    #Raise error if character does not exist
    except TypeError:
        print("Player with PlayerID '{}' does not exist".format(characterID))
        return
    #Raise error if database error
    except db.Error:
        print("Error!")
        db.rollback()
        return
    return

#Print example queries
def printQueries():
    try:
        print("")
        print("Example queries:\n")
        print("All players, and their stats")
        print("SELECT * FROM Character;")
        print("(PlayerID, name, health, isSelected)")
        print("----------------------------------")
        cur.execute("SELECT * FROM Character;")
        data = cur.fetchall()
        for i in range(len(data)):
            print(data[i])
        
        print("")
        print("Player 1 inventory")
        print("SELECT * FROM Inventory WHERE PlayerID = 1;")
        print("(PlayerID, WeaponID)")
        print("----------------------------------")
        cur.execute("SELECT * FROM Inventory WHERE PlayerID = 1;")
        data = cur.fetchall()
        for i in range(len(data)):
            print(data[i])
        
        print("")
        print("All players weapons stats")
        print("SELECT * FROM Weapon INNER JOIN Inventory ON Weapon.WeaponID = Inventory.WeaponID;")
        print("(WeaponID, damage, name, PlayerID, WeaponID)")
        print("----------------------------------")
        cur.execute("SELECT * FROM Weapon INNER JOIN Inventory ON Weapon.WeaponID = Inventory.WeaponID;")
        data = cur.fetchall()
        for i in range(len(data)):
            print(data[i])
        
        print("")
        print("Player friendlist")
        print("SELECT * FROM FriendList INNER JOIN Friend ON FriendList.FriendID = Friend.PlayerID;")
        print("(PlayerID, FriendID, FriendPlayerID, name, health)")
        print("----------------------------------")
        cur.execute("SELECT * FROM FRIENDLIST INNER JOIN Friend ON FriendList.FriendID = Friend.PlayerID;")
        data = cur.fetchall()
        for i in range(len(data)):
            print(data[i])
        
        print("")
        print("All weapons and their attack types where attack multiplier is over 1")
        print("SELECT * FROM Weapon INNER JOIN AttackType ON Weapon.WeaponID = AttackType.WeaponID WHERE AttackType.AttackMultiplier > 1 ORDER BY Weapon.name;")
        print("(WeaponID, damage, name, WeaponID, AttackMultiplier)")
        print("----------------------------------")
        cur.execute("SELECT * FROM Weapon INNER JOIN AttackType ON Weapon.WeaponID = AttackType.WeaponID WHERE AttackType.AttackMultiplier > 1 ORDER BY Weapon.name;")
        data = cur.fetchall()
        for i in range(len(data)):
            print(data[i])

    except db.Error:
        print("Error!")
        db.rollback()
        return
    return

main()