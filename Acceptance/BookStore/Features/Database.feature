Feature: Storing books in a catalog
    Scenario: Access book catalog
        Given A user added books to the catalog
        When The catalog is accessed
        Then The user can see the books in the catalog
