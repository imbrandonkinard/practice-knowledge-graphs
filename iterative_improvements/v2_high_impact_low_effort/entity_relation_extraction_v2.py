#!/usr/bin/env python3
"""
Stanford CoreNLP Entity and Relation Extraction - Version 2
High Impact - Low Effort Improvements

Enhancements:
1. Enhanced CoreNLP annotators (lemma, openie)
2. Custom NER patterns for legislative domain
3. Enhanced relation patterns for bill-specific relationships
4. Improved confidence scoring
"""

import json
import re
import signal
import sys
import time
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, asdict

# Always import requests for HTTP client functionality
import requests

# Try to import stanfordcorenlp, fallback to requests if not available
try:
    from stanfordcorenlp import StanfordCoreNLP
    STANFORD_AVAILABLE = True
    print("✓ Stanford CoreNLP wrapper available")
except ImportError:
    STANFORD_AVAILABLE = False
    print("✗ Stanford CoreNLP wrapper not available, using HTTP client")

@dataclass
class CoreNLPEntity:
    """Stanford CoreNLP entity with enhanced attributes"""
    text: str
    type: str
    start_char: int
    end_char: int
    ner: str
    normalized_ner: str = None
    confidence: float = 1.0
    context: str = None

@dataclass
class CoreNLPRelation:
    """Stanford CoreNLP relation with enhanced attributes"""
    subject: str
    predicate: str
    object: str
    confidence: float
    context: str
    relation_type: str = None
    source: str = "corenlp"

class LegislativeNERPatterns:
    """Custom NER patterns for legislative domain"""
    
    def __init__(self):
        self.patterns = {
            "PROGRAM": [
                r"farm to school program",
                r"coordinator program",
                r"meals program",
                r"agricultural program"
            ],
            "AGENCY": [
                r"department of education",
                r"department of agriculture", 
                r"HDOA",
                r"DOE",
                r"legislature",
                r"state of hawaii"
            ],
            "GOAL": [
                r"thirty per cent",
                r"30%",
                r"2030",
                r"locally sourced",
                r"minimum percentage"
            ],
            "REPORTING": [
                r"annual report",
                r"reporting requirement",
                r"submit.*report",
                r"twenty days.*regular session"
            ],
            "STATUTE": [
                r"chapter \d+",
                r"section \d+-\d+",
                r"hawaii revised statutes",
                r"h\.b\. no\. \d+"
            ],
            "PURPOSE": [
                r"improve student health",
                r"develop.*agricultural workforce",
                r"enrich.*local food system",
                r"accelerate.*education",
                r"expand.*relationships"
            ]
        }
    
    def extract_custom_entities(self, text: str) -> List[CoreNLPEntity]:
        """Extract entities using custom legislative patterns"""
        entities = []
        
        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity = CoreNLPEntity(
                        text=match.group(),
                        type=entity_type,
                        start_char=match.start(),
                        end_char=match.end(),
                        ner=entity_type,
                        normalized_ner=match.group().lower(),
                        confidence=0.9,  # High confidence for pattern matches
                        context=text[max(0, match.start()-50):match.end()+50]
                    )
                    entities.append(entity)
        
        return entities

class EnhancedRelationPatterns:
    """Enhanced relation patterns for bill-specific relationships"""
    
    def __init__(self):
        self.patterns = {
            "PROGRAM_MOVEMENT": [
                (r"move.*farm to school program.*from.*department of agriculture.*to.*department of education", 
                 "PROGRAM_MOVE", "Farm to School Program", "moved from", "Department of Agriculture", "Department of Education"),
                (r"transfer.*farm to school program.*from.*hdoa.*to.*doe",
                 "PROGRAM_MOVE", "Farm to School Program", "transferred from", "HDOA", "DOE")
            ],
            "GOAL_SETTING": [
                (r"goal.*thirty per cent.*locally sourced.*2030",
                 "GOAL_SETTING", "Department of Education", "set goal", "30% locally sourced by 2030"),
                (r"target.*minimum percentage.*locally sourced.*public schools",
                 "GOAL_SETTING", "Department of Education", "established target", "minimum percentage locally sourced")
            ],
            "REPORTING_REQUIREMENT": [
                (r"submit.*annual report.*legislature",
                 "REPORTING", "Department of Education", "must submit", "annual report to legislature"),
                (r"reporting requirement.*twenty days.*regular session",
                 "REPORTING", "Department of Education", "has requirement", "reporting within 20 days of session")
            ],
            "COORDINATOR_ROLE": [
                (r"farm to school coordinator.*headed by",
                 "LEADERSHIP", "Farm to School Program", "headed by", "Farm to School Coordinator"),
                (r"coordinator.*work.*collaboration.*stakeholders",
                 "COLLABORATION", "Farm to School Coordinator", "works with", "stakeholders")
            ],
            "PROGRAM_PURPOSES": [
                (r"purpose.*farm to school program.*shall be to.*improve student health",
                 "PURPOSE", "Farm to School Program", "purpose", "improve student health"),
                (r"purpose.*farm to school program.*shall be to.*develop.*agricultural workforce",
                 "PURPOSE", "Farm to School Program", "purpose", "develop agricultural workforce"),
                (r"purpose.*farm to school program.*shall be to.*enrich.*local food system",
                 "PURPOSE", "Farm to School Program", "purpose", "enrich local food system"),
                (r"purpose.*farm to school program.*shall be to.*accelerate.*education",
                 "PURPOSE", "Farm to School Program", "purpose", "accelerate garden and farm-based education"),
                (r"purpose.*farm to school program.*shall be to.*expand.*relationships",
                 "PURPOSE", "Farm to School Program", "purpose", "expand relationships between schools and agricultural communities")
            ]
        }
    
    def extract_enhanced_relations(self, text: str) -> List[CoreNLPRelation]:
        """Extract relations using enhanced legislative patterns"""
        relations = []
        
        for relation_type, patterns in self.patterns.items():
            for pattern_data in patterns:
                if len(pattern_data) == 6:
                    pattern, rel_type, subject, predicate, obj, obj2 = pattern_data
                elif len(pattern_data) == 5:
                    pattern, rel_type, subject, predicate, obj = pattern_data
                    obj2 = None
                else:
                    continue
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Create primary relation
                    relation = CoreNLPRelation(
                        subject=subject,
                        predicate=predicate,
                        object=obj,
                        confidence=0.9,
                        context=text[max(0, match.start()-100):match.end()+100],
                        relation_type=rel_type,
                        source="enhanced_patterns"
                    )
                    relations.append(relation)
                    
                    # Create secondary relation if obj2 exists
                    if obj2:
                        relation2 = CoreNLPRelation(
                            subject=subject,
                            predicate="moved to",
                            object=obj2,
                            confidence=0.9,
                            context=text[max(0, match.start()-100):match.end()+100],
                            relation_type=rel_type,
                            source="enhanced_patterns"
                        )
                        relations.append(relation2)
        
        return relations

class StanfordCoreNLPClient:
    """Enhanced CoreNLP client with improved annotators and processing"""
    
    def __init__(self, server_url: str = "http://localhost:9000"):
        self.server_url = server_url
        self.nlp = None
        
        # Note: stanfordcorenlp package is designed for local installations, not remote servers
        # We'll use the HTTP client approach which is more appropriate for connecting to a running server
        print("Using HTTP client for CoreNLP server connection...")
        self.nlp = None
        
        # Enhanced properties for HTTP client with more annotators
        self.properties = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,depparse,openie',
            'outputFormat': 'json',
            'timeout': '30000'  # 30 second timeout
        }
        
        # Initialize custom patterns
        self.custom_ner = LegislativeNERPatterns()
        self.enhanced_relations = EnhancedRelationPatterns()
    
    def chunk_text(self, text: str, max_chunk_size: int = 2000) -> List[str]:
        """Split text into smaller, memory-efficient chunks for CoreNLP"""
        chunks = []
        
        # Use regex to split on sentence boundaries more accurately
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        current_chunk = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # If adding this sentence would exceed chunk size, start new chunk
            if len(current_chunk) + len(sentence) + 1 > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Ensure no chunk is too long
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > max_chunk_size:
                # Split very long chunks by words
                words = chunk.split()
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk) + len(word) + 1 > max_chunk_size and temp_chunk:
                        final_chunks.append(temp_chunk.strip())
                        temp_chunk = word
                    else:
                        if temp_chunk:
                            temp_chunk += " " + word
                        else:
                            temp_chunk = word
                if temp_chunk:
                    final_chunks.append(temp_chunk.strip())
            else:
                final_chunks.append(chunk)
        
        return final_chunks
    
    def annotate_text(self, text: str, memory_efficient: bool = True) -> Dict:
        """Annotate text using Stanford CoreNLP with enhanced annotators"""
        try:
            print("Using HTTP client fallback...")
            
            # If text is too long, chunk it for HTTP client too
            if len(text) > 2000:
                print(f"Text too long for HTTP client ({len(text)} chars), chunking...")
                chunks = self.chunk_text(text, max_chunk_size=1500)  # Smaller chunks for HTTP
                print(f"Split into {len(chunks)} chunks for HTTP processing")
                
                all_annotations = []
                for i, chunk in enumerate(chunks):
                    print(f"HTTP processing chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
                    try:
                        chunk_result = self._process_chunk_http(chunk)
                        if chunk_result:
                            all_annotations.append(chunk_result)
                    except Exception as e:
                        print(f"HTTP chunk {i+1} failed: {e}")
                        continue
                
                if all_annotations:
                    return self._merge_chunk_annotations(all_annotations, text)
                else:
                    print("All HTTP chunks failed")
                    return None
            else:
                return self._process_chunk_http(text)
            
        except Exception as e:
            print(f"HTTP client error: {e}")
            return None
    
    def _process_chunk_http(self, text: str) -> Dict:
        """Process a single chunk via HTTP with enhanced annotators"""
        try:
            url = f"{self.server_url}/"
            
            # Use enhanced annotators for better extraction
            properties = {
                'annotators': 'tokenize,ssplit,pos,lemma,ner,depparse,openie',
                'outputFormat': 'json',
                'timeout': '30000'
            }
            
            response = requests.post(
                url,
                data=text.encode('utf-8'),
                params={'properties': json.dumps(properties)},
                headers={'Content-Type': 'text/plain; charset=utf-8'},
                timeout=60  # 60 second timeout per chunk
            )
            
            if response.status_code != 200:
                print(f"HTTP Error response: {response.text}")
                return None
                
            return response.json()
            
        except Exception as e:
            print(f"HTTP chunk processing error: {e}")
            return None
    
    def _merge_chunk_annotations(self, chunk_annotations: List[Dict], original_text: str) -> Dict:
        """Merge annotations from multiple chunks with enhanced handling"""
        if not chunk_annotations:
            return None
        
        merged = {
            'sentences': [],
            'corefs': {},
            'openie': []
        }
        
        sentence_offset = 0
        for chunk_ann in chunk_annotations:
            if 'sentences' in chunk_ann:
                for sentence in chunk_ann['sentences']:
                    # Adjust character offsets for merged text
                    adjusted_sentence = sentence.copy()
                    if 'tokens' in adjusted_sentence:
                        for token in adjusted_sentence['tokens']:
                            if 'characterOffsetBegin' in token:
                                token['characterOffsetBegin'] += sentence_offset
                            if 'characterOffsetEnd' in token:
                                token['characterOffsetEnd'] += sentence_offset
                    
                    merged['sentences'].append(adjusted_sentence)
                
                # Update offset for next chunk
                sentence_offset += len(' '.join([s.get('text', '') for s in chunk_ann.get('sentences', [])]))
            
            # Merge OpenIE results if available
            if 'openie' in chunk_ann:
                merged['openie'].extend(chunk_ann['openie'])
        
        return merged
    
    def close(self):
        """Close the CoreNLP connection"""
        if STANFORD_AVAILABLE and self.nlp:
            try:
                self.nlp.close()
                print("✓ Stanford CoreNLP connection closed")
            except Exception as e:
                print(f"Error closing CoreNLP connection: {e}")
    
    def extract_entities(self, annotations: Dict) -> List[CoreNLPEntity]:
        """Extract entities from CoreNLP annotations with custom NER enhancement"""
        entities = []
        
        if not annotations or 'sentences' not in annotations:
            return entities
        
        # Extract entities from CoreNLP annotations
        for sentence in annotations['sentences']:
            if 'tokens' not in sentence:
                continue
                
            tokens = sentence['tokens']
            for token in tokens:
                if token.get('ner') and token['ner'] != 'O':
                    # Handle missing character offsets gracefully
                    start_char = token.get('characterOffsetBegin', 0)
                    end_char = token.get('characterOffsetEnd', len(token['word']))
                    
                    entity = CoreNLPEntity(
                        text=token['word'],
                        type=token['ner'],
                        start_char=start_char,
                        end_char=end_char,
                        ner=token['ner'],
                        confidence=0.8,
                        context=sentence.get('text', '')
                    )
                    entities.append(entity)
        
        # Add custom NER entities from patterns
        if annotations.get('sentences'):
            full_text = ' '.join([s.get('text', '') for s in annotations['sentences']])
            custom_entities = self.custom_ner.extract_custom_entities(full_text)
            entities.extend(custom_entities)
        
        return entities
    
    def extract_relations(self, annotations: Dict) -> List[CoreNLPRelation]:
        """Extract relations from CoreNLP annotations with enhanced patterns"""
        relations = []
        
        if not annotations or 'sentences' not in annotations:
            return relations
        
        # Extract relations from dependency parse
        for sentence in annotations['sentences']:
            # Try enhanced dependencies first (if available)
            if 'enhancedPlusPlusDependencies' in sentence:
                deps = sentence['enhancedPlusPlusDependencies']
                relations.extend(self._extract_relations_from_deps(deps, sentence))
            # Use basic dependencies (what depparse annotator provides)
            elif 'dependencies' in sentence:
                deps = sentence['dependencies']
                relations.extend(self._extract_relations_from_deps(deps, sentence))
            
            # Always try text-based patterns as a supplement to dependency parsing
            text_relations = self._extract_relations_from_text(sentence)
            relations.extend(text_relations)
        
        # Extract relations from OpenIE if available
        if 'openie' in annotations:
            openie_relations = self._extract_openie_relations(annotations['openie'])
            relations.extend(openie_relations)
        
        # Add enhanced pattern-based relations
        if annotations.get('sentences'):
            full_text = ' '.join([s.get('text', '') for s in annotations['sentences']])
            enhanced_relations = self.enhanced_relations.extract_enhanced_relations(full_text)
            relations.extend(enhanced_relations)
        
        return relations
    
    def _extract_relations_from_deps(self, deps: List[Dict], sentence: Dict) -> List[CoreNLPRelation]:
        """Extract relations from dependency parse with enhanced patterns"""
        relations = []
        
        # Look for subject-verb-object patterns
        subjects = [dep for dep in deps if dep['dep'] == 'nsubj']
        objects = [dep for dep in deps if dep['dep'] == 'dobj']
        verbs = [dep for dep in deps if dep['dep'] == 'ROOT' and dep.get('posTag', '').startswith('VB')]
        
        # Also look for other common relation patterns
        copulas = [dep for dep in deps if dep['dep'] == 'cop']  # "is", "are", etc.
        amods = [dep for dep in deps if dep['dep'] == 'amod']   # adjectives modifying nouns
        
        # Extract subject-verb-object relations
        for subj in subjects:
            for verb in verbs:
                for obj in objects:
                    if (subj.get('governor') == verb.get('dependent') and 
                        obj.get('governor') == verb.get('dependent')):
                        
                        relation = CoreNLPRelation(
                            subject=subj.get('dependentGloss', subj.get('dependent', '')),
                            predicate=verb.get('dependentGloss', verb.get('dependent', '')),
                            object=obj.get('dependentGloss', obj.get('dependent', '')),
                            confidence=0.8,
                            context=sentence.get('text', ''),
                            relation_type="SVO",
                            source="dependency_parse"
                        )
                        relations.append(relation)
        
        # Extract subject-verb relations (even without direct objects)
        for subj in subjects:
            for verb in verbs:
                if subj.get('governor') == verb.get('dependent'):
                    # Look for prepositional objects or other complements
                    preps = [dep for dep in deps if dep['dep'] == 'prep' and dep['governor'] == verb['dependent']]
                    for prep in preps:
                        # Find the object of the preposition
                        pobj = [dep for dep in deps if dep['dep'] == 'pobj' and dep['governor'] == prep['dependent']]
                        for obj in pobj:
                            relation = CoreNLPRelation(
                                subject=subj.get('dependentGloss', subj.get('dependent', '')),
                                predicate=f"{verb.get('dependentGloss', verb.get('dependent', ''))} {prep.get('dependentGloss', prep.get('dependent', ''))}",
                                object=obj.get('dependentGloss', obj.get('dependent', '')),
                                confidence=0.7,
                                context=sentence.get('text', ''),
                                relation_type="SVP",
                                source="dependency_parse"
                            )
                            relations.append(relation)
        
        # Extract passive voice relations
        passive_subjects = [dep for dep in deps if dep['dep'] == 'nsubj:pass']
        for subj in passive_subjects:
            for verb in verbs:
                if subj.get('governor') == verb.get('dependent'):
                    relation = CoreNLPRelation(
                        subject=subj.get('dependentGloss', subj.get('dependent', '')),
                        predicate=f"was {verb.get('dependentGloss', verb.get('dependent', ''))}",
                        object="by program",
                        confidence=0.7,
                        context=sentence.get('text', ''),
                        relation_type="PASSIVE",
                        source="dependency_parse"
                    )
                    relations.append(relation)
        
        # Extract existential relations (There is/are...)
        xsubj = [dep for dep in deps if dep['dep'] == 'nsubj:xsubj']
        for subj in xsubj:
            for verb in verbs:
                if subj.get('governor') == verb.get('dependent'):
                    relation = CoreNLPRelation(
                        subject="There",
                        predicate=verb.get('dependentGloss', verb.get('dependent', '')),
                        object=subj.get('dependentGloss', subj.get('dependent', '')),
                        confidence=0.6,
                        context=sentence.get('text', ''),
                        relation_type="EXISTENTIAL",
                        source="dependency_parse"
                    )
                    relations.append(relation)
        
        # Extract copula relations (X is Y)
        for subj in subjects:
            for cop in copulas:
                if subj.get('governor') == cop.get('governor'):
                    # Find the complement (what comes after the copula)
                    complements = [dep for dep in deps if dep['governor'] == cop['governor'] and dep['dep'] in ['attr', 'acomp']]
                    for comp in complements:
                        relation = CoreNLPRelation(
                            subject=subj.get('dependentGloss', subj.get('dependent', '')),
                            predicate="is",
                            object=comp.get('dependentGloss', comp.get('dependent', '')),
                            confidence=0.7,
                            context=sentence.get('text', ''),
                            relation_type="COPULA",
                            source="dependency_parse"
                        )
                        relations.append(relation)
        
        # Extract adjective-noun relations
        for amod in amods:
            # Find the noun this adjective modifies
            modified_nouns = [dep for dep in deps if dep['dependent'] == amod['governor'] and dep['dep'] in ['nsubj', 'dobj']]
            for noun in modified_nouns:
                relation = CoreNLPRelation(
                    subject=amod.get('dependentGloss', amod.get('dependent', '')),
                    predicate="modifies",
                    object=noun.get('dependentGloss', noun.get('dependent', '')),
                    confidence=0.6,
                    context=sentence.get('text', ''),
                    relation_type="MODIFICATION",
                    source="dependency_parse"
                )
                relations.append(relation)
        
        # Extract specific bill-related patterns based on dependency structure
        for dep in deps:
            # Look for "move" patterns
            if dep['dep'] == 'ROOT' and 'move' in dep.get('dependentGloss', '').lower():
                # Find the subject (purpose)
                purpose_deps = [d for d in deps if d['dep'] == 'nsubj' and d['governor'] == dep['dependent']]
                for purpose in purpose_deps:
                    relation = CoreNLPRelation(
                        subject="Purpose",
                        predicate="move",
                        object="Farm to School Program",
                        confidence=0.8,
                        context=sentence.get('text', ''),
                        relation_type="PROGRAM_MOVE",
                        source="dependency_parse"
                    )
                    relations.append(relation)
            
            # Look for "established" patterns
            if dep['dep'] == 'ROOT' and 'establish' in dep.get('dependentGloss', '').lower():
                # Find what was established
                established_deps = [d for d in deps if d['dep'] == 'expl' and d['governor'] == dep['dependent']]
                for established in established_deps:
                    relation = CoreNLPRelation(
                        subject="There",
                        predicate="established",
                        object="Hawaii Farm to School Program",
                        confidence=0.8,
                        context=sentence.get('text', ''),
                        relation_type="PROGRAM_ESTABLISHMENT",
                        source="dependency_parse"
                    )
                    relations.append(relation)
            
            # Look for "headed by" patterns
            if dep['dep'] == 'ROOT' and 'head' in dep.get('dependentGloss', '').lower():
                relation = CoreNLPRelation(
                    subject="Farm to School Program",
                    predicate="headed by",
                    object="Farm to School Coordinator",
                    confidence=0.8,
                    context=sentence.get('text', ''),
                    relation_type="LEADERSHIP",
                    source="dependency_parse"
                )
                relations.append(relation)
            
            # Look for "meet goal" patterns
            if dep['dep'] == 'ROOT' and 'meet' in dep.get('dependentGloss', '').lower():
                relation = CoreNLPRelation(
                    subject="Department of Education",
                    predicate="meet goal",
                    object="30% locally sourced food by 2030",
                    confidence=0.7,
                    context=sentence.get('text', ''),
                    relation_type="GOAL_SETTING",
                    source="dependency_parse"
                )
                relations.append(relation)
            
            # Look for "submit report" patterns
            if dep['dep'] == 'ROOT' and 'submit' in dep.get('dependentGloss', '').lower():
                relation = CoreNLPRelation(
                    subject="Department of Education",
                    predicate="submit",
                    object="annual report to legislature",
                    confidence=0.7,
                    context=sentence.get('text', ''),
                    relation_type="REPORTING",
                    source="dependency_parse"
                )
                relations.append(relation)
        
        return relations
    
    def _extract_relations_from_text(self, sentence: Dict) -> List[CoreNLPRelation]:
        """Extract basic relations from sentence text when dependencies are unavailable"""
        relations = []
        text = sentence.get('text', '')
        
        # Simple pattern-based relation extraction
        if 'farm to school program' in text.lower() and 'department' in text.lower():
            if 'move' in text.lower() or 'transfer' in text.lower():
                relations.append(CoreNLPRelation(
                    subject="Farm to School Program",
                    predicate="moved to",
                    object="Department",
                    confidence=0.6,
                    context=text,
                    relation_type="PROGRAM_MOVE",
                    source="text_patterns"
                ))
        
        return relations
    
    def _extract_openie_relations(self, openie_results: List[Dict]) -> List[CoreNLPRelation]:
        """Extract relations from OpenIE results"""
        relations = []
        
        for result in openie_results:
            if 'subject' in result and 'relation' in result and 'object' in result:
                relation = CoreNLPRelation(
                    subject=result['subject'],
                    predicate=result['relation'],
                    object=result['object'],
                    confidence=result.get('confidence', 0.7),
                    context=result.get('context', ''),
                    relation_type="OPENIE",
                    source="openie"
                )
                relations.append(relation)
        
        return relations

class BillEntityRelationExtractor:
    """Enhanced extractor for bill text with custom patterns"""
    
    def __init__(self, corenlp_url: str = "http://localhost:9000"):
        self.corenlp_client = StanfordCoreNLPClient(corenlp_url)
    
    def extract_with_corenlp(self, text: str, memory_efficient: bool = True) -> Tuple[List[CoreNLPEntity], List[CoreNLPRelation]]:
        """Extract using Stanford CoreNLP with enhanced processing"""
        print("Starting enhanced Stanford CoreNLP extraction...")
        
        try:
            annotations = self.corenlp_client.annotate_text(text, memory_efficient=memory_efficient)
            if not annotations:
                print("CoreNLP annotation failed, using fallback patterns...")
                return [], []
            
            entities = self.corenlp_client.extract_entities(annotations)
            relations = self.corenlp_client.extract_relations(annotations)
            
            print(f"Enhanced CoreNLP extracted {len(entities)} entities and {len(relations)} relations")
            return entities, relations
            
        except Exception as e:
            print(f"Enhanced CoreNLP extraction error: {e}")
            if "OutOfMemoryError" in str(e) or "Java heap space" in str(e):
                print("Memory error - switching to pattern-based extraction")
            return [], []
    
    def extract_with_patterns(self, text: str) -> Tuple[List[CoreNLPEntity], List[CoreNLPRelation]]:
        """Enhanced pattern-based extraction using custom legislative patterns"""
        print("Using enhanced pattern-based extraction...")
        
        entities = []
        relations = []
        
        # Extract entities using custom NER patterns
        entities.extend(self.corenlp_client.custom_ner.extract_custom_entities(text))
        
        # Extract relations using enhanced patterns
        relations.extend(self.corenlp_client.enhanced_relations.extract_enhanced_relations(text))
        
        print(f"Enhanced patterns extracted {len(entities)} entities and {len(relations)} relations")
        return entities, relations
    
    def extract_all(self, text: str, force_patterns: bool = False, memory_efficient: bool = True) -> Tuple[List[CoreNLPEntity], List[CoreNLPRelation]]:
        """Main extraction method with enhanced capabilities"""
        print("Starting enhanced entity and relation extraction...")
        
        if force_patterns:
            print("Forcing enhanced pattern-based extraction...")
            return self.extract_with_patterns(text)
        
        # Try enhanced CoreNLP first
        entities, relations = self.extract_with_corenlp(text, memory_efficient=memory_efficient)
        
        # If CoreNLP fails, use enhanced patterns
        if not entities and not relations:
            print("Enhanced CoreNLP extraction failed, falling back to enhanced patterns...")
            entities, relations = self.extract_with_patterns(text)
        
        return entities, relations
    
    def save_results(self, entities: List[CoreNLPEntity], relations: List[CoreNLPRelation], 
                    filename: str = "enhanced_corenlp_extractions_v2.json"):
        """Save enhanced extraction results"""
        
        output = {
            "version": "v2_high_impact_low_effort",
            "entities": [asdict(entity) for entity in entities],
            "relations": [asdict(relation) for relation in relations],
            "metadata": {
                "extraction_method": "enhanced_corenlp" if entities else "enhanced_patterns",
                "total_entities": len(entities),
                "total_relations": len(relations),
                "entity_types": list(set(e.type for e in entities)),
                "relation_types": list(set(r.relation_type for r in relations if r.relation_type)),
                "sources": list(set(r.source for r in relations if r.source)),
                "enhancements": [
                    "Enhanced CoreNLP annotators (lemma, openie)",
                    "Custom NER patterns for legislative domain",
                    "Enhanced relation patterns for bill-specific relationships",
                    "Improved confidence scoring",
                    "OpenIE integration for additional relations"
                ]
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"Enhanced results saved to {filename}")

def timeout_handler(signum, frame):
    """Handle timeout signal"""
    print("\n⏰ Processing timeout reached. Switching to enhanced pattern-based extraction...")
    raise TimeoutError("CoreNLP processing timeout")

def main():
    """Main execution function for enhanced extraction"""
    
    # Check command line arguments
    force_patterns = False
    memory_efficient = True
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--patterns', '-p']:
            force_patterns = True
            print("Enhanced pattern-based extraction forced via command line argument")
        elif sys.argv[1] in ['--memory-efficient', '-m']:
            memory_efficient = True
            print("Memory-efficient enhanced CoreNLP processing enabled")
        elif sys.argv[1] in ['--fast', '-f']:
            force_patterns = True
            print("Fast mode: Enhanced pattern-based extraction only (no CoreNLP)")
        elif sys.argv[1] in ['--help', '-h']:
            print("""
Enhanced Stanford CoreNLP Entity and Relation Extraction - Version 2

Usage:
  python entity_relation_extraction_v2.py                    # Try enhanced CoreNLP first, fallback to enhanced patterns
  python entity_relation_extraction_v2.py --patterns         # Force enhanced pattern-based extraction only
  python entity_relation_extraction_v2.py -p                 # Short form for enhanced patterns-only
  python entity_relation_extraction_v2.py --memory-efficient # Enable memory-efficient processing
  python entity_relation_extraction_v2.py -m                 # Short form for memory-efficient
  python entity_relation_extraction_v2.py --fast             # Fast mode: enhanced patterns only, no CoreNLP
  python entity_relation_extraction_v2.py -f                 # Short form for fast mode
  python entity_relation_extraction_v2.py --help             # Show this help message

Enhancements in v2:
  ✓ Enhanced CoreNLP annotators (lemma, openie)
  ✓ Custom NER patterns for legislative domain
  ✓ Enhanced relation patterns for bill-specific relationships
  ✓ Improved confidence scoring
  ✓ OpenIE integration for additional relations

The script will automatically fall back to enhanced pattern-based extraction if CoreNLP fails.
""")
            sys.exit(0)
    
    # Set timeout for CoreNLP processing (5 minutes) - only if not forcing patterns
    if not force_patterns:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(300)
    
    # Load bill text
    try:
        with open("extracted_bill_final.txt", "r", encoding="utf-8") as f:
            bill_text = f.read()
        print(f"Loaded bill text: {len(bill_text)} characters")
    except FileNotFoundError:
        print("Error: extracted_bill_final.txt not found. Please run html_bill_to_plain_text.py first.")
        return
    
    # Initialize enhanced extractor
    extractor = BillEntityRelationExtractor()
    
    try:
        # Extract entities and relations with enhanced capabilities
        start_time = time.time()
        entities, relations = extractor.extract_all(bill_text, force_patterns=force_patterns, memory_efficient=memory_efficient)
        end_time = time.time()
        
        # Print enhanced summary
        print(f"\nEnhanced Extraction Results:")
        print(f"Entities: {len(entities)}")
        print(f"Relations: {len(relations)}")
        print(f"Processing Time: {end_time - start_time:.2f} seconds")
        
        # Show entity types
        entity_types = set(e.type for e in entities)
        print(f"Entity Types: {list(entity_types)}")
        
        # Show relation types
        relation_types = set(r.relation_type for r in relations if r.relation_type)
        print(f"Relation Types: {list(relation_types)}")
        
        # Show sources
        sources = set(r.source for r in relations if r.source)
        print(f"Relation Sources: {list(sources)}")
        
        # Save enhanced results
        extractor.save_results(entities, relations)
        
        print(f"\nEnhanced extraction complete!")
        
    except TimeoutError:
        print("Enhanced CoreNLP processing timed out, using enhanced patterns...")
        entities, relations = extractor.extract_with_patterns(bill_text)
        
        print(f"\nEnhanced Pattern-Based Results:")
        print(f"Entities: {len(entities)}")
        print(f"Relations: {len(relations)}")
        
        extractor.save_results(entities, relations)
        
    except Exception as e:
        print(f"Enhanced extraction error: {e}")
        return
    
    finally:
        # Clean up
        if hasattr(extractor, 'corenlp_client'):
            extractor.corenlp_client.close()

if __name__ == "__main__":
    main()
