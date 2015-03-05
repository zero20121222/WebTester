# WebTester
WebTester based on python, the user can customize the testing process, convenient to get on the page displays the message. Must configure Chrome WebDriver / Firefox WebDriver / Remote WebDriver

### Init WebTester
* git clonse webtester

##### If you want to build Test Server Client, you need:
    * pip install tornado
    * pip install MySQLdb
    * pip install DBUtils
    * pip install PyYAML
    * pip install splinter
    Config Server
    copy *.yaml.example to *.yaml
    then change db, redis config with username & password

##### Start Test Server
    * python web_tester.py

##### TestServer Client Images
![Tester Server](http://img.blog.csdn.net/20150305230326359)


##### If you just want to use Test Client, you need:
    * pip install splinter

##### Install Test Client
    need be used by chrome extension
    * sudo python client_setup.py install
    * move tester-extension.crx to chrome://extensions/
    * tester-extension will save COM+Click event

##### Test Client Images
<img src="http://img.blog.csdn.net/20150305232913569" width = "450" height = "300" />

### Tester WebDriver
* [Chrome WebDriver](http://splinter.cobrateam.info/en/latest/drivers/chrome.html) brew install chromedriver
* [Firefox WebDriver](http://splinter.cobrateam.info/en/latest/drivers/firefox.html) brew install firefoxdriver
* [Remote WebDriver](http://splinter.cobrateam.info/en/latest/drivers/remote.html) brew install remotedriver

