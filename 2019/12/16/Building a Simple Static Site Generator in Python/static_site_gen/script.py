from markdown2 import markdown 
from jinja2 import Environment, FileSystemLoader
from json import load

template_env = Environment(loader=FileSystemLoader(searchpath='./'))
template = template_env.get_template('layout.html')

with open('article.md') as markdown_file:
    article = markdown(
        markdown_file.read(),
        extras=['fenced-code-blocks', 'code-friendly'])

with open('config.json') as config_file:
    config = load(config_file)

with open('site/tutorials/index.html', 'w') as output_file:
    output_file.write(
        template.render(
            title=config['title'],
            description=config['description'],
            author=config['author'],
            code_link=config['code_link'],
            identifier=config['identifier'],
            url=config['url'],
            article=article
        )
    )