<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">


<h3 align="center">Discord Chat History Bot</h3>

  <p align="center">
    The primary goal of the chat history discord bot is to archive every message and message edit in a server. The secondary goal is to provide the basic commands one expects of a general purpose discord bot. 
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][bot-screenshot]

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org/)
* [Pycord](https://docs.pycord.dev/en/master/)
* [SQLite](https://www.sqlite.org/index.html)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
### Prerequisites

 You will need [Python 3.8](https://www.python.org/downloads/release/python-3813/) or higher. 

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Jake-Andrews/discord_bot_.git 
   cd discord_bot_
   ```
2. Install dependencies:
   ```sh
   pipenv install
   ```
3. Create a .env file and enter your token inside of the file
   ```js
   DISCORD_TOKEN=your_token_goes_here
   ```
4. To run the discord bot on windows, type:
   ```js
   py -3 __main__.py
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

![Product Name Screen Shot][bot-screenshot]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Change Formatting of bots messages to embeds
- [ ] Refactor code in databasehelper.py and chat.py
- [ ] Commands to add
    - [ ] Ban with message
    - [ ] Clear a channel of message with an int specifying the amount
    - [ ] Slow Channel command to timeout anyone who sends more than the specified amount of messages in a minute in a specified channel
- [ ] Add proper logging


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[bot-screenshot]: images/basic_usage.PNG?raw=true
