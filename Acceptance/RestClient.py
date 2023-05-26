import socket
from Unit.Client import Client
from Source.RestMessage import GetCatalogRestMessage


class RestClient(Client):
    @staticmethod
    def createClientThatGetsCatalog(port=8091):
        client = RestClient.createClient(port)
        client.send(GetCatalogRestMessage().toBytes())
        return client

    @staticmethod
    def createClient(port):
        return Client.createClient(port)
