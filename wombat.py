## Wombat: by @Saffire33 a.k.a. Hattendo
## Bashir: by @MachineArts a.k.a @newsbubbles

import os, time, uuid, argparse, pexpect
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import openai
import getpass

## Support
def parse_args():
    parser = argparse.ArgumentParser(description='Bashir Command Line Arguments')
    parser.add_argument('--os', default='Windows10', help='Operating system; eg "Windows10"')
    parser.add_argument('--shell', default='cmd', help='Shell name; eg "cmd" or "PowerShell"')
    args = parser.parse_args()
    return args.os, args.shell

def save_script(content, comment=None):
    fn = sdir + '\\' + str(uuid.uuid4()) + '.cmd'
    comment_section = '' if comment is None else 'REM ' + comment + '\n'
    content = '@echo off\n\n' + comment_section + content
    with open(fn, 'w+') as f:
        f.write(content)
    return fn

## Body

# Context Settings: can be any OS and command line interpreter
operating_system, cli = parse_args()

# Confirmation state
CONFIRM_NONE, CONFIRM_ALL, CONFIRM_SUDO = 0, 1, 2
confirmation = CONFIRM_NONE

# Config langchain chat model
openai.api_key = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=1.24)
system_message = SystemMessage(content=f"You are an advanced coding translator. You take natural language and convert whatever the user explains they want to do as a sequence of {cli} commands for {operating_system}. If a user asks how much space they have left on their hard drive, you output the proper commands needed to run in order to see that as a final output. Do not include explanations, only the translation into cmd commands. Always use command arguments that bypass user confirmation.")

# Prepare scripts folder
sdir = os.path.join(os.getcwd(), 'scripts')
if not os.path.exists(sdir):
    os.makedirs(sdir)

print('\n--------------------------------------------\nBashir: LLM based Junior System Admin v0.1.0\n--------------------------------------------\n')
print('OS:', operating_system, '\nCLI:', cli, '\n')

import pexpect
import time
from pexpect.popen_spawn import PopenSpawn

# Spawn a new command prompt
child = PopenSpawn('cmd', encoding='utf-8')
def_prompt = 'Prompt> '

while True:
    try:
        print(def_prompt, end='', flush=True)

        # Get command
        command = input()

        # If the user types 'exit', then end the loop and close
        if command.strip() == 'exit':
            break

        # Perform call to LLM and get a bash script in return
        response = chat([system_message, HumanMessage(content=command)])
        bash_script = response.content

        # Save the bash script
        script_path = save_script(bash_script, comment=def_prompt + command.strip())

        # Send command to command prompt
        child.sendline(script_path)
        time.sleep(0.5)

        # Expect the command prompt again or asking for sudo pass
        try:
            child.expect(def_prompt, timeout=10)
        except pexpect.TIMEOUT:
            print(child.before.strip())
            continue
        except pexpect.EOF:
            print(child.before.strip())
            break

        # Print the output of the command
        print(child.before.strip())
    except Exception as e:
        print(str(e))

# Close the command prompt
child.close()