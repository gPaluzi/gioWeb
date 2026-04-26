import markdown
import frontmatter
from pathlib import Path

def parse_md(path: str | Path):
    path = Path(path) if isinstance(path, str) else path

    post = frontmatter.load(path)
    html = markdown.markdown(post.content)

    return {
        'metadata': post.metadata,
        'content': post.content,
        'html': html
    }
    