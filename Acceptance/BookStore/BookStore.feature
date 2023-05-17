Feature: View catalog
    As a user
    I want to view the entire catalog

    #example needed here
Scenario: View catalog
    Given A catalog
    When I view the catalog
    Then The entire catalog is displayed

Feature: Change catalog
    As an admin
    I want to make changes to the catalog

    #example needed here
Scenario: Add to catalog
    Given A catalog
    When I add a book to the catalog
    And I save the catalog
    Then We will have one more book in the catalog

    #example needed here
Scenario: No duplicates in the catalog
    Given A catalog
    When I add a duplicate book to the catalog
    And I save the catalog
    Then There will be no changes to the catalog