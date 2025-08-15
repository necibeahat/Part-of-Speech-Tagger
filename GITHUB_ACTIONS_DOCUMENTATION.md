# GitHub Actions Documentation

This document provides comprehensive documentation for the GitHub Actions workflows implemented in this Part-of-Speech Tagger project.

## Overview

The project uses GitHub Actions for continuous integration, documentation validation, security scanning, and automated releases. The workflows are designed to ensure code quality, documentation standards, and security best practices.

## Workflows

### 1. Documentation Validation (`documentation.yml`)

**Purpose**: Validates README.md and project documentation for quality and completeness.

**Triggers**:
- Push to `main` or `master` branches
- Pull requests to `main` or `master` branches
- Manual workflow dispatch

**Jobs**:
- **Markdown Linting**: Uses `markdownlint-cli` to check markdown formatting
- **Link Checking**: Uses `markdown-link-check` to verify external links
- **Section Validation**: Ensures README contains required sections

**Configuration Files**:
- `.markdownlint.json`: Markdown linting rules
- `.markdown-link-check.json`: Link checking configuration

**Key Features**:
- Runs on Ubuntu 24.04 (matching the provided logs)
- Uses `|| true` to prevent workflow failure on linting issues (warnings only)
- Validates presence of: introduction, installation, usage, data, method sections

### 2. Python CI (`python-ci.yml`)

**Purpose**: Continuous integration for Python code quality and testing.

**Triggers**:
- Push to `main` or `master` branches
- Pull requests to `main` or `master` branches
- Manual workflow dispatch

**Matrix Strategy**: Tests against Python versions 3.8, 3.9, 3.10, and 3.11

**Jobs**:
- **Code Linting**: Uses `flake8` for Python code analysis
- **Code Formatting**: Uses `black` for code formatting validation
- **Import Sorting**: Uses `isort` for import organization
- **Testing**: Runs `pytest` with coverage reporting
- **Auto-test Creation**: Creates basic tests if none exist

**Key Features**:
- Pip caching for faster builds
- Automatic test generation for basic validation
- Code coverage reporting with Codecov integration
- Comprehensive Python code quality checks

### 3. Security Scanning (`security.yml`)

**Purpose**: Automated security vulnerability scanning for dependencies and code.

**Triggers**:
- Push to `main` or `master` branches
- Pull requests to `main` or `master` branches
- Weekly scheduled scan (Sundays at 2 AM UTC)
- Manual workflow dispatch

**Jobs**:
- **Dependency Scan**: Uses `safety` to check for known vulnerabilities in Python packages
- **Code Scan**: Uses GitHub's CodeQL for static code analysis

**Key Features**:
- Scheduled weekly security scans
- Artifact upload for security reports
- Integration with GitHub Security tab
- Non-blocking security checks (warnings only)

### 4. Release Management (`release.yml`)

**Purpose**: Automated release creation and artifact generation.

**Triggers**:
- Push of version tags (e.g., `v1.0.0`)
- Manual workflow dispatch with version input

**Jobs**:
- **Changelog Generation**: Automatically generates changelog from git commits
- **Archive Creation**: Creates source code archives (zip and tar.gz)
- **Release Creation**: Creates GitHub release with assets

**Key Features**:
- Automatic changelog generation
- Clean source code archives
- GitHub release integration
- Support for both tag-triggered and manual releases

## Configuration Files

### `.markdownlint.json`

Configures markdown linting rules:
- Line length limit: 120 characters
- Heading spacing requirements
- List formatting standards
- Code block language specification
- Strong text style preferences (asterisk over underscore)

### `.markdown-link-check.json`

Configures link checking behavior:
- Timeout settings (20 seconds)
- Retry configuration for rate-limited requests
- HTTP headers for GitHub compatibility
- Acceptable status codes (including redirects)
- Pattern ignoring for localhost URLs

## Workflow Status and Monitoring

### Status Badges

Add these badges to your README.md to display workflow status:

```markdown
![Documentation](https://github.com/necibeahat/Part-of-Speech-Tagger/workflows/Validate%20README%20and%20Documentation/badge.svg)
![Python CI](https://github.com/necibeahat/Part-of-Speech-Tagger/workflows/Python%20CI/badge.svg)
![Security Scan](https://github.com/necibeahat/Part-of-Speech-Tagger/workflows/Security%20Scan/badge.svg)
```

### Monitoring and Notifications

- **Failed Workflows**: Check the Actions tab for detailed logs
- **Security Alerts**: Review the Security tab for vulnerability reports
- **Coverage Reports**: View coverage trends in Codecov (if configured)

## Best Practices

### For Contributors

1. **Before Committing**:
   - Run `markdownlint README.md` locally
   - Check that README includes all required sections
   - Ensure Python code follows PEP 8 standards

2. **Pull Request Guidelines**:
   - All workflows must pass before merging
   - Address any linting or security warnings
   - Update documentation if adding new features

3. **Release Process**:
   - Create version tags following semantic versioning (e.g., `v1.0.0`)
   - Releases are automatically created from tags
   - Manual releases can be triggered via workflow dispatch

### For Maintainers

1. **Workflow Maintenance**:
   - Review and update Python versions in matrix strategy annually
   - Update action versions when security updates are available
   - Monitor workflow performance and optimize as needed

2. **Security Management**:
   - Review weekly security scan reports
   - Update dependencies when vulnerabilities are found
   - Configure branch protection rules to require workflow success

3. **Documentation Standards**:
   - Ensure README.md remains comprehensive and up-to-date
   - Update workflow documentation when making changes
   - Maintain consistent markdown formatting across all documentation

## Troubleshooting

### Common Issues

1. **Markdown Linting Failures**:
   - Check line length (max 120 characters)
   - Ensure proper heading spacing
   - Verify list formatting and indentation

2. **Link Check Failures**:
   - Verify external URLs are accessible
   - Check for typos in link syntax
   - Review timeout settings for slow-responding sites

3. **Python CI Failures**:
   - Ensure all dependencies are listed in requirements.txt
   - Check for Python syntax errors
   - Verify import statements and module availability

4. **Security Scan Issues**:
   - Review dependency versions for known vulnerabilities
   - Update packages to secure versions
   - Check CodeQL alerts for potential security issues

### Getting Help

- **Workflow Logs**: Check the Actions tab for detailed execution logs
- **GitHub Documentation**: Refer to [GitHub Actions documentation](https://docs.github.com/en/actions)
- **Tool Documentation**: 
  - [markdownlint](https://github.com/DavidAnson/markdownlint)
  - [markdown-link-check](https://github.com/tcort/markdown-link-check)
  - [flake8](https://flake8.pycqa.org/)
  - [black](https://black.readthedocs.io/)
  - [safety](https://pyup.io/safety/)

## Customization

### Modifying Workflows

1. **Adding New Checks**: Edit workflow files in `.github/workflows/`
2. **Changing Triggers**: Modify the `on:` section of workflow files
3. **Updating Configurations**: Edit configuration files in the project root
4. **Adding Secrets**: Use repository settings to add sensitive configuration

### Environment-Specific Settings

- **Branch Names**: Update branch references if using different default branches
- **Python Versions**: Modify the matrix strategy in `python-ci.yml`
- **Security Scanning**: Adjust scan frequency in `security.yml`
- **Release Patterns**: Modify tag patterns in `release.yml`

## Performance Optimization

### Caching Strategies

- **Python Dependencies**: Pip caching is enabled in Python workflows
- **Node.js Dependencies**: Consider adding npm caching for documentation tools
- **Action Caching**: Leverage GitHub's action caching for repeated operations

### Resource Management

- **Concurrent Jobs**: Workflows run jobs in parallel where possible
- **Matrix Builds**: Python CI uses matrix strategy for efficient multi-version testing
- **Conditional Execution**: Some steps only run under specific conditions

## Integration with Development Workflow

### Branch Protection

Recommended branch protection rules:
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Include administrators in restrictions
- Require review from code owners

### Automated Dependency Updates

Consider integrating with:
- **Dependabot**: For automated dependency updates
- **Renovate**: For more advanced dependency management
- **Snyk**: For enhanced security monitoring

This documentation should be updated whenever workflows are modified or new automation is added to the project.