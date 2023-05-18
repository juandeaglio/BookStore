Feature: Book catalog
    As a user
    I want to view the entire catalog

    #example needed here
Scenario: View catalog
    Given A catalog
    |Title                                  |Author             |Year   |
    |The Hunger Games                       |Suzanne Collins    |2012   |
    |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998   |
    |To Kill a Mockingbird                  |Harper Lee         |1960   |
    When I view the catalog
    Then The entire catalog is displayed
    |Title                                  |Author             |Year   |
    |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998   |
    |The Hunger Games                       |Suzanne Collins    |2012   |
    |To Kill a Mockingbird                  |Harper Lee         |1960   |