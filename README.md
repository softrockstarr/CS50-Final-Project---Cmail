# Cmail - A CS50 Final Project

#### Video Demo:  [https://youtu.be/h4k6pW6AckA](https://youtu.be/h4k6pW6AckA)
#### Description:
Cmail is a simple web app built to mimic an email service such as Gmail, allowing users to create email accounts and send messages amongst themselves. Unlike a real email client that allows you to email real addresses, this project was built to practice working with SQL, so all the emails and user information is simply stored in a SQL database and populated when required throughout the app. Cmail's visuals are based on CS50's Finance PSET with some additional Bootstrap elements to make it responsive and give it a clean look.

## Technology used
- Python
- Flask
- SQL
- Jinja
- HTML/CSS
- Bootstrap

## Installation

If the CS50 [Codespace](https://code.cs50.io/) is available to you, simply download a copy of this app, drag it into your codespace, and run it with:

```bash
flask run
```

Otherwise, clone this repo and install all dependencies with:

```bash
pip install -r requirements.txt
```
..and then:

```bash
flask run
```

## Usage

After creating an account and logging in, your homepage will list all of the emails in your inbox. From there you can open emails to read them, or reply to them. When emails are sent, you will be redirected to a page displaying all of your sent emails. If you'd like to send an email of your own, hit "compose", sill in the fields and hit "send". You can create multiple accounts to send/receive emails between them, or log in with:

- username: cs50@email.com
- password: cs50

to look around an account already pre-populated with some emails.
