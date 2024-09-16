DEFAULT_CONFIG = {
    "kaizen_api_key": None,
    "language_model": {
        "models": [
            {
                "model_name": "default",
                "litellm_params": {
                    "model": "azure/gpt-4o-mini",
                    "api_key": "os.environ/AZURE_API_KEY",
                    "api_base": "os.environ/AZURE_API_BASE",
                },
            },
        ]
    },
}
