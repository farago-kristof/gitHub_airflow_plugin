.. gitHubAirflow documentation master file, created by
   sphinx-quickstart on Wed Jan 29 15:15:09 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

gitHubAirflow documentation
===========================

Streamline GitHub Workflow Automation with Apache Airflow
----------------------------------------------------------

The **GitHub Airflow Plugin** provides seamless integration between **Apache Airflow** and **GitHub**, enabling automated repository management, pull request operations, branch handling, and issue tracking—all within Airflow DAGs.

Core Operators
--------------

- **🔐 GitHubAuthOperator** – Handles authentication with GitHub, ensuring secure and efficient API interactions.
- **🔄 GitHubPullRequestOperator** – Retrieve information about open or closed PRs.
- **🌿 GitHubBranchesOperator** – Lists branches.
- **📜 GitHubCommitsOperator** – Retrieves commit data.
- **🐞 GitHubIssuesOperator** – Retrieves a list of issues.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
