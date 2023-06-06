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

```sql
CREATE TABLE "User" (
  "ID" PK,
  "First Name" string,
  "Last Name" string,
  "Email" string,
  "Password" string,
  "Created on" datetime,
  "Updated on" datetime
);

CREATE TABLE "Optimise" (
  "ID" PK,
  "User" FK,
  "Content" string,
  "Created on" datetime,
  "Updated on" datetime,
  CONSTRAINT "FK_Optimise.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);

CREATE TABLE "Notes" (
  "ID" PK,
  "User" FK,
  "Content" string,
  "Created on" datetime,
  "Updated on" datetime,
  CONSTRAINT "FK_Notes.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);

CREATE TABLE "Thankfful" (
  "ID" PK,
  "User" FK,
  "Content" string,
  "Created on" datetime,
  "Updated on" datetime,
  CONSTRAINT "FK_Thankfful.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);

CREATE TABLE "Settings" (
  "ID" PK,
  "User" FK,
  "Verified" boolean,
  "Startt Week Day" string,
  "Morning Check-in" time,
  "Evening Check-in" time,
  "Created on" datetime,
  "Updated on" datetime,
  CONSTRAINT "FK_Settings.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);

CREATE TABLE "Targets" (
  "ID" PK,
  "User" FK,
  "Title" string,
  "Order" integer,
  "Created on" datetime,
  "Updated on" dateime,
  CONSTRAINT "FK_Targets.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);

CREATE TABLE "Sub-Targets" (
  "ID" PK,
  "Target" FK,
  "Content" string,
  "Created on" datetime,
  "Updated on" datetime,
  CONSTRAINT "FK_Sub-Targets.Target"
    FOREIGN KEY ("Target")
      REFERENCES "Targets"("ID")
);

CREATE TABLE "Wins" (
  "ID" PK,
  "User" FK,
  "Content" string,
  "Created on" datetime,
  "Updated on" datetime,
  CONSTRAINT "FK_Wins.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);

CREATE TABLE "Ideas" (
  "ID" PK,
  "User" FK,
  "Content" string,
  "Created on" datetime,
  "Updated on" datetime,
  CONSTRAINT "FK_Ideas.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);

CREATE TABLE "Learnt" (
  "ID" PK,
  "User" FK,
  "Content" string,
  "Created on" datetime,
  "Updated on" datetime,
  CONSTRAINT "FK_Learnt.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);

CREATE TABLE "Appointment Diary" (
  "ID" PK,
  "User" FK,
  "Title" string,
  "Date" datetime,
  "From" datetime,
  "Until" datetime,
  "Created on" datetime,
  "Updated on" dateime,
  CONSTRAINT "FK_Appointment Diary.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);

CREATE TABLE "Mood" (
  "ID" PK,
  "User" FK,
  "Emotion" string,
  "Created on" datetime,
  "Updated on" datetime,
  CONSTRAINT "FK_Mood.User"
    FOREIGN KEY ("User")
      REFERENCES "User"("ID")
);


```

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