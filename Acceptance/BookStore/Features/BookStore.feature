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

    Scenario: Add to persistent catalog
        Given An empty catalog
        When The admin adds a book to the catalog
        Then There will be one more book in the catalog