Feature: Book catalog
    Scenario: View a persistent catalog
        Given A catalog
        |Title                                  |Author             |Release year   |
        |The Hunger Games                       |Suzanne Collins    |2008           |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |
        When A user views the catalog
        Then The entire catalog is displayed
        |Title                                  |Author             |Release year   |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |
        |The Hunger Games                       |Suzanne Collins    |2008           |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |

    Scenario: No duplicates in the catalog
        Given A catalog
        |Title                                  |Author             |Release year   |
        |The Hunger Games                       |Suzanne Collins    |2008           |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |
        When The admin add a duplicate book to the catalog
        Then There will be no changes to the catalog
        |Title                                  |Author             |Release year   |
        |The Hunger Games                       |Suzanne Collins    |2008           |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |


    Scenario: Log in as admin
        Given A user has admin permissions
        When A user logs in as an admin
        Then The user can access admin pages


    Scenario: Add to persistent catalog
        Given An empty catalog
        When The admin adds a book to the catalog
        Then There will be one more book in the catalog

    Scenario: Search the catalog by title or author
        Given A catalog
        |Title                                  |Author             |Release year   |
        |The Hunger Games                       |Suzanne Collins    |2008           |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |
        When A user searches for a word or author in search bar
        Then Relevant results are displayed

    Scenario: Purchase books
        Given A cart with books in it
        When A user fills out their billing/mailing data
        Then The book stock is decremented
