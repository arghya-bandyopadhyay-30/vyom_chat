# Contribution Guide for Vyom Chatbot
_Thank you for considering contributing to Vyom Chatbot!_

Vyom is a personal assistant chatbot built to answer questions about Arghya Bandyopadhyay, utilizing a combination of Neo4j for knowledge graph 
management, Streamlit for the frontend interface, and a language model for intelligent query handling. 
We welcome contributions that help improve Vyom’s performance, add new features, fix bugs, and enhance user experience.

## Getting Started

To get started with contributing to Vyom, please follow these steps:
1. **Fork the Repository:** Visit the [Vyom repository](https://github.com/arghya-bandyopadhyay-30/vyom_chat.git) on GitHub and fork the project to your own GitHub account.
2. **Clone the Repository:** Clone your forked repository to your local machine using:
```shell
git clone https://github.com/<your-username>/vyom_my_bot.git
```
3. **Create a Branch:** Create a new branch for your contribution, following a naming convention such as `feature/new-feature-name` or `bugfix/fix-description`.
```shell
git checkout -b feature/your-feature
```
4. **Set Up Environment:** Set up a virtual environment and install the required dependencies:
```shell
conda create -p ./venv python==3.11 -y
conda activate
pip install -r requirements.txt
```
5. **Update Environment Files:** Create a copy of the `.env_template` file and rename it to `.env`. Update the credentials and API keys accordingly.

## Contribution Guidelines

We follow certain guidelines to maintain a clean and manageable codebase. Please make sure your contribution adheres to the following:

1. **Coding Standards:** Adhere to PEP8 standards for Python code. Ensure your code is clean, readable, and follows best practices for structure and naming conventions.


2. **Documentation:** Update the relevant documentation files if your changes affect them. This includes updating `README.md`, adding new configuration descriptions, or detailing new features.


3. **Commit Messages:** Write clear and concise commit messages that describe your changes. Use the following convention: `[Name] type. commit message` added sentiment analysis for blog responses.


4. **Pull Requests:** Once your branch is ready for review, push your changes to your fork and open a pull request against the `main` branch of the original repository. Provide a detailed description of your changes and mention any related issues.

## Areas to Contribute

1. **Bug Fixes:** Help us resolve existing bugs and improve stability.

2. **Feature Development:** You can contribute to building new features, such as enhancing the user experience in the chat UI or adding new integrations for sentiment analysis.

3. **Documentation:** Improve the existing documentation or create new ones to make it easier for others to use and understand Vyom.

4. **Code Refactoring:** Identify areas where code can be improved, simplified, or better organized for efficiency and maintainability.

## Need Help?

If you have any questions or need assistance, feel free to open an issue or reach out via the discussions section on the GitHub repository. We’re always here to help!

Thank you again for considering contributing to Vyom Chatbot! Every contribution makes a difference.

