from pathlib import Path
import shutil
import subprocess
import os
from weakref import ref
from jinja2 import Environment, FileSystemLoader


PATH_RT = Path(__file__).parent.parent.absolute()

PATH_TEMP =  PATH_RT / 'templates' / 'temp'
PATH_TEX = PATH_RT  / 'templates' / 'tex'

def refresh_tex_env()-> Environment:

    tex_env = Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%%',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = FileSystemLoader(PATH_TEX))

    return tex_env

def compile_from_tex(name: str)-> str:
    try:
        ext_list = [(name + ext) for ext in ['.tex', '.pdf', '.log', '.aux']]
        tex_file, pdf_file, log_file, aux_file = ext_list

        with open(PATH_TEX / tex_file, 'r') as tex_temp:

            pass

        sp1 = subprocess.run(['pdflatex',  (PATH_TEMP / tex_file).__str__()], capture_output=True, check=True)

        shutil.move(PATH_RT / pdf_file, PATH_TEMP / pdf_file)
        
    # Intermediate file cleanup
        if os.path.isfile(PATH_RT / log_file):
            os.remove(PATH_RT / log_file)

        if os.path.isfile(PATH_RT / aux_file):
            os.remove(PATH_RT / aux_file)

    except subprocess.CalledProcessError as err:
        print('Subprocess pdflatex failed to run with the following output:\n%s' % err.stderr)

    return PATH_TEMP / pdf_file


def write_tex_template(name: str, template_form: dict, refresh=True)-> None:
    if refresh:
        tex_env = refresh_tex_env()

    tex_file = '%s.tex' % name

    temp = tex_env.get_template(tex_file)

    with open(PATH_TEMP / tex_file, 'w+') as temp_file:
        temp_file.write(temp.render(template_form))

    return compile_from_tex(name)

    

     




