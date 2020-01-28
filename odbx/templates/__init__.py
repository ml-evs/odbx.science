from pathlib import Path
from starlette.templating import Jinja2Templates

template_dir = Path(__file__).parent
TEMPLATES = Jinja2Templates(directory=[template_dir])
