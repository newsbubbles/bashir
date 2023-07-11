## Bashir: by @MachineArts a.k.a @newsbubbles

import os, time, uuid, argparse, pexpect
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import openai
import getpass
try:
    import readline
except ImportError:
    import pyreadline as readline


## Support
def parse_args():
    parser = argparse.ArgumentParser(description='Bashir Command Line Arguments')
    parser.add_argument('--os', default='RHEL9', help='Operating system; eg "RHEL9"')
    parser.add_argument('--shell', default='bash', help='Shell name; eg "bash" or "PowerShell"')
    args = parser.parse_args()
    return args.os, args.shell

def save_script(content, comment=None):
    fn = sdir + '/' + str(uuid.uuid4()) + '.sh'
    #print('Writing script:', fn)
    comment_section = '' if comment is None else '# ' + comment + '\n'
    #content = '#!/bin/bash\n\n' + comment_section + content
    content = '#!/bin/bash\n\n' + 'export SYSTEMD_PAGER=""\n' + comment_section + content
    perm = 0o755
    with open(fn, 'w+') as f:
        f.write(content)
    os.chmod(fn, perm)
    return fn

## Body

# Context Settings: can be any OS and command line interpreter
operating_system, cli = parse_args()

# Confirmation state and other vars
CONFIRM_NONE, CONFIRM_ALL, CONFIRM_SUDO = 0, 1, 2
confirmation = CONFIRM_NONE

# Configure prompt history for fancier more util input
try:
    readline.read_history_file()
except FileNotFoundError:
    pass

# Config langchain chat model
openai.api_key = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=1.24)
system_message = SystemMessage(content=f"You are an advanced coding translator. You take natural language and convert whatever the user explains they want to do as a sequence of {cli} commands for {operating_system}. If a user asks how much space they have left on their hard drive, you output the proper commands needed to run in order to see that as a final output. Do not include explanations, only the translation into {cli}. Always use command arguments that bypass user confirmation like -y when using `apt install`.")

# Prepare scripts folder
sdir = os.path.join(os.getcwd(), 'scripts')
if not os.path.exists(sdir):
    os.makedirs(sdir)

# Title
print('\n--------------------------------------------\nBashir: LLM based Junior System Admin v0.1.0\n--------------------------------------------\n')
print('OS:', operating_system, '\nCLI:', cli, '\n')

# Spawn a new bash shell
child = pexpect.spawn('/bin/bash', echo=False)

# Set up for sudo prompting
password = None if confirmation > CONFIRM_NONE else getpass.getpass("Enter sudo password: ")
sudo_prompt = r'\[sudo\] password for .*: '
def_prompt = 'Prompt> '

while True:
    try:
        # Display the command prompt
        # This can vary depending on system configuration
        child.sendline(f'PS1="{def_prompt}"')
        child.expect(def_prompt)
        print(def_prompt, end='', flush=True)
        
        # Get command
        command = input()

        # If the user types 'exit', then end the loop and close
        if command.strip() == 'exit':
            break

        # Write history file for pretty history
        readline.write_history_file()

        # Perform call to LLM and get a bash script in return
        response = chat([system_message, HumanMessage(content=command)])
        bash_script = response.content

        # Save the bash script
        script_path = save_script(bash_script, comment=def_prompt + command.strip())

        # Send command to bash
        child.sendline(f'bash {script_path}')
        time.sleep(0.5)
        
        # Expect the command prompt again or asking for sudo pass
        try:
            eindex = child.expect([def_prompt, sudo_prompt], timeout=10)
            if eindex == 1 and password is not None:
                child.sendline(password)
                child.expect(def_prompt)
        except pexpect.TIMEOUT:
            print(child.before.decode('utf-8').strip())
            # if child.isalive():
            #     child.sendintr()
            continue
        except pexpect.EOF:
            print(child.before.decode('utf-8').strip())
            break
        
        # Print the output of the command
        print(child.before.decode('utf-8').strip())
    except Exception as e:
        print(str(e))

# Close the bash shell
child.close()
