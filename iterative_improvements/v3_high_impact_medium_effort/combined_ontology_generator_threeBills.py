#!/usr/bin/env python3
"""
Generate combined ontology from both HB767 (Farm to School) and SB2182 (School Gardens) bills
Creates a comprehensive legislative knowledge graph ontology
"""
import json
from pathlib import Path

def create_combined_ontology():
    """Create combined OWL ontology for both bills"""
    
    owl_content = '''<?xml version="1.0"?>
<rdf:RDF xmlns="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#"
     xml:base="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:xml="http://www.w3.org/XML/1998/namespace"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
    <owl:Ontology rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills">
        <rdfs:comment>Combined ontology for HB767 (Farm to School Program), SB2182 (School Gardens), and SB666 (UH Agriculture Education) bills</rdfs:comment>
        <rdfs:label>Combined Legislative Bills Ontology</rdfs:label>
    </owl:Ontology>
    
    <!-- Object Properties -->
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasPurpose">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Purpose"/>
        <rdfs:comment>Relates a program to its purposes</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasGoal">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Goal"/>
        <rdfs:comment>Relates a program to its goals</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasCoordinator">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Position"/>
        <rdfs:comment>Relates a program to its coordinator position</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasFunding">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Funding"/>
        <rdfs:comment>Relates a program to its funding</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#operatesAt">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Location"/>
        <rdfs:comment>Relates a program to its operating locations</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#serves">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Person"/>
        <rdfs:comment>Relates a program to the people it serves</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#managedBy">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Agency"/>
        <rdfs:comment>Relates a program to the agency that manages it</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#enactedBy">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeBody"/>
        <rdfs:comment>Relates a bill to the legislative body that enacted it</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#references">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegalSection"/>
        <rdfs:comment>Relates a bill to legal sections it references</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#movedFrom">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Agency"/>
        <rdfs:comment>Relates a program to the agency it was moved from</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#movedTo">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Agency"/>
        <rdfs:comment>Relates a program to the agency it was moved to</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#engagesWith">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#InterestGroup"/>
        <rdfs:comment>Relates a program to interest groups it engages with</rdfs:comment>
    </owl:ObjectProperty>
    
    <!-- Data Properties -->
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasConfidence">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#float"/>
        <rdfs:comment>Confidence score for entity extraction</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasText">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Text content of the entity</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasBillNumber">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Bill number identifier</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasSession">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Legislative session identifier</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasEffectiveDate">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Effective date of the bill</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasBillYear">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Calendar year associated with the bill (disambiguates same-number bills across years)</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasMeasureVersion">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Measure version labels such as H.D. 1, S.D. 2, C.D. 1</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasAmount">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Funding"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Funding amount</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasFiscalYear">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Funding"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Fiscal year for funding</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasPercentage">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Goal"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Percentage target for goals</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasTargetYear">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Goal"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Target year for goals</rdfs:comment>
    </owl:DatatypeProperty>
    
    <!-- Classes -->
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity">
        <rdfs:comment>Base class for all extracted entities</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Legislative bill</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Government or educational program</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Agency">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Government agency or department</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeBody">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Legislative body (House, Senate, Legislature)</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Location">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Physical or institutional location</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Person">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Individual person or group of people</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Position">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Job position or role</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Purpose">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Purpose or objective of a program</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Goal">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Target goal or objective</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HealthGoal">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Goal"/>
        <rdfs:comment>Health-related goal or objective</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Funding">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Funding allocation or appropriation</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#EducationalSpace">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Educational space or facility</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegalSection">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Legal section or statute reference</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SessionIdentifier">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Legislative session identifier</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#InterestGroup">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Interest group or stakeholder community</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Statute">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Legal statute or act</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Reporting">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Reporting requirement or obligation</rdfs:comment>
    </owl:Class>

    <!-- New SB666-driven classes -->
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Profession">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Occupational roles such as farmer, agriculture educator, extension agent</rdfs:comment>
    </owl:Class>
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Organization">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Organizations such as University of Hawaii, CTAHR, Cooperative Extension</rdfs:comment>
    </owl:Class>
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#EducationTopic">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Subjects and pathways in education (e.g., agriculture education, CTE)</rdfs:comment>
    </owl:Class>
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#TrainingAction">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Training-related actions (e.g., reduced training, new farmer programs)</rdfs:comment>
    </owl:Class>
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeMeasure">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Measures like S.R. No. 80 (2015), H.B. No. N, S.B. No. N</rdfs:comment>
    </owl:Class>
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AgeStatistic">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Age-related statistics (e.g., average age of farmers)</rdfs:comment>
    </owl:Class>
    
    <!-- Named Individuals - HB767 (Farm to School Program) -->
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HB767">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <hasBillNumber rdf:datatype="http://www.w3.org/2001/XMLSchema#string">HB767</hasBillNumber>
        <hasSession rdf:datatype="http://www.w3.org/2001/XMLSchema#string">THIRTY-FIRST LEGISLATURE, 2021</hasSession>
        <hasEffectiveDate rdf:datatype="http://www.w3.org/2001/XMLSchema#string">July 1, 2021</hasEffectiveDate>
        <enactedBy rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HouseOfRepresentatives"/>
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Chapter302A"/>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HouseOfRepresentatives">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeBody"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">HOUSE OF REPRESENTATIVES</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#FarmToSchoolProgram">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">farm to school program</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
        <managedBy rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#DepartmentOfEducation"/>
        <movedFrom rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#DepartmentOfAgriculture"/>
        <movedTo rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#DepartmentOfEducation"/>
        <hasPurpose rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#ImproveStudentHealth"/>
        <hasPurpose rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#DevelopAgriculturalWorkforce"/>
        <hasPurpose rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#EnrichLocalFoodSystem"/>
        <hasPurpose rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AccelerateEducation"/>
        <hasPurpose rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#ExpandRelationships"/>
        <hasGoal rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#ThirtyPercentGoal"/>
        <operatesAt rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#PublicSchools"/>
        <serves rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Students"/>
        <engagesWith rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AgriculturalCommunities"/>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#DepartmentOfEducation">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Agency"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">department of education</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#DepartmentOfAgriculture">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Agency"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">department of agriculture</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#ThirtyPercentGoal">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Goal"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">thirty per cent</hasText>
        <hasPercentage rdf:datatype="http://www.w3.org/2001/XMLSchema#string">30%</hasPercentage>
        <hasTargetYear rdf:datatype="http://www.w3.org/2001/XMLSchema#string">2030</hasTargetYear>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <!-- Named Individuals - SB2182 (School Gardens) -->
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SB2182">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <hasBillNumber rdf:datatype="http://www.w3.org/2001/XMLSchema#string">SB2182</hasBillNumber>
        <hasSession rdf:datatype="http://www.w3.org/2001/XMLSchema#string">THIRTY-FIRST LEGISLATURE, 2022</hasSession>
        <hasEffectiveDate rdf:datatype="http://www.w3.org/2001/XMLSchema#string">July 1, 2022</hasEffectiveDate>
        <enactedBy rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#TheSenate"/>
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Act175"/>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#TheSenate">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeBody"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">THE SENATE</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SchoolGardenProgram">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">school garden program</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
        <managedBy rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#DepartmentOfEducation"/>
        <hasCoordinator rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SchoolGardenCoordinator"/>
        <hasFunding rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SchoolGardenFunding"/>
        <operatesAt rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#PublicSchools"/>
        <serves rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Students"/>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SchoolGardenCoordinator">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Position"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">school garden coordinator</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SchoolGardenFunding">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Funding"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">$200,000</hasText>
        <hasAmount rdf:datatype="http://www.w3.org/2001/XMLSchema#string">$200,000</hasAmount>
        <hasFiscalYear rdf:datatype="http://www.w3.org/2001/XMLSchema#string">fiscal year 2022-2023</hasFiscalYear>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <!-- Shared Named Individuals -->
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#PublicSchools">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Location"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">public schools</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Students">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Person"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">students</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#ImproveStudentHealth">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HealthGoal"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">improving student health</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#DevelopAgriculturalWorkforce">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Purpose"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">developing an educated agricultural workforce</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AccelerateEducation">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Purpose"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">accelerating garden and farm-based education</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AgriculturalCommunities">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#InterestGroup"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">agricultural communities</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Chapter302A">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegalSection"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">chapter 302a</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Act175">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Statute"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">act 175</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <!-- Additional Purpose Individuals for HB767 -->
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#EnrichLocalFoodSystem">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Purpose"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">enriching the local food system</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>
    
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#ExpandRelationships">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Purpose"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">expanding relationships between schools and agricultural communities</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">0.95</hasConfidence>
    </owl:NamedIndividual>

    <!-- Extensions: Bill packages, reports, and cross-bill links -->
    <!-- Object Properties -->
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#partOfPackage">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#BillPackage"/>
        <rdfs:comment>Indicates that a bill is part of a larger bill package</rdfs:comment>
    </owl:ObjectProperty>
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#referencesBill">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeReport"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:comment>Legislative reports can reference multiple bills</rdfs:comment>
    </owl:ObjectProperty>
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#amends">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:comment>Indicates that one bill amends another bill</rdfs:comment>
    </owl:ObjectProperty>
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#supersedes">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:comment>Indicates that one bill supersedes another bill</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#partOf">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Relates an entity to another entity it is part of</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#relatesTo">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Relates an entity to another entity it relates to</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#worksFor">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Person"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Organization"/>
        <rdfs:comment>Relates a person to an organization they work for</rdfs:comment>
    </owl:ObjectProperty>

    <!-- Classes -->
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#BillPackage">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>A package or bundle of related bills grouped by a theme or initiative</rdfs:comment>
    </owl:Class>
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeReport">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>An organizational legislative report that can reference many bills</rdfs:comment>
    </owl:Class>

    <!-- Data Properties -->
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasFullText">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Full text content of the bill</rdfs:comment>
    </owl:DatatypeProperty>
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasPackageName">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#BillPackage"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Name of the bill package</rdfs:comment>
    </owl:DatatypeProperty>
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasReportTitle">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeReport"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Title of a legislative report</rdfs:comment>
    </owl:DatatypeProperty>

    <!-- Example instances for packages and reports -->
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HealthySchools2021Package">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#BillPackage"/>
        <hasPackageName rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Healthy Schools 2021 Package</hasPackageName>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AgricultureEducationPackage">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#BillPackage"/>
        <hasPackageName rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Agriculture Education 2025 Package</hasPackageName>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#DOEAnnualReport2022">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeReport"/>
        <hasReportTitle rdf:datatype="http://www.w3.org/2001/XMLSchema#string">DOE Annual Legislative Report 2022</hasReportTitle>
        <referencesBill rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HB767"/>
        <referencesBill rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SB2182"/>
    </owl:NamedIndividual>
    
    <!-- Link bills to package -->
    <owl:Axiom>
        <owl:annotatedSource rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HB767"/>
        <owl:annotatedProperty rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#partOfPackage"/>
        <owl:annotatedTarget rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HealthySchools2021Package"/>
    </owl:Axiom>
    <owl:Axiom>
        <owl:annotatedSource rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SB2182"/>
        <owl:annotatedProperty rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#partOfPackage"/>
        <owl:annotatedTarget rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HealthySchools2021Package"/>
    </owl:Axiom>
    <owl:Axiom>
        <owl:annotatedSource rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SB666"/>
        <owl:annotatedProperty rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#partOfPackage"/>
        <owl:annotatedTarget rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AgricultureEducationPackage"/>
    </owl:Axiom>


    <!-- Named Individuals - SB666 (UH / Agriculture Education) -->
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SB666">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <hasBillNumber rdf:datatype="http://www.w3.org/2001/XMLSchema#string">SB666</hasBillNumber>
        <hasSession rdf:datatype="http://www.w3.org/2001/XMLSchema#string">THIRTY-THIRD LEGISLATURE, 2025</hasSession>
        <hasEffectiveDate rdf:datatype="http://www.w3.org/2001/XMLSchema#string">July 31, 2050</hasEffectiveDate>
        <hasBillYear rdf:datatype="http://www.w3.org/2001/XMLSchema#string">2025</hasBillYear>
        <hasMeasureVersion rdf:datatype="http://www.w3.org/2001/XMLSchema#string">S.D. 1</hasMeasureVersion>
        <enactedBy rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#TheSenate"/>
        <!-- SB666 relationships to its entities -->
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#UniversityOfHawaii"/>
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#CTAHR"/>
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#CooperativeExtension"/>
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AgricultureEducation"/>
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#TrainingForAgricultureEducators"/>
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#ExtensionAgents"/>
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SR80_2015"/>
        <references rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AverageFarmerAgeStat"/>
    </owl:NamedIndividual>

    <!-- SB666 domain individuals (representative examples) -->
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#UniversityOfHawaii">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Organization"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">University of Hawaii</hasText>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#CTAHR">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Organization"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">College of Tropical Agriculture and Human Resilience</hasText>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#CooperativeExtension">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Organization"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Cooperative Extension</hasText>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AgricultureEducation">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#EducationTopic"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">agriculture education</hasText>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#TrainingForAgricultureEducators">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#TrainingAction"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">training for agriculture educators</hasText>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#ExtensionAgents">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Profession"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">extension agents</hasText>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SR80_2015">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeMeasure"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">S.R. No. 80 (2015)</hasText>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AverageFarmerAgeStat">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AgeStatistic"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">average farmer is sixty years old</hasText>
    </owl:NamedIndividual>

    <!-- SB666 Entity Relationships -->
    <owl:Axiom>
        <owl:annotatedSource rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#CTAHR"/>
        <owl:annotatedProperty rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#partOf"/>
        <owl:annotatedTarget rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#UniversityOfHawaii"/>
    </owl:Axiom>
    <owl:Axiom>
        <owl:annotatedSource rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#CooperativeExtension"/>
        <owl:annotatedProperty rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#partOf"/>
        <owl:annotatedTarget rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#CTAHR"/>
    </owl:Axiom>
    <owl:Axiom>
        <owl:annotatedSource rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#TrainingForAgricultureEducators"/>
        <owl:annotatedProperty rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#relatesTo"/>
        <owl:annotatedTarget rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#AgricultureEducation"/>
    </owl:Axiom>
    <owl:Axiom>
        <owl:annotatedSource rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#ExtensionAgents"/>
        <owl:annotatedProperty rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#worksFor"/>
        <owl:annotatedTarget rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#CooperativeExtension"/>
    </owl:Axiom>
    <owl:Axiom>
        <owl:annotatedSource rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SR80_2015"/>
        <owl:annotatedProperty rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#referencesBill"/>
        <owl:annotatedTarget rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SB666"/>
    </owl:Axiom>

</rdf:RDF>'''
    
    return owl_content

def main():
    """Generate combined ontology"""
    owl_content = create_combined_ontology()
    
    output_file = 'combined_legislative_bills_ontology_threeBills.owl'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(owl_content)
    
    # Count actual content in the generated ontology
    bill_count = owl_content.count('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HB')
    bill_count += owl_content.count('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SB')
    class_count = owl_content.count('<owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#')
    property_count = owl_content.count('<owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#')
    data_property_count = owl_content.count('<owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#')
    individual_count = owl_content.count('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#')
    
    print(f"Combined ontology created: {output_file}")
    print(f"Ontology includes:")
    print(f"- {class_count} entity classes")
    print(f"- {property_count} object properties")
    print(f"- {data_property_count} data properties")
    print(f"- {individual_count} named individuals")
    print(f"- {bill_count} legislative bills (HB767, SB2182, SB666)")
    print("- Comprehensive relationships across all three bills")
    print("- Shared entities between bills (Department of Education, Students, Public Schools)")
    print("- Bill-specific entities and relationships")
    print("- Cross-bill connections and dependencies")
    print("- SB666 agriculture education entities (University of Hawaii, CTAHR, etc.)")
    print("- Legislative packages (Healthy Schools 2021, Agriculture Education 2025)")

if __name__ == '__main__':
    main()
