import markdown

from flask import render_template, request
from .utils.content import get_experience, generate_experience, generate_skills, get_projects

def init_routes(app) -> None:
    @app.route('/')
    def index():
        return render_template('home.html')

    @app.route('/about')
    def about():
        filter_type = request.args.get('exp_filter', 'all')

        experiences = generate_experience(get_experience(filter_type))
        skills = generate_skills()

        return render_template(
            'about.html',
            experiences = experiences, 
            skills = skills,
            active_filter = filter_type
        )

    @app.route("/portfolio")
    def portfolio():
        projects = get_projects()

        for project in projects:
            project.html_content = markdown.markdown(project.content)

        return render_template('portfolio.html', projects=projects)