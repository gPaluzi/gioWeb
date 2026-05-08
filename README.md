# Personal Web

Flask based web app, a simple exercise for me to learn web development and upgrade my personal branding.

Recently deployed on [Render.com](https://gioweb.onrender.com/).

## How it works
Data -> seeded to DB -> Flask route -> Jinja Templates

## Future works
### Content
- AboutMe: Insert all experiences
- AboutMe: Add more skills

### Frontends
- Create personalities pagination in aboutme

### Backends
- Add error handling in seed.py
- Move data validations to services/utils instead in models
- Add advanced filtering in aboutme sections
- Add small api route to learn JS fetching
- Add portofolios data model, *make sure have FK to skills table*
- Sanitize the html from markdown before seeded to db
- Use flask blueprints if things start messy

### Others
- Check typing for easier development