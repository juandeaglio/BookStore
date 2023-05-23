from Source.Database.SqlDatabase import SqlDatabase


def before_scenario(context, scenario):
    clearDatabase()


def clearDatabase():
    SqlDatabase().clearData()
