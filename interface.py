import sqlite3
db = sqlite3.connect('database.db')
cur = db.cursor()

def main():
    userInput = -1
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
            insertPlayer()
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

def insertPlayer():
    playerName = input("Add characher name: ")
    if playerName == "":
        print("Invalid name")
        return
    selectedWeapon = int(input("Select weapon for you character: \n 1) Sword, 2) Axe, 3) Bow, 4), Spear, 5) Staff: "))
    if selectedWeapon < 1 or selectedWeapon > 5:
        print("Invalid weapon selection")
        return
    health = int(input("Add health (10 - 1 000): "))
    if health < 10 or health > 1000:
        print("Invalid health selection")
        return
    try:
        cur.execute("SELECT PlayerID FROM Character ORDER BY PlayerID DESC LIMIT 1;")
        playerID = cur.fetchone()[0]
        playerID = int(playerID) + 1
        cur.execute("INSERT INTO Character (PlayerID, name, health, isSelected) VALUES (?, ?, ?, ?);", (playerID, playerName, health, selectedWeapon))
        db.commit()
    except sqlite3.IntegrityError:
        print("Name already exists. Choose different name.")
        db.rollback()
        return      
    except db.Error:
        print("Error!")
        db.rollback()
        return
    print("Character added: \n PlayerID:", playerID, " \n Name: ", playerName, " \n Weapon: ", selectedWeapon, " \n Health: ", health)
    return

def updateCharacter():
    characterID = input("What is the character's ID: ")
    try:
        cur.execute("SELECT * FROM Character WHERE PlayerID = ?;", (characterID,))
        data = cur.fetchall()
        cur.execute("SELECT name FROM Weapon WHERE WeaponID = ?;", (data[0][3],))
        weaponName = cur.fetchone()[0]
        print("Character selected: ", data[0][1])
        print("Your character's current weapon is: ", weaponName)
        print("Your character's current health is: ", data[0][2])
        cur.execute("SELECT WeaponID FROM Inventory WHERE PlayerID = ?;", (characterID,))
        weaponID = cur.fetchall()
        listOfWeapons = []
        for i in range(len(weaponID)):
            cur.execute("SELECT name FROM Weapon WHERE WeaponID = ?;", (weaponID[i][0],))
            weaponName = cur.fetchone()[0]
            listOfWeapons.append(weaponName)
        print()
        if len(listOfWeapons) == 0:
            print("Your inventory is empty. Cannot change weapon.")
            health = int(input("Add new health (10 - 1 000): "))
            if health < 10 or health > 1000:
                print("Invalid health selection")
                return
            cur.execute("UPDATE Character SET health = ? WHERE PlayerID = ?;", (health, characterID,))
            db.commit()
            print("Character updated: \n New health: ", health)
            return
        else:
            print("Select new weapon from your inventory:")
            for i in range(len(listOfWeapons)):
                print(i+1, ")", listOfWeapons[i])
            selectedWeapon = int(input("Select weapon: "))
            if selectedWeapon < 1 or selectedWeapon > len(listOfWeapons):
                print("Invalid weapon selection")
                return
            health = int(input("Add new health (10 - 1 000): "))
            if health < 10 or health > 1000:
                print("Invalid health selection")
                return
            cur.execute("UPDATE Character SET isSelected = ?, health = ? WHERE PlayerID = ?;", (selectedWeapon, health, characterID,))
            db.commit()
            cur.execute("SELECT name FROM Weapon WHERE WeaponID = ?;", (selectedWeapon,))
            newWeaponName = cur.fetchone()[0]
            print("Character updated: \n New weapon: ", newWeaponName, " \n New health: ", health)
            return
    except IndexError:
        print("Player with PlayerID '{}' does not exist".format(characterID))
        return
    except db.Error:
        print("Error!")
        db.rollback()
        return

def deleteCharacter():
    characterID = input("What is the player's PlayerID you want to delete: ")
    try:
        cur.execute("SELECT name FROM Character WHERE PlayerID = ?;", (characterID,))
        name = cur.fetchone()[0]
        cur.execute("DELETE FROM Character WHERE PlayerID = ?;", (characterID,))
        db.commit()
    except TypeError:
        print("Player with PlayerID '{}' does not exist".format(characterID))
        return
    except db.Error:
        print("Error!")
        db.rollback()
        return
    print("Character '{}' deleted".format(name))
    return

def searchInventory():
    characterID = input("What PlayerID's inventory you want to search: ")
    try:    
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
    except TypeError:
        print("Player with PlayerID '{}' does not exist".format(characterID))
        return
    except db.Error:
        print("Error!")
        db.rollback()
        return
    return

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
        print("Player 1 weapons stats")
        print("SELECT * FROM Weapon INNER JOIN Inventory ON Weapon.WeaponID = Inventory.WeaponID WHERE PlayerID = 1;")
        print("(WeaponID, damage, name, PlayerID, WeaponID)")
        print("----------------------------------")
        cur.execute("SELECT * FROM Weapon INNER JOIN Inventory ON Weapon.WeaponID = Inventory.WeaponID WHERE PlayerID = 1;")
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
        print("All weapons and their attack types")
        print("SELECT * FROM Weapon INNER JOIN AttackType ON Weapon.WeaponID = AttackType.WeaponID ORDER BY Weapon.name;")
        print("(WeaponID, damage, name, WeaponID, AttackMultiplier)")
        print("----------------------------------")
        cur.execute("SELECT * FROM Weapon INNER JOIN AttackType ON Weapon.WeaponID = AttackType.WeaponID ORDER BY Weapon.name;")
        data = cur.fetchall()
        for i in range(len(data)):
            print(data[i])

    except db.Error:
        print("Error!")
        db.rollback()
        return
    return

main()