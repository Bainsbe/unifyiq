# Getting Started with UI

The UI was created by using ReactJS, Tailwind, Charka, React router dom.

## Install NPM

- For most user:
    - Follow instruction from : https://nodejs.org/en/download
    - npm -v (This will check if npm is already installed on your system. If you see a version number displayed, then
      npm is already installed. If not, continue with the next step.)
    - npm install npm@latest -g (This will install the latest version of npm globally on your machine.)
- For mac you can use Homebrew as an alternate
    - /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    - Add /opt/homebrew/bin to PATH (export PATH=$PATH:/opt/homebrew/bin)
    - brew install node
    - npm -v (This will check if npm is already installed on your system. If you see a version number displayed, then
      npm is already installed. If not, continue with the next step.)
    - npm install npm@latest -g (This will install the latest version of npm globally on your machine.)

## Install & Run project for development

- cd unifyiq/ui
- You will need to run **npm install** to install all your dependencies
- Run this application from this location using **npm start**
- After installation, there are ~76 vulnerabilities...Dont worry! Its expected. npm audit is designed for Node apps so
  it flags issues that can occur when you run actual Node code in production. It is broken for front-end tooling by
  design. That is categorically not how Create React App works. We should run npm audit --production (If you interested
  in, please read the explanation here: https://github.com/facebook/create-react-app/issues/11174)
