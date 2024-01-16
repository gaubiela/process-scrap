# Scraping Ongoing Judicial Processes 🏛️📊

## Objective

This project focuses on web scraping ongoing judicial processes from various courts of justice in Brazil. The scraping process extracts comprehensive information related to each legal case, including its current status, involved participants, and recent movements.

## Database Structure

The database contains a main table that stores the process numbers to be searched on designated websites. Each entry in this table represents a unique ongoing judicial process, identified by its unique number.

Example of Main Table Structure:

| ID  | Process Number | Search | 
| --- | -------------- |--------|
| 1   | XXXXXXXX       |    N   |
| 2   | XXXXXXXY       |    Y   |
| 3   | XXXXXXXZ       |    N   |

After reading the process numbers from the database, scraping is performed on specific websites, particularly those of different courts of justice in Brazil. The results are organized into three distinct tables to provide a clear and modular view of the data.

1. **Process Data Table:**
   - Stores general information about each process, such as opening date, type, current status, etc.

   Example Structure:

   | Process Number | Process Type | Opening Date | Current Status | ... |
   | -------------- | ------------ | --------------| --------------- | --- |
   | XXXXXXXX       | Civil        | YYYY-MM-DD    | In Progress     | ... |
   | XXXXXXXY       | Criminal     | YYYY-MM-DD    | Completed       | ... |
   | XXXXXXXZ       | Labor        | YYYY-MM-DD    | Pending         | ... |
   | ...            | ...          | ...           | ...             | ... |

2. **Participants Table:**
   - Records information about the involved parties, lawyers, judges, among others.

   Example Structure:

   | Process Number | Participant        | Participant Type | ... |
   | -------------- | ------------------ | ----------------- | --- |
   | XXXXXXXX       | John Doe           | Plaintiff         | ... |
   | XXXXXXXX       | Mary Smith         | Defendant         | ... |
   | XXXXXXXY       | Carlos Rodriguez   | Plaintiff         | ... |
   | XXXXXXXZ       | Ana Souza          | Defendant         | ... |
   | ...            | ...                | ...               | ... |

3. **Last 5 Movements Table:**
   - Contains the last 5 recorded movements for each process.

   Example Structure:

   | Process Number | Movement Date | Movement Description | ... |
   | -------------- | ------------- | --------------------- | --- |
   | XXXXXXXX       | YYYY-MM-DD    | Initial Petition Received | ... |
   | XXXXXXXX       | YYYY-MM-DD    | Hearing Scheduled         | ... |
   | XXXXXXXY       | YYYY-MM-DD    | Judgment Issued           | ... |
   | XXXXXXXZ       | YYYY-MM-DD    | Notice Sent               | ... |
   | ...            | ...           | ...                       | ... |

## Usage and Execution

1. **Database Configuration:**
   - Ensure that the database containing the process numbers is properly configured.

2. **Running the Scraping:**
   - Execute the script responsible for scraping, ensuring the proper connection to the database.

3. **Results Verification:**
   - Check the process data, participants, and movements tables to ensure the results are correct and complete.

---
