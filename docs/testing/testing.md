<!-- omit from toc -->
# Testing

[*Return to main README file*](../../../README.md)
<!-- omit from toc -->
## Table of Contents
- [Django REST Framework](#django-rest-framework)
  - [RESTful Routes](#restful-routes)
    - [Appointment Entries](#appointment-entries)
    - [Targets](#targets)
    - [Notes](#notes)
    - [Knowledge Entries](#knowledge-entries)
    - [Gratitude Entries](#gratitude-entries)
    - [Win Entries](#win-entries)
    - [Ideas Entries](#ideas-entries)
    - [Improvement Entries](#improvement-entries)
    - [Ideas Entries](#ideas-entries-1)
    - [Emotion Entries](#emotion-entries)

## Django REST Framework

### RESTful Routes

#### Appointment Entries

| Endpoint                | HTTP Method | CRUD Method | Result                         |         |
| :---------------------- | :---------: | :---------: | :----------------------------- | ------- |
| /api/appointments/      |     GET     |    READ     | get all appointments           | &#9745; |
| /api/appointments/:date |     GET     |    READ     | get all appointments by date   | &#9745; |
| /api/appointments/:id   |     GET     |    READ     | get a single appointment by ID | &#9745; |
| /api/appointments/      |    POST     |   CREATE    | add an appointment             | &#9745; |
| /api/appointments/:id   |     PUT     |   UPDATE    | update an appointment          |         |
| /api/appointments/:id   |   DELETE    |   DELETE    | delete an appointment          | &#9745; |

---

#### Targets

| Endpoint           | HTTP Method | CRUD Method | Result                    |     |
| :----------------- | :---------: | :---------: | :------------------------ | --- |
| /api/targets/      |     GET     |    READ     | get all targets           |     |
| /api/targets/:date |     GET     |    READ     | get all targets by date   |     |
| /api/targets/:id   |     GET     |    READ     | get a single target by ID |     |
| /api/targets/      |    POST     |   CREATE    | add an target             |     |
| /api/targets/:id   |     PUT     |   UPDATE    | update an target          |     |
| /api/targets/:id   |   DELETE    |   DELETE    | delete an target          |     |

---

#### Notes

| Endpoint         | HTTP Method | CRUD Method | Result                  |     |
| :--------------- | :---------: | :---------: | :---------------------- | --- |
| /api/notes/      |     GET     |    READ     | get all notes           |     |
| /api/notes/:date |     GET     |    READ     | get all notes by date   |     |
| /api/notes/:id   |     GET     |    READ     | get a single note by ID |     |
| /api/notes/      |    POST     |   CREATE    | add an note             |     |
| /api/notes/:id   |     PUT     |   UPDATE    | update an note          |     |
| /api/notes/:id   |   DELETE    |   DELETE    | delete an note          |     |

---

#### Knowledge Entries

| Endpoint                     | HTTP Method | CRUD Method | Result                             |     |
| :--------------------------- | :---------: | :---------: | :--------------------------------- | --- |
| /api/knowledge_entries/      |     GET     |    READ     | get all knowledge_entries          |     |
| /api/knowledge_entries/:date |     GET     |    READ     | get all knowledge_entries by date  |     |
| /api/knowledge_entries/:id   |     GET     |    READ     | get a single knowledge_entry by ID |     |
| /api/knowledge_entries/      |    POST     |   CREATE    | add an knowledge_entry             |     |
| /api/knowledge_entries/:id   |     PUT     |   UPDATE    | update an knowledge_entry          |     |
| /api/knowledge_entries/:id   |   DELETE    |   DELETE    | delete an knowledge_entry          |     |

---


#### Gratitude Entries

| Endpoint                     | HTTP Method | CRUD Method | Result                             |     |
| :--------------------------- | :---------: | :---------: | :--------------------------------- | --- |
| /api/gratitude_entries/      |     GET     |    READ     | get all gratitude_entries          |     |
| /api/gratitude_entries/:date |     GET     |    READ     | get all gratitude_entries by date  |     |
| /api/gratitude_entries/:id   |     GET     |    READ     | get a single gratitude_entry by ID |     |
| /api/gratitude_entries/      |    POST     |   CREATE    | add an gratitude_entry             |     |
| /api/gratitude_entries/:id   |     PUT     |   UPDATE    | update an gratitude_entry          |     |
| /api/gratitude_entries/:id   |   DELETE    |   DELETE    | delete an gratitude_entry          |     |

---

#### Win Entries

| Endpoint        | HTTP Method | CRUD Method | Result                 |     |
| :-------------- | :---------: | :---------: | :--------------------- | --- |
| /api/wins/      |     GET     |    READ     | get all wins           |     |
| /api/wins/:date |     GET     |    READ     | get all wins by date   |     |
| /api/wins/:id   |     GET     |    READ     | get a single win by ID |     |
| /api/wins/      |    POST     |   CREATE    | add an win             |     |
| /api/wins/:id   |     PUT     |   UPDATE    | update an win          |     |
| /api/wins/:id   |   DELETE    |   DELETE    | delete an win          |     |

---


#### Ideas Entries

| Endpoint         | HTTP Method | CRUD Method | Result                  |     |
| :--------------- | :---------: | :---------: | :---------------------- | --- |
| /api/ideas/      |     GET     |    READ     | get all ideas           |     |
| /api/ideas/:date |     GET     |    READ     | get all ideas by date   |     |
| /api/ideas/:id   |     GET     |    READ     | get a single idea by ID |     |
| /api/ideas/      |    POST     |   CREATE    | add an idea             |     |
| /api/ideas/:id   |     PUT     |   UPDATE    | update an idea          |     |
| /api/ideas/:id   |   DELETE    |   DELETE    | delete an idea          |     |

---


#### Improvement Entries

#### Ideas Entries

| Endpoint                | HTTP Method | CRUD Method | Result                         |     |
| :---------------------- | :---------: | :---------: | :----------------------------- | --- |
| /api/improvements/      |     GET     |    READ     | get all improvements           |     |
| /api/improvements/:date |     GET     |    READ     | get all improvements by date   |     |
| /api/improvements/:id   |     GET     |    READ     | get a single improvement by ID |     |
| /api/improvements/      |    POST     |   CREATE    | add an improvement             |     |
| /api/improvements/:id   |     PUT     |   UPDATE    | update an improvement          |     |
| /api/improvements/:id   |   DELETE    |   DELETE    | delete an improvement          |     |

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