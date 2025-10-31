# ACRRM Training Tracker - Notion Database Setup Guide

This guide will help you set up comprehensive Notion databases to track your ACRRM Fellowship training timeline, requirements, and case logs.

## Database 1: Training Timeline & Requirements

### Database Name: **ACRRM Training Timeline**

This database tracks your overall training progress across Core Generalist Training (CGT) and Advanced Specialised Training (AST).

#### Properties to Create:

1. **Requirement Name** (Title)
   - Type: Title
   - Description: The name of the training requirement or rotation

2. **Training Phase** (Select)
   - Type: Select
   - Options:
     - Core Generalist Training (CGT)
     - Advanced Specialised Training (AST)

3. **Category** (Select)
   - Type: Select
   - Options:
     - Primary Care
     - Secondary Care
     - Emergency Care
     - Rural/Remote Practice
     - Paediatrics
     - Obstetrics
     - Anaesthetics
     - Aboriginal and Torres Strait Islander Health
     - Academic Practice
     - Adult Internal Medicine
     - Mental Health
     - Obstetrics and Gynaecology
     - Palliative Care
     - Population Health
     - Remote Medicine
     - Surgery

4. **Required Duration** (Number)
   - Type: Number
   - Format: Number
   - Description: Required months/weeks for this component

5. **Completed Duration** (Number)
   - Type: Number
   - Format: Number
   - Description: Months/weeks completed so far

6. **Progress %** (Formula)
   - Type: Formula
   - Formula: `round((prop("Completed Duration") / prop("Required Duration")) * 100)`

7. **Status** (Status)
   - Type: Status
   - Options:
     - Not Started
     - In Progress
     - Completed
     - Deferred

8. **Start Date** (Date)
   - Type: Date

9. **End Date** (Date)
   - Type: Date

10. **Training Site** (Relation)
    - Type: Relation
    - Related Database: Training Sites (create this as a separate database)

11. **Supervisor** (Text)
    - Type: Text

12. **Competencies Required** (Multi-select)
    - Type: Multi-select
    - Options (8 domains of rural practice):
      - Clinical Practice
      - Primary Healthcare
      - Emergency Care
      - Procedural Skills
      - Aboriginal and Torres Strait Islander Health
      - Population Health
      - Academic Practice
      - Professional Development

13. **Cases Logged** (Relation)
    - Type: Relation
    - Related Database: Case Log (Database 2)

14. **Assessments** (Multi-select)
    - Type: Multi-select
    - Options:
      - Supervisor Report
      - Mini-CEX
      - Case-based Discussion
      - MSF (Multi-Source Feedback)
      - logbook Review

15. **Notes** (Text)
    - Type: Text (long text)

16. **Resources** (Files & Media)
    - Type: Files & Media

#### Pre-populate with these entries:

**Core Generalist Training Requirements:**
1. Primary Care - 6 months required
2. Secondary Care - 3 months required
3. Emergency Care - 3 months required
4. Rural/Remote Practice - 12 months required
5. Paediatrics Rotation - duration varies
6. Obstetrics Rotation - duration varies
7. Anaesthetics Rotation - duration varies

**AST Options (select one, or Surgery for 24 months):**
1. Aboriginal and Torres Strait Islander Health - 12 months
2. Academic Practice - 12 months
3. Adult Internal Medicine - 12 months
4. Anaesthetics - 12 months
5. Emergency Medicine - 12 months
6. Mental Health - 12 months
7. Obstetrics and Gynaecology - 12 months
8. Paediatrics - 12 months
9. Palliative Care - 12 months
10. Population Health - 12 months
11. Remote Medicine - 12 months
12. Surgery - 24 months

---

## Database 2: Case Log & Requirements Tracker

### Database Name: **ACRRM Case Log**

This database tracks individual cases that fulfill specific training requirements.

#### Properties to Create:

1. **Case Number/Title** (Title)
   - Type: Title
   - Description: Brief case description or unique ID

2. **Date** (Date)
   - Type: Date

3. **Training Phase** (Select)
   - Type: Select
   - Options:
     - Core Generalist Training
     - Advanced Specialised Training

4. **Rotation** (Relation)
   - Type: Relation
   - Related Database: ACRRM Training Timeline

5. **Category** (Select)
   - Type: Select
   - Options: (same as Database 1 categories)
     - Primary Care
     - Emergency Care
     - Paediatrics
     - Obstetrics
     - Anaesthetics
     - Surgery
     - Remote Medicine
     - Mental Health
     - Adult Internal Medicine
     - etc.

6. **Procedure/Presentation** (Text)
   - Type: Text
   - Description: What was the procedure or presenting complaint?

7. **Patient Age Group** (Select)
   - Type: Select
   - Options:
     - Neonate (0-28 days)
     - Infant (1-12 months)
     - Child (1-12 years)
     - Adolescent (13-18 years)
     - Adult (19-65 years)
     - Elderly (65+ years)

8. **Role** (Select)
   - Type: Select
   - Options:
     - Observed
     - Assisted
     - Supervised
     - Independent

9. **Complexity** (Select)
   - Type: Select
   - Options:
     - Low
     - Medium
     - High

10. **Competencies Demonstrated** (Multi-select)
    - Type: Multi-select
    - Options: (8 domains)
      - Clinical Practice
      - Primary Healthcare
      - Emergency Care
      - Procedural Skills
      - Aboriginal and Torres Strait Islander Health
      - Population Health
      - Academic Practice
      - Professional Development

11. **Setting** (Select)
    - Type: Select
    - Options:
      - Hospital ED
      - Hospital Inpatient
      - Hospital Outpatient
      - General Practice
      - Community Health
      - Remote Clinic
      - Telehealth
      - Home Visit

12. **Supervisor** (Text)
    - Type: Text

13. **Feedback Received** (Checkbox)
    - Type: Checkbox

14. **Assessment Type** (Select)
    - Type: Select
    - Options:
      - Mini-CEX
      - Case-based Discussion
      - Direct Observation
      - Informal Feedback
      - None

15. **Learning Points** (Text)
    - Type: Text (long text)

16. **Attachments** (Files & Media)
    - Type: Files & Media
    - Description: Upload de-identified case notes, images, etc.

17. **Fulfills Requirement** (Relation)
    - Type: Relation
    - Related Database: ACRRM Training Timeline

18. **MMM Level** (Select)
    - Type: Select
    - Options: MMM 1, MMM 2, MMM 3, MMM 4, MMM 5, MMM 6, MMM 7

19. **Submitted to Portfolio** (Checkbox)
    - Type: Checkbox

---

## Database 3: Training Sites

### Database Name: **Training Sites**

This database tracks all available training sites and your applications/placements.

#### Properties to Create:

1. **Site Name** (Title)
   - Type: Title

2. **State** (Select)
   - Type: Select
   - Options: QLD, NSW, VIC, SA, WA, TAS, NT, ACT

3. **City** (Text)
   - Type: Text

4. **Site Type** (Select)
   - Type: Select
   - Options:
     - Hospital
     - General Practice
     - Aboriginal Medical Service
     - Community Health
     - Specialized Service
     - ADF

5. **MMM Level** (Select)
   - Type: Select
   - Options: MMM 1-7

6. **Training Types Available** (Multi-select)
   - Type: Multi-select
   - Options:
     - Core Generalist Training
     - AST - Anaesthetics
     - AST - Emergency Medicine
     - AST - Paediatrics
     - AST - Obstetrics and Gynaecology
     - AST - Remote Medicine
     - AST - Aboriginal and Torres Strait Islander Health
     - AST - Surgery
     - AST - Adult Internal Medicine
     - AST - Mental Health
     - AST - Palliative Care
     - AST - Academic Practice
     - AST - Population Health

7. **Rotations Offered** (Multi-select)
   - Type: Multi-select
   - Options: Primary Care, Emergency Care, Paediatrics, Obstetrics, Anaesthesia, Surgery, etc.

8. **Director Contact** (Text)
   - Type: Text

9. **Supervisors** (Text)
   - Type: Text (long text)

10. **Website** (URL)
    - Type: URL

11. **Application Status** (Status)
    - Type: Status
    - Options:
      - Interested
      - Applied
      - Interview Scheduled
      - Offered
      - Accepted
      - Declined
      - Completed

12. **Application Date** (Date)
    - Type: Date

13. **Interview Date** (Date)
    - Type: Date

14. **Placement Period** (Date)
    - Type: Date
    - Enable date range

15. **Notes** (Text)
    - Type: Text (long text)

16. **Associated Sites** (Text)
    - Type: Text

17. **Coordinates** (Text)
    - Type: Text
    - Description: Store lat,lng for reference

---

## Database 4: Competency Tracking

### Database Name: **Competency Assessments**

Track your assessments and competency sign-offs across the 8 domains.

#### Properties to Create:

1. **Assessment Title** (Title)
   - Type: Title

2. **Assessment Type** (Select)
   - Type: Select
   - Options:
     - Supervisor Report
     - Mini-CEX
     - Case-based Discussion
     - MSF (Multi-Source Feedback)
     - Logbook Review
     - OSCE
     - Written Exam

3. **Date Completed** (Date)
   - Type: Date

4. **Domain** (Select)
   - Type: Select
   - Options:
     - Clinical Practice
     - Primary Healthcare
     - Emergency Care
     - Procedural Skills
     - Aboriginal and Torres Strait Islander Health
     - Population Health
     - Academic Practice
     - Professional Development

5. **Training Phase** (Select)
   - Type: Select
   - Options:
     - Core Generalist Training
     - Advanced Specialised Training

6. **Assessor Name** (Text)
   - Type: Text

7. **Assessor Role** (Text)
   - Type: Text

8. **Result** (Select)
   - Type: Select
   - Options:
     - Competent
     - Not Yet Competent
     - Needs Improvement
     - Excellent

9. **Score** (Number)
   - Type: Number

10. **Feedback** (Text)
    - Type: Text (long text)

11. **Action Items** (Text)
    - Type: Text (long text)

12. **Related Cases** (Relation)
    - Type: Relation
    - Related Database: ACRRM Case Log

13. **Related Rotation** (Relation)
    - Type: Relation
    - Related Database: ACRRM Training Timeline

14. **Submitted to ACRRM** (Checkbox)
    - Type: Checkbox

15. **Certificate/Evidence** (Files & Media)
    - Type: Files & Media

---

## Database 5: CPD & Learning Activities

### Database Name: **CPD Activities**

Track Continuing Professional Development activities, courses, conferences, and learning.

#### Properties to Create:

1. **Activity Title** (Title)
   - Type: Title

2. **Activity Type** (Select)
   - Type: Select
   - Options:
     - Course
     - Conference
     - Workshop
     - Webinar
     - Journal Club
     - Self-directed Learning
     - Research
     - Teaching
     - QI Project

3. **Date** (Date)
   - Type: Date

4. **CPD Hours** (Number)
   - Type: Number

5. **Category** (Multi-select)
   - Type: Multi-select
   - Options: (aligned with training categories)

6. **Provider** (Text)
   - Type: Text

7. **Status** (Status)
   - Type: Status
   - Options:
     - Planned
     - Registered
     - Completed
     - Cancelled

8. **Cost** (Number)
   - Type: Number
   - Format: Australian Dollar

9. **Receipt** (Files & Media)
   - Type: Files & Media

10. **Certificate** (Files & Media)
    - Type: Files & Media

11. **Learning Outcomes** (Text)
    - Type: Text (long text)

12. **Related to Requirement** (Relation)
    - Type: Relation
    - Related Database: ACRRM Training Timeline

13. **Logged in Portfolio** (Checkbox)
    - Type: Checkbox

---

## How to Use These Databases Together

### Workflow:

1. **Setup Phase:**
   - Import training sites from the interactive map into the Training Sites database
   - Pre-populate the Training Timeline with all CGT and AST requirements
   - Set your target completion dates

2. **During Rotations:**
   - Log every case in the Case Log database
   - Link cases to the specific rotation/requirement they fulfill
   - Track your progress automatically as cases accumulate

3. **Assessment Time:**
   - Record all assessments in the Competency Assessments database
   - Link them to relevant cases and rotations

4. **Planning:**
   - Use the Training Sites database to track applications
   - View your overall progress in the Training Timeline
   - Identify gaps in your case mix or competencies

5. **CPD:**
   - Log all learning activities
   - Track total CPD hours
   - Link activities to specific requirements

### Dashboard Views to Create:

1. **Timeline Dashboard** (in Training Timeline database)
   - Board view grouped by Status
   - Timeline view by Start Date
   - Gallery view with progress bars

2. **Case Statistics** (in Case Log database)
   - Gallery grouped by Category
   - Table filtered by current rotation
   - Chart view showing cases by complexity

3. **Sites Overview** (in Training Sites database)
   - Map view (if using Notion Plus)
   - Board grouped by Application Status
   - Gallery filtered by desired training type

---

## Quick Setup Checklist

- [ ] Create Database 1: Training Timeline
- [ ] Create Database 2: Case Log
- [ ] Create Database 3: Training Sites
- [ ] Create Database 4: Competency Assessments
- [ ] Create Database 5: CPD Activities
- [ ] Set up relations between databases
- [ ] Pre-populate Training Timeline with requirements
- [ ] Import training sites from interactive map
- [ ] Create custom dashboard page with linked views
- [ ] Set up templates for common case types
- [ ] Configure reminders for assessment deadlines

---

## Tips for Success

1. **Log cases immediately** - Use Notion mobile app to log cases right after encounters
2. **Use templates** - Create case templates for common presentations
3. **Regular reviews** - Weekly review of progress and gaps
4. **Backup regularly** - Export your databases periodically
5. **Link everything** - Use relations to connect cases, rotations, and assessments
6. **Dashboard first** - Create a main dashboard page with all database views
7. **Privacy** - Ensure all case entries are de-identified

---

## Integration with Interactive Map

The interactive map website ([http://localhost:3000](http://localhost:3000) when running locally) can be used alongside your Notion databases:

1. Use the map to explore training locations
2. Copy site information into your Training Sites Notion database
3. Filter by state, MMM level, and training type to find suitable placements
4. Track your applications and placements in Notion
5. Reference the map when planning your training pathway

---

## Need Help?

Refer to:
- [ACRRM Curriculum](https://curriculum.acrrm.org.au/fellowship-training/introduction)
- [ACRRM Training Posts](https://mycollege.acrrm.org.au/search/find-training-post)
- Notion documentation for advanced features
