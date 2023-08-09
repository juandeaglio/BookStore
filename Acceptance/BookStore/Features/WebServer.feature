Feature: Web Server That Hosts A Webpage
    Scenario: Start Web Server and Shutdown Django Development Web Server
        Given A user starts the web server
        When The web server starts
        Then The user can access the web page
        When The user shuts down the web server
        Then The user can no longer access the web page
