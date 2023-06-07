<!-- omit from toc -->
# Mindful Minutes

<!-- omit from toc -->
## Table of Contents
- [Product Information](#product-information)
- [UX / UI Design](#ux--ui-design)
  - [Design Thinking](#design-thinking)
  - [5 Planes of Design](#5-planes-of-design)
  - [Future Implementations](#future-implementations)
  - [Accessibility](#accessibility)
- [Technologies Used](#technologies-used)
  - [Stack](#stack)
  - [Frameworks, Libraries \& Additional Programs/Software used](#frameworks-libraries--additional-programssoftware-used)
- [Remote \& Local Deployment](#remote--local-deployment)
  - [Remote Deployment](#remote-deployment)
  - [Local Deployment](#local-deployment)
  - [Contributing](#contributing)
- [Data Models](#data-models)
  - [Schematics](#schematics)
- [Testing](#testing)
  - [Django Test Driven Development using REST Framework](#django-test-driven-development-using-rest-framework)
  - [User experience](#user-experience)
  - [Bugs \& Fixes](#bugs--fixes)
  - [Lighthouse](#lighthouse)
  - [Validator Testing](#validator-testing)
- [Credits](#credits)
  - [Code Used](#code-used)
  - [References \& Resources](#references--resources)
  - [Content](#content)
  - [Media](#media)
  - [Acknowledgements](#acknowledgements)

## Product Information

The app is designed to help cultivate a habit of daily introspection and self-reflection. By using the app, the user can establish a routine of engaging with their thoughts, goals and achievements every current day and evening.

The primary goal of the Mindful Minutes App is to encourage users to build a habit of checking in daily and reflecting on their experiences. To reinforce this habit, the app allows users to create, edit, delete and access their current day's journal entries while keeping the previous days' entries in a read-only mode. This approach ensures that users focus on the present, fostering a send of mindfulness and self-awareness.

## UX / UI Design

For further details of the design process, please see:

### [Design Thinking](docs/ui-ux/design-thinking/design-thinking.md)

### [5 Planes of Design](docs/ui-ux/five-planes/five-planes.md)

### Future Implementations

### Accessibility

## Technologies Used

### Stack

- HTML5
- CSS3
- JavaScript
- Python

### Frameworks, Libraries & Additional Programs/Software used

- Django

## Remote & Local Deployment

### Remote Deployment

### Local Deployment

### Contributing

## Data Models
### Schematics

![Mindful Minutes ERD - Database ER diagram (crow's foot)](docs/media/images/mm_erd.png)

For the diagram on [LucidChart](https://lucid.app), click [here](https://lucid.app/documents/view/eceb8ec6-75f3-4138-9efa-b05138d3aad4)


<details>
  <summary>Entity Relationship in PostgreSQL</summary>

  ```sql
  CREATE TABLE "user" (
    "id" PK,
    "first_name" string,
    "last_name" string,
    "email" string,
    "password" string,
    "created_on" datetime,
    "updated_on" datetime
  );

  CREATE TABLE "optimise" (
    "id" PK,
    "user" FK,
    "content" string,
    "created_on" datetime,
    "updated_on" datetime,
    CONSTRAINT "FK_optimise.user"
      FOREIGN KEY ("user")
        REFERENCES "user"("id")
  );

  CREATE TABLE "notes" (
    "id" PK,
    "user" FK,
    "content" string,
    "created_on" datetime,
    "updated_on" datetime,
    CONSTRAINT "FK_notes.user"
      FOREIGN KEY ("user")
        REFERENCES "user"("id")
  );

  CREATE TABLE "thankful" (
    "id" PK,
    "user" FK,
    "content" string,
    "created_on" datetime,
    "updated_on" datetime,
    CONSTRAINT "FK_thankful.user"
      FOREIGN KEY ("user")
        REFERENCES "user"("id")
  );

  CREATE TABLE "settings" (
    "id" PK,
    "user" FK,
    "verified" boolean,
    "start_week_day" string,
    "morning_check_in" time,
    "evening_check_in" time,
    "created_on" datetime,
    "updated_on" datetime
  );

  CREATE TABLE "targets" (
    "id" PK,
    "user" FK,
    "title" string,
    "order" integer,
    "created_on" datetime,
    "updated_on" datetime,
    CONSTRAINT "FK_targets.user"
      FOREIGN KEY ("user")
        REFERENCES "user"("id")
  );

  CREATE TABLE "sub_targets" (
    "id" PK,
    "target" FK,
    "content" string,
    "created_on" datetime,
    "updated_on" datetime,
    CONSTRAINT "FK_sub_targets.target"
      FOREIGN KEY ("target")
        REFERENCES "targets"("id")
  );

  CREATE TABLE "wins" (
    "id" PK,
    "user" FK,
    "content" string,
    "created_on" datetime,
    "updated_on" datetime,
    CONSTRAINT "FK_wins.user"
      FOREIGN KEY ("user")
        REFERENCES "User"("id")
  );

  CREATE TABLE "ideas" (
    "id" PK,
    "user" FK,
    "content" string,
    "created_on" datetime,
    "updated_on" datetime,
    CONSTRAINT "FK_ideas.user"
      FOREIGN KEY ("user")
        REFERENCES "user"("id")
  );

  CREATE TABLE "learnt" (
    "id" PK,
    "user" FK,
    "content" string,
    "created_on" datetime,
    "updated_on" datetime,
    CONSTRAINT "FK_learnt.user"
      FOREIGN KEY ("user")
        REFERENCES "user"("id")
  );

  CREATE TABLE "appointment_diary" (
    "id" PK,
    "user" FK,
    "title" string,
    "date" date,
    "from" time,
    "until" time,
    "created_on" datetime,
    "updated_on" datetime,
    CONSTRAINT "FK_appointment_diary.user"
      FOREIGN KEY ("user")
        REFERENCES "user"("id")
  );


  CREATE TABLE "mood" (
    "id" PK,
    "user" FK,
    "emotion" string,
    "created_on" datetime,
    "updated_on" datetime
  );
  ```
</details>

## Testing

### Django Test Driven Development using REST Framework

For further details on testing, click [here](docs/testing/testing.md).

### User experience

[Browserstack](https://www.browserstack.com) was used for testing. The devices were:

### Bugs & Fixes

### Lighthouse

### Validator Testing

## Credits

### Code Used

### References & Resources

### Content

### Media

### Acknowledgements

Thanks to Adam Gilroy for giving me permission to use his LinkedIn Post as inspiration for a Use Case. 