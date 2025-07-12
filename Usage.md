# 📖 Usage Guide

## Overview

This guide provides step-by-step instructions for using the Compound Analysis Pipeline effectively.

## Stage 1: Data Curation with Jupyter Notebook

### 1. Prepare Your Data

#### Input File Format
Create a CSV file with compound names:

```csv
"Name","Formula","Annot. DeltaMass [ppm]","Calc. MW","RT [min]","Area (Max.)"
"Rhynchophylline","C22 H28 N2 O4","-3.08","384.20372","6.81","23288814985.171"
"Mitragynine","C23 H30 N2 O4","-3.35","398.21922","8.635","14364893452.408"
"deacetylvindoline","C23 H30 N2 O5","-2.8","414.21431","7.443","5066565186.2213"
"L-α-PALMITIN","C19 H38 O4","-3.15","330.27597","14.341","925221458.83439"
"1-Stearoylglycerol","C21 H42 O4","-3.24","358.30715","15.378","693539239.29014"
```

**Required Column:**
- `Name`: Compound names (required)
- `Formula`
- `Calc. MW`

**Optional Columns:**
- Any additional columns (Source, Category, etc.) will be preserved

#### File Naming
- Default expected filename: `compound_data.csv`
- Place in the same directory as the notebook
- Or modify the filename in Cell 2

### 2. Launch Jupyter Notebook

```bash
# Navigate to project directory
cd compound-analysis-pipeline

# Start Jupyter Notebook
jupyter notebook

# Open the notebook
notebooks/curated_compound_swiss_target.ipynb
```

### 3. Execute Notebook Cells

#### Cell 1: Setup and Configuration
```python
# Automatically creates timestamped result folder
# Initializes logging system
# Installs required libraries
```

**Output:** Success message and folder creation

#### Cell 2: Input Data Validation
```python
# Reads your CSV file
# Validates required columns
# Checks for duplicates
# Displays data preview
```

**Output:** Data statistics and preview

#### Cell 3: PubChem API Functions
```python
# Defines functions for PubChem API interaction
# Handles name variations and special characters
# Implements retry mechanisms
```

**Output:** Function definitions loaded

#### Cell 4: Data Processing
```python
# Main processing loop
# Fetches CID and SMILES for each compound
# Handles errors and retries
# Saves intermediate results
```

**Output:** Processing progress and results

#### Cell 5: Quality Control
```python
# Filters successful compounds
# Validates SMILES strings
# Creates clean dataset
# Generates final statistics
```

**Output:** Clean dataset ready for SwissTarget

#### Cell 6: Download Results (Optional)
```python
# Downloads files in Google Colab
# Shows completion message
```

**Output:** Downloaded files (if in Colab)

### 4. Understanding Results

#### Output Files
```
curation_results_2024-01-15_14-30-25/
├── curation_log.txt                    # Detailed processing log
├── compounds_with_cid_smiles.csv       # All results (including failed)
└── data_compounds_final_full.csv     # Clean dataset for SwissTarget
```

#### Result Columns
- `Name`: Original compound name
- `PubChem_CID`: PubChem Compound ID
- `Smiles`: SMILES string representation
- `Status`: Processing status
- Additional columns from input file

#### Status Values
- `Success (Original Name)`: Found using original name
- `Success (Name Variant)`: Found using modified name
- `Failed`: Could not find in PubChem

### 5. Success Rate Optimization

#### Improving Success Rates
1. **Check compound names for typos**
2. **Use standard chemical names**
3. **Avoid proprietary or brand names**
4. **Include synonyms in separate rows**

#### Common Issues
- **Greek letters**: Automatically converted (α → alpha)
- **Special characters**: May cause lookup failures
- **Very new compounds**: May not be in PubChem yet
- **Proprietary names**: Use generic names instead

## Stage 2: SwissTarget Prediction

### 1. Prepare Input File

#### File Setup
1. Use the clean dataset from Stage 1
2. Rename to `data_compounds_final_full.csv`
3. Place in the same directory as `swisstarget.py`

#### Required Columns
- `Name`: Compound name
- `Smiles`: SMILES string

### 2. Run SwissTarget Script

```bash
# Ensure ChromeDriver is available
chromedriver --version

# Run the script
python scripts/swisstarget.py
```

### 3. Manual Interaction Process

#### For Each Compound:
1. **Browser Opens**: Chrome opens with SwissTarget page
2. **Automatic Processing**: Script fills SMILES and submits
3. **Results Display**: Target predictions appear
4. **Manual Action Required**:
   - Download CSV/Excel/PDF files
   - Take screenshots if needed
   - Save to the created compound folder
5. **Close Browser**: Close Chrome to continue to next compound

#### File Organization
```
swisstarget_results_2024-01-15_15-45-30/
├── process_log.txt
├── 001_Quercetin/
│   ├── targets.csv              # Download manually
│   ├── results.xlsx             # Download manually
│   └── screenshot.png           # Optional
├── 002_Kaempferol/
│   └── ...
```

### 4. Understanding SwissTarget Results

#### Target Prediction Columns
- **Target Name**: Protein target name
- **Common Name**: Alternative name
- **Uniprot ID**: Protein database ID
- **ChEMBL ID**: Chemical database ID
- **Target Class**: Protein family/class
- **Probability**: Prediction confidence (0-1)
- **Known Actives**: Number of known active compounds

#### Filtering Recommendations
- **High Probability**: > 0.5 (reliable predictions)
- **Medium Probability**: 0.1-0.5 (potential targets)
- **Low Probability**: < 0.1 (less reliable)

## Best Practices

### 1. Data Preparation
- Clean compound names before processing
- Remove duplicates manually if needed
- Keep backup of original data
- Use consistent naming conventions

### 2. Processing Optimization
- Process in batches for large datasets
- Monitor internet connectivity
- Allow sufficient time for each compound
- Keep detailed logs

### 3. Result Management
- Organize results by date/project
- Document processing parameters
- Keep both raw and cleaned datasets
- Back up important results

### 4. Quality Control
- Verify SMILES strings visually
- Check target predictions for consistency
- Cross-reference with literature
- Validate unexpected results

## Troubleshooting Common Issues

### PubChem Stage Issues

#### Low Success Rate
```
Solutions:
- Check compound name spelling
- Try alternative names
- Verify internet connection
- Check PubChem service status
```

#### Timeout Errors
```
Solutions:
- Increase timeout values in code
- Check network stability
- Retry failed compounds
- Process in smaller batches
```

### SwissTarget Stage Issues

#### ChromeDriver Problems
```
Solutions:
- Update ChromeDriver version
- Check Chrome browser version
- Verify ChromeDriver in PATH
- Try manual ChromeDriver placement
```

#### Browser Automation Failures
```
Solutions:
- Close other Chrome instances
- Check system resources
- Verify SwissTarget website accessibility
- Try different Chrome options
```

## Advanced Usage

### 1. Batch Processing
```python
# Process compounds in batches
batch_size = 10
for i in range(0, len(compounds), batch_size):
    batch = compounds[i:i+batch_size]
    process_batch(batch)
```

### 2. Custom Filtering
```python
# Filter by molecular weight
df_filtered = df[df['MW'] < 500]

# Filter by drug-likeness
df_filtered = df[df['Lipinski_violations'] <= 1]
```

### 3. Results Analysis
```python
# Analyze success rates by compound class
success_by_class = df.groupby('Category')['Status'].value_counts()

# Plot success rates
import matplotlib.pyplot as plt
success_by_class.plot(kind='bar')
```

## Tips for Large Datasets

### 1. Memory Management
- Process in chunks for very large files
- Clear variables when not needed
- Monitor memory usage
- Use appropriate data types

### 2. Error Recovery
- Implement checkpointing
- Save intermediate results
- Log failed compounds for retry
- Use robust error handling

### 3. Performance Optimization
- Use parallel processing where possible
- Optimize API call frequency
- Cache results to avoid re-processing
- Profile code for bottlenecks

## Next Steps

After successful processing:
1. Analyze target prediction results
2. Perform statistical analysis
3. Visualize results
4. Compare with literature data
5. Plan experimental validation

## Support

For additional help:
- Check the [Troubleshooting Guide](troubleshooting.md)
- Review log files for error details
- Search existing GitHub issues
- Create detailed issue reports
