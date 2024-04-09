## Github App Setup

This is a short guide to how to setup your github app:

#### Step 1: Registering Your GitHub App
- Go to GitHub and click on your profile photo in the upper-right corner of any page.
- Navigate to your account settings.
- Click on "Developer settings" in the left sidebar.
- Select "GitHub Apps" and then click "New GitHub App".
- Fill in the necessary details for your app:
  - "GitHub App name": Enter a name for your app.
  - "Homepage URL": Enter a URL for your app, such as the repository URL where your app's code will be stored.
  - Under "Webhook", make sure "Active" is selected.
  - Enter your "Webhook URL", which is the server URL where the webhook requests will be sent.
  - Optionally, enter a "Webhook secret", a random string that will be used to validate that incoming requests are from GitHub

#### Step 2: Setting Permissions and Events
- In the sidebar, click "Permissions & events".
- Under "Repository permissions", "Organization permissions", and "Account permissions", select the permissions your app will need.
    - Repository Content
    - Pull Request
    - Metadata
    - Check Runs
- Under "Subscribe to Events", select the webhook events you want your GitHub App to receive, such as "Pull request" if you want to respond to pull request events

