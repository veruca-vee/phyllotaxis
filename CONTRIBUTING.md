# Contributing to Phyllotaxis

Thank you for your interest in contributing to Phyllotaxis! We welcome contributions from everyone.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How to Contribute](#-how-to-contribute)
- [Development Setup](#-development-setup)
- [Pull Request Guidelines](#-pull-request-guidelines)
- [Commit Message Conventions](#-commit-message-conventions)
- [Coding Standards](#-coding-standards)
- [Reporting Issues](#-reporting-issues)
- [Feature Requests](#-feature-requests)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🌟 How to Contribute

### Reporting Bugs

- Use the GitHub [Issues](https://github.com/veruca-vee/phyllotaxis/issues) page
- Include clear steps to reproduce
- Provide screenshots if possible
- Specify device, browser, and OS version

### Suggesting Features

- Open a new issue with the "enhancement" label
- Describe the feature and its use case
- Include mockups or examples if helpful

### Submitting Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚙️ Development Setup

### Prerequisites

- Node.js (v18+ recommended)
- npm (v9+ recommended)
- Git
- A code editor (VS Code, Sublime, etc.)

### Installation

```bash
# Clone the repository
git clone https://github.com/veruca-vee/phyllotaxis.git
cd phyllotaxis

# Install dependencies (if any)
npm install
```

### Running the Project

```bash
# Start a local development server
python3 -m http.server 8000
# or
npx serve

# Open in browser
# http://localhost:8000
```

### Building Android APK

```bash
# Install Cordova
npm install -g cordova

# Add Android platform
cordova platform add android

# Build debug APK
cordova build android

# Build release APK (requires signing)
cordova build android --release
```

## 📝 Pull Request Guidelines

### Before Submitting

- [ ] Read the [README](README.md)
- [ ] Read the [Code of Conduct](CODE_OF_CONDUCT.md)
- [ ] Test your changes on multiple devices/browsers
- [ ] Update relevant documentation
- [ ] Ensure code follows the project's coding standards

### Pull Request Template

```markdown
## Description

[Clear description of the changes]

## Related Issues

[List any related issues, e.g., Closes #123]

## Changes Made

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing

[Describe how you tested your changes]

## Screenshots

[Add screenshots if applicable]

## Checklist

- [ ] Code follows the project's coding standards
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Changes are backward compatible
```

## 📝 Commit Message Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

### Format

```
type(scope): subject

body

footer
```

### Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Changes that do not affect the meaning of the code |
| `refactor` | A code change that neither fixes a bug nor adds a feature |
| `perf` | A code change that improves performance |
| `test` | Adding missing tests |
| `chore` | Changes to the build process or auxiliary tools |
| `revert` | Reverts a previous commit |

### Examples

```bash
# Good commit messages
feat: add rainbow color mode
fix(mobile): prevent scrolling on canvas
docs: update README with APK instructions
perf: reduce point count on mobile devices
refactor: extract color mode logic to separate function

# Bad commit messages
fixed bug
added new feature
update
```

## 💻 Coding Standards

### JavaScript

- Use ES6+ syntax
- Use `const` and `let` instead of `var`
- Use template literals for strings
- Use arrow functions where appropriate
- Follow the existing code style

### HTML

- Use semantic HTML5 elements
- Proper indentation (2 or 4 spaces)
- Self-closing tags where appropriate
- Accessible markup (alt text, ARIA attributes)

### CSS

- Use lowercase for all selectors
- Use shorthand properties where possible
- Avoid `!important` unless absolutely necessary
- Use relative units (em, rem, %) for responsive design

### File Structure

- Use lowercase filenames with hyphens (e.g., `color-modes.js`)
- Keep related files in appropriate directories
- Use meaningful, descriptive names

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: How to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**:
   - Device type (mobile, tablet, desktop)
   - OS version
   - Browser and version
   - App version (if applicable)
6. **Screenshots/Video**: Visual evidence of the issue

## 💡 Feature Requests

When requesting features, please include:

1. **Description**: Clear description of the feature
2. **Use Case**: Why this feature is needed
3. **Examples**: Any examples or references
4. **Mockups**: Visual mockups if applicable

## 📄 Additional Notes

### Code Reviews

All contributions will be reviewed. Please be patient and responsive to feedback.

### License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

### Recognition

All meaningful contributions will be recognized in the project's contributors list.

---

Thank you for contributing to Phyllotaxis! Your help makes this project better for everyone.
