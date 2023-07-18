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
  - [Packages](#packages)
  - [Frameworks, Libraries \& Additional Programs/Software used](#frameworks-libraries--additional-programssoftware-used)
    - [Libraries](#libraries)
- [Remote \& Local Deployment](#remote--local-deployment)
  - [Remote Deployment](#remote-deployment)
    - [Create Heroku App (via the Dashboard)](#create-heroku-app-via-the-dashboard)
    - [Create a new PostgreSQL Database Instance](#create-a-new-postgresql-database-instance)
    - [Set up Heroku Config Vars](#set-up-heroku-config-vars)
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
  - [References](#references)
  - [Code Used](#code-used)
  - [References \& Resources](#references--resources)
    - [Agile](#agile)
    - [Deployment](#deployment)
    - [CI / CD](#ci--cd)
    - [Django](#django)
    - [Django Testing](#django-testing)
      - [Automated testing](#automated-testing)
    - [Django](#django-1)
    - [Performance and Optimisation](#performance-and-optimisation)
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

Personalise experience:
- [How to use ChatGPT as a Personalized Mantra Generation for Meditation](https://chatgptschool.org/how-to-use-chatgpt-as-a-personalized-mantra-generator-for-meditation-2/)

### Accessibility

## Technologies Used

### Stack

- HTML5
- CSS3
- JavaScript
- Python

### Packages

- [CKEditor](https://ckeditor.com/)
  - Used this editor, rather than [Summernote](https://summernote.org), due to conflict with Django version. I previously worked with CKEditor when I worked with ConcreteCMS

### Frameworks, Libraries & Additional Programs/Software used

- Django

#### Libraries

- [Black](https://black.readthedocs.io/)


```
# install packages
pip install <package_name>

# uninstall packages
pip uninstall <package_name>

# update requirements.txt file
pip freeze --local > requirements.txt
```

## Remote & Local Deployment

[Agile User Story Master on Google Sheets](https://docs.google.com/spreadsheets/d/1AhkEDuU5mDY9n6TMRGyk5BchJ2ijZUxiFlvbauW9HUE/edit?usp=sharing) was created from a template supplied by our Cohort October 2022 Tutor, Rebecca Tracey-Timoney.

```shell
pip install django

pip install gunicorn # Server used to run Django on Heroku
```

### Remote Deployment

Install `python-dotenv` package with `pip install python-dotenv`
Create a `.env` file at the root of the project with the following keys

```
SECRET=<YOUR_SECRET_KEY>
DATABASE_URL=<ELEPHANTSQL_URL>
DEVELOPMENT=<SET TO 'True' if in development mode or remove or set to 'False' for production>
```

#### Create Heroku App (via the Dashboard)

[heroku _create_app.webm](https://github.com/halfpintutopia/mindful-minutes/assets/30613818/17142ef0-b723-4652-a0a9-53acdbcd5ce9)

1. Login
2. From the Dashboard, click the "New" button
3. Choose "Create new app" from the drop-down menu
4. Give the app a unique name, it *must* be unique otherwise Heroku complains
5. Choose the region appropriate to you
6. Click the "Create app" button

#### Create a new PostgreSQL Database Instance

[elephantsql_database_instance.webm](https://github.com/halfpintutopia/mindful-minutes/assets/30613818/e061fe61-76db-4157-b7cf-c7e720e2783e)

1. Login
2. Click the "Create New Instance" button
3. Set up a plan
   - Provide a name
   - Select the _Tiny Turtle (Free)_ plan
   - Add tags if needed
4. Click the "Select Region" button
   - Choose the data centre closest to you
5. Click the "Review" button
6. Click the "Create instance" button
7. From the list of instances on your dashboard, click the name of the new instance
8. Copy the URL from the "Details" page and paste this link into your settings.py file in your Django project


#### Set up Heroku Config Vars

[heroku _config_vars.webm](https://github.com/halfpintutopia/mindful-minutes/assets/30613818/d19dd102-eab2-4750-a5ee-0963ad7039be)

1. Login
2. Go to the project and click on the Settings tab
3. Go to the "Config Vars" section and add the following variables:
   - DATABASE_URL
   - SECRET_KEY
   - PORT
   - CLOUDINARY_URL

DISABLE_COLLECT_STATIC 1


### Local Deployment

#### GitHub Actions

##### Configuration steps

1. Docker Registry 
   - Set up a Docker registry on Docker Hub
2. Docker Registry Image
   - Name and tag Docker image for project, with the following format:
     - `registry-url/username/repo-name:tag` (e.g. `docker.io/username/project:latest`)
3. GitHub Repository
   - Set up repo secrets
     - Go to "Settings" and under "Secrets and variables", click on "Actions"
     - Create a secret for `DOCKER_REGISTRY_IMAGE`. Set this to the Docker Registry Image name and tag set in Step 2
   - Create a new `YAML` file in the located in the `.github/workflows` directory located in the root of the repo 


### Contributing

## Data Models
### Schematics

![Mindful Minutes ERD - Database ER diagram (crow's foot)](docs/media/images/mm_erd.png) created with [LucidChart](https://lucid.app).

Considered creating a base model or mixin as models most of the models contained the same fields e.g.

```python
# Creating the base model to be inherited by models
class BaseModel(models.Model):
  field_1 = models.CharField(max_length=50)
  field_2 = models.IntegerField()
  field_3 = models.TimeField()

  class Meta:
    abstract = True

# implementation of BaseModel by inheritance as follows:
class ModelOne(BaseModel):
  additional_field_1 = models.TextField()


# Creating the mixin to be reused by models
class MixinModel(models.Model):
  field_1 = models.CharField(max_length=50)
  field_2 = models.IntegerField()
  field_3 = models.TimeField()

  class Meta:
    abstract = True

# implementation of reusing the MixinModel
class ModelTwo(MixinModel):
  additional_field_1 = models.TextField()
```

As the models had the exactly the same fields with not additional fields or behaviours, I chose to keep the models separate. Having individual models allows for clarity and simplicity as well as making it more maintainable, as then the codebase is more flexible to evolve independently.


## Testing

### Django Test Driven Development using REST Framework

For further details on testing, click [here](docs/testing/testing.md).

### User experience

[Browserstack](https://www.browserstack.com) was used for testing. The devices were:

### Bugs & Fixes

### Lighthouse

### Validator Testing

- [CI Python Linter](https://pep8ci.herokuapp.com/)

## Credits

### References
[Add 'go to top' button on Readme.md](https://github.com/orgs/community/discussions/42712)

### Code Used

### References & Resources


#### Agile

- [Agile User Story Template Spread Sheet, resource provided by Rebecca Tracey-Timoney](https://docs.google.com/spreadsheets/d/1E87iXrwStqmuy0DatpK8e-pD3ygBqotS91npelTbVVs/edit?usp=sharing)
- [Project Management on GitHub](https://www.topcoder.com/thrive/articles/project-management-on-github)
- [Acceptance Criteria for User Stories: Purposes, Formats, Examples, and Best Practices](https://www.altexsoft.com/blog/business/acceptance-criteria-purposes-formats-and-best-practices/)
- [User stories with examples and a template](https://www.atlassian.com/agile/project-management/user-stories)
- [Define features and epics, organize your product and portfolio backlogs in Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/define-features-epics?view=azure-devops&tabs=agile-process)
- [Chapter 15: Requirements and user stories](https://www.agilebusiness.org/dsdm-project-framework/requirements-and-user-stories.html)
- [Epics, User Stories, Themes, and Initiatives: The Key Difference and Examples](https://www.altamira.ai/blog/difference-between-epics-vs-user-stories/)
- [How to Write a Good User Story: with Examples & Templates](https://stormotion.io/blog/how-to-write-a-good-user-story-with-examples-templates/)
- [Epics vs. User Stories: what’s the difference?](https://www.delibr.com/post/epics-vs-user-stories-whats-the-difference)

#### Deployment

- [How to use Environment Variables in Django](https://codinggear.blog/django-environment-variables/)

#### CI / CD

- [GitHub Actions - Create starter workflows](https://docs.github.com/en/actions/using-workflows/creating-starter-workflows-for-your-organization)

#### Django

- [Django Documentation](https://docs.djangoproject.com)
- [Test-Driven Development with Django, Django REST Framework and Docker](https://testdriven.io/courses/tdd-django)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/en/)
- [Getting the Most Out of the Django's User Model](https://www.youtube.com/watch?v=sXZ3ntGp_Xc)
- [Django - Extend User Model](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)

#### Django Testing

##### Automated testing

- [Creating a Custom User Model in Django](https://testdriven.io/blog/django-custom-user-model/)
- [Testing Models with Django using Faker and Factory Boy](https://medium.com/analytics-vidhya/factoryboy-usage-cd0398fd11d2)
- [Pytest for Beginners](https://testdriven.io/blog/pytest-for-beginners/)
- [Pytest](https://docs.pytest.org/en/latest/getting-started.html)
- [Testing in Django with Selenium](https://ordinarycoders.com/blog/article/testing-django-selenium)
- [How to authorize user in Django testing REST framework APIClient post method](https://stackoverflow.com/questions/70967642/how-to-authorize-user-in-django-testing-rest-framework-apiclient-post-method)
- [Freezegun](https://github.com/spulec/freezegun)

#### Django

- [Effectively Using Django REST Framework Serializers](https://testdriven.io/blog/drf-serializers/)
- [Introduction to Django Channels](https://testdriven.io/blog/django-channels/)
- [Migrating a Custom User Model Mid-Project in Django](https://testdriven.io/blog/django-custom-user-model-migration/)
- [Customize Django Admin](https://earthly.dev/blog/customize-django-admin-site/)

#### Performance and Optimisation

- [A Guide to Performance Testing and Optimization with Python and Django](https://medium.com/designcentered/ux-design-5-planes-method-b1b1d6587c05)
- [Scaling Django Applications: Best Practices and Strategies](https://medium.com/ux-diaries/imdb-website-redesign-ux-case-study-c42f65a69b98)

### Content

### Media

### Acknowledgements

Thanks to Adam Gilroy for giving me permission to use his LinkedIn Post as inspiration for a Use Case.

[Back to the top](#mindful-minutes)
