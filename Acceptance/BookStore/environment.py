from Source.SocketServer.HTTPSocketService import HTTPSocketService
from Source.BookStore import BookStore
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlDatabase import SqlDatabase
from Source.SocketServer.SimpleSocketServer import SimpleSocketServer


def before_scenario(context, scenario):
    clearDatabase()
    context.defaultPort = 8091
    context.bookStore = BookStore(PersistentCatalog())
    context.service = HTTPSocketService(context.bookStore)
    context.server = SimpleSocketServer(service=context.service, port=context.defaultPort)
    context.server.start()


def after_scenario(context,scenario):
    context.server.stop()


def clearDatabase():
    SqlDatabase().clearData()
