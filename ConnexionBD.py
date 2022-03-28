from http.client import NotConnected
from sqlite3 import connect
import mysql.connector
import time
import json

class Database:
  def __init__(self, host, port, user, password, database, serveur):
    self.host = host
    self.port = port
    self.user = user
    self.password = password
    self.database = database
    self.cursor = None
    self.con = None
    self.serveur = serveur

  def connect(self):
    try:
      self.con = mysql.connector.connect(
        host = self.host,
        port = self.port,
        user = self.user,
        password = self.password,
        database = self.database
      )
      
      self.cursor = self.con.cursor()

    except mysql.connector.Error as error:
      print("Database error : try later")

  def addUser(self, username = str, password = str):
    try:
      self.connect()

      sqlverif = "SELECT username FROM users WHERE username = '" + str(username) +"'"
      self.cursor.execute(sqlverif)
      result = self.cursor.fetchone()

      if result != None:
        print("Try something else")

      else:
        sql = "INSERT INTO users (id, username, password, privilege) VALUES (%s, %s, %s, %s)"
        val = (0 , username, password, 1)
        self.cursor.execute(sql, val)
        self.con.commit()
        time.sleep(2)
        self.serveur.sendMsg("addUser : Success")

    except mysql.connector.Error as error:
      print("Database error : try later\n {}".format(error))

    finally:
      if self.con.is_connected():
        self.con.close()
        self.cursor.close()
        
  def addCharacter(self, username = str, password = str, characterName = str):
    try:
      self.connect()
      
      sqlUserVerif = "SELECT username, password FROM users WHERE username = '" + str(username) +"' AND password = '" + str(password) +"'"
      self.cursor.execute(sqlUserVerif)
      resultUser = self.cursor.fetchone()
      
      if resultUser != None:
        #print("compte valide")
        sqlverif = "SELECT name FROM characters WHERE name = '" + str(characterName) +"'"
        self.cursor.execute(sqlverif)
        result = self.cursor.fetchone()
        
        if result != None:
          print("Try something else")
          
        else:
          #print("pseudoValide")
          sqlPseudoVerif = "SELECT id FROM users WHERE username = '" + str(username) +"'"
          self.cursor.execute(sqlPseudoVerif)
          idcompte = str(self.cursor.fetchone())
          
          sql = "INSERT INTO characters (id, idcompte, name, level, hp, mp, map, cellule) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
          val = (0, int(idcompte[1:idcompte.find(',')]), characterName, 1, 25, 25, 1, "A1")
          self.cursor.execute(sql, val)
          self.con.commit()
          self.cursor.close()
          print("addCharacter : Success")

    except mysql.connector.Error as error:
      print("Database error : try later\n {}".format(error))

    finally:
      if self.con.is_connected():
        self.con.close()
        self.cursor.close()

  def getCharacter(self, username = str, password = str):
    try:
      self.connect()

      sqlverif = "SELECT username, password FROM users WHERE username = '" + str(username) +"' AND password = '" + str(password) +"'"
      self.cursor.execute(sqlverif)
      result = self.cursor.fetchone()

      if result == None:
        print("username or password incorrect")

      else:
        sqlPseudoVerif = "SELECT id FROM users WHERE username = '" + str(username) +"'"
        self.cursor.execute(sqlPseudoVerif)
        idcompte = str(self.cursor.fetchone())
        print("idcompte:" + idcompte[1:idcompte.find(',')])
        
        sql = "SELECT * FROM characters WHERE idcompte =" + idcompte[1:idcompte.find(',')]
        self.cursor.execute(sql)
        characters = self.cursor.fetchall()
        if(len(characters) <= 3):
          self.serveur.sendMsg("getchaempty")
        else:
          self.serveur.sendMsg("getCharacter " + str(characters))

    except mysql.connector.Error as error:
      print("Database error : try later\n {}".format(error))

    finally:
      if self.con.is_connected():
        self.con.close()
        self.cursor.close()
        
  def getCharacterJson(self, username = str, password = str):
    try:
      self.connect()

      sqlverif = "SELECT username, password FROM users WHERE username = '" + str(username) +"' AND password = '" + str(password) +"'"
      self.cursor.execute(sqlverif)
      result = self.cursor.fetchone()

      if result == None:
        print("username or password incorrect")

      else:
        sqlPseudoVerif = "SELECT id FROM users WHERE username = '" + str(username) +"'"
        self.cursor.execute(sqlPseudoVerif)
        idcompte = str(self.cursor.fetchone())
        print("idcompte:" + idcompte[1:idcompte.find(',')])
        
        sql = "SELECT * FROM characters WHERE idcompte =" + idcompte[1:idcompte.find(',')]
        self.cursor = self.con.cursor(dictionary=True)
        self.cursor.execute(sql)
        characters = self.cursor.fetchall()
        self.serveur.sendMsg("getCharacterJson " + json.dumps(characters))

    except mysql.connector.Error as error:
      print("Database error : try later\n {}".format(error))

    finally:
      if self.con.is_connected():
        self.con.close()
        self.cursor.close()

  def getuser(self, username = str, password = str):
    try:
      self.connect()

      sqlverif = "SELECT username, password FROM users WHERE username = '" + str(username) +"' AND password = '" + str(password) +"'"
      self.cursor.execute(sqlverif)
      result = self.cursor.fetchone()

      if result == None:
        print("username or password incorrect")
      else:
        print("user ok")
        self.serveur.sendMsg("tryco valide" + username + password)
        
        
    except mysql.connector.Error as error:
      print("Database error : try later\n {}".format(error))
      
    finally:
      if self.con.is_connected():
        self.con.close()
        self.cursor.close()
        
  def updatePos(self, chaName = str, cellule = str):
    try:
      self.connect()

      sqlverif = "SELECT name FROM characters WHERE name = '" + str(chaName) + "'"
      self.cursor.execute(sqlverif)
      result = self.cursor.fetchone()

      if result == None:
        print("chaName incorrect :" + chaName)
      else:
        sqlup = "UPDATE characters SET cellule = '" + cellule + "' WHERE name = '" + str(chaName) + "'"
        self.cursor.execute(sqlup)
        self.con.commit()
    except mysql.connector.Error as error:
      print("Database error : try later\n {}".format(error))
    finally:
      if self.con.is_connected():
        self.con.close()
        self.cursor.close()
        
  def setPos(self, chaName = str):
    try:
      self.connect()
      sqlverif = "SELECT cellule FROM characters WHERE name = '" + str(chaName) + "'"
      self.cursor.execute(sqlverif)
      result = self.cursor.fetchone()
      self.serveur.sendMsg("curPos " + str(result))
      self.serveur.grid.setXYJ(str(result))
    except mysql.connector.Error as error:
      print("Database error : try later\n {}".format(error))
    finally:
      if self.con.is_connected():
        self.con.close()
        self.cursor.close()
