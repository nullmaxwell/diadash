import json

from src import data


class CredentialHandler:
    """
    Medtronic CareLink Credential Handler.
    """

    # Class Attributes
    RAW_DATA = None
    credential_loc = "src/credentials/credentials.json"

    def __init__(self) -> None:
        """
        Constructor for the credentials.
        """
        CredentialHandler.loadCredentials()
        self.USER = CredentialHandler.setUser()
        self.TOKEN = CredentialHandler.setToken()
        self.NOTE = CredentialHandler.setNote()
        pass

    @classmethod
    def setUser(cls):
        """
        Sets the user credential.
        """
        return CredentialHandler.RAW_DATA["user"]

    def getUser(self) -> str:
        """
        Getter method for the token.
        """
        return self.USER

    @classmethod
    def setToken(cls):
        """
        Sets the token credential.
        """
        return CredentialHandler.RAW_DATA["token"]

    def getToken(self) -> str:
        """
        Getter method for the token.
        """
        return self.TOKEN

    @classmethod
    def setNote(cls):
        """
        Sets the token credential.
        """
        return CredentialHandler.RAW_DATA["note"]

    def getNote(self) -> str:
        """
        Getter method for the note.
        """
        return self.NOTE

    @classmethod
    def loadCredentials(cls) -> any:
        """
        Loads User and Token information from a credential file.
        """
        try:
            f = open(CredentialHandler.credential_loc)
            data = json.load(f)
            CredentialHandler.RAW_DATA = data["Credential"][0]
            f.close()
        except FileNotFoundError:
            print(">>> Credentials not found... exiting.")
            raise
        pass
