Feature: Web Server That Hosts A Webpage

  Scenario Outline: Starting and Stopping Different Web Servers
    Given "<web_server_type>" web server is started
    Then The user can access the web page
    When The user shuts down the web server
    Then The user can no longer access the web page

    Examples:
      | web_server_type |
      | Django          |
      | Gunicorn        |
      | GunicornNginx   |


  Scenario Outline: Fetching Static Images From a Web Server
    Given "<web_server_type>" web server is started
    When The user fetches a static image
    Then The user can see the static image
    Examples:
      | web_server_type |
      | Django          |
      | GunicornNginx   |

  Scenario: Create a web server hosted in public
    Given The user hosts the web server on the public web
    Then The user can access the web page over the internet
