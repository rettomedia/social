# Retto Core Documentation

## Installation Instructions
To install Retto on your local machine, follow these steps:


1 - Clone the repository from GitHub:

```
git clone https://github.com/rettomedia/social.git
```

2 - Navigate to the project directory:

```
cd social
```

3 - Install a Pipenv environment:

```
pipenv install
```

4 - Activate environment:

```
pipenv shell
```

5 - Apply migrations:

```
python manage.py migrate
```

6 - Start the development server:

```
python manage.py runserver
```


## Project Structure
The Retto project follows the standard Django project structure. Here are the main components:

- `accounts`: Handles user authentication and profile management.
- `groups`: User groups and group events.
- `network`: Manages user posts and interactions.
- `posts`: User posts and post options.


## User Guide
For detailed instructions on how to use Retto, refer to the [User Guide](GUIDES/USER_GUIDE.md).


## Administrator Guide
For administrators managing the Retto platform, refer to the [Administrator Guide](GUIDES/ADMINISTRATOR_GUIDE.md).

API Documentation
The Retto API documentation can be found [here]().

## Development Guide
If you're a developer looking to contribute to Retto, check out the [Development Guide](GUIDES/DEVELOPMENT_GUIDE.md).

## Security and Privacy Policies
For information on how Retto handles security and user privacy, refer to Security and [Privacy Policies]().