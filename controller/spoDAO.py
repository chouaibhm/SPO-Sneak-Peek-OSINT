__Author__ = 'Victor de Queiroz'
"""
 Data Access Object
 
 class for querys sql

"""
from controller import DataFactory
from controller import PasswdHash
from controller import validatorSQLI

class SpoDAO(object):


    #instance of controller.dataFactory
    connection = DataFactory.DataFactory()
    #instance of PasswordHash
    passhash = PasswdHash.PasswdHash()
    #validator SQLI
    sqli = validatorSQLI.ValidateSQLI()

    #function for test if first access
    def testFirstAccess(self):
        # if is first access return True
        sql = "select * from user_spo;"
        if self.connection.select(sql) is None:
            return True
        else:
            return False

    #for first access create an user
    #recive password on plain text, send to cripto and cripto
    # returns a hash for db insert
    def insertUser(self,user,passwd):

        #send password for PasswdHash
        password = self.passhash.hash(passwd)
        #query sql for insert user and pass
        #validate SQLI
        if self.sqli.validatorSQLI(user) == False:
            sql = "insert into user_spo(login,password) values ('"+user+"','"+password+"');"
        #execute a query
        self.connection.insert(sql)

    #validator for login
    def testLogin(self,user,passwd):
        #validate SQLI
        if self.sqli.validatorSQLI(user) == False:
            #hash the password
            password = self.passhash.hash(passwd)
            #select query
            sql ="select login,password from user_spo where login ='"+user+"' and password ='"+password+"';"
            if self.connection.select(sql) is None:
                return False
            else:
                return True

    #get id user
    def getIDUser(self,user):
        # get id to user
        id = self.connection.select("select id_user from user_spo where login='" + user + "'")
        return id

    #insert key
    def insertKey(self,id,key,nameKey):
       #validate SQLI
        if self.sqli.validatorSQLI(key) == False and self.sqli.validatorSQLI(nameKey) == False:
            #insert query
            sql =  "insert into key_api(key_value,name_key,id_user) values('"+key+"','"+nameKey+"',"+str(id['id_user'])+");"

            self.connection.insert(sql)




