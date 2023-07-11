# bashir
An LLM based Junior System Admin for Linux/Bash originally but also every other type of cli.

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

## If you have Alternate OS and shell environment
```bash
python bashir.py --os=Ubuntu22 --shell=sh
```
Assumed defaults are OS=RHEL9 and shell=bash.  These two variables go into the LLM's prompt so the format of OS name/version is not strict.

## How it Works
Bashir creates a `scripts` folder wherever you are running it.  In this folder it places a bash script. (yes, not currently working to change the actual shell, still a priority). The bash script includes a comment with the original prompt and is assigned a unique identifier as it's name.  It is then chmodded to allow execution, and executed in a wrapped shell process.  Bashir uses pexpect to expect the prompt and effectively wrap the bash shell within the python instance, so you get actual output from the embedded shell.

To exit bashir type `exit` at the prompt and hit `Enter`.

## To Be Added
- Human verification (on all scripts or only on ones that use "sudo" thus performing system changes)
- Properly changing the shell environment and using ".bat" scripts for windows as default if used as OS

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

## Conclusion
It is pretty experimental but it was a quick script to put together and it seems like it will definitely help me set up EC2 instances on Amazon Linux, etc.

Let me know if you run into issues, I will actively check this project and make regular updates if people start using it.
