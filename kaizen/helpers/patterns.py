ignore_patterns = [
    # Version Control System files
    r"\.git/",
    r"\.svn/",
    r"\.hg/",
    # Dependency directories
    r"node_modules/",
    r"venv/",
    r"env/",
    r"\.virtualenv/",
    r"vendor/",
    # Build and compiled files
    r".*\.pyc$",
    r".*\.pyo$",
    r".*\.class$",
    r".*\.o$",
    r".*\.so$",
    r".*\.dll$",
    r".*\.exe$",
    r".*\.bin$",
    r"dist/",
    r"build/",
    # IDE and editor-specific files
    r"\.vscode/",
    r"\.idea/",
    r".*\.swp$",
    r".*\.swo$",
    r".*\.sublime-.*",
    r"\.DS_Store",
    # Log files
    r".*\.log$",
    r"logs/",
    # Cache directories
    r"__pycache__/",
    r"\.cache/",
    # Configuration files that might contain sensitive information
    r".*\.env",
    r"\.env\..*",
    r"config\.json",
    r"secrets\.yaml",
    # Data files
    r".*\.csv$",
    r".*\.json$",
    r".*\.xml$",
    r".*\.sql$",
    # Documentation files
    r".*\.md$",
    r".*\.rst$",
    r".*\.txt$",
    r"docs/",
    # Package manager files
    r"package-lock\.json",
    r"yarn\.lock",
    r"Pipfile\.lock",
    # Test coverage reports
    r"coverage/",
    r"\.coverage",
    # Temporary files
    r".*\.tmp$",
    r".*\.bak$",
    r".*\.swp$",
    r".*~$",
    # Media files
    r".*\.jpg$",
    r".*\.jpeg$",
    r".*\.png$",
    r".*\.gif$",
    r".*\.svg$",
    r".*\.mp3$",
    r".*\.mp4$",
    # Compiled documentation
    r"site/",
    r"_build/",
    # Deployment-specific files
    r"Dockerfile",
    r"docker-compose\.yml",
    r".*\.dockerfile",
    # Minified JavaScript files
    r".*\.min\.js$",
]
