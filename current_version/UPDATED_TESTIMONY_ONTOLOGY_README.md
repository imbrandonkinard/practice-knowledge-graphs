# Updated Testimony Ontology for Protégé

This directory contains an updated TTL (Turtle) file that accurately reflects the detailed testimony data with proper relationships between testifiers, organizations, and bills.

## Files Overview

### 1. `complete_updated_testimony_ontology.ttl` (Recommended for Protégé)
- **Main file to import into Protégé**
- Contains all testimony data with accurate testifier names and bill versions
- Includes proper relationships between individuals, organizations, and testimonies
- Ready for immediate use in Protégé

### 2. `updated_testimony_ontology.ttl` and `updated_testimony_ontology_part2.ttl`
- Split versions of the complete file
- Use these if you need to import testimony data in parts

## Key Improvements in Updated Ontology

### Enhanced Data Model
- **Individual Class**: Separate class for individual testifiers
- **BillVersion Class**: Specific versions of bills (e.g., "HB767 HD2 SD1")
- **Proper Relationships**: Clear connections between individuals, organizations, and testimonies

### Accurate Testifier Information
- **Full Names**: Complete names of all testifiers
- **Organization Affiliations**: Clear links between individuals and their organizations
- **Multiple Testimonies**: Same individuals can testify on different bills
- **Individual vs. Organizational Testimony**: Distinguishes between organizational representatives and individual citizens

### Improved Position Types
- **Support**: General support for the bill
- **Support/Amend**: Support with requested amendments
- **Support/Comment**: Support with comments
- **Strong Support**: Strong endorsement
- **Comment**: Neutral comments
- **Amend/Recommend**: Recommends amendments

## Data Structure

### Bills and Versions
- **HB767 HD2 SD1**: Farm-to-School Program transfer to DOE
- **SB2182 SD1 HD1**: School Garden Coordinator establishment  
- **SB666**: Agricultural Extension Agent positions
- **SB1548**: Procurement threshold increases
- **HB1293**: Procurement reforms for local food

### Organizations (40+ organizations)
#### Government Agencies
- Hawaii Department of Education
- Hawaii Department of Agriculture
- Hawaii Department of Health
- Budget & Finance Dept.
- Hawaii DOE
- State Procurement Office
- Dept. of Attorney General

#### Non-Governmental Organizations
- Hawaii Farm Bureau
- Local Food Coalition
- Hawaii Farm to School Hui
- Ulupono Initiative
- Hawaii Alliance for Progressive Action
- Climate Protectors Hawaii
- 350Hawaii.org
- Blue Zones Project
- Ka Ohana O Na Pua
- And many more...

### Individuals (80+ individuals)
#### Organizational Representatives
- Dr. Christina M. Kishimoto (Hawaii DOE)
- Phyllis Shimabukuro-Geiser (Hawaii DOA)
- Shwe Win (Hawaii State Youth Commission)
- Brian Miyamoto (Hawaii Farm Bureau)
- And many more...

#### Individual Citizens
- cheryl B.
- John Kawamoto
- Fern Anuenue Holland
- Chad Taniguchi
- And many more...

## Key Relationships

### Individual → Organization
- **affiliated_with**: Links individuals to their organizations
- **represents_organization**: Links testimonies to the organization being represented

### Individual → Testimony
- **provides_testimony**: Direct relationship between individual and their testimony

### Testimony → Bill
- **testifies_on**: Links testimony to specific bill version
- **has_position**: Position taken (Support, Support/Amend, etc.)

### Organization → Individual
- Multiple individuals can be affiliated with the same organization
- Same individual can be affiliated with different organizations across different bills

## Sample SPARQL Queries

### Find all individuals who testified on HB767
```sparql
PREFIX : <http://example.org/farm-to-school-ontology#>

SELECT ?individual ?fullName ?position ?organization WHERE {
  ?testimony :provides_testimony ?individual .
  ?testimony :testifies_on :HB767_HD2_SD1 .
  ?testimony :has_position ?position .
  ?individual :hasFullName ?fullName .
  OPTIONAL { ?individual :affiliated_with ?organization }
}
ORDER BY ?fullName
```

### Find all testimonies by Brian Miyamoto
```sparql
PREFIX : <http://example.org/farm-to-school-ontology#>

SELECT ?bill ?position ?organization WHERE {
  ?testimony :provides_testimony :Brian_Miyamoto .
  ?testimony :testifies_on ?bill .
  ?testimony :has_position ?position .
  ?testimony :represents_organization ?organization .
}
```

### Find all organizations with multiple testifiers
```sparql
PREFIX : <http://example.org/farm-to-school-ontology#>

SELECT ?organization (COUNT(DISTINCT ?individual) as ?testifierCount) WHERE {
  ?individual :affiliated_with ?organization .
  ?testimony :provides_testimony ?individual .
  ?testimony :represents_organization ?organization .
}
GROUP BY ?organization
HAVING (COUNT(DISTINCT ?individual) > 1)
ORDER BY DESC(?testifierCount)
```

### Find all individuals who testified on multiple bills
```sparql
PREFIX : <http://example.org/farm-to-school-ontology#>

SELECT ?individual ?fullName (COUNT(DISTINCT ?bill) as ?billCount) WHERE {
  ?testimony :provides_testimony ?individual .
  ?testimony :testifies_on ?bill .
  ?individual :hasFullName ?fullName .
}
GROUP BY ?individual ?fullName
HAVING (COUNT(DISTINCT ?bill) > 1)
ORDER BY DESC(?billCount)
```

## How to Import into Protégé

### Step 1: Open Protégé
1. Launch Protégé
2. Create a new ontology or open an existing one

### Step 2: Import the TTL File
1. Go to **File > Import ontology**
2. Select **complete_updated_testimony_ontology.ttl**
3. Choose import format as "Turtle (TTL)"
4. Click "Import"

### Step 3: Verify Import
1. Check the **Classes** tab for new classes:
   - Testimony
   - Organization
   - Individual
   - Position
   - Bill
   - BillVersion

2. Check the **Object Properties** tab for new properties:
   - provides_testimony
   - testifies_on
   - has_position
   - represents_organization
   - affiliated_with
   - has_version

3. Check the **Data Properties** tab for new properties:
   - hasComments
   - hasSourceFile
   - hasFullName
   - hasVersionIdentifier

4. Check the **Individuals** tab for new individuals organized by:
   - Bills and BillVersions
   - Organizations
   - Individuals (with full names)
   - Positions
   - Testimonies (with complete relationships)

### Step 4: Explore the Enhanced Data
1. Use the **OntoGraf** tab to visualize complex relationships
2. Use the **SPARQL Query** tab to run the sample queries above
3. Use the **Entities** tab to browse individuals and their affiliations

## Key Features for Analysis

### Cross-Bill Analysis
- Same individuals can testify on multiple bills
- Track consistency of positions across bills
- Identify key stakeholders who engage on multiple issues

### Organizational Influence
- Multiple representatives from the same organization
- Organizational positions vs. individual positions
- Track organizational engagement across different bills

### Position Analysis
- Detailed position types beyond simple support/oppose
- Amendment requests and recommendations
- Strong support vs. conditional support

### Source Traceability
- Complete source file references
- Maintains link to original PDF documents
- Enables verification and further research

## Integration with Existing Ontology

The updated testimony ontology integrates with the existing Farm-to-School ontology by:
- Connecting organizations to existing government agencies
- Linking testimonies to existing programs and goals
- Relating bills to existing processes and requirements
- Maintaining compatibility with existing SPARQL queries

## Notes for Analysis

1. **Cross-Reference Individuals**: Same individuals appear across multiple bills with different organizational affiliations
2. **Position Consistency**: Track how individuals' positions change across bills
3. **Organizational Patterns**: Identify which organizations engage most frequently
4. **Amendment Requests**: Focus on testimonies requesting amendments for policy refinement
5. **Individual vs. Organizational**: Distinguish between personal and organizational positions

## Troubleshooting

### Import Issues
- Ensure Protégé supports TTL format (version 5.0+)
- Check file encoding (should be UTF-8)
- Verify file path is accessible

### Missing Relationships
- Check if all TTL files are imported
- Verify namespace prefixes are correct
- Ensure no syntax errors in TTL files

### Query Performance
- Large ontology may load slowly
- Use filters to limit result sets
- Consider using specific bill or individual filters

## Future Enhancements

Potential improvements to consider:
1. Add temporal data (hearing dates)
2. Include committee information
3. Add sentiment analysis of testimonies
4. Create visualization templates for stakeholder networks
5. Add more detailed position subcategories
6. Include testimony length or detail metrics
