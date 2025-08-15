# GitHub Actions Documentation

This document provides comprehensive documentation for the GitHub Actions workflows implemented in this NLP Part of Speech Tagging project.

## Overview

The project includes four main GitHub Actions workflows that provide comprehensive CI/CD coverage:

1. **Continuous Integration (CI)** - Main testing and validation pipeline
2. **Security Scanning** - Security vulnerability detection and analysis
3. **Documentation** - Documentation building and deployment
4. **Release Management** - Automated release creation and package publishing

## Workflows Detail

### 1. Continuous Integration (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

#### Test Job
- **Purpose**: Run comprehensive tests across multiple Python versions and operating systems
- **Matrix Strategy**: 
  - Python versions: 3.8, 3.9, 3.10, 3.11
  - Operating systems: Ubuntu, Windows, macOS
  - Optimized to exclude some combinations for efficiency
- **Steps**:
  1. Install system dependencies (Graphviz for visualization)
  2. Set up Python environment with caching
  3. Install project dependencies
  4. Download required NLTK data
  5. Run tests with coverage reporting
  6. Upload coverage to Codecov (Ubuntu + Python 3.9 only)

#### Lint Job
- **Purpose**: Ensure code quality and consistent formatting
- **Tools**:
  - **Black**: Code formatting validation
  - **isort**: Import sorting validation
  - **flake8**: Code linting and style checking
- **Failure Conditions**: Syntax errors, undefined names, formatting issues

#### Notebook Validation Job
- **Purpose**: Validate Jupyter notebooks execute without errors
- **Process**:
  1. Execute notebooks with timeout protection
  2. Convert to HTML for artifact storage
  3. Upload executed notebooks as artifacts
- **Timeout Settings**:
  - HMM notebook: 600 seconds (10 minutes)
  - Data download notebook: 300 seconds (5 minutes)

#### Data Validation Job
- **Purpose**: Ensure data file integrity and format correctness
- **Validations**:
  - File existence checks
  - Universal tagset validation
  - Brown corpus format verification
  - File size sanity checks

### 2. Security Scanning (`security.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Weekly scheduled runs (Mondays at 9 AM UTC)

**Jobs:**

#### Dependency Scan Job
- **Tools**:
  - **Safety**: Known vulnerability database checking
  - **Bandit**: Python security linter
- **Outputs**: JSON reports uploaded as artifacts
- **Non-blocking**: Continues on security findings for reporting

#### CodeQL Analysis Job
- **Purpose**: Advanced semantic code analysis
- **Features**:
  - Security-focused query sets
  - Quality analysis
  - GitHub Security tab integration
- **Permissions**: Requires security-events write access

#### Dependency Review Job
- **Purpose**: Review dependency changes in pull requests
- **Scope**: Only runs on pull requests
- **Thresholds**: Fails on moderate or higher severity issues
- **License Checking**: Validates against approved license list

### 3. Documentation (`documentation.yml`)

**Triggers:**
- Push to `main` branch
- Pull requests to `main` branch

**Jobs:**

#### Build Documentation Job
- **Components**:
  - **Sphinx API Documentation**: Auto-generated from docstrings
  - **Notebook Conversion**: Jupyter notebooks to Markdown
  - **Project Documentation**: Installation, usage guides
- **Output**: Complete documentation site ready for deployment

#### Deploy Documentation Job
- **Condition**: Only on main branch pushes
- **Target**: GitHub Pages deployment
- **Dependencies**: Requires successful documentation build

#### Validate README Job
- **Tools**:
  - **markdownlint**: Markdown formatting validation
  - **markdown-link-check**: Broken link detection
- **Content Validation**: Ensures required sections exist

### 4. Release Management (`release.yml`)

**Triggers:**
- Git tags matching `v*` pattern (e.g., `v1.0.0`)
- Manual workflow dispatch with version input

**Jobs:**

#### Create Release Job
- **Pre-release Validation**:
  - Full test suite execution
  - Notebook execution validation
  - Artifact generation
- **Release Artifacts**:
  - Source code archive
  - Executed notebooks (HTML)
  - Documentation files
  - Changelog generation

#### Publish Package Job
- **Condition**: Only for version tags
- **Process**:
  - Dynamic `setup.py` generation
  - Package building and validation
  - Test PyPI publication
  - Optional PyPI publication (commented out)

#### Docker Build Job
- **Features**:
  - Multi-architecture builds (AMD64, ARM64)
  - Jupyter notebook server setup
  - Non-root user configuration
  - Build caching for efficiency

## Configuration Files

### Code Quality Configuration

#### `.flake8`
```ini
[flake8]
max-line-length = 127
max-complexity = 10
exclude = .git, __pycache__, .pytest_cache, .venv, build, dist
ignore = E203, E501, W503, W504
```

#### `pyproject.toml`
- **Black**: Line length 127, Python 3.8+ compatibility
- **isort**: Black-compatible profile
- **pytest**: Test discovery and execution configuration
- **coverage**: Coverage reporting settings

#### `.markdownlint.json`
- Markdown formatting rules
- Line length: 120 characters
- ATX-style headers required

#### `.markdown-link-check.json`
- Link validation configuration
- Timeout and retry settings
- Pattern exclusions for localhost

## Usage Instructions

### Setting Up the Repository

1. **Required Secrets** (for full functionality):
   ```
   CODECOV_TOKEN          # For coverage reporting
   TEST_PYPI_API_TOKEN    # For test package publishing
   PYPI_API_TOKEN         # For production package publishing
   DOCKER_USERNAME        # For Docker Hub publishing
   DOCKER_PASSWORD        # For Docker Hub publishing
   ```

2. **Branch Protection Rules** (recommended):
   - Require status checks: `Test`, `Code Quality`, `Validate Jupyter Notebooks`
   - Require up-to-date branches
   - Require linear history

### Development Workflow

1. **Feature Development**:
   ```bash
   git checkout -b feature/new-feature
   # Make changes
   git push origin feature/new-feature
   # Create pull request
   ```

2. **Pre-commit Validation** (local):
   ```bash
   # Format code
   black .
   isort .
   
   # Run tests
   pytest test_helpers.py -v --cov=helpers
   
   # Lint code
   flake8 .
   ```

3. **Release Process**:
   ```bash
   # Create and push tag
   git tag v1.0.0
   git push origin v1.0.0
   
   # GitHub Actions will automatically:
   # - Run full test suite
   # - Create GitHub release
   # - Build and publish packages
   # - Build Docker images
   ```

### Monitoring and Maintenance

#### Workflow Status Monitoring
- **GitHub Actions Tab**: Monitor all workflow runs
- **Status Badges**: Add to README for visibility
- **Notifications**: Configure for failed runs

#### Security Monitoring
- **Security Tab**: Review CodeQL findings
- **Dependabot**: Enable for automated dependency updates
- **Weekly Reports**: Review security scan results

#### Documentation Updates
- **Automatic Deployment**: Documentation updates on main branch pushes
- **GitHub Pages**: Accessible at `https://username.github.io/repository-name`
- **API Documentation**: Auto-generated from code docstrings

## Troubleshooting

### Common Issues

#### Test Failures
```bash
# Local debugging
pytest test_helpers.py -v -s --tb=long

# Check specific test
pytest test_helpers.py::TestClassName::test_method_name -v
```

#### Dependency Issues
```bash
# Update requirements
pip-compile requirements.in

# Check for conflicts
pip check
```

#### Notebook Execution Failures
```bash
# Test notebook locally
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb
```

#### Security Scan Failures
```bash
# Local security check
safety check
bandit -r . -ll
```

### Performance Optimization

#### Workflow Optimization
- **Caching**: Python dependencies cached automatically
- **Matrix Exclusions**: Reduce unnecessary test combinations
- **Conditional Jobs**: Skip jobs when not needed
- **Parallel Execution**: Jobs run concurrently when possible

#### Resource Management
- **Timeout Settings**: Prevent hanging workflows
- **Artifact Cleanup**: Automatic cleanup after retention period
- **Build Caching**: Docker layer caching for faster builds

## Best Practices

### Code Quality
1. **Consistent Formatting**: Use Black and isort
2. **Type Hints**: Add type annotations for better code quality
3. **Documentation**: Maintain comprehensive docstrings
4. **Testing**: Aim for >80% code coverage

### Security
1. **Dependency Updates**: Regular security updates
2. **Secret Management**: Use GitHub Secrets for sensitive data
3. **Least Privilege**: Minimal required permissions
4. **Regular Scans**: Weekly automated security scans

### Documentation
1. **Keep Updated**: Documentation should match code changes
2. **Examples**: Include practical usage examples
3. **API Documentation**: Auto-generate from docstrings
4. **User Guides**: Provide clear installation and usage instructions

### Release Management
1. **Semantic Versioning**: Use semver for version numbers
2. **Changelog**: Maintain detailed change logs
3. **Testing**: Comprehensive testing before releases
4. **Rollback Plan**: Ability to revert problematic releases

## Integration with Development Tools

### IDE Integration
- **VS Code**: Use Python extension with Black, isort, flake8
- **PyCharm**: Configure code style to match project settings
- **Pre-commit Hooks**: Install for automatic validation

### Local Development
```bash
# Install development dependencies
pip install -r requirements.txt

# Set up pre-commit hooks
pre-commit install

# Run quality checks
make lint  # If Makefile provided
```

This comprehensive GitHub Actions setup provides enterprise-grade CI/CD capabilities for the NLP project, ensuring code quality, security, and reliable releases while maintaining developer productivity.