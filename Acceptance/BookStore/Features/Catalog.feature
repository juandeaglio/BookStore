Feature: Book catalog
    As a user
    I want to view and change the catalog

    Scenario: View catalog
        Given A catalog
        |Title                                  |Author             |Release year   |
        |The Hunger Games                       |Suzanne Collins    |2008           |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |
        When I view the catalog
        Then The entire catalog is displayed
        |Title                                  |Author             |Release year   |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |
        |The Hunger Games                       |Suzanne Collins    |2008           |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |

        #example needed here
    Scenario: Add to catalog
        Given An empty catalog
        When I add a book to the catalog
        Then There will be one more book in the catalog

        #example needed here
    Scenario: No duplicates in the catalog
        Given A catalog
        When I add a duplicate book to the catalog
        And I save the catalog
        Then There will be no changes to the catalog