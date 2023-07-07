<!-- omit from toc -->
# Testing

[*Return to main README file*](../../../README.md)
<!-- omit from toc -->
## Table of Contents
- [Django REST Framework](#django-rest-framework)
  - [RESTful Routes](#restful-routes)
    - [Custom User](#custom-user)
    - [User Settings](#user-settings)
    - [Appointment Entries](#appointment-entries)
    - [Target Entries](#target-entries)
    - [Note Entries](#note-entries)
    - [Knowledge Entries](#knowledge-entries)
    - [Gratitude Entries](#gratitude-entries)
    - [Win Entries](#win-entries)
    - [Ideas Entries](#ideas-entries)
    - [Improvement Entries](#improvement-entries)
    - [Emotion Entries](#emotion-entries)

## Django REST Framework

### RESTful Routes

#### Custom User

| Endpoint       | HTTP Method | CRUD Method | Result                  |         |
| :------------- | :---------: | :---------: | :---------------------- | ------- |
| /api/users/    |     GET     |    READ     | get all users           | &#9745; |
| /api/users/:id |     GET     |    READ     | get a single user by ID | &#9745; |
| /api/users     |    POST     |   CREATE    | add an user             | &#9745; |
| /api/users/:id |     PUT     |   UPDATE    | update an user          | &#9745; |
| /api/users/:id |   DELETE    |   DELETE    | delete an user          | &#9745; |

---

#### User Settings

| Endpoint                    | HTTP Method | CRUD Method | Result                       |         |
| :-------------------------- | :---------: | :---------: | :--------------------------- | ------- |
| /api/user-settings/:user_id |     GET     |    READ     | get all user's user-settings | &#9745; |
| /api/user-settings/:user_id |    POST     |   CREATE    | add an user's user-settings  | &#9745; |
| /api/user-settings/:user_id |     PUT     |   UPDATE    | update user's user-settings  | &#9745; |
| /api/user-settings/:user_id |   DELETE    |   DELETE    | delete user's user-settings  | &#9745; |

---

#### Appointment Entries

| Endpoint                    | HTTP Method | CRUD Method | Result                               |         |
| :-------------------------- | :---------: | :---------: | :----------------------------------- | ------- |
| /api/appointments/:date     |     GET     |    READ     | get all appointments by date         | &#9745; |
| /api/appointments/:date/:id |     GET     |    READ     | get a single appointment entry by ID | &#9745; |
| /api/appointments/:date     |    POST     |   CREATE    | add an appointment entry             | &#9745; |
| /api/appointments/:date/:id |     PUT     |   UPDATE    | update an appointment entry          | &#9745; |
| /api/appointments/:date/:id |   DELETE    |   DELETE    | delete an appointment entry          | &#9745; |

---

#### Target Entries

| Endpoint               | HTTP Method | CRUD Method | Result                          |         |
| :--------------------- | :---------: | :---------: | :------------------------------ | ------- |
| /api/targets/:date     |     GET     |    READ     | get all targets by date         | &#9745; |
| /api/targets/:date/:id |     GET     |    READ     | get a single target entry by ID | &#9745; |
| /api/targets/:date     |    POST     |   CREATE    | add an target entry             | &#9745; |
| /api/targets/:date/:id |     PUT     |   UPDATE    | update an target entry          | &#9745; |
| /api/targets/:date/:id |   DELETE    |   DELETE    | delete an target entry          | &#9745; |

---

#### Note Entries

| Endpoint             | HTTP Method | CRUD Method | Result                        |         |
| :------------------- | :---------: | :---------: | :---------------------------- | ------- |
| /api/notes/:date     |     GET     |    READ     | get all notes by date         | &#9745; |
| /api/notes/:date/:id |     GET     |    READ     | get a single note entry by ID | &#9745; |
| /api/notes/:date     |    POST     |   CREATE    | add an note entry             | &#9745; |
| /api/notes/:date/:id |     PUT     |   UPDATE    | update an note entry          | &#9745; |
| /api/notes/:date/:id |   DELETE    |   DELETE    | delete an note entry          | &#9745; |

---

#### Knowledge Entries

| Endpoint                 | HTTP Method | CRUD Method | Result                             |         |
| :----------------------- | :---------: | :---------: | :--------------------------------- | ------- |
| /api/knowledge/:date     |     GET     |    READ     | get all knowledge by date          | &#9745; |
| /api/knowledge/:date/:id |     GET     |    READ     | get a single knowledge entry by ID | &#9745; |
| /api/knowledge/:date     |    POST     |   CREATE    | add an knowledge entry             | &#9745; |
| /api/knowledge/:date/:id |     PUT     |   UPDATE    | update an knowledge entry          | &#9745; |
| /api/knowledge/:date/:id |   DELETE    |   DELETE    | delete an knowledge entry          | &#9745; |

---


#### Gratitude Entries

| Endpoint                 | HTTP Method | CRUD Method | Result                             |         |
| :----------------------- | :---------: | :---------: | :--------------------------------- | ------- |
| /api/gratitude/:date     |     GET     |    READ     | get all gratitude by date          | &#9745; |
| /api/gratitude/:date/:id |     GET     |    READ     | get a single gratitude entry by ID | &#9745; |
| /api/gratitude/:date     |    POST     |   CREATE    | add an gratitude entry             | &#9745; |
| /api/gratitude/:date/:id |     PUT     |   UPDATE    | update an gratitude entry          | &#9745; |
| /api/gratitude/:date/:id |   DELETE    |   DELETE    | delete an gratitude entry          | &#9745; |

---

#### Win Entries

| Endpoint            | HTTP Method | CRUD Method | Result                       |         |
| :------------------ | :---------: | :---------: | :--------------------------- | ------- |
| /api/wins/:date     |     GET     |    READ     | get all wins by date         | &#9745; |
| /api/wins/:date/:id |     GET     |    READ     | get a single win entry by ID | &#9745; |
| /api/wins/:date     |    POST     |   CREATE    | add an win entry             | &#9745; |
| /api/wins/:date/:id |     PUT     |   UPDATE    | update an win entry          | &#9745; |
| /api/wins/:date/:id |   DELETE    |   DELETE    | delete an win entry          | &#9745; |

---


#### Ideas Entries

| Endpoint             | HTTP Method | CRUD Method | Result                        |         |
| :------------------- | :---------: | :---------: | :---------------------------- | ------- |
| /api/ideas/:date     |     GET     |    READ     | get all ideas by date         | &#9745; |
| /api/ideas/:date/:id |     GET     |    READ     | get a single idea entry by ID | &#9745; |
| /api/ideas/:date     |    POST     |   CREATE    | add an idea entry             | &#9745; |
| /api/ideas/:date/:id |     PUT     |   UPDATE    | update an idea entry          | &#9745; |
| /api/ideas/:date/:id |   DELETE    |   DELETE    | delete an idea entry          | &#9745; |

---


#### Improvement Entries

| Endpoint                   | HTTP Method | CRUD Method | Result                               |         |
| :------------------------- | :---------: | :---------: | :----------------------------------- | ------- |
| /api/improvement/:date     |     GET     |    READ     | get all improvement by date          | &#9745; |
| /api/improvement/:date/:id |     GET     |    READ     | get a single improvement entry by ID | &#9745; |
| /api/improvement/:date     |    POST     |   CREATE    | add an improvement entry             | &#9745; |
| /api/improvement/:date/:id |     PUT     |   UPDATE    | update an improvement entry          | &#9745; |
| /api/improvement/:date/:id |   DELETE    |   DELETE    | delete an improvement entry          | &#9745; |


--- 


#### Emotion Entries

| Endpoint            | HTTP Method | CRUD Method | Result                     |     |
| :------------------ | :---------: | :---------: | :------------------------- | --- |
| /api/emotions/      |     GET     |    READ     | get all emotions           |     |
| /api/emotions/:date |     GET     |    READ     | get all emotions by date   |     |
| /api/emotions/:id   |     GET     |    READ     | get a single emotion by ID |     |
| /api/emotions/      |    POST     |   CREATE    | add an emotion             |     |
| /api/emotions/:id   |     PUT     |   UPDATE    | update an emotion          |     |
| /api/emotions/:id   |   DELETE    |   DELETE    | delete an emotion          |     |

---


[Back to the top](#testing)