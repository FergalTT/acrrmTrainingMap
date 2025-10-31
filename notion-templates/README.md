# Notion Template Files

This folder contains CSV templates that can be imported into Notion to quickly set up your training tracking databases.

## 📥 How to Import CSV Files into Notion

### Method 1: Import to New Database
1. In Notion, create a new page
2. Type `/table` and select "Table - Inline"
3. Click the `⋮⋮` menu (top right of table)
4. Select "Merge with CSV"
5. Upload the CSV file
6. Notion will create columns and populate data

### Method 2: Import to Existing Database
1. Open your existing Notion database
2. Click the `⋮⋮` menu (top right)
3. Select "Merge with CSV"
4. Upload the CSV file
5. Map CSV columns to your database properties

## 📋 Available Templates

### training-timeline-template.csv
Pre-populated with all ACRRM training requirements:
- 7 Core Generalist Training requirements
- 12 Advanced Specialised Training options

**Columns included:**
- Requirement Name
- Training Phase
- Category
- Required Duration
- Completed Duration
- Status
- Start Date
- End Date
- Supervisor
- Notes

**After importing, manually add these properties in Notion:**
- Progress % (Formula: `round((prop("Completed Duration") / prop("Required Duration")) * 100)`)
- Training Site (Relation to Training Sites database)
- Competencies Required (Multi-select)
- Cases Logged (Relation to Case Log database)
- Assessments (Multi-select)
- Resources (Files & Media)

## 🔧 Customization After Import

### 1. Add Formula Properties
Formulas can't be imported via CSV. After importing, add:

**Progress %:**
```
round((prop("Completed Duration") / prop("Required Duration")) * 100)
```

### 2. Set Up Relations
After importing all databases, link them:
- Training Timeline → Training Sites
- Training Timeline → Case Log
- Case Log → Training Timeline
- Competency Assessments → Case Log
- Competency Assessments → Training Timeline

### 3. Convert to Multi-Select
Some fields may import as text. Convert to multi-select:
1. Click column header
2. Select "Edit property"
3. Change type to "Multi-select"
4. Notion will convert existing values to options

### 4. Set Up Status Property
If "Status" imported as text, convert to Status type:
1. Click column header → Edit property
2. Change type to "Status"
3. Configure status groups:
   - Not Started (To Do)
   - In Progress (In Progress)
   - Completed (Complete)
   - Deferred (Custom)

## 💡 Tips for Import

1. **Clean import**: Import CSVs into fresh databases for best results
2. **Check data types**: Verify dates import as Date type, numbers as Number type
3. **Add relations last**: Set up database relations after all databases are created
4. **Use templates**: After setup, create templates for common entry types
5. **Backup first**: Export your existing data before merging new CSVs

## 🎯 Recommended Import Order

1. **First**: Training Timeline (use training-timeline-template.csv)
2. **Second**: Training Sites (manually create or import from map)
3. **Third**: Case Log (start with empty database)
4. **Fourth**: Competency Assessments (start with empty database)
5. **Fifth**: CPD Activities (start with empty database)
6. **Finally**: Set up all relations between databases

## 📝 Creating Your Own Templates

To create templates from your databases:
1. Open database
2. Click `⋮⋮` menu → Export
3. Select "CSV" format
4. Download and customize
5. Re-import or share with colleagues

## 🔄 Updating Existing Data

To update existing databases with new requirements:
1. Export current database to CSV (backup)
2. Merge new CSV (Notion will add new rows)
3. Review for duplicates
4. Clean up if needed

## ⚠️ Important Notes

- **De-identify data**: Never include patient identifying information
- **Backup regularly**: Export your databases monthly
- **Privacy**: Notion databases are private by default, keep them that way
- **Version control**: Save dated exports as you progress through training

## 🆘 Troubleshooting Import Issues

### "Column not found"
- Create all columns manually first
- Then use "Merge with CSV" to populate data

### "Date format error"
- Notion accepts: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY
- Ensure dates in CSV match one of these formats

### "Number format error"
- Remove any commas from numbers in CSV
- Use plain numbers (e.g., 12, not "12 months")

### Duplicates after merge
- Notion doesn't check for duplicates during merge
- Manually review and delete duplicates after import

---

**Need more help?** Check the main [NOTION_SETUP.md](../NOTION_SETUP.md) guide for complete database setup instructions.
