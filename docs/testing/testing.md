<!-- omit from toc -->

<h1>Testing & Future Implementation</h1>

[*Return to main README file*](../../../README.md)
<!-- omit from toc -->

<h2>Table of Contents</h2>

<!-- TOC -->
* [Testing](#testing)
  * [User Management](#user-management)
    * [Create account](#create-account)
    * [Log in](#log-in)
    * [Manage account settings](#manage-account-settings)
    * [Reset password](#reset-password)
  * [Daily Journaling](#daily-journaling)
    * [Create morning journal entries](#create-morning-journal-entries)
    * [Create evening journal entries](#create-evening-journal-entries)
    * [Edit & delete journal entries](#edit--delete-journal-entries)
    * [List journal entries](#list-journal-entries)
    * [Tag & categories](#tag--categories)
  * [Goal Setting and Tracking](#goal-setting-and-tracking)
    * [Set goals](#set-goals)
    * [Manage goals](#manage-goals)
    * [Reminders and notifications](#reminders-and-notifications)
    * [Track progress](#track-progress)
  * [Data Privacy and Security](#data-privacy-and-security)
    * [Personal Data Protection](#personal-data-protection)
    * [Third-party data sharing](#third-party-data-sharing)
    * [Delete account](#delete-account)
  * [Analytics and Insights](#analytics-and-insights)
    * [Personalised recommendations](#personalised-recommendations)
    * [Journal entry analysis](#journal-entry-analysis)
    * [Data and trends](#data-and-trends)
  * [User Interface and Experience](#user-interface-and-experience)
    * [Clean and intuitive user interface](#clean-and-intuitive-user-interface)
    * [Cross browser and device](#cross-browser-and-device)
    * [Enhanced user experience](#enhanced-user-experience)
  * [Backend Development](#backend-development)
    * [Set up API](#set-up-api)
    * [User manage functionality](#user-manage-functionality)
    * [Create and manage journal entries](#create-and-manage-journal-entries)
    * [Goal setting and tracking](#goal-setting-and-tracking-1)
  * [Frontend Development](#frontend-development)
    * [API Test](#api-test)
  * [Deployment](#deployment)
    * [Data privacy and security](#data-privacy-and-security-1)
    * [Insights and recommendations](#insights-and-recommendations)
    * [Backend optimisation](#backend-optimisation)
    * [Remote deployment](#remote-deployment)
* [Future Implementation](#future-implementation)
<!-- TOC -->

# Testing

## User Management

### Create account

As a new user, I want to **create an account and provide my basic information** to **have a personalized experience**.

| Assessment Criteria                                                      | Tested | Successful |
|--------------------------------------------------------------------------|--------|------------|
| User should be able to register a new account.                           |        |            |
| User should be able to enter basic information (such as name and email). |        |            |
| User should be able to receive a confirmation email.                     |        |            |

---

### Log in

As a **registered user**, I want to **log in and securely access my account** to **maintain privacy and security**.

| Assessment Criteria                                                                              | Tested | Successful |
|--------------------------------------------------------------------------------------------------|--------|------------|
| User should be able to log in with their registered credentials.                                 |        |            |
| User should be able to update account settings, including password change and email preferences. |        |            |

---

### Manage account settings

As a **user**, I want to **update my profile information and manage account settings** to **customize my experience**

| Assessment Criteria                                                                                    | Tested | Successful |
|--------------------------------------------------------------------------------------------------------|--------|------------|
| User should be able to edit their profile information such as name, email and profile picture.         |        |            |
| User should be able to update their account settings, including password change and email preferences. |        |            |

---

### Reset password

As a **user**, I want the to **have the option to reset my password in case I forget it** to **recover my account**

| Assessment Criteria                                                                                                    | Tested | Successful |
|------------------------------------------------------------------------------------------------------------------------|--------|------------|
| User should have the ability to reset their password via a password reset link sent to their registered email address. |        |            |

---

## Daily Journaling

### Create morning journal entries

As a **user**, I want to **create morning journal entries with intentions and targets** to **start the day with purpose
**.

| Assessment Criteria                                                                      | Tested | Successful |
|------------------------------------------------------------------------------------------|--------|------------|
| User should be able to access the journal entry creation interface.                      |        |            |
| User should be able to create a new morning journal entry.                               |        |            |
| User should be able to view and edit their existing morning journal entries.             |        |            |
| User should be able to save it for future reference, associated with the user's account. |        |            |
| User should be able to delete their morning journal entries.                             |        |            |

---

### Create evening journal entries

As a **user**, I want to **create evening journal entries with reflections and gratitude** to **foster self-awareness
and mindfulness**

| Assessment Criteria                                                                  | Tested | Successful |
|--------------------------------------------------------------------------------------|--------|------------|
| User should be able to access the journal entry creation interface.                  |        |            |
| User should be able to create a new evening journal entry.                           |        |            |
| User should be able to view and edit their existing evening journal entries.         |        |            |
| User should be able to save it for future reference, associated with user's account. |        |            |
| User should be able to delete their evening journal entries.                         |        |            |

---

### Edit & delete journal entries

As a **user**, I want to **edit or delete my journal entries** to **ensure accuracy and organization**.

| Assessment Criteria                                       | Tested | Successful |
|-----------------------------------------------------------|--------|------------|
| User should be able to edit the content of their journal. |        |            |
| User should be able to delete them entirely if needed.    |        |            |

---

### List journal entries

As a **user**, I want to **view a list of past journal entries and navigate between them** to **be able to easily
reference and reflect upon**.

| Assessment Criteria                                                            | Tested | Successful |
|--------------------------------------------------------------------------------|--------|------------|
| User should be able to view a list of their pass journal entries.              |        |            |
| User should be able to sort by date.                                           |        |            |
| User should be able to navigate between them to review their previous entries. |        |            |

---

### Tag & categories

As a **user**, I want to **be able to categorise and tag my journal entries** to **be able to filter and search entries
**.

| Assessment Criteria                                                                     | Tested | Successful |
|-----------------------------------------------------------------------------------------|--------|------------|
| User should be able to create categories or tags for their journal entries.             |        |            |
| User should be able to assign one or multiple categories or tags to each journal entry. |        |            |
| User should be able to filter and search journal entries based on categories or tags.   |        |            |
| User should be able to see only relevant journal entries when filtering or searching.   |        |            |
| User should be able to edit or remove categories or tags from journal entries.          |        |            |
| User should be able to easily manage and organise their categories or tags.             |        |            |

---

## Goal Setting and Tracking

### Set goals

As a **user**, I want to **set goals for different areas of my life** to **stay focused and motivated**.

| Assessment Criteria                                                                      | Tested | Successful |
|------------------------------------------------------------------------------------------|--------|------------|
| User should be able to set goals for various areas (e.g. health, work, personal growth). |        |            |
| User should be able to specify goals' details.                                           |        |            |
| User should be able to set target dates.                                                 |        |            |

---

### Manage goals

As a **user**, I want to **be able to view and manage my goals**.

| Assessment Criteria                                | Tested | Successful |
|----------------------------------------------------|--------|------------|
| User should be able to view a list of their goals. |        |            |
| User should be able to create new goals.           |        |            |
| User should be able to edit existing goals.        |        |            |

---

### Reminders and notifications

As a **user**, I want to **receive reminders or notifications** to **help me stay on track with my goals and progress**.

| Assessment Criteria                                                                       | Tested | Successful |
|-------------------------------------------------------------------------------------------|--------|------------|
| User should receive reminders or notifications for upcoming goal deadlines.               |        |            |
| User should receive reminders or notifications for goal progress milestones.              |        |            |
| User should have control over the frequency and timing of the reminders or notifications. |        |            |

---

### Track progress

As a **user**, I want to **track my goal progress and visualize my achievements** to **promote motivation and
accountability**.

| Assessment Criteria                                                                                   | Tested | Successful |
|-------------------------------------------------------------------------------------------------------|--------|------------|
| User should be able to track the progress of their goals.                                             |        |            |
| User should be able to view visual representations of their achievements.                             |        |            |
| User should be able to have access to visual representations of their goal progress and achievements. |        |            |

---

[Back to the top](#user-stories)

## Data Privacy and Security

### Personal Data Protection

As a **user**, I want to **ensure my personal and journal data is securely stored and protected** to **ensure
confidentiality**.

| Assessment Criteria                                                                                                     | Tested | Successful |
|-------------------------------------------------------------------------------------------------------------------------|--------|------------|
| User's personal journal and data should be securely encrypted and stored, ensuring confidentiality and data protection. |        |            |

---

### Third-party data sharing

As a **user**, I want to **be assured that my data won't be shared with third parties without my consent to **ensure
privacy**.

| Assessment Criteria                                                                             | Tested | Successful |
|-------------------------------------------------------------------------------------------------|--------|------------|
| The system ensures user data privacy implementing appropriate security measures.                |        |            |
| User data is stored securely and protected from unauthorised access.                            |        |            |
| The system provides clear and transparent privacy policy that outline how user data is handled. |        |            |
| Users have control over their data and can provide consent for sharing with third parties.      |        |            |
| The system complies with relevant data protection regulations and laws (of the country).        |        |            |

---

### Delete account

As a **user**, I want to **be able to delete my account and associated data** to **ensure control and data management**.

| Assessment Criteria                                                                                 | Tested | Successful |
|-----------------------------------------------------------------------------------------------------|--------|------------|
| User should be able to initiate the deletion of their account.                                      |        |            |
| User should have their associated data securely and permanently deleted.                            |        |            |
| User should receive confirmation and notification upon successful deletion of the account and data. |        |            |

---

## Analytics and Insights

### Personalised recommendations

As a **user**, I want to **receive insights and recommendations based on my journal entries** to **support personal
growth**.

| Assessment Criteria                                                                                                                                    | Tested | Successful |
|--------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------|
| User should be able to view an analysis of journal entries, as the app should extract meaningful insights.                                             |        |            |
| User should receive personalised insights and recommendations based on the analysis of their journal entries to support their personal growth journey. |        |            |
| User should receive insights and recommendations that are relevant and valuable for supporting personal growth.                                        |        |            |

---

### Journal entry analysis

As a **user**, I want to **view visualisations of my journaling patterns and progress over time** to **self-reflect**.

| Assessment Criteria                                                                                                                               | Tested | Successful |
|---------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------|
| User should be able to view visual representations (charts, graphs etc.) of their journaling patterns and progress over time for self-reflection. |        |            |

---

### Data and trends

As a **user**, I want to **be able to access statistical data and trends related to my journaling activities** to *
*promote self-awareness**.

| Assessment Criteria                                                                                                     | Tested | Successful |
|-------------------------------------------------------------------------------------------------------------------------|--------|------------|
| The app should provide statistical data and trends based on the user's journaling activities.                           |        |            |
| Users should be able to access visual representations of their journaling data, such as charts or graphs.               |        |            |
| The statistical data and trends should promote self-awareness and provide insights into the user's journaling patterns. |        |            |

---

## User Interface and Experience

### Clean and intuitive user interface

As a **user**, I want to **have a clean and intuitive user interface** to **be able to easily navigate and enjoy the
experience**.

| Assessment Criteria                                              | Tested | Successful |
|------------------------------------------------------------------|--------|------------|
| User should experience a clean and intuitive user interface.     |        |            |
| User should experience clear navigation and smooth interactions. |        |            |
| User should provide a pleasant experience.                       |        |            |

---

### Cross browser and device

As a **user**, I want to **use the app across different devices and be responsive** to ** accessible and flexible**.

| Assessment Criteria                                                                                                  | Tested | Successful |
|----------------------------------------------------------------------------------------------------------------------|--------|------------|
| App should be accessible and usable across different devices including desktop, laptops, tablets and mobile devices. |        |            |
| User interface should adapt and be responsive to different screen sizes and resolutions.                             |        |            |
| App allows users to be able to interact seamlessly regardless of the device.                                         |        |            |

---

### Enhanced user experience

As a **user**, I want to **have a seamless and enjoyable user experience** to **enhance engagement and satisfaction**.

| Assessment Criteria                                                                              | Tested | Successful |
|--------------------------------------------------------------------------------------------------|--------|------------|
| App should provide a seamless and intuitive user experience.                                     |        |            |
| App should allow users to be able to navigate and interact with the app easily and effortlessly. |        |            |
| App should have a design and functionality that should enhance user engagement and satisfaction. |        |            |

---

## Backend Development

### Set up API

As a **developer**, I want to **set up the API for the app** to **handle data requests and interactions**.

| Assessment Criteria                                                                                                                           | Tested | Successful |
|-----------------------------------------------------------------------------------------------------------------------------------------------|--------|------------|
| Developer should be able to set up the Django project with the necessary directory structure, configuration files and initial database setup. |        |            |
| Developer should be able to design the API architecture and endpoints.                                                                        |        |            |
| Developer should be able to set up the Django REST Framework for building the API.                                                            |        |            |
| Developer should be able to implement authentication and authorisation mechanisms.                                                            |        |            |
| Developer should be able to create the necessary API view and serializers.                                                                    |        |            |
| Developer should be able to write unit tests for API endpoints using Django REST Framework's testing tools.                                   |        |            |
| Developer should be able to test API endpoints for various scenarios, including success cases and error handling.                             |        |            |
| Developer should be able to implement pagination on filtering.                                                                                |        |            |
| Developer should be able to document the API endpoints and provide usage instructions.                                                        |        |            |

---

### User manage functionality

As a **developer**, I want to **implement the user management functionality** to ** enable user registration, login, and
account management**.

| Assessment Criteria                                                                                                        | Tested | Successful |
|----------------------------------------------------------------------------------------------------------------------------|--------|------------|
| User should be able to register a new account.                                                                             |        |            |
| User should be able to log in with their credentials securely.                                                             |        |            |
| User should be able to manage their account settings, such as updating their profile information or change their password. |        |            |
| User should be able to register and login with proper validation and error handling mechanisms.                            |        |            |

---

### Create and manage journal entries

As a **developer**, I want to **implement the functionality for creating and managing journal entries** to **allow the
users to manage their journal entries**.

| Assessment Criteria                                                                                 | Tested | Successful |
|-----------------------------------------------------------------------------------------------------|--------|------------|
| User should be able to create new journal entries.                                                  |        |            |
| User should be able to edit and update existing entries.                                            |        |            |
| User should be able to delete entries when needed.                                                  |        |            |
| Journal entries should be securely stored and associated with the user's account.                   |        |            |
| Proper validation and error handling mechanisms should be implemented for journal entry operations. |        |            |

---

### Goal setting and tracking

As a **developer**, I want to **implement goal setting and tracking functionality** to **enable the user to be able to
set goals and track them**.

| Assessment Criteria                                                             | Tested | Successful |
|---------------------------------------------------------------------------------|--------|------------|
| User should be able to create new goals.                                        |        |            |
| User should be able to set the target and timeline for their goals.             |        |            |
| User should be able to track their progress towards their goals.                |        |            |
| User should be able to receive feedback and updates on their goal progress.     |        |            |
| Goals should be associated with user's account and securely stored.             |        |            |
| Proper validation and error handling mechanisms should be implemented for goal. |        |            |

---

## Frontend Development

### API Test

As a **developer**, I want to **create frontend components** to **consume the API and display the data to users**.

| Assessment Criteria                                                                                     | Tested | Successful |
|---------------------------------------------------------------------------------------------------------|--------|------------|
| Developer should be able to display relevant data to users and their respective roles (e.g. superuser). |        |            |

---

## Deployment

### Data privacy and security

As a **developer**, I want to **ensure data privacy and security in the backend** to **ensure journal entries are secure
**.

| Assessment Criteria                                                                                           | Tested | Successful |
|---------------------------------------------------------------------------------------------------------------|--------|------------|
| User data should be stored securely and protected from unauthorised access.                                   |        |            |
| Proper authentication and authorisation mechanisms should be implemented to control access to sensitive data. |        |            |
| Implement encryption techniques to protect sensitive information, such as user passwords.                     |        |            |
| Implement secure communication protocols, such as HTTPS, to protect data transmission.                        |        |            |
| Regularly update and patch backend systems to address any security vulnerabilities.                           |        |            |
| Implement logging and monitoring mechanisms to detect and respond to security incidents.                      |        |            |
| Conduct regular security audits and assessments to identify and mitigate potential risks.                     |        |            |

---

### Insights and recommendations

As a **developer**, I want to **implement analytics and insights generation based on user journal entries** to **
generate insights and recommendations based on user journal entries**.

| Assessment Criteria                                                                                                  | Tested | Successful |
|----------------------------------------------------------------------------------------------------------------------|--------|------------|
| Generate analytics and insights based on user journal entries, such as trends, patterns and correlations.            |        |            |
| Provide visual representation fo analytics and insights to make them easily understandable and interpretable.        |        |            |
| Generate personalised recommendations based on user journal entries to support personal growth and goal achievement. |        |            |
| Ensure the accuracy and reliability of generated analytics and insights.                                             |        |            |
| Regularly update the refine the analytics algorithms and models to improve the quality of insights.                  |        |            |

---

### Backend optimisation

As a **developer**, I want to **optimize backend performance and scalability** to **improve performance and scale
accordingly to user base**.

| Assessment Criteria                                                                                          | Tested | Successful |
|--------------------------------------------------------------------------------------------------------------|--------|------------|
| Backend system should demonstrate improved performance in terms of response time and resource utilisation.   |        |            |
| The system should be able to handle increased user load without significant performance degradation.         |        |            |
| Performance optimisation should be measurable and validated through load testing and performance monitoring. |        |            |
| The system should be designed to scale horizontally and vertically to accommodate future growth.             |        |            |
| Scalability improvements should be implemented without sacrificing data integrity or security.               |        |            |
| The backend system should be resilient and able to recover quickly from failures or high loads.              |        |            |

---

### Remote deployment

As a **developer**, I want to **deploy the Django app on Heroku (remote server)** to **enable remote access**.

| Assessment Criteria                                                                     | Tested | Successful |
|-----------------------------------------------------------------------------------------|--------|------------|
| The Django app is successfully deployed on Heroku.                                      |        |            |
| The deployed app is accessible remotely through a public URL.                           |        |            |
| The app is configured with appropriate settings for production deployment.              |        |            |
| The deployment process is documented and reproducible.                                  |        |            |
| The deployed ap is secure and protected from unauthorised access.                       |        |            |
| Appropriate environment variables and configurations are set for the Heroku deployment. |        |            |

---

# Future Implementation

