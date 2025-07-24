# TM-auto-questionnaire
Questionnaire with automated Excel generating system

Folder WEBQ
- Client need to enter his/her email, DOB and last 4 digits of SSN/ITIN
- If matches data on DB, then automatically send an email with unique URL of his/her questionnaire
- If not, the error page appears and "trial_count" increases
- The trial_count can be no more than 5. If it exceeds 5, the error page appears.
-- OTHER THINGS
  - Using flask and Python
  - Using SQLite and SQLAlchemy
  - Using flask_mail
  - Using dotenv
