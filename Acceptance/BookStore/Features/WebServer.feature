Feature: Web Server That Hosts A Webpage

  Scenario Outline: Starting and Stopping Different Web Servers
    Given A user starts the "<web_server_type>" web server
    Then The user can access the web page
    When The user shuts down the web server
    Then The user can no longer access the web page

    Examples:
      | web_server_type |
      | Django          |