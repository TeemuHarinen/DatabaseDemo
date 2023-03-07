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
        print("0: Quit")
        userInput = input("What do you want to do: ")
        if int(userInput) < 0 or int(userInput) > 4:
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
    except db.Error:
        print("Error!")
        db.rollback()
        return
    print("Character added: \n PlayerID", playerID, " \n Name: ", playerName, " \n Weapon: ", selectedWeapon, " \n Health: ", health)
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
        print()
        selectedWeapon = int(input("Select new weapon for your character: \n 1) Sword, 2) Axe, 3) Bow, 4), Spear, 5) Staff: "))
        if selectedWeapon < 1 or selectedWeapon > 5:
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
    except db.Error:
        print("Error!")
        db.rollback()
        return
    print("Character updated: \n New weapon: ", newWeaponName, " \n New health: ", health)
    return

def deleteCharacter():
    characterID = input("What is the player's PlayerID you want to delete: ")
    try:
        cur.execute("SELECT name FROM Character WHERE PlayerID = ?;", (characterID,))
        name = cur.fetchone()[0]
        cur.execute("DELETE FROM Character WHERE PlayerID = ?;", (characterID,))
        db.commit()
    except db.Error:
        print("Error!")
        db.rollback()
        return
    print("Character '{}' deleted".format(name))
    return

def searchInventory():
    charaterID = input("What PlayerID's inventory you want to search: ")
    try:    
        cur.execute("SELECT name FROM Character WHERE PlayerID = ?;", (charaterID,))
        playerName = cur.fetchone()[0]
        cur.execute("SELECT WeaponID FROM Inventory WHERE PlayerID = ?;", (charaterID,))
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
    except db.Error:
        print("Error!")
        db.rollback()

    return
main()