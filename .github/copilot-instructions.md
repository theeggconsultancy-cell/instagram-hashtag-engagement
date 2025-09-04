# Instagram Hashtag Engagement - n8n Workflow

Instagram hashtag engagement workflow using n8n that surfaces high-quality posts for manual engagement with AI-drafted comment suggestions. This is a configuration-driven n8n workflow project with JSON configuration files and documentation.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and validate the repository:
- `python3 -m json.tool files/config/workflow-config.json` -- validates JSON syntax (takes <1 second)
- Create comprehensive validation script:
```bash
cat > /tmp/validate-workflow.py << 'EOF'
#!/usr/bin/env python3
import json, sys, re
from typing import Dict, Any

def validate_all(config_path="files/config/workflow-config.json"):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # JSON syntax check
        print("✓ JSON syntax valid")
        
        # Required sections
        required = ['version', 'workflow', 'hashtags', 'content_filtering', 'scoring', 'ai_comments', 'delivery', 'storage']
        for section in required:
            assert section in config, f"Missing section: {section}"
        print("✓ All required sections present")
        
        # Scoring weights sum to 1.0
        weights_sum = sum(config['scoring']['weights'].values())
        assert abs(weights_sum - 1.0) < 0.001, f"Weights sum to {weights_sum}, should be 1.0"
        print(f"✓ Scoring weights valid: {weights_sum}")
        
        # Cron schedule format
        schedule = config['workflow']['schedule']
        assert len(schedule.split()) == 5, f"Invalid cron format: {schedule}"
        print(f"✓ Cron schedule valid: {schedule}")
        
        # Value constraints
        assert config['hashtags']['daily_limit'] > 0, "daily_limit must be positive"
        assert config['content_filtering']['min_engagement_rate'] >= 0, "min_engagement_rate must be non-negative"
        assert config['ai_comments']['suggestions_per_post'] > 0, "suggestions_per_post must be positive"
        print("✓ Configuration constraints satisfied")
        
        print("\n✓ All validation checks passed!")
        return True
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if validate_all() else 1)
EOF
```
- `python3 /tmp/validate-workflow.py` -- comprehensive validation (takes <1 second)

### Run validation suite:
- `python3 /tmp/validate-workflow.py && echo "✓ Configuration ready for n8n deployment"` -- validates entire configuration
- `test -f README.md && test -f files/README.md && test -f files/docs/setup-guide.md && test -f files/config/workflow-config.json && echo "✓ All required files present"` -- structure validation
- All validation commands complete in under 1 second

### Manual validation scenarios:
Since this is an n8n workflow project, validation focuses on configuration correctness rather than running applications:
1. **Configuration validation**: Ensure JSON is syntactically correct and semantically valid
2. **Documentation validation**: Verify all setup steps are documented and URLs are valid
3. **Schema validation**: Confirm all required configuration sections are present with valid values
4. **Deployment readiness**: Check that configuration can be imported into n8n

## Validation

Always run the comprehensive validation after making configuration changes:
- ALWAYS run `python3 /tmp/validate-workflow.py` after editing `files/config/workflow-config.json`
- ALWAYS verify documentation changes don't break setup instructions
- You cannot run the actual n8n workflow locally, but you can validate the configuration is deployment-ready
- For testing the actual workflow, it must be deployed to n8n Cloud or self-hosted n8n instance

## Common tasks

### Repository structure
```
./README.md                           - Project overview (185 bytes)
./files/README.md                     - Detailed project description
./files/config/workflow-config.json   - n8n workflow configuration (JSON)
./files/docs/setup-guide.md          - Complete setup instructions
```

### Configuration file schema
`files/config/workflow-config.json` contains:
- `version`: Configuration version
- `workflow`: Schedule and basic settings
- `hashtags`: Hashtag rotation and limits
- `content_filtering`: Post filtering criteria
- `scoring`: Weighted scoring algorithm configuration
- `ai_comments`: OpenAI integration settings
- `delivery`: Telegram/Slack delivery settings
- `storage`: Google Sheets storage configuration

### Key validation commands
All validation commands complete in under 1 second:

1. **JSON syntax check**:
```bash
python3 -m json.tool files/config/workflow-config.json > /dev/null && echo "✓ JSON valid" || echo "✗ JSON invalid"
```

2. **Scoring weights validation**:
```bash
python3 -c "import json; config=json.load(open('files/config/workflow-config.json')); print(f'Weights sum: {sum(config[\"scoring\"][\"weights\"].values())}')"
```

3. **Configuration completeness**:
```bash
python3 /tmp/validate-workflow.py
```

### Working with this repository
- **No build process**: This is a configuration repository, not a traditional codebase
- **No dependencies to install**: Uses standard tools (Python 3, curl, jq)
- **No tests to run**: Validation scripts serve as "tests" for configuration
- **No server to start**: The workflow runs in n8n, not locally
- **JSON linting**: Use `python3 -m json.tool` for formatting and validation
- **Documentation editing**: Standard markdown editing, validate links manually

### External dependencies and APIs referenced
- Meta Graph API (https://graph.facebook.com/) - for Instagram data
- OpenAI API - for comment generation
- Google Sheets API - for data storage
- Telegram Bot API or Slack API - for notifications
- n8n Cloud or self-hosted - for workflow execution

### Deployment validation
To validate deployment readiness:
1. Run all validation commands listed above
2. Verify all external API credentials are available
3. Confirm Google Sheets are created per setup guide
4. Test API access tokens have correct permissions
5. Import configuration into n8n and verify no import errors

### Common file operations
- **Edit configuration**: Modify `files/config/workflow-config.json`, then run `python3 /tmp/validate-workflow.py`
- **Update documentation**: Edit markdown files in `files/docs/` or root `README.md`
- **Add new settings**: Update JSON schema in configuration file, update validation script if needed
- **Version control**: All changes should be committed; no build artifacts to ignore

### Troubleshooting
- **JSON syntax errors**: Use `python3 -m json.tool files/config/workflow-config.json` to identify issues
- **Validation failures**: Run comprehensive validation script for detailed error messages
- **Documentation links**: Some external URLs may not be accessible due to network restrictions
- **n8n import errors**: Ensure JSON structure matches n8n workflow schema requirements