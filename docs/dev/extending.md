# Extending the App

This document provides guidance on how to extend the Nautobot IGP Models app with additional functionality.

## Contributing Guidelines

Extending the application is welcome! However, it is best to open an issue first to ensure that a pull request would be accepted and makes sense in terms of features and design direction.

## Adding New IGP Protocols

To add support for a new IGP protocol (e.g., EIGRP, RIP, BGP):

1. **Create Protocol Configuration Model**: Add a new model inheriting from `PrimaryModel` that includes:
   - A foreign key to `IGPRoutingInstance`
   - Protocol-specific configuration fields
   - Appropriate validators and constraints

2. **Create Interface Configuration Model**: Add a corresponding interface configuration model with:
   - Foreign key to your protocol configuration model
   - Foreign key to `Interface` model
   - Interface-level protocol settings

3. **Add API Components**:
   - Serializer in `api/serializers.py`
   - ViewSet in `api/views.py`
   - URL patterns in `api/urls.py`

4. **Add UI Components**:
   - Form class in `forms.py`
   - Filter class in `filters.py`
   - Table class in `tables.py`
   - Views in `views.py`
   - Templates in `templates/nautobot_igp_models/`

5. **Update Navigation**: Add navigation menu items in `navigation.py`

6. **Write Tests**: Add comprehensive test coverage:
   - Model tests
   - Form tests
   - Filter tests
   - API tests
   - View tests

## Extending Existing Models

If you need to add fields to existing models:

1. Update the model in `models.py`
2. Create a migration: `nautobot-server makemigrations nautobot_igp_models`
3. Update forms, filters, and serializers accordingly
4. Add tests for the new functionality
5. Update documentation

## Adding Custom Validation

Custom validation can be added at multiple levels:

- **Model Level**: Override the `clean()` method in your model
- **Form Level**: Add validation in form's `clean()` or `clean_<fieldname>()` methods
- **Serializer Level**: Add validation in serializer's `validate()` or `validate_<fieldname>()` methods

## Adding Management Commands

To add custom management commands:

1. Create a new file in `nautobot_igp_models/management/commands/`
2. Inherit from `BaseCommand`
3. Implement the `handle()` method
4. Document the command usage

## Integration Points

The app provides several integration points:

- **Signals**: The app emits Django signals on model changes that can be used for integration
- **REST API**: All models are exposed via REST API for external integrations
- **GraphQL**: Models can be accessed via Nautobot's GraphQL interface
- **Custom Scripts/Jobs**: Create Nautobot Jobs that interact with IGP models

## Best Practices

- Follow the existing code style and patterns
- Write comprehensive tests for all new functionality
- Update documentation for user-facing changes
- Use type hints where appropriate
- Validate data at multiple levels (model, form, serializer)
- Consider backwards compatibility when making changes
