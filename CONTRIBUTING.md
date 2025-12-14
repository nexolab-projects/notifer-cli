# Contributing to Notifer CLI

Thank you for your interest in contributing to Notifer CLI!

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/notifer-cli.git
   cd notifer-cli
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install in development mode:
   ```bash
   pip install -e .
   ```

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Keep functions focused and small

### Testing Changes

Before submitting a PR, test your changes:

```bash
# Test basic commands
notifer --version
notifer --help
notifer config show

# Test against local server (if available)
notifer config set server http://localhost:8080
notifer publish test-topic "Test message"
```

## Submitting Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a Pull Request

## Commit Message Format

We use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## Reporting Issues

When reporting issues, please include:

- CLI version (`notifer --version`)
- Python version (`python --version`)
- Operating system
- Steps to reproduce
- Expected vs actual behavior

## Questions?

Feel free to open an issue for any questions or suggestions.
