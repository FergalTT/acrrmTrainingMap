# Quick Start Guide

## 🚀 Get the Map Running in 2 Minutes

### Step 1: Open Terminal
Navigate to the project folder:
```bash
cd ~/acrrm-training-map
```

### Step 2: Start the Application
```bash
npm run dev
```

### Step 3: Open Browser
Visit: **http://localhost:3000**

That's it! The interactive map should now be running.

---

## 🎯 Quick Tour

### Using the Map
1. **Zoom & Pan**: Use mouse wheel to zoom, click and drag to pan
2. **Click Markers**: Click any marker to see site details
3. **Color Codes**:
   - 🟢 Green = Core training sites
   - 🔴 Red = AST sites
   - 🔵 Blue = Mixed sites

### Using Filters (Left Sidebar)
1. **Select filters** by clicking checkboxes
2. **Multiple selections** are combined (AND logic within category, OR across categories)
3. **Clear All** button resets all filters
4. **Select/Deselect All** buttons in each section for quick filtering

### Example Filter Workflows

**Find QLD Anaesthetics Sites:**
1. Check "QLD" under State
2. Check "AST - Anaesthetics" under Training Type
3. Result: All anaesthetics training sites in Queensland

**Find Remote Core Training:**
1. Check "MMM 6" and "MMM 7" under MMM Level
2. Check "Core Generalist Training" under Training Type
3. Result: All remote core training locations

**Find Sites with Obstetrics:**
1. Check "Obstetrics" under Rotations
2. Result: All sites offering obstetrics training

---

## 📊 Setting Up Notion (15 minutes)

### Option 1: Use Notion Template (Coming Soon)
- Import the pre-built template
- All databases and relations already configured

### Option 2: Manual Setup
Follow the detailed guide in [NOTION_SETUP.md](./NOTION_SETUP.md)

**Quick Manual Setup:**
1. Create 5 new databases in Notion
2. Copy property configurations from NOTION_SETUP.md
3. Set up relations between databases
4. Pre-populate with training requirements
5. Start logging!

---

## 🔄 Typical Workflow

### Phase 1: Planning (Start of Training)
1. **Explore Map**: Browse all training sites
2. **Filter by Interest**: Use filters to find suitable sites
3. **Document in Notion**: Copy site details to "Training Sites" database
4. **Set Timeline**: Plan your 4-year training pathway in "Training Timeline"

### Phase 2: Applications
1. **Track Applications**: Update status in "Training Sites" database
2. **Schedule Interviews**: Record dates and notes
3. **Accept Placement**: Update status to "Accepted"

### Phase 3: During Rotation
1. **Log Cases**: Record every case in "Case Log" database
2. **Link Cases**: Connect to current rotation requirement
3. **Track Progress**: Watch completion percentage increase
4. **Record Assessments**: Add supervisor reports to "Competency Assessments"

### Phase 4: Review & Planning
1. **Weekly Review**: Check progress dashboard
2. **Identify Gaps**: Find areas needing more cases
3. **Plan Next Rotation**: Use map to explore next placement options
4. **CPD Tracking**: Log all learning activities

---

## 💡 Pro Tips

### For the Map:
- **Bookmark the page** for quick access
- **Mobile friendly** - use on phone during site visits
- **Save filters** by keeping the tab open
- **Screenshot sites** of interest for your applications

### For Notion:
- **Use templates** - Create case entry templates for speed
- **Mobile app** - Log cases immediately after patient encounters
- **Linked databases** - Create views showing relevant data
- **Regular backups** - Export monthly
- **Dashboard page** - Create one master page with all database views

### Workflow Integration:
1. **Morning**: Check Notion for today's learning objectives
2. **During work**: Note interesting cases
3. **Evening**: Log all cases in Notion
4. **Weekly**: Review progress, plan next week
5. **Monthly**: Update training timeline, plan rotations using map

---

## 🆘 Troubleshooting

### Map won't load
```bash
# Check if server is running
# Should see "Local: http://localhost:3000"

# If not, restart:
cd ~/acrrm-training-map
npm run dev
```

### Map loads but no markers
- Check browser console (F12) for errors
- Verify `data/training-sites.json` exists
- Check network tab for failed JSON requests

### Filters not working
- Try "Clear All Filters" button
- Refresh the page (Cmd+R or Ctrl+R)
- Check browser console for JavaScript errors

### Port 3000 already in use
```bash
# Use a different port
npm run dev -- --port 3001

# Then visit http://localhost:3001
```

---

## 📱 Using on Mobile

### iPhone/iPad:
1. Open Safari
2. Visit http://[your-computer-ip]:3000
3. Tap Share → Add to Home Screen
4. Now it's an app icon!

### Android:
1. Open Chrome
2. Visit http://[your-computer-ip]:3000
3. Menu → Add to Home Screen
4. Now it's an app icon!

**Note**: Your computer must be running the dev server and on the same WiFi network.

---

## 🎓 Learning Resources

### ACRRM Resources:
- [Training Handbook](https://www.acrrm.org.au/)
- [Curriculum Documents](https://curriculum.acrrm.org.au/)
- [My College Portal](https://mycollege.acrrm.org.au/)

### Map & Notion Tips:
- YouTube: Search "Notion database tutorial"
- YouTube: Search "medical training portfolio notion"
- Notion Help Center: https://www.notion.so/help

---

## 📞 Getting Help

**Technical Issues:**
- Check README.md for detailed documentation
- Check NOTION_SETUP.md for Notion help
- Raise issue on GitHub (if applicable)

**Training Questions:**
- Contact ACRRM directly
- Speak with your training supervisor
- Connect with other registrars

---

## ✅ Setup Checklist

### Initial Setup:
- [ ] Project folder exists at ~/acrrm-training-map
- [ ] Dependencies installed (npm install)
- [ ] Development server runs (npm run dev)
- [ ] Map loads in browser
- [ ] Filters work correctly

### Notion Setup:
- [ ] Training Timeline database created
- [ ] Case Log database created
- [ ] Training Sites database created
- [ ] Competency Assessments database created
- [ ] CPD Activities database created
- [ ] Relations between databases set up
- [ ] Pre-populated training requirements
- [ ] Dashboard page created

### Workflow Ready:
- [ ] First training sites imported from map
- [ ] First case logged in Notion
- [ ] Training timeline has start dates
- [ ] Mobile access configured (optional)
- [ ] Backup system in place

---

## 🎉 You're Ready!

You now have:
✅ Interactive map of all Australian ACRRM training sites
✅ Comprehensive Notion tracking system
✅ Workflow for logging cases and tracking progress
✅ Planning tools for your 4-year training journey

**Next Steps:**
1. Explore the map and find sites that interest you
2. Set up your Notion databases
3. Start your first rotation and log your first case!

**Good luck with your ACRRM Fellowship! 🏥**
