Feature: Book catalog
    Scenario: View a persistent catalog
        Given A catalog
        |Title                                  |Author             |Release year   | Image path                                        | Summary                                                   |
        |The Hunger Games                       |Suzanne Collins    |2008           |/static/The Hunger Games.jpg                       | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |/static/Harry Potter and the Sorcerer's Stone.jpg  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |/static/To Kill a Mockingbird.jpg                  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        When A user views the catalog
        Then The entire catalog is displayed
        |Title                                  |Author             |Release year   | Image path                                        | Summary                                                   |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |/static/Harry Potter and the Sorcerer's Stone.jpg  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |The Hunger Games                       |Suzanne Collins    |2008           |/static/The Hunger Games.jpg                       | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |/static/To Kill a Mockingbird.jpg                  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |

    Scenario: No duplicates in the catalog
        Given A catalog
        |Title                                  |Author             |Release year   | Image path                                        | Summary                                                   |
        |The Hunger Games                       |Suzanne Collins    |2008           |/static/The Hunger Games.jpg                       | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |/static/Harry Potter and the Sorcerer's Stone.jpg  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |/static/To Kill a Mockingbird.jpg                  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        When The admin add a duplicate book to the catalog
        Then There will be no changes to the catalog
        |Title                                  |Author             |Release year   | Image path                                        | Summary                                                   |
        |The Hunger Games                       |Suzanne Collins    |2008           |/static/The Hunger Games.jpg                       | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |/static/Harry Potter and the Sorcerer's Stone.jpg  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |/static/To Kill a Mockingbird.jpg                  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |

    Scenario: Log in as admin
        Given A user has admin permissions
        When A user logs in as an admin
        Then The user can access admin pages

    Scenario: Add to persistent catalog
        Given An empty catalog
        When The admin adds a book to the catalog
        Then There will be one more book in the catalog

    Scenario: Deny unauthorized user from adding book
        Given An empty catalog
        When An unauthorized user try to add a book to the catalog
        Then The user will be denied and the catalog is still empty

    Scenario: Search the catalog by title
        Given A catalog
        |Title                                      |Author             |Release year   | Image path                                            | Summary                                                   |
        |The Hunger Games                           |Suzanne Collins    |2008           |/static/The Hunger Games.jpg                           | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |Harry Potter and the Sorcerer's Stone      |J.K. Rowling       |1998           |/static/Harry Potter and the Sorcerer's Stone.jpg      | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |Harry Potter and the Chamber of Secrets    |J.K. Rowling       |1999           |/static/Harry Potter and the Chamber of Secrets.jpg    | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |Harry Potter and the Prisoner of Azkaban   |J.K. Rowling       |1999           |/static/Harry Potter and the Prisoner of Azkaban.jpg   | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |To Kill a Mockingbird                      |Harper Lee         |1960           |/static/To Kill a Mockingbird.jpg                      | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        When A user searches for Harry Potter
        Then Relevant results are displayed
        |Title                                      |Author             |Release year   | Image path                                            | Summary                                                   |
        |Harry Potter and the Sorcerer's Stone      |J.K. Rowling       |1998           |/static/Harry Potter and the Sorcerer's Stone.jpg      | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |Harry Potter and the Chamber of Secrets    |J.K. Rowling       |1999           |/static/Harry Potter and the Chamber of Secrets.jpg    | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |Harry Potter and the Prisoner of Azkaban   |J.K. Rowling       |1999           |/static/Harry Potter and the Prisoner of Azkaban.jpg   | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |

    Scenario: Delete a book
        Given A catalog
        |Title                                  |Author             |Release year   | Image path                                        | Summary                                                   |
        |The Hunger Games                       |Suzanne Collins    |2008           |/static/The Hunger Games.jpg                       | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |/static/Harry Potter and the Sorcerer's Stone.jpg  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |/static/To Kill a Mockingbird.jpg                  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        When An authorized user deletes the first book in the catalog
        Then Relevant results are displayed
        |Title                                  |Author             |Release year   | Image path                                        | Summary                                                   |
        |Harry Potter and the Sorcerer's Stone  |J.K. Rowling       |1998           |/static/Harry Potter and the Sorcerer's Stone.jpg  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
        |To Kill a Mockingbird                  |Harper Lee         |1960           |/static/To Kill a Mockingbird.jpg                  | Lorem ipsum dolor sit amet, consectetur adipiscing elit.  |
