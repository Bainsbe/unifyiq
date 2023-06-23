# Database Schemas to for UnifyIQ's config & meta data
## Supported Systems
### MySQL
  - Follow instructions in https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/
  - For mac you can use Homebrew as an alternate
      - /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      - Add /opt/homebrew/bin to PATH (export PATH=$PATH:/opt/homebrew/bin)
      - brew install mysql
      - brew services start mysql
      - mysql_secure_installation
### Build Database
  - Run the SQL Commands in [schema folder](/schema/database/) to setup the tables
