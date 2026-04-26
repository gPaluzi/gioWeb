import markdown
import frontmatter

def parse_md(path):
    with open(path, 'r', encoding='utf-8') as file:
        return markdown.markdown(file.read())
    
def get_yaml(path):
    with open(path, 'r') as file:
        data = frontmatter.load(file)
    return data.metadata