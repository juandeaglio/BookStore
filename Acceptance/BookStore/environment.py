from Source.SqlDatabase import SqlDatabase

def before_feature(context, feature):
    clearDatabase()

def clearDatabase():
    SqlDatabase().clearData()

