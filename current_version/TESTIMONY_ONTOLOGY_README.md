# Testimony Ontology for Protégé

This directory contains TTL (Turtle) files that extend the existing Farm-to-School ontology with comprehensive testimony data extracted from legislative hearings.

## Files Overview

### 1. `complete_testimony_ontology.ttl` (Recommended for Protégé)
- **Main file to import into Protégé**
- Contains all testimony data in a single, well-organized file
- Includes new classes, properties, and individuals
- Ready for immediate use in Protégé

### 2. `testimony_data.ttl` and `testimony_data_part2.ttl`
- Split versions of the complete file
- Use these if you need to import testimony data in parts
- Contains the same data as the complete file

## New Ontology Components

### Classes Added
- **Testimony**: Represents legislative testimony provided on bills
- **Organization**: Organizations and institutions that provide testimony  
- **Position**: Stance or position taken in testimony (Support, Support w/ Amendment, etc.)
- **Bill**: Legislative bills under consideration

### Object Properties Added
- **provides_testimony**: Links organizations to their testimonies
- **testifies_on**: Links testimonies to specific bills
- **has_position**: Links testimonies to positions taken
- **has_source**: Links testimonies to source documents

### Data Properties Added
- **hasComments**: Contains the main comments or rationale from testimony
- **hasSourceFile**: Contains the source file reference

## Bills Covered

1. **HB767_SD1** - Farm-to-School Program transfer to DOE
2. **SB2182_HD1** - School Garden Coordinator establishment
3. **SB666** - Agricultural Extension Agent positions
4. **SB1548** - Procurement threshold increases
5. **HB1293** - Procurement reforms for local food

## Organizations Included

### Government Agencies
- Department of Education (DOE)
- Department of Agriculture (DOA)
- Department of Health
- Department of Budget and Finance
- State Procurement Office

### Non-Governmental Organizations
- Hawaii Farm Bureau
- Local Food Coalition
- Hawaii Farm to School Hui
- Ulupono Initiative
- Hawaii Alliance for Progressive Action (HAPA)
- Climate Protectors Hawaii
- And many more...

### Individual Testifiers
- Various individual citizens and advocates

## How to Import into Protégé

### Step 1: Open Protégé
1. Launch Protégé
2. Create a new ontology or open an existing one

### Step 2: Import the TTL File
1. Go to **File > Import ontology**
2. Select **complete_testimony_ontology.ttl**
3. Choose import format as "Turtle (TTL)"
4. Click "Import"

### Step 3: Verify Import
1. Check the **Classes** tab for new classes:
   - Testimony
   - Organization
   - Position
   - Bill

2. Check the **Object Properties** tab for new properties:
   - provides_testimony
   - testifies_on
   - has_position
   - has_source

3. Check the **Data Properties** tab for new properties:
   - hasComments
   - hasSourceFile

4. Check the **Individuals** tab for new individuals organized by:
   - Bills (HB767_SD1, SB2182_HD1, etc.)
   - Organizations (various organizations)
   - Positions (Support, Support w/ Amendment, etc.)
   - Testimonies (individual testimony instances)

### Step 4: Explore the Data
1. Use the **OntoGraf** tab to visualize relationships
2. Use the **SPARQL Query** tab to query the data
3. Use the **Entities** tab to browse all entities

## Sample SPARQL Queries

### Find all testimonies supporting HB767_SD1
```sparql
PREFIX : <http://example.org/farm-to-school-ontology#>

SELECT ?testimony ?organization ?comments WHERE {
  ?testimony :testifies_on :HB767_SD1 .
  ?testimony :has_position :Support .
  ?testimony :provides_testimony ?organization .
  ?testimony :hasComments ?comments .
}
```

### Find all organizations that provided testimony
```sparql
PREFIX : <http://example.org/farm-to-school-ontology#>

SELECT DISTINCT ?organization ?label WHERE {
  ?testimony :provides_testimony ?organization .
  ?organization rdfs:label ?label .
}
ORDER BY ?label
```

### Find testimonies mentioning "30%" goal
```sparql
PREFIX : <http://example.org/farm-to-school-ontology#>

SELECT ?testimony ?organization ?comments WHERE {
  ?testimony :provides_testimony ?organization .
  ?testimony :hasComments ?comments .
  FILTER(CONTAINS(?comments, "30%"))
}
```

## Data Structure

Each testimony includes:
- **Organization/Person**: Who provided the testimony
- **Bill**: Which bill the testimony addresses
- **Position**: Support, Support w/ Amendment, Comments, etc.
- **Comments**: Main rationale and comments
- **Source**: Original PDF file reference

## Integration with Existing Ontology

The testimony data integrates with the existing Farm-to-School ontology by:
- Connecting organizations to existing government agencies
- Linking testimonies to existing programs and goals
- Relating bills to existing processes and requirements

## Notes for Analysis

1. **Position Analysis**: Most testimonies are supportive, with some requesting amendments
2. **Key Themes**: Local sourcing goals, procurement reforms, garden education, workforce development
3. **Stakeholder Engagement**: Wide range of organizations from government to NGOs to individuals
4. **Policy Alignment**: Testimonies show strong support for farm-to-school initiatives

## Troubleshooting

### Import Issues
- Ensure Protégé supports TTL format (version 5.0+)
- Check file encoding (should be UTF-8)
- Verify file path is accessible

### Missing Data
- Check if all TTL files are imported
- Verify namespace prefixes are correct
- Ensure no syntax errors in TTL files

### Performance
- Large ontology may load slowly
- Consider using SPARQL queries for specific data extraction
- Use filters to limit result sets

## Future Enhancements

Potential improvements to consider:
1. Add temporal data (hearing dates)
2. Include committee information
3. Add sentiment analysis of testimonies
4. Create visualization templates
5. Add more detailed position categories
