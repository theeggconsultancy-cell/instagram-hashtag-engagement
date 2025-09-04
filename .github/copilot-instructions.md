# Instagram Hashtag Engagement - n8n Workflow Project

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

This is a human-in-the-loop Instagram hashtag engagement workflow using n8n that surfaces high-quality posts for manual engagement with AI-drafted comment suggestions. This is NOT a traditional code project - it is a configuration-based workflow project using external services.

## Working Effectively

### Project Structure Validation
- Validate repository structure and files:
  ```bash
  cd /home/runner/work/instagram-hashtag-engagement/instagram-hashtag-engagement
  ls -la  # Should show: .git, README.md, files/
  ls -la files/  # Should show: README.md, config/, docs/
  ```
- Validate JSON configuration:
  ```bash
  python3 -m json.tool files/config/workflow-config.json > /dev/null && echo "✓ Configuration JSON is valid"
  ```

### Configuration Validation Script
- ALWAYS run this validation script when modifying workflow-config.json:
  ```bash
  python3 -c "
import json
with open('files/config/workflow-config.json', 'r') as f:
    config = json.load(f)
    
# Validate required sections
required = ['version', 'workflow', 'hashtags', 'content_filtering', 'scoring', 'ai_comments', 'delivery', 'storage']
missing = [s for s in required if s not in config]
if missing:
    print(f'❌ Missing sections: {missing}')
    exit(1)

# Validate scoring weights
if 'weights' in config.get('scoring', {}):
    total = sum(config['scoring']['weights'].values())
    if abs(total - 1.0) > 0.01:
        print(f'⚠️ Scoring weights sum to {total}, should be 1.0')

print('✓ Configuration validation passed')
"
  ```

## Prerequisites and External Dependencies

**CRITICAL**: This project requires extensive external service setup that CANNOT be automated. The following services must be configured manually:

### Required External Services
1. **Instagram Business/Creator Account** - Linked to Facebook Page
2. **Meta App with Instagram Graph API Access** - With long-lived token
3. **n8n Cloud or Self-hosted Instance** - Workflow automation platform
4. **OpenAI API Access** - For comment generation
5. **Google Sheets or Database** - For data storage
6. **Telegram Bot or Slack App** - For human notifications

### API Endpoints Used
- Meta Graph API: `https://graph.facebook.com/v18.0/`
- OpenAI API: `https://api.openai.com/v1/`
- Google Sheets API
- Telegram Bot API / Slack API

## Build and Deployment Process

**IMPORTANT**: There is NO traditional build process. This is a configuration project.

### Setup Steps (All External)
1. **Meta App Setup** - Follow `files/docs/setup-guide.md`
2. **Instagram API Token** - Generate long-lived token (60-day expiry)
3. **Google Sheets Creation** - Create three sheets: hashtags_config, media_cache, sent_log
4. **n8n Workflow Import** - Import workflow using `files/config/workflow-config.json`
5. **API Credentials Configuration** - Set environment variables in n8n

### Validation Commands
- Check file accessibility:
  ```bash
  find files/ -type f -exec echo "✓ {}" \;
  ```
- Validate all JSON configurations:
  ```bash
  find . -name "*.json" -exec python3 -m json.tool {} \; > /dev/null && echo "✓ All JSON files valid"
  ```

## Testing and Validation

**NEVER CANCEL**: Manual testing takes 30-60 minutes due to external API setup requirements.

### Manual Testing Process
1. **Configuration Validation** - Use validation script above
2. **n8n Workflow Import** - Test workflow import in n8n interface
3. **API Connectivity** - Test all external API endpoints
4. **End-to-End Workflow** - Execute complete workflow with test hashtags
5. **Human Interface Testing** - Verify Telegram/Slack notifications work

### Expected Testing Time
- **Configuration Validation**: 2-3 minutes
- **External Service Setup**: 45-60 minutes (manual)
- **End-to-End Testing**: 15-30 minutes
- **NEVER CANCEL** these testing phases - external API delays are normal

### Test Scenarios
After any configuration changes:
1. Import workflow into n8n
2. Configure test hashtags (use sandbox/test hashtags)
3. Execute workflow manually
4. Verify Instagram posts are fetched
5. Confirm AI comments are generated
6. Test Telegram/Slack notifications
7. Validate human interaction buttons work

## Common File Operations

### Key Project Files
```bash
# Project documentation
cat README.md                           # Project overview
cat files/README.md                     # Detailed documentation
cat files/docs/setup-guide.md          # Setup instructions

# Configuration files
cat files/config/workflow-config.json   # Main workflow configuration
python3 -m json.tool files/config/workflow-config.json  # Pretty-print config
```

### Configuration File Structure
```
files/config/workflow-config.json
├── version: "1.0"
├── workflow: {schedule, timezone}
├── hashtags: {limits, rotation}
├── content_filtering: {engagement, keywords}
├── scoring: {weights for ranking}
├── ai_comments: {OpenAI settings}
├── delivery: {Telegram/Slack config}
└── storage: {Google Sheets config}
```

## Workflow Architecture

### Daily Flow
1. **Cron Trigger** - Runs at 9 AM UTC daily
2. **Hashtag Selection** - Rotates through configured hashtags (max 30/week)
3. **Media Fetching** - Instagram Graph API to get recent/top posts
4. **Scoring & Filtering** - Weighted algorithm filters to 5-20 posts
5. **AI Comment Generation** - OpenAI generates 3 suggestions per post
6. **Human Delivery** - Telegram/Slack cards with engagement buttons
7. **Manual Engagement** - Human opens Instagram and engages manually
8. **Logging** - Track engagement activities in Google Sheets

### n8n Node Types Required
- Manual/Cron Trigger
- HTTP Request (Meta Graph API)
- Google Sheets (Read/Write)
- OpenAI (Comment generation)
- Telegram/Slack (Notifications)
- Function nodes (Scoring/filtering)
- Error handling nodes

## Troubleshooting

### Common Issues
1. **Invalid JSON Configuration**
   ```bash
   python3 -m json.tool files/config/workflow-config.json
   ```
   
2. **Missing External Services**
   - Check Meta App credentials
   - Verify Instagram Business account setup
   - Confirm n8n instance accessibility
   - Test API tokens and permissions

3. **Workflow Import Failures**
   - Ensure n8n has required nodes installed
   - Check JSON configuration format
   - Verify all credentials are configured

### Validation Checklist
- [ ] Repository files accessible
- [ ] JSON configuration valid
- [ ] Meta App created and configured
- [ ] Instagram Graph API token generated
- [ ] Google Sheets created with correct schemas
- [ ] n8n instance accessible
- [ ] OpenAI API key configured
- [ ] Telegram bot or Slack app set up
- [ ] Workflow imported successfully
- [ ] Test execution completes without errors

## Important Notes

**NO Traditional Development Tools**: This project does not use npm, pip, docker, make, or any compilation tools.

**External Dependencies Only**: All functionality depends on external services that must be configured manually.

**Manual Testing Required**: Automated testing is limited - most validation requires manual verification of external service integrations.

**API Rate Limits**: Respect Instagram Graph API and OpenAI rate limits during testing.

**Security**: Never commit API keys or credentials to the repository - use environment variables in n8n.

## Frequently Asked Questions

**Q: How do I build this project?**
A: There is no build process. Import the workflow configuration into n8n after setting up external services.

**Q: How do I run tests?**
A: Execute the workflow manually in n8n with test hashtags and verify each step works correctly.

**Q: Why are there no package.json/requirements.txt files?**
A: This is a configuration project, not a code project. All logic runs within n8n workflows.

**Q: How long does setup take?**
A: Initial setup takes 45-60 minutes due to external service configuration requirements.