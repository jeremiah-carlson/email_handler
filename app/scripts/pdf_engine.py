from pathlib import Path
import shutil
import subprocess
import os

PATH_RT = Path(__file__).parent.parent.absolute()

PATH_TEMP =  PATH_RT / 'templates' / 'temp'

def compile_from_tex(name: str)-> None:
    try:
        ext_list = [(name + ext) for ext in ['.tex', '.pdf', '.log', '.aux']]
        tex_file, pdf_file, log_file, aux_file = ext_list
        sp1 = subprocess.run(['pdflatex',  (PATH_TEMP / tex_file).__str__()], capture_output=True, check=True)

        shutil.move(PATH_RT / pdf_file, PATH_TEMP / pdf_file)
        
    # Intermediate file cleanup
        if os.path.isfile(PATH_RT / log_file):
            os.remove(PATH_RT / log_file)

        if os.path.isfile(PATH_RT / aux_file):
            os.remove(PATH_RT / aux_file)

    except subprocess.CalledProcessError as err:
        print('Subprocess pdflatex failed to run with the following output:\n%s' % err.stderr)







