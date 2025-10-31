# Notion MCP Integration Guide

## 🔗 What is the Notion MCP Integration?

The Notion MCP (Model Context Protocol) server has been added to your Claude Code setup. This allows Claude to interact directly with your Notion databases to:
- Create database entries
- Update existing entries
- Query and search databases
- Automate data entry from the map into Notion

## ✅ Current Status

The Notion MCP server has been configured at:
```
https://mcp.notion.com/mcp
```

**Status**: ✅ Installed and ready (requires authentication on first use)

## 🔐 Authentication Required

When you first try to use Notion features through Claude Code, you'll be prompted to authenticate:

1. Claude will provide an authentication URL
2. Visit the URL in your browser
3. Log in to your Notion account
4. Authorize Claude Code to access your Notion workspace
5. Return to Claude Code - authentication complete!

## 💡 How to Use Notion Integration

### Example 1: Create Training Timeline Entry
```
You: "Create a new entry in my ACRRM Training Timeline database for Primary Care rotation, 6 months required, status Not Started"

Claude: [Uses Notion MCP to create the entry directly]
```

### Example 2: Log a Case
```
You: "Log a new case: Emergency appendectomy, supervised role, emergency care category, high complexity"

Claude: [Creates entry in Case Log database with all details]
```

### Example 3: Update Progress
```
You: "Update my Anaesthetics rotation to show 2 months completed"

Claude: [Updates the existing database entry]
```

### Example 4: Query Your Data
```
You: "How many cases have I logged in Paediatrics?"

Claude: [Queries your Case Log database and reports the count]
```

### Example 5: Batch Import
```
You: "Import all the training sites from the map data into my Notion Training Sites database"

Claude: [Reads training-sites.json and creates Notion entries]
```

## 🚀 Getting Started with Notion MCP

### Step 1: Set Up Your Notion Databases First
Follow the `NOTION_SETUP.md` guide to create all 5 databases with the proper structure.

### Step 2: Share Databases with Integration
Once Claude authenticates:
1. Open each Notion database
2. Click "Share" in the top right
3. Make sure the integration has access
4. Claude will guide you through this

### Step 3: Start Using Claude to Manage Notion
Now you can ask Claude to:
- Create entries: "Add a new case to my log"
- Update entries: "Mark Primary Care rotation as completed"
- Query data: "Show me all sites in Queensland"
- Bulk operations: "Import all training requirements"

## 📋 Useful Commands

### Data Entry
```
"Log today's case: [details]"
"Add a new training site: [name, location, details]"
"Create CPD entry for [course name]"
"Record assessment: [type, date, result]"
```

### Queries
```
"How many cases in Emergency Care?"
"Show my completed rotations"
"List all sites offering Anaesthetics AST"
"What's my progress percentage?"
```

### Updates
```
"Mark [rotation name] as In Progress"
"Update [case number] with feedback"
"Change [site] application status to Accepted"
```

### Bulk Operations
```
"Import all map training sites to Notion"
"Create all CGT requirements in my timeline"
"Populate AST options in my database"
```

## 🎯 Powerful Workflows

### Workflow 1: Map to Notion Pipeline
1. Use the map to find interesting sites
2. Ask Claude: "Add [site name] to my Training Sites database"
3. Claude extracts info from map data and creates Notion entry
4. Continue tracking application status in Notion

### Workflow 2: End-of-Day Case Logging
1. Tell Claude: "I saw 5 cases today, let me describe them"
2. Describe each case conversationally
3. Claude formats and logs each one properly
4. Links cases to relevant rotations automatically

### Workflow 3: Progress Reports
1. Ask Claude: "Generate my training progress report"
2. Claude queries all databases
3. Calculates completion percentages
4. Identifies gaps in case mix
5. Suggests next steps

### Workflow 4: Application Tracking
1. Tell Claude: "I'm applying to [site name]"
2. Claude creates entry in Training Sites
3. Sets status to "Applied"
4. Can set reminders for follow-ups

## 🔧 Technical Details

### What the MCP Can Access
- ✅ Databases you've shared with the integration
- ✅ Pages within those databases
- ✅ Properties and values
- ❌ Private pages not shared
- ❌ Pages in other workspaces

### Security & Privacy
- All data stays in your Notion workspace
- Claude Code connects via secure API
- You control what databases are shared
- Revoke access anytime in Notion settings
- Patient data should still be de-identified

### Rate Limits
- Notion API has rate limits
- Claude will handle this automatically
- Bulk operations may take time
- Progress updates provided for large operations

## 🆘 Troubleshooting

### "Not authenticated with Notion"
**Solution**: Complete the OAuth flow when prompted

### "Cannot find database"
**Solution**:
1. Check database is shared with integration
2. Verify database name is correct
3. Try using database URL instead

### "Property not found"
**Solution**:
1. Ensure database has the required properties
2. Check property names match exactly
3. Refer to NOTION_SETUP.md for proper structure

### "Rate limit exceeded"
**Solution**:
- Wait a few minutes
- Notion API limits: 3 requests per second
- Claude will retry automatically

### Operation failed
**Solution**:
1. Check your internet connection
2. Verify Notion is accessible
3. Ensure database structure is correct
4. Try the operation again

## 💡 Pro Tips

### 1. Use Natural Language
Don't worry about exact syntax - Claude understands:
- "Log a case for me"
- "Add this site to Notion"
- "Update my progress"

### 2. Batch Operations
Save time with bulk requests:
- "Import all QLD sites"
- "Create all my timeline entries"
- "Log these 5 cases"

### 3. Smart Queries
Ask for insights:
- "What's my case mix?"
- "Which competencies need more work?"
- "Show sites I haven't applied to"

### 4. Automated Linking
Claude automatically:
- Links cases to rotations
- Connects assessments to cases
- Associates sites with applications

### 5. Error Recovery
If something fails:
- Claude will explain what went wrong
- Suggest corrections
- Retry automatically when possible

## 🔄 Sync Workflow

### Recommended Daily Workflow:
```
Morning:
"Claude, what's on my training schedule today?"

During Day:
[Note interesting cases]

Evening:
"Claude, log today's cases: [describe cases]"
"Update my rotation progress"

Weekly:
"Claude, show my progress report"
"What gaps do I have in competencies?"
```

## 📊 Example: Complete Setup Conversation

```
You: "Help me set up my ACRRM Notion tracking"

Claude: "I'll help you import the training requirements. First, let me authenticate with Notion..."
[OAuth flow]

You: "Import all CGT requirements from the template"

Claude: "Creating 7 Core Generalist Training entries in your Training Timeline database..."
[Creates entries]

You: "Import all the training sites from the map"

Claude: "Reading training-sites.json... Found 30+ sites. Creating entries..."
[Batch creates entries]

You: "Great! Log my first case: Appendectomy in ED, supervised, high complexity"

Claude: "Creating case log entry..."
[Creates detailed entry with all fields]

You: "Link that case to my Emergency Care rotation"

Claude: "Linking case #1 to Emergency Care rotation... Done!"

You: "Show my progress"

Claude: [Queries databases]
"Here's your current progress:
- Emergency Care: 1 case logged
- Primary Care: Not started
- Total cases: 1
[...]"
```

## ✨ Advanced Features

### 1. Templates
Claude can use templates:
```
"Use the case log template for chest pain presentation"
```

### 2. Views
Create custom views:
```
"Show me a board view of sites grouped by state"
```

### 3. Formulas
Claude updates calculated fields automatically

### 4. Relations
All database links handled automatically

### 5. Exports
Generate reports:
```
"Export my last month's cases as a summary"
```

## 🎓 Learning More

### Notion MCP Documentation
- [Notion API Docs](https://developers.notion.com/)
- [MCP Protocol](https://mcp.notion.com/docs)

### ACRRM + Notion Resources
- Check the main README.md
- See NOTION_SETUP.md for database structure
- Review example workflows in QUICK_START.md

---

## ✅ Setup Checklist

- [ ] Notion MCP server installed (✅ Already done!)
- [ ] Notion databases created (follow NOTION_SETUP.md)
- [ ] OAuth authentication completed
- [ ] Databases shared with integration
- [ ] Test entry created successfully
- [ ] Map data imported to Notion
- [ ] First case logged via Claude
- [ ] Progress query working

---

## 🎉 You're Ready!

With Notion MCP integration, you can now:
- ✅ Create Notion entries conversationally
- ✅ Update databases with natural language
- ✅ Query your training progress anytime
- ✅ Automate data import from the map
- ✅ Generate progress reports on demand
- ✅ Link related entries automatically

**Next Steps:**
1. Complete Notion database setup (NOTION_SETUP.md)
2. Tell Claude: "Let's authenticate with Notion"
3. Start logging: "Add my first case"
4. Explore: "Show me what's in my timeline"

---

**Happy training tracking! 🎓**
