<!-- omit from toc -->
# 5 Planes of Design

<!-- omit from toc -->
## Table of Contents
- [Strategy](#strategy)
  - [Target Audience](#target-audience)
  - [User \& Client Needs](#user--client-needs)
  - [Opportunity Matrices](#opportunity-matrices)
- [Scope](#scope)
- [Structure](#structure)
  - [Information Architecture \& User Journey](#information-architecture--user-journey)
    - [User Management](#user-management)
    - [Admin Management](#admin-management)
    - [Repo Management](#repo-management)
- [Skeleton](#skeleton)
  - [Home page](#home-page)
  - [Features](#features)
    - [Sign up / Register \& Login / Logout](#sign-up--register--login--logout)
    - [Morning page](#morning-page)
    - [Evening page](#evening-page)
    - [My profile page](#my-profile-page)
    - [Contact page](#contact-page)
    - [Modals](#modals)
- [Surface](#surface)
  - [Imagery](#imagery)
  - [Colour Palette](#colour-palette)
  - [Typography](#typography)
  - [Mock-ups](#mock-ups)


## Strategy

### Target Audience

The following sections provide an overview of the target audience for the Mindful Minutes (Journal App). Further research and user surveys were taken to gather more specific insights and refined the target audience description. This helped tailor the app's features, user experience and content to meet the needs and preferences of the identified target audience.

![Strategy Plane: Target Audience](../../media/images/strategy_target-audience.png)

<details>
  <summary>Roles (groups of people with similar goals)</summary>

- Personal Journalisers
  - Individuals who use the app for:
    - personal reflection
    - goal tracking
    - self-improvement
- Professionals
  - Individuals who use the app for:
    - work-related task
    - set targets
    - track progress
- Students
  - Individuals who use the app for:
    - study schedules
    - track assignments
    - take notes
- Create Professionals
  - Individuals who use the app for:
    - take ideas
    - take inspiration
    - track creative process
- Entrepreneurs
  - Individuals who use the app for:
    - planning
    - goal setting
    - documenting business journey

</details>

<details>
  <summary>Demographics</summary>

- Age
  - for adults (18+)
  - older teenagers
  - college students
- Gender
  - all genders
- Occupation
  - various professional backgrounds i.e.
    - corporate employees
    - freelancers
    - students
    - entrepreneurs
- Education
  - different levels of education i.e.
    - high school
    - graduates
    - university-educated individuals
- Geography
  - various regions or countries

</details>

<details>
  <summary>Psychographics</summary>

1. Tech-savvy
  - Personality & Attributes
    - tech-savvy
    - digitally fluent
    - adaptive to new technologies
    - comfortable with digital interfaces
    - quick learners
  - Values
    - efficiency
    - convenience
    - staying connected
    - staying up-to-date with technology
  - Lifestyles:
    - embrace digital tools in various aspects of life
    - rely on technology for communication
    - work
    - entertainment
    - actively seeking new apps for digital solutions
2. Goal Orientated
  - Personality & Attributes
    - ambitious
    - determined
    - focused
    - proactive
    - resilient
  - Values
    - personal growth
    - achievement
    - progress
    - self-improvement
    - self-motivation
  - Lifestyles
    - set clear goals and milestones
    - prioritise tasks and activities aligned to goals
    - regularly track progress
    - seek opportunities for learning and development
3. Reflective Thinkers
  - Personality & Attributes
    - thoughtful
    - introspective
    - observant
    - self-aware
    - contemplative
  - Values
    - self-discovery
    - self-expression
    - self-reflection
    - personal insight
    - emotional well-being
  - Lifestyles
    - engage in journaling
    - engage in mediation
    - engage in mindfulness practices
    - value alone time for reflection
    - seeks moments of introspection and self-analysis
4. Organised and Productive
  - Personality & Attributes
    - detail orientated
    - systematic
    - disciplined
    - efficient
    - time-conscious
  - Values
    - order
    - productivity
    - time management
    - effective planning
    - accomplishment
  - Lifestyles
    - rely on schedules and to-do lists
    - prioritise tasks
    - seek tools and strategies to enhance productivity
    - maintain an organised physical and digital environment
5. Creatively inclined
  - Personality & Attributes
    - imaginative
    - artistic
    - open-minded
    - expressive
    - inspired by aesthetics
  - Values
     - creativity
     - self-expression
     - originality
     - artistic exploration
     - inspiration
  - Lifestyles
    - engage in creative pursuits (writing, drawing, photography)
    - appreciate art and design
    - seek inspiration from various sources
    - incorporate creativity into daily life

</details>

---

### User & Client Needs

Based on the target audience, these are the user and client needs for the Mindful Minutes (Journal App).

The user and client needs provide a foundation for understanding the requirements and expectations for both users and the app owner (or developer). By addressing these needs, the app is designed to cater to the target audience effectively and meet client's objectives.

![Strategy: User and Client Needs](../../media/images/strategy_user-and-client-needs.png)

References on [Figma](http://figma.com) screenshot:
- [CCPA vs GDPR](https://www.cookieyes.com/blog/ccpa-vs-gdpr/)
- [Data Protection EU](https://commission.europa.eu/law/law-topic/data-protection/data-protection-eu_en)
- [Django Performance](https://docs.djangoproject.com/en/4.2/topics/performance/)
- [Performance Optimization Testing Django](https://www.toptal.com/python/performance-optimization-testing-django)
- [Scaling Django Application Best Practices and Strategies](https://medium.com/@danielbuilescu/scaling-django-applications-best-practices-and-strategies-1b537f62e5c8)

<details>
  <summary>User Needs</summary>

- Personal Journalisers:
  - Enable users the ability to record:
    - thoughts
    - emotions
    - personal experiences
  - Set personal goals
  - Track progress
  - Receive reminders and prompts
  - Privacy features to ensure their personal reflections remain confidential
- Professional:
  - Facilitate task management
    - set and prioritise work-related targets
  - Be able to track deadlines
  - Collaborate with team members
  - Schedule appointments
  - Integration with productivity tools (e.g. Google Calendar)
  - Have reporting options to monitor their work progress, such as visualisation tools
- Students:
  - Able to assist students with organising:
    - schedules
    - assignments
    - exams
  - Able to take notes and categorise / tag notes by subject
  - Be able to set reminders and notifications to stay on top of deadlines or upcoming exams
  - Integration with educational platforms to enhance user experience
- Creative Professionals:
  - Capture and organise creative ideas (inspiration, visual content)
  - Features to enable user to sketch or annotate images
  - Ability to create mood boards or visual collections for inspiration
  - Integration with design software or image repositories
- Entrepreneurs:
  - Enable user to document business ideas, plan and strategies
  - Sections to track financial goals, marketing plans and customer insights
  - Collaboration with team members and mentors
  - Option to export and create reports and presentations for investors and stakeholders

</details>

<details>
  <summary>Client Needs</summary>

- User engagement
  - Provide a captivating and intuitive interface to keep users engaged
  - Users should find value in the app's features, leading to regular usage and retention
  - Implement gamification elements / achievement rewards to encourage user activity
- Scalability and Performance
  - Be able to handle number of users without compromising performance
  - Efficient back architecture and database management
  - Regular maintenance and optimisation to address any performance bottlenecks
- Data Security and Privacy
  - Priority regarding user data security and implement appropriate measures to protect user information
  - Compliance with data protection regulations such as GDPR if applicable
  - User permission and privacy settings to allow users control over their data
- Continuous Improvement
  - Provide opportunities for user feedback
  - Regular updates and bugfixes to improve the app's functionality
  - Stay up-to-date with industry trends and technological advancements

</details>

---

### Opportunity Matrices

![Strategy: Opportunity matrices](../../media/images/strategy_opportunity-matrices.png)

## Scope

The Scope Plane defines the overall boundaries and scope of the project, including the Content and Functionality Requirements.

The following content and functionality requirements help define the scope of the project and provide a clear understanding of what needs to be implemented to meet the objectives of the Mindful Minutes application. They serve has a foundation for subsequent stages of the design and development process. These are documented to ensure the final product meets expectations and needs of the users and clients.

<details>
  <summary>Content Requirements</summary>

The content requirements refer to the specific content elements and information that need to be included in the project. These requirements define what type of content should be present and what information should be communicated to users. Content requirements include text, images, videos, documents and any other form of media or data.

- User generated journal entries with fields including:
  - title
  - date
  - content

-Sections for:
  - appointment diary
  - day targets
  - notes
  - what I have learnt
  - successes
  - wins
  - what I could do better
  - future ideas

- Customisable settings and preferences for user profiles

- Privacy settings to control the visibility of journal entries

- Integration with a repository for file uploads and storage

</details>

<details>
  <summary>Functionality Requirements</summary>

The functionality requirements define specific features, actions and capabilities that the application should provide its users. These requirements focus on the desired functionality and behaviour of the application.

- User registration and authentication system

- Ability manipulate journal entries:
  - create
  - read
  - update
  - delete

- Search functionality to find specific journal entries

- Calendar integration for appointment scheduling

- Task management system with deadlines (and reminders)

- Collaboration features for shared journals and notes

- Reporting and analytics to track progress and achievements

- Admin management functionality to manage users, roles and permissions

</details>

## Structure

### Information Architecture & User Journey

#### User Management

The User is the main entry point in this Information Architecture. The User has access to various sections to the Mindful Minutes (Journal App) including:
- Login
- Appointment Diary
- Day Targets
- Note
- Successes
- Wins
- Improvements
- Ideas
- What I've Learnt

Each section represents a specific functionality or feature within the app that the User can interact with.

The simple User Journey represents the typical flow of actions for the User in interacting with the different sections of the Mindful Minutes (Journal App). The User can navigate through the sections, view, create or delete content as per their needs and preferences.

![Structure: User User Journey](../../media/images/structure_user-user-journey.png)

---

#### Admin Management

The Admin is the main entry point in this Information Architecture. The Admin has access to various sections of the Mindful Minutes (Journal App). The Admin has access to various sections of the app, including Login, Manage Users, Manage Content and Reports. Each section represents a specific functionality or feature within the app the Admin can manage.

The simple User Journey represents the typical flow of actions for the Admin in managing and interacting with the different sections of the Journal app. The Admin can navigate through the sections, perform CRUD (Create, Retrieve, Update, Delete) operations, manage user accounts and generate reports when necessary.

![Structure: Admin User Journey](../../media/images/structure_admin-user-journey.png)

---

#### Repo Management

The Repository is the main component in this Information Architecture. The User Journey includes login to ensure secure access to the repository functionality for authorised users only. 

![Structure: Repository User Journey](../../media/images/structure_repo-user-journey.png)

## Skeleton

### Home page

---

### Features

#### Sign up / Register & Login / Logout

---

#### Morning page

---

#### Evening page

---

#### My profile page

---

#### Contact page

---

#### Modals

## Surface

### Imagery

Using [Unsplash](https://unsplash.com), with the keywords:

- peace
- mindfulness
- reflection
- journal
- diary

I gathered the selected images, to use as a reference to create a [Color Palette](#colour-palette).

![Surface: Imagery - Mood Board](../../media/images/surface_imagery.png)

Image references:

- [a black and white photo on a white wall by Annie Spratt](https://unsplash.com/photos/Bf9PT5qVZvM)
- [white printer paper beside black pen by Markus Spiske](https://unsplash.com/photos/IqVqS1V1ch8)
- [flat lane photo of book and highlighters by Estée Janssens](https://unsplash.com/photos/hb00NH1JXh0)
- [white notebook beside white ceramic mug on brown wooden table by Susan Weber](https://unsplash.com/photos/xcWd06vcsJo)
- [blue sky with white clouds by Jessica Delp](https://unsplash.com/photos/c7YYeMemTzw)
- [selective focus photo of pink petaled flowers by Kien Do](https://unsplash.com/photos/NjT4O7WYmwk)
- [body of water and snow-covered mountains during daytime by Tim Stief](https://unsplash.com/photos/YFFGkE3y4F8)
- [white and brown greeting card by Emily Park](https://unsplash.com/photos/jGjBDv06hDw)
- [white flowers in clear glass vase by Sixteen Miles Out](https://unsplash.com/photos/TN6kLg466Bc)
- [green and white sky by Marek Szturc](https://unsplash.com/photos/2s3fI3M1lO0)
- [orange flowers by Masaaki Komori](https://unsplash.com/photos/7xP5BJ34ybg)
- [black stones with sun in the distance b< Siim Lukka](https://unsplash.com/photos/C5tIVJaa-Ic)

---

### Colour Palette

From the Mood Board created under [Imagery](#imagery), I looked for predominant colours and colour combinations in the images that were visually appealing and aligned to the the Mindful Minutes' (Journal App) theme. Using [Adobe Color](https://color.adobe.com/create/color-wheel) to extract colours from [white notebook beside white ceramic mug on brown wooden table by Susan Weber](https://unsplash.com/photos/xcWd06vcsJo) taken from the Mood Board and create a cohesive colour palette.

![Adobe Color Extract Theme Screenshot](../../media/images/surface_colour-palette_extract-theme.png)

While considering the colours which would evoke the desired mood, other considerations regarding the application's user interface were:

- provide good contrast
- readability
- accessibility

![Surface: Colour Palette](../../media/images/surface_colour-palette.png)

---

### Typography

---

### Mock-ups