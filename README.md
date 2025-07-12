# 🧪 Curated Compound Analysis

A comprehensive pipeline for compound data curation and target prediction analysis using PubChem API and SwissTargetPrediction.

## 📋 Overview

This project provides a two-stage pipeline for compound analysis:

1. **Data Curation Stage**: Extract CID and SMILES from compound names using PubChem API
2. **Target Prediction Stage**: Predict molecular targets using SwissTargetPrediction web interface

## 🚀 Features

- **Automated PubChem Integration**: Fetch compound IDs and SMILES strings from compound names
- **Robust Name Handling**: Supports Greek letters (α, β, γ) and name variations
- **Quality Control**: Validates and cleans data before analysis
- **Comprehensive Logging**: Detailed logs for troubleshooting and monitoring
- **Error Handling**: Retry mechanisms and fallback options
- **Semi-Automated SwissTarget**: Browser automation for target prediction

## 📁 Project Structure

```
curated_compound_analysis/
├── notebooks/
│   └── curated_compound_swiss_target.ipynb
├── scripts/
│   └── swisstarget.py
├── data/
│   └── compound_sample_data.csv
├── requirements.txt
├── README.md
└── docs/
    ├── installation.md
    ├── usage.md
    └── troubleshooting.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- Google Chrome browser (for SwissTarget automation)
- ChromeDriver (see [ChromeDriver Setup](#chromedriver-setup))

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/curated_compound_analysis.git
cd curated_compound_analysis
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: ChromeDriver Setup

#### Option A: Automatic Installation (Recommended)
The script will automatically download ChromeDriver using `webdriver-manager`.

#### Option B: Manual Installation
1. Check your Chrome version: `chrome://version/`
2. Download matching ChromeDriver from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
3. Extract and place `chromedriver.exe` in the project folder

#### Option C: System PATH Installation
1. Download ChromeDriver
2. Add to system PATH
3. Verify: `chromedriver --version`

## 📊 Usage

### Stage 1: Data Curation (Jupyter Notebook)

1. **Prepare Input Data**
   - Create CSV file with compound names in 'Name' column
   - Example: `compound_data.csv`

2. **Run Curation Notebook**
   ```bash
   jupyter notebook notebooks/curated_compound_swiss_target.ipynb
   ```

3. **Execute All Cells**
   - Cell 1: Setup and configuration
   - Cell 2: Input data validation
   - Cell 3: PubChem API functions
   - Cell 4: Data processing and CID/SMILES extraction
   - Cell 5: Quality control and cleaning
   - Cell 6: Download results (optional)

4. **Output Files**
   - `compounds_with_cid_smiles.csv`: All processing results
   - `data_compounds_final_full.csv`: Clean dataset for SwissTarget
   - `curation_log.txt`: Detailed processing log

### Stage 2: SwissTarget Prediction (Python Script)

1. **Prepare Input**
   - Use the clean dataset from Stage 1
   - Rename to `data_compounds_final_full.csv`

2. **Run SwissTarget Script**
   ```bash
   python scripts/swisstarget.py
   ```

3. **Manual Interaction Required**
   - Script opens Chrome browser for each compound
   - Download results manually (CSV/Excel/PDF)
   - Take screenshots as needed
   - Close browser to continue to next compound

4. **Output Organization**
   - Results saved in timestamped folders
   - Individual folders for each compound
   - Processing logs included

## 📋 Input Data Format

Your input CSV should have this structure:   
#### "Name","Formula","Calc. MW" => must have this.
```csv
"Name","Formula","Annot. DeltaMass [ppm]","Calc. MW","RT [min]","Area (Max.)"
"Rhynchophylline","C22 H28 N2 O4","-3.08","384.20372","6.81","23288814985.171"
"Mitragynine","C23 H30 N2 O4","-3.35","398.21922","8.635","14364893452.408"
"deacetylvindoline","C23 H30 N2 O5","-2.8","414.21431","7.443","5066565186.2213"
"L-α-PALMITIN","C19 H38 O4","-3.15","330.27597","14.341","925221458.83439"
"1-Stearoylglycerol","C21 H42 O4","-3.24","358.30715","15.378","693539239.29014"
```

Additional columns are preserved in the output.

## 🔧 Configuration

### PubChem API Settings
- Request delay: 0.5 seconds (respects rate limits)
- Timeout: 20 seconds per request
- Retry mechanism: Name variations for better success rates

### SwissTarget Settings
- Browser timeout: 60 seconds for page load
- Results timeout: 240 seconds for predictions
- Retry attempts: 3 per compound
- Target organism: Homo sapiens (default)

## 📈 Success Rates

Typical success rates based on compound types:
- **Well-known compounds**: 85-95%
- **Natural products**: 70-85%
- **Synthetic compounds**: 60-80%
- **Rare/proprietary compounds**: 40-60%

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver Version Mismatch**
   ```
   Solution: Update ChromeDriver to match your Chrome version
   ```

2. **PubChem API Timeout**
   ```
   Solution: Check internet connection, compound names for typos
   ```

3. **SwissTarget Page Load Issues**
   ```
   Solution: Retry with stable internet, check if website is accessible
   ```

4. **Missing Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Debug Information

Enable detailed logging by checking the generated log files:
- `curation_log.txt`: PubChem processing logs
- `process_log.txt`: SwissTarget automation logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PubChem](https://pubchem.ncbi.nlm.nih.gov/) for compound data API
- [SwissTargetPrediction](http://www.swisstargetprediction.ch/) for target prediction service
- [Selenium](https://selenium.dev/) for web automation
- [ChromeDriver](https://chromedriver.chromium.org/) for browser automation

## 📞 Support

If you encounter issues or have questions:
1. Check the [troubleshooting guide](docs/troubleshooting.md)
2. Search existing [issues](https://github.com/yourusername/curated_compound_analysis/issues)
3. Create a new issue with detailed information

## 📊 Citation

If you use this pipeline in your research, please cite:

```bibtex
@software{curated_compound_analysis,
  title={Compound Analysis Pipeline: Automated PubChem and SwissTarget Integration},
  author={Nandatama, Engki},
  year={2024},
  url={https://github.com/yourusername/curated_compound_analysis}
}
```

---

⭐ **Star this repository if you find it helpful!** ⭐
