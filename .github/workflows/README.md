# GitHub Actions Workflows Documentation

This directory contains GitHub Actions workflows for the NLP Part of Speech Tagging project. The workflows provide comprehensive CI/CD pipeline including testing, security scanning, code quality checks, and documentation generation.

## Workflows Overview

### 1. CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual dispatch via GitHub UI

**Jobs:**

#### Test Job
- **Matrix Strategy**: Tests across Python versions 3.8, 3.9, 3.10, and 3.11
- **System Dependencies**: Installs Graphviz for model visualization
- **Caching**: Implements pip dependency caching for faster builds
- **NLTK Data**: Downloads required Brown Corpus and universal tagset
- **Code Quality**: Runs flake8 linting and black formatting checks
- **Module Testing**: Validates Python module imports
- **Notebook Validation**: Executes Jupyter notebooks to ensure they run without errors
- **Artifacts**: Uploads notebook HTML outputs and test results using `actions/upload-artifact@v4`

#### Security Scan Job
- **Dependencies**: Runs after test job completion
- **Tools**: Uses `safety` and `bandit` for security vulnerability scanning
- **Reports**: Generates JSON reports for security findings
- **Artifacts**: Uploads security reports with 30-day retention

#### Code Quality Job
- **Tools**: Runs `pylint` and `mypy` for code quality and type checking
- **Reports**: Generates detailed quality reports
- **Artifacts**: Uploads quality reports for review

#### Documentation Job
- **Trigger**: Only runs on pushes to `main` branch
- **Output**: Converts Jupyter notebooks to HTML and PDF formats
- **Index Page**: Creates a documentation index page
- **Artifacts**: Uploads complete documentation with 90-day retention

### 2. Dependency Updates (`dependency-update.yml`)

**Triggers:**
- Weekly schedule (Mondays at 9 AM UTC)
- Manual dispatch via GitHub UI
- Pull request events (for dependency review)

**Jobs:**

#### Dependency Review Job
- **Trigger**: Only on pull request events
- **Tool**: Uses GitHub's dependency review action
- **Security**: Fails on moderate or higher severity vulnerabilities

#### Security Audit Job
- **Tools**: Uses `pip-audit` and `safety` for comprehensive security auditing
- **Reports**: Generates detailed security audit reports
- **Summary**: Creates human-readable security summaries
- **Artifacts**: Uploads audit results with 90-day retention

#### Update Dependencies Job
- **Automation**: Automatically updates dependencies using `pip-tools`
- **Pull Requests**: Creates automated PRs for dependency updates
- **Review Process**: Includes checklist for manual review and testing

## Key Features

### 🔧 Modern Actions Usage
- **Updated Artifacts**: Uses `actions/upload-artifact@v4` (fixes deprecated v3 issue)
- **Latest Actions**: All actions use current stable versions
- **Security**: Proper token handling and permissions

### 🧪 Comprehensive Testing
- **Multi-Python Support**: Tests across 4 Python versions
- **Notebook Execution**: Validates that Jupyter notebooks run successfully
- **Import Testing**: Ensures all Python modules import correctly
- **NLTK Integration**: Handles NLTK data downloads automatically

### 🔒 Security Focus
- **Vulnerability Scanning**: Multiple security tools (safety, bandit, pip-audit)
- **Dependency Review**: Automated review of dependency changes
- **Regular Audits**: Weekly security audits
- **Report Generation**: Detailed security reports with retention

### 📊 Code Quality
- **Linting**: flake8 for PEP 8 compliance
- **Formatting**: black for consistent code formatting
- **Type Checking**: mypy for static type analysis
- **Complexity Analysis**: pylint for code quality metrics

### 📚 Documentation
- **Automated Generation**: Converts notebooks to multiple formats
- **Web Interface**: Creates browsable documentation
- **Long Retention**: 90-day artifact retention for documentation

### ⚡ Performance Optimization
- **Caching**: Pip dependency caching across builds
- **Matrix Strategy**: Parallel execution across Python versions
- **Conditional Jobs**: Smart job execution based on conditions

## Artifact Management

### Artifact Types and Retention

| Artifact Type | Retention | Description |
|---------------|-----------|-------------|
| Notebooks | 30 days | HTML converted notebooks per Python version |
| Test Results | 7 days | Coverage reports and test outputs |
| Security Reports | 30-90 days | Vulnerability and audit reports |
| Code Quality | 30 days | Linting and type checking reports |
| Documentation | 90 days | Complete project documentation |

### Artifact Naming Convention
- `notebooks-python-{version}`: Notebook outputs for specific Python version
- `test-results-python-{version}`: Test results for specific Python version
- `security-reports`: Security scan results
- `security-audit-{run_number}`: Timestamped security audits
- `code-quality-reports`: Code quality analysis results
- `documentation`: Complete project documentation

## Configuration Details

### Environment Setup
```yaml
# Python versions tested
python-version: [3.8, 3.9, '3.10', '3.11']

# System dependencies
- graphviz graphviz-dev  # For model visualization

# Python dependencies
- pytest pytest-cov      # Testing framework
- flake8 black          # Code quality
- jupyter nbconvert     # Notebook processing
- safety bandit         # Security scanning
- pylint mypy          # Advanced code analysis
```

### Caching Strategy
```yaml
# Pip cache configuration
path: ~/.cache/pip
key: ${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('**/requirements.txt') }}
restore-keys: |
  ${{ runner.os }}-pip-${{ matrix.python-version }}-
  ${{ runner.os }}-pip-
```

## Troubleshooting

### Common Issues

1. **Notebook Execution Failures**
   - Check NLTK data downloads
   - Verify all dependencies are installed
   - Review notebook cell dependencies

2. **Security Scan Failures**
   - Review security reports in artifacts
   - Update vulnerable dependencies
   - Consider security exceptions for false positives

3. **Dependency Conflicts**
   - Check requirements.txt for version conflicts
   - Review dependency update PRs carefully
   - Test locally before merging

4. **Artifact Upload Issues**
   - Ensure using `actions/upload-artifact@v4`
   - Check file paths and permissions
   - Verify artifact naming conventions

### Debugging Steps

1. **Enable Debug Logging**
   ```yaml
   env:
     ACTIONS_STEP_DEBUG: true
     ACTIONS_RUNNER_DEBUG: true
   ```

2. **Manual Workflow Dispatch**
   - Use `workflow_dispatch` trigger for testing
   - Run individual jobs to isolate issues

3. **Local Testing**
   - Test notebook execution locally
   - Verify dependency installation
   - Run security scans manually

## Maintenance

### Regular Tasks
- Review weekly dependency update PRs
- Monitor security audit reports
- Update workflow actions to latest versions
- Review and update Python version matrix

### Quarterly Reviews
- Evaluate workflow performance and optimization opportunities
- Review artifact retention policies
- Update documentation and troubleshooting guides
- Assess new GitHub Actions features for integration

## Contributing

When modifying workflows:
1. Test changes in a feature branch first
2. Use `workflow_dispatch` for manual testing
3. Update documentation for any new features
4. Consider backward compatibility
5. Review security implications of changes

## Support

For workflow issues:
1. Check the Actions tab in GitHub for detailed logs
2. Review artifact contents for error details
3. Consult this documentation for troubleshooting
4. Create an issue with workflow logs and error details