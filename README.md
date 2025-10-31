# ACRRM Training Map & Tracker

An interactive web application and Notion database system for tracking ACRRM Fellowship training locations, requirements, and case logs across Australia.

## 🗺️ Features

### Interactive Map
- **Visual Training Site Explorer**: Interactive map showing all ACRRM training locations across Australia
- **Advanced Filtering**: Filter by state, training type (Core/AST), rotations, MMM level, and site type
- **Detailed Information**: Click markers to view site details including contacts, supervisors, and available rotations
- **Color-coded Markers**:
  - 🟢 Green = Core Generalist Training sites
  - 🔴 Red = AST (Advanced Specialised Training) sites
  - 🔵 Blue = Mixed training types

### Notion Database System
Comprehensive tracking system with 5 integrated databases:
1. **Training Timeline** - Track CGT and AST requirements and progress
2. **Case Log** - Record cases fulfilling training requirements
3. **Training Sites** - Manage site applications and placements
4. **Competency Assessments** - Track supervisor reports and assessments
5. **CPD Activities** - Log continuing professional development

## 📍 Training Sites Included

Currently includes:
- **30+ training sites** across QLD, NSW, VIC, SA, WA, TAS, and NT
- **AST Anaesthetics sites** from ANZCA RGA program
- **Core training sites** from ACRRM
- **O&G training sites** (RANZCOG data pending full scrape)
- Sites categorized by:
  - Hospitals
  - General Practice
  - Aboriginal Medical Services
  - Specialized Services (Antarctic, ADF)

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd ~/acrrm-training-map
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm run dev
```

4. **Open your browser:**
Navigate to [http://localhost:3000](http://localhost:3000)

### Building for Production

```bash
npm run build
npm run preview
```

## 📊 Notion Setup

See the comprehensive [NOTION_SETUP.md](./NOTION_SETUP.md) guide for detailed instructions on:
- Creating all 5 databases
- Setting up properties and relations
- Pre-populating training requirements
- Creating dashboard views
- Workflow and best practices

### Quick Notion Setup

1. Create a new Notion workspace or page
2. Follow the NOTION_SETUP.md guide to create each database
3. Import training site data from the interactive map
4. Start logging your training progress!

## 📁 Project Structure

```
acrrm-training-map/
├── data/
│   └── training-sites.json      # Training location data
├── src/
│   ├── components/
│   │   ├── MapView.jsx          # Interactive map component
│   │   └── Sidebar.jsx          # Filter sidebar component
│   ├── styles/
│   │   └── App.css              # Application styles
│   ├── App.jsx                  # Main application component
│   └── main.jsx                 # Application entry point
├── public/                       # Static assets
├── index.html                    # HTML template
├── package.json                  # Dependencies
├── vite.config.js               # Vite configuration
├── README.md                     # This file
└── NOTION_SETUP.md              # Notion database guide
```

## 🎯 Training Requirements Overview

### Core Generalist Training (CGT) - 3 Years
- Primary Care: 6 months
- Secondary Care: 3 months
- Emergency Care: 3 months
- Rural/Remote Practice: 12 months
- Paediatrics, Obstetrics, Anaesthetics rotations

### Advanced Specialised Training (AST) - 1 Year
Choose from 12 specialties:
- Aboriginal and Torres Strait Islander Health
- Academic Practice
- Adult Internal Medicine
- Anaesthetics
- Emergency Medicine
- Mental Health
- Obstetrics and Gynaecology
- Paediatrics
- Palliative Care
- Population Health
- Remote Medicine
- Surgery (24 months)

## 🔍 Using the Filters

### State/Territory
Filter by Australian states and territories to find sites in specific locations.

### Training Type
- **Core Generalist Training**: General practice and hospital rotations
- **AST options**: Specialized 12-month (or 24-month for surgery) programs

### Rotations
Filter by specific clinical areas:
- Primary Care
- Emergency Care
- Anaesthesia
- Obstetrics
- Paediatrics
- Remote Medicine
- And more...

### MMM Level
Modified Monash Model classification:
- **MMM 1**: Major cities
- **MMM 2**: Regional centres
- **MMM 3-5**: Large rural, medium rural, small rural towns
- **MMM 6-7**: Remote and very remote areas

### Site Type
- Hospital
- General Practice
- Aboriginal Medical Service
- ADF (Australian Defence Force)
- Specialized Services

## 📈 Data Sources

Training location data compiled from:
- [ACRRM Fellowship Training Curriculum](https://curriculum.acrrm.org.au/fellowship-training/introduction)
- [ACRRM Training Posts](https://mycollege.acrrm.org.au/search/find-training-post)
- [ANZCA RGA Training Sites](https://www.anzca.edu.au/education-and-training/anaesthesia-training-and-pathways/rural-generalist-anaesthesia-training-program) (QLD, NSW, VIC, SA, WA, TAS, NT)
- [RANZCOG Training Sites](https://ranzcog.edu.au/training/sites/)

## 🛠️ Technologies Used

- **React** - UI framework
- **Leaflet** - Interactive mapping
- **React-Leaflet** - React bindings for Leaflet
- **Vite** - Build tool and dev server
- **OpenStreetMap** - Map tiles

## 🗺️ Map Features

- **Pan and Zoom**: Explore all of Australia
- **Click Markers**: View detailed site information
- **Responsive**: Works on desktop and mobile
- **Fast Loading**: Optimized marker clustering for performance

## 📝 Adding More Training Sites

To add additional training sites, edit `data/training-sites.json`:

```json
{
  "id": "unique-id",
  "name": "Hospital Name",
  "state": "QLD",
  "city": "City Name",
  "lat": -27.4698,
  "lng": 153.0251,
  "type": "Hospital",
  "trainingTypes": ["Core Generalist Training"],
  "rotations": ["Emergency Care", "Primary Care"],
  "mmm": 3,
  "contacts": {
    "directorOfAnaesthesia": "Dr Name",
    "supervisors": ["Dr Supervisor 1", "Dr Supervisor 2"]
  }
}
```

## 🔄 Future Enhancements

Potential additions:
- [ ] Complete RANZCOG O&G training sites data
- [ ] Add Emergency Medicine AST sites
- [ ] Include Paediatrics AST training sites
- [ ] Add Mental Health training locations
- [ ] Integration with ACRRM API (if available)
- [ ] Export filtered results to CSV
- [ ] Direct integration with Notion API
- [ ] User accounts for saving preferences
- [ ] Application deadline tracking
- [ ] Site comparison tool

## 🤝 Contributing

This is a personal training tracker, but if you'd like to:
- Report incorrect site information
- Suggest additional features
- Contribute training site data

Please create issues or pull requests.

## 📄 License

MIT License - feel free to use this for your own training planning.

## ⚕️ Disclaimer

This tool is for informational and educational purposes only. Always verify training site information, accreditation status, and requirements with:
- Official ACRRM resources
- The training sites directly
- Your training program supervisor

Training requirements and site accreditations may change. Last updated: January 2025.

## 🙋 Support

For questions about:
- **ACRRM Training**: Contact [ACRRM](https://www.acrrm.org.au/)
- **This Tool**: Check documentation or create an issue
- **Notion Setup**: See NOTION_SETUP.md

## 🔗 Useful Links

- [ACRRM Website](https://www.acrrm.org.au/)
- [ACRRM Curriculum](https://curriculum.acrrm.org.au/)
- [ACRRM Training Post Search](https://mycollege.acrrm.org.au/search/find-training-post)
- [ANZCA RGA Program](https://www.anzca.edu.au/education-and-training/anaesthesia-training-and-pathways/rural-generalist-anaesthesia-training-program)
- [RANZCOG Training](https://ranzcog.edu.au/training/)

---

**Good luck with your ACRRM Fellowship training! 🎓**
