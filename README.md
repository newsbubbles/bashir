# bashir & wombat
An LLM based Junior System Admin for wrapping Linux/Bash shell and it's Windows counterpart. Bashir for Linux and Wombat for Windows.

I have done system admin for a long time and I've gotten tired of having to look up commands on different types of operating systems for things I don't often use. This handy little script translates a natural language prompt into commands for my terminal and shows me the output as if I were just entering the right commands. I just tell bashir (or wombat) what I want it to do or ask it what I want to know about the system, and it will put together a script, run it and forward me the output as if it were the shell.

![Screenshot](https://github.com/newsbubbles/bashir/assets/1012779/923db62e-fa21-4635-8014-12c665c31313)

## Disclaimer
*Bashir uses gpt-3.5 by default and is an experimental script. Use caution when using bashir as it will perform superuser commands if needed.  I suggest testing capabilities within a VM or dedicated cloud instance.  Any damages, direct or indirect, real or perceived, implied or unexpected, that you may incur on your person or your devices while using bashir are not the responsibility of the author and by using bashir you are legally pardoning the author from any such claim of responsibility or damages.*

## Privacy
I like privacy and I know you probably do too. Short of using a local model (which I encourage you to try and let me know how it turns out), I have included some security features into how bashir works.  It does not send your OSes responses or chat history to the LLM API.  It only sends the system message and your current user message as if it were the first message in the chat.  Since the prompts you are sending are pretty much questions about your OS or broad commands like "install a node/react online store dev stack", this will avoid most possible privacy breaches when using hosted LLMs like OpenAI's models.

## Features
- Run entirely generated customized bash scripts with just a natural language prompt
- Ask any question the operating system can answer and it will
- Keeps a copy of all scripts generated in `scripts` folder

## Features To Be Added
- Human verification (on all scripts or only on ones that use "sudo" thus performing system changes)
- Script line selection with cursor (lets user decide which lines to run from script)
- Properly changing the shell environment and using ".bat" scripts for windows as default if used as OS
- Some way to properly forward output on long running processes with pexpect
- Alternate solutions (multiple generations and a choice between running entire scripts)

## Requirements
- OpenAI
- LangChain

## Install
```bash
pip install openai, langchain, pexpect
```
If you haven't already added `OPENAI_API_KEY` to your environment this is a good time to do it.
```bash
export OPENAI_API_KEY={YOUR-API-KEY}
```
Replace `{YOUR-API-KEY}` with your OpenAI API Key.
If you want this to persist when you reboot your computer, make sure to add that line to the end of your ~/.bashrc file

## Usage
To be lazy and just let python choose what tool to use, use `entry`
```bash
python entry.py
```
for **Linux** or **MacOS** use
```bash
python bashir.py
```
for **Windows** use
```cmd
python wombat.py
```
When you run bashir, it will start out by asking you the `sudo` password.  This is in the case that you are going to ask bashir questions that will make it generate commands that need to use the superuser permissions level.  This is where I exercise using caution when asking it things.  It will write any bash script, so it might even be able to mess up your environment pretty bad if you aren't careful what you ask for.  I will work on putting more effort into security in future versions.

### If you have Alternate OS and shell environment
```bash
python bashir.py --os=Ubuntu22 --shell=sh
```
Assumed defaults are OS=RHEL9 and shell=bash.  These two variables go into the LLM's prompt so the format of OS name/version is not strict.

## How it Works
Bashir creates a `scripts` folder wherever you are running it.  In this folder it places a bash script. The bash script includes a comment with the original prompt and is assigned a unique identifier as it's name.  It is then chmodded to allow execution, and executed in a wrapped shell process.  Bashir uses pexpect to expect the prompt or a few other things and effectively wrap the bash shell within the python instance, so you get actual output from the embedded shell. Bashir tries to take advantage of the "conversational" way that terminals and command line interfaces already work

To exit bashir type `exit` at the prompt and hit `Enter`.

## Examples
In these examples, the bash script is shown and original prompt as a comment at the top followed by the bash commands that the LLM responded to the prompt with to be run

Asking the time in Linux
```bash
# Prompt> what time is it?
date "+%T"
```
Asking the time in Windows
```cmd
REM Prompt> what time is it?
echo %TIME%
```
More examples in Linux...
```bash
# Prompt> what folder am I in?
pwd
```
```bash
# Prompt> how much system memory am I using?
free -m
```
```bash
# Prompt> give me a list of the groups on this system
cat /etc/group
```
```bash
# Prompt> initialize a git project and create a README.md file
mkdir project_name
cd project_name
git init
touch README.md
```
```bash
# Prompt> do I have the urllib3 pip package installed?
pip list | grep urllib3
```
```bash
# Prompt> open a new terminal window
gnome-terminal
```
Installing a classic stack on Red Hat Enterprise Linux
```bash
# Prompt> install a LAMP stack
sudo yum install httpd
sudo systemctl enable httpd
sudo systemctl start httpd
sudo yum install mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb
sudo mysql_secure_installation
sudo yum install php php-mysql
sudo systemctl restart httpd
```
Installing that same stack on Ubuntu 22
```bash
# Prompt> install a LAMP stack
sudo apt update
sudo apt install -y apache2
sudo apt install -y mariadb-server
sudo apt install -y php libapache2-mod-php php-mysql
```
Some more novel ideas for prompts...
```bash
# Prompt> what is 7 + 298
echo $((7 + 298))
```
LangChain has "Tool using Agents" where you define a set of tools in the prompt for the agent to use. That is a great and pretty useful concept within a small set of possible actions, but an agent that can make bash script has literally all of the tools of the operating system at it's behest. Not only calculator but curl with data manipulation and comprehension...
```bash
# Prompt> what is the top headline on reddit.com?
curl -s "https://www.reddit.com/.json" | jq -r '.data.children[0].data.title'
```

## More Reflections on this prompt shell paradigm

### A set of questions
![scshot2](https://github.com/newsbubbles/bashir/assets/1012779/46e3f683-3b07-4aaf-95bf-27bc7161a1c3)

Perhaps the most interesting context that emerges from going about command line as a sequence of prompts is that natural language prompts are cross-OS-compatible. Technicaly one could save a sequence of prompts as a server set up and then just run bashir aftter installing python on the server and let bashir handle translating the sequence of server setup prompts into the proper OS and shell language.

### Using bashir to update bashir properly
![image](https://github.com/newsbubbles/bashir/assets/1012779/7fe54729-e283-44bf-a1db-1da73a2391e3)

I actually run into this problem sometimes with git repos where I end up making some change, only to realize I needed to do it another way but I already saved that file and it is now ahead of `master` or `main`... It happens so inoften that I have to look up the proper commands.  This morning bashir saved me at least 5 minutes looking for this solution, *again*, and it was solved in about 4 seconds.

## Limitations I've Found
There are probably way more I haven't found, but here are the ones so far:
- When outputting large lists of things like asking to list installed packages you shouldn't try to force it to use things like `more` or subcommands that pretty up the output.  It is fine to make it get a little creative and pipe to grep or something, but it is best if you want to actually read some long list, tell it in plain english to "output the list to a file named out.txt"
- There is still no really good way to handle longer running processes so things like detecting timeout and sending Ctrl+C to the process are not really that great of a solution. Currently I try to have it just every 10 seconds try to flush the output of the command to screen if process takes longer than that.
- This one is perhaps a design choice, but I have not built any sort of memory into the agent that allows it to keep context within the prompt about things that the OS says.  That being said, one limitation is that you can't make "chains" of scripts that rely on the output from previous scripts.  Well, not yet anyway.

## Conclusion
It is pretty experimental but it was a quick script to put together and it seems like it will definitely help me set up EC2 instances on Amazon Linux, etc.

Let me know if you run into issues, I will actively check this project and make regular updates if people start using it.
