# bashir
An LLM based Junior System Admin for wrapping Linux/Bash shell originally but also every other type of shell.

I have done system admin for a long time and I've gotten tired of having to look up commands on different types of linux for things I don't often use. This handy little script translates a natural language prompt into commands for my terminal and shows me the output as if I were just entering the right commands. I just tell bashir what I want it to do or ask it what I want to know about the system, and it will put together a bash script, run it and forward me the output as if it were the shell.

![Screenshot from 2023-07-10 20-35-40](https://github.com/newsbubbles/bashir/assets/1012779/923db62e-fa21-4635-8014-12c665c31313)

## Disclaimer
*Bashir uses gpt-3.5 by default and is an experimental script. Use caution when using bashir as it will perform superuser commands if needed.  I suggest testing capabilities within a VM or dedicated cloud instance.  Any damages, direct or indirect, real or perceived, implied or unexpected, that you may incur on your person or your devices while using bashir are not the responsibility of the author and by using bashir you are legally pardoning the author from any such claim of responsibility or damages.*

## Requirements
- OpenAI
- LangChain

## Install
```bash
pip install openai, langchain
```
If you haven't already added `OPENAI_API_KEY` to your environment this is a good time to do it.
```bash
export OPENAI_API_KEY={YOUR-API-KEY}
```
Replace `{YOUR-API-KEY}` with your OpenAI API Key.
If you want this to persist when you reboot your computer, make sure to add that line to the end of your ~/.bashrc file

## Usage
```bash
python bashir.py
```
When you run bashir, it will start out by asking you the `sudo` password.  This is in the case that you are going to ask bashir questions that will make it generate commands that need to use the superuser permissions level.  This is where I exercise using caution when asking it things.  It will write any bash script, so it might even be able to mess up your environment pretty bad if you aren't careful what you ask for.  I will work on putting more effort into security in future versions.

### If you have Alternate OS and shell environment
```bash
python bashir.py --os=Ubuntu22 --shell=sh
```
Assumed defaults are OS=RHEL9 and shell=bash.  These two variables go into the LLM's prompt so the format of OS name/version is not strict.

## How it Works
Bashir creates a `scripts` folder wherever you are running it.  In this folder it places a bash script. The bash script includes a comment with the original prompt and is assigned a unique identifier as it's name.  It is then chmodded to allow execution, and executed in a wrapped shell process.  Bashir uses pexpect to expect the prompt or a few other things and effectively wrap the bash shell within the python instance, so you get actual output from the embedded shell.

To exit bashir type `exit` at the prompt and hit `Enter`.

## To Be Added
- Human verification (on all scripts or only on ones that use "sudo" thus performing system changes)
- Properly changing the shell environment and using ".bat" scripts for windows as default if used as OS
- Some way to properly forward output on long running processes with pexpect

## Examples
In these examples, the bash script is shown and original prompt as a comment at the top followed by the bash commands that the LLM responded to the prompt with to be run

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
# Prompt> open a new terminal window
gnome-terminal
```
I am pretty sure this next one needs to be run using bashir as root or with `sudo python bashir.py`
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

## Limitations I've Found
There are probably way more I haven't found, but here are the ones so far:
- When outputting large lists of things like asking to list installed packages you shouldn't try to force it to use things like `more` or subcommands that pretty up the output.  It is fine to make it get a little creative and pipe to grep or something, but it is best if you want to actually read some long list, tell it in plain english to "output the list to a file named out.txt"
- There is still no really good way to handle longer running processes so things like etecting timeout and sending Ctrl+C to the process are not really that great of a solution. Currently I try to have it just every 10 seconds try to flush the output of the command to screen if process takes longer than that.

## Conclusion
It is pretty experimental but it was a quick script to put together and it seems like it will definitely help me set up EC2 instances on Amazon Linux, etc.

Let me know if you run into issues, I will actively check this project and make regular updates if people start using it.
