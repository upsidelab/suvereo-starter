# Replaces Suvereo's pecl/settings_override.py inside the image.
# Register your domain definitions, agents, integrations and entities here.

INSTALLED_DOMAIN_DEFINITIONS = ["diet_advice_domain"]

AVAILABLE_AGENTS = [
    "diet_advice_domain.nutrition_agent.NutritionAssistantAgent",
]
AVAILABLE_AGENTIC_EXECUTION_DEFINITIONS = [
    "diet_advice_domain.nutrition_agent.WeeklyMealPlanExecutionDefinition",
]

CATALOG_LANGUAGE_MODEL_PROVIDERS = [
    "suvereo_model_openai.OpenAILanguageModelProvider",
]

CATALOG_INTEGRATION_PLUGINS = [
    "diet_advice_domain.sources.SampleRecipeSource",
    "diet_advice_domain.sources.MealDbRecipeSource",
    "diet_advice_domain.sources.SampleUserSource",
]
CATALOG_INTEGRATION_MANAGERS = [
    "diet_advice_domain.sync.RecipeSourceManager",
    "diet_advice_domain.sync.UserSourceManager",
]
CATALOG_ENTITY_PLUGINS = [
    "diet_advice_domain.models.Recipe",
    "diet_advice_domain.models.UserProfile",
]
