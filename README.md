# Django personal blog
<img src="https://github.com/ImustAdmit/Personal-blog-django/blob/master/personal_blog/conf/static/admin/coverage.svg"> <img src="https://img.shields.io/badge/License-MIT-yellow.svg"> <img src="https://img.shields.io/badge/python-3.8-blue.svg">


This is my personal website built using Django framework and Bootstrap as frontend. [Live here](https://uczsieit.pl)
Website allows you to add personalized articles (thanks to installed WYSIWYM content editor - ckeditor). Visitors to the site can comment on articles that are displayed after being accepted by the administrator. 
The website thanks to Google Analytics allows you to track website traffic, and thanks to Sentry you can be up to date with information on the status of the website (logs registration).
Website include features improving UX such as infinite scrolling, hiding navbar and swiper.
To the project was also added caching (via memcached) which makes delay due to network latency unnoticeable.

## Installing

```
$ git clone https://github.com/ImustAdmit/Personal-blog-django.git
```

## Running the tests

Project is almost fully covered with tests :bookmark_tabs:!

```
$ pytest
```

## Screenshots

![image](https://user-images.githubusercontent.com/58914643/80281998-429bfe00-870f-11ea-8133-c622e3d5ccd6.png)

![image](https://user-images.githubusercontent.com/58914643/80281885-91956380-870e-11ea-9509-66916f2d3467.png)

![image](https://user-images.githubusercontent.com/58914643/80281930-d7eac280-870e-11ea-8037-bf534727813e.png)

## Structure

In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods. Endpoints are logically organized around applications - In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods. Endpoints are logically organized around applications - in case of that project **Blog(Posts)** and **Comments**. Details below:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`categories/` | GET | READ | Get all categories
`categories/:id/` | GET | READ | Get a single category with posts belonging to it
`posts/:id/`| GET | READ | Get a single post with comments belonging to it
`posts/:id/content/` | GET | READ | Get pre-rendered HTML post content
`comments/` | GET | READ | Get all comments
`comments/:id/` | GET | READ | Get a single comment with replies belonging to it
`comments/` | POST | CREATE | Create a new comment

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
