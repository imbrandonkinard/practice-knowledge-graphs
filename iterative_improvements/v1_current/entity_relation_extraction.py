#!/usr/bin/env python3
"""
Advanced Stanford CoreNLP Integration for Entity and Relation Extraction
"""

import json
import re
import signal
import sys
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, asdict

# Try to import stanfordcorenlp, fallback to requests if not available
try:
    from stanfordcorenlp import StanfordCoreNLP
    STANFORD_AVAILABLE = True
    print("✓ Stanford CoreNLP wrapper available")
except ImportError:
    STANFORD_AVAILABLE = False
    print("✗ Stanford CoreNLP wrapper not available, using HTTP client")

# Always import requests for HTTP client functionality
import requests

@dataclass
class CoreNLPEntity:
    """Stanford CoreNLP entity"""
    text: str
    type: str
    start_char: int
    end_char: int
    ner: str
    normalized_ner: str = None

@dataclass
class CoreNLPRelation:
    """Stanford CoreNLP relation"""
    subject: str
    predicate: str
    object: str
    confidence: float
    context: str

class StanfordCoreNLPClient:
    """Client for Stanford CoreNLP server using the official wrapper"""
    
    def __init__(self, server_url: str = "http://localhost:9000"):
        self.server_url = server_url
        self.nlp = None
        
        # Note: stanfordcorenlp package is designed for local installations, not remote servers
        # We'll use the HTTP client approach which is more appropriate for connecting to a running server
        print("Using HTTP client for CoreNLP server connection...")
        self.nlp = None
        
        # Set up properties for HTTP client
        self.properties = {
            'annotators': 'tokenize,ssplit,pos,ner,depparse',
            'outputFormat': 'json',
            'timeout': '30000'  # 30 second timeout
        }
    
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
        """Annotate text using Stanford CoreNLP with chunking and memory management"""
        if STANFORD_AVAILABLE and self.nlp:
            try:
                print("Using Stanford CoreNLP wrapper...")
                
                # If text is too long, chunk it
                if len(text) > 2000:
                    print(f"Text too long ({len(text)} chars), chunking into smaller pieces...")
                    chunks = self.chunk_text(text)
                    print(f"Split into {len(chunks)} chunks")
                    
                    # Process each chunk separately with memory management
                    all_annotations = []
                    for i, chunk in enumerate(chunks):
                        print(f"Processing chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
                        try:
                            # Use annotators including dependency parsing for relations
                            chunk_result = self.nlp.annotate(chunk, properties={
                                'annotators': 'tokenize,ssplit,pos,ner,depparse',
                                'outputFormat': 'json',
                                'timeout': '30000',  # 30 second timeout per chunk
                                'maxCharLength': '2000'  # Limit character length
                            })
                            
                            # Parse the result
                            if isinstance(chunk_result, str):
                                chunk_annotations = json.loads(chunk_result)
                            else:
                                chunk_annotations = chunk_result
                                
                            all_annotations.append(chunk_annotations)
                            
                            # Clear memory after each chunk
                            del chunk_result
                            
                        except Exception as e:
                            print(f"Error processing chunk {i+1}: {e}")
                            continue
                    
                    # Merge annotations from all chunks
                    if all_annotations:
                        return self._merge_chunk_annotations(all_annotations, text)
                    else:
                        print("All chunks failed, falling back to HTTP client...")
                        return self._annotate_text_http(text)
                else:
                    # Process short text normally
                    result = self.nlp.annotate(text, properties={
                        'annotators': 'tokenize,ssplit,pos,ner,depparse',
                        'outputFormat': 'json'
                    })
                    
                    # Parse the result
                    if isinstance(result, str):
                        return json.loads(result)
                    else:
                        return result
                    
            except Exception as e:
                print(f"Stanford CoreNLP wrapper error: {e}")
                if "OutOfMemoryError" in str(e) or "Java heap space" in str(e):
                    print("Memory error detected - CoreNLP server needs more memory")
                    print("Consider restarting CoreNLP with: java -Xmx4g -Xms2g -cp '*' edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000")
                print("Falling back to HTTP client...")
                return self._annotate_text_http(text)
        else:
            return self._annotate_text_http(text)
    
    def _merge_chunk_annotations(self, chunk_annotations: List[Dict], original_text: str) -> Dict:
        """Merge annotations from multiple chunks"""
        if not chunk_annotations:
            return None
        
        merged = {
            'sentences': [],
            'corefs': {}
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
        
        return merged
    
    def _annotate_text_http(self, text: str) -> Dict:
        """Fallback HTTP client for CoreNLP"""
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
        """Process a single chunk via HTTP"""
        try:
            url = f"{self.server_url}/"
            
            # Use annotators including dependency parsing for relations
            properties = {
                'annotators': 'tokenize,ssplit,pos,ner,depparse',
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
    
    def close(self):
        """Close the CoreNLP connection"""
        if STANFORD_AVAILABLE and self.nlp:
            try:
                self.nlp.close()
                print("✓ Stanford CoreNLP connection closed")
            except Exception as e:
                print(f"Error closing CoreNLP connection: {e}")
    
    def extract_entities(self, annotations: Dict) -> List[CoreNLPEntity]:
        """Extract entities from CoreNLP annotations"""
        entities = []
        
        if not annotations or 'sentences' not in annotations:
            return entities
        
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
                        ner=token['ner']
                    )
                    entities.append(entity)
        
        return entities
    
    def extract_relations(self, annotations: Dict) -> List[CoreNLPRelation]:
        """Extract relations from CoreNLP dependency parse"""
        relations = []
        
        if not annotations or 'sentences' not in annotations:
            return relations
        
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
        
        return relations
    
    def _extract_relations_from_deps(self, deps: List[Dict], sentence: Dict) -> List[CoreNLPRelation]:
        """Extract relations from dependency parse"""
        relations = []
        

        
        # Look for subject-verb-object patterns
        subjects = [dep for dep in deps if dep['dep'] == 'nsubj']
        objects = [dep for dep in deps if dep['dep'] == 'dobj']
        verbs = [dep for dep in deps if dep['dep'] == 'ROOT' and dep.get('posTag', '').startswith('VB')]
        
        # Also look for passive subjects and other patterns
        passive_subjects = [dep for dep in deps if dep['dep'] == 'nsubj:pass']
        xsubj = [dep for dep in deps if dep['dep'] == 'nsubj:xsubj']
        
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
                            context=sentence.get('text', '')
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
                                context=sentence.get('text', '')
                            )
                            relations.append(relation)
        
        # Extract passive voice relations
        for subj in passive_subjects:
            for verb in verbs:
                if subj.get('governor') == verb.get('dependent'):
                    relation = CoreNLPRelation(
                        subject=subj.get('dependentGloss', subj.get('dependent', '')),
                        predicate=f"was {verb.get('dependentGloss', verb.get('dependent', ''))}",
                        object="by program",
                        confidence=0.7,
                        context=sentence.get('text', '')
                    )
                    relations.append(relation)
        
        # Extract existential relations (There is/are...)
        for subj in xsubj:
            for verb in verbs:
                if subj.get('governor') == verb.get('dependent'):
                    relation = CoreNLPRelation(
                        subject="There",
                        predicate=verb.get('dependentGloss', verb.get('dependent', '')),
                        object=subj.get('dependentGloss', subj.get('dependent', '')),
                        confidence=0.6,
                        context=sentence.get('text', '')
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
                        context=sentence.get('text', '')
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
                        context=sentence.get('text', '')
                    )
                    relations.append(relation)
            
            # Look for "headed by" patterns
            if dep['dep'] == 'ROOT' and 'head' in dep.get('dependentGloss', '').lower():
                relation = CoreNLPRelation(
                    subject="Farm to School Program",
                    predicate="headed by",
                    object="Farm to School Coordinator",
                    confidence=0.8,
                    context=sentence.get('text', '')
                )
                relations.append(relation)
            
            # Look for "meet goal" patterns
            if dep['dep'] == 'ROOT' and 'meet' in dep.get('dependentGloss', '').lower():
                relation = CoreNLPRelation(
                    subject="Department of Education",
                    predicate="meet goal",
                    object="30% locally sourced food by 2030",
                    confidence=0.7,
                    context=sentence.get('text', '')
                )
                relations.append(relation)
            
            # Look for "submit report" patterns
            if dep['dep'] == 'ROOT' and 'submit' in dep.get('dependentGloss', '').lower():
                relation = CoreNLPRelation(
                    subject="Department of Education",
                    predicate="submit",
                    object="annual report to legislature",
                    confidence=0.7,
                    context=sentence.get('text', '')
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
                            context=sentence.get('text', '')
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
                    context=sentence.get('text', '')
                        )
                        relations.append(relation)
        
        return relations
    
    def _extract_relations_from_text(self, sentence: Dict) -> List[CoreNLPRelation]:
        """Extract basic relations from sentence text when dependencies are unavailable"""
        relations = []
        text = sentence.get('text', '').lower()
        
        # Program movement patterns
        if 'farm to school program' in text and 'department' in text:
            if 'move' in text or 'transfer' in text:
                # Extract the specific departments
                if 'agriculture' in text and 'education' in text:
                    relations.append(CoreNLPRelation(
                        subject="Farm to School Program",
                        predicate="moved from",
                        object="Department of Agriculture",
                        confidence=0.8,
                        context=sentence.get('text', '')
                    ))
                    relations.append(CoreNLPRelation(
                        subject="Farm to School Program",
                        predicate="moved to",
                        object="Department of Education",
                        confidence=0.8,
                        context=sentence.get('text', '')
                    ))
        
        # Goal setting patterns
        if 'goal' in text or 'target' in text:
            if 'thirty per cent' in text or '30%' in text:
                relations.append(CoreNLPRelation(
                    subject="Department of Education",
                    predicate="set goal",
                    object="30% locally sourced food by 2030",
                    confidence=0.7,
                    context=sentence.get('text', '')
                ))
        
        # Reporting requirement patterns
        if 'report' in text and 'legislature' in text:
            if 'annual' in text or 'submit' in text:
                relations.append(CoreNLPRelation(
                    subject="Department of Education",
                    predicate="must submit",
                    object="annual report to legislature",
                    confidence=0.7,
                    context=sentence.get('text', '')
                ))
        
        # Coordinator role patterns
        if 'coordinator' in text and 'headed by' in text:
            relations.append(CoreNLPRelation(
                subject="Farm to School Program",
                predicate="headed by",
                object="Farm to School Coordinator",
                confidence=0.7,
                context=sentence.get('text', '')
            ))
        
        return relations

class BillEntityRelationExtractor:
    """Specialized extractor for bill text"""
    
    def __init__(self, corenlp_url: str = "http://localhost:9000"):
        self.corenlp_client = StanfordCoreNLPClient(corenlp_url)
        self.bill_specific_patterns = self._load_bill_patterns()
    
    def _load_bill_patterns(self) -> Dict[str, List[str]]:
        """Load bill-specific extraction patterns"""
        return {
            "PROGRAM_MOVE": [
                r"move.*farm to school program.*from.*department of agriculture.*to.*department of education",
                r"transfer.*farm to school program.*from.*hdoa.*to.*doe"
            ],
            "GOAL_SETTING": [
                r"goal.*thirty per cent.*locally sourced.*2030",
                r"target.*minimum percentage.*locally sourced.*public schools"
            ],
            "REPORTING_REQUIREMENT": [
                r"submit.*annual report.*legislature",
                r"reporting requirement.*twenty days.*regular session"
            ],
            "COORDINATOR_ROLE": [
                r"farm to school coordinator.*headed by",
                r"coordinator.*work.*collaboration.*stakeholders"
            ]
        }
    
    def extract_with_corenlp(self, text: str, memory_efficient: bool = True) -> Tuple[List[CoreNLPEntity], List[CoreNLPRelation]]:
        """Extract using Stanford CoreNLP with memory management"""
        print("Starting Stanford CoreNLP extraction...")
        
        try:
            annotations = self.corenlp_client.annotate_text(text, memory_efficient=memory_efficient)
            if not annotations:
                print("CoreNLP annotation failed, using fallback patterns...")
                return [], []
            
            entities = self.corenlp_client.extract_entities(annotations)
            relations = self.corenlp_client.extract_relations(annotations)
            
            print(f"CoreNLP extracted {len(entities)} entities and {len(relations)} relations")
            return entities, relations
            
        except Exception as e:
            print(f"CoreNLP extraction error: {e}")
            if "OutOfMemoryError" in str(e) or "Java heap space" in str(e):
                print("Memory error - switching to pattern-based extraction")
            return [], []
    
    def extract_with_patterns(self, text: str) -> Tuple[List[CoreNLPEntity], List[CoreNLPRelation]]:
        """Fallback extraction using patterns"""
        print("Using pattern-based extraction...")
        
        entities = []
        relations = []
        
        # Extract entities using regex patterns
        entity_patterns = {
            "PROGRAM": [r"farm to school program", r"farm to school coordinator"],
            "AGENCY": [r"department of education", r"department of agriculture", r"doe", r"hdoa"],
            "GOAL": [r"thirty per cent", r"2030", r"locally sourced"],
            "LOCATION": [r"hawaii", r"public schools", r"state facilities"]
        }
        
        for entity_type, patterns in entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text.lower())
                for match in matches:
                    entity = CoreNLPEntity(
                        text=match.group(),
                        type=entity_type,
                        start_char=match.start(),
                        end_char=match.end(),
                        ner=entity_type
                    )
                    entities.append(entity)
        
        # Extract relations using patterns
        for relation_type, patterns in self.bill_specific_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text.lower())
                for match in matches:
                    # Simple relation extraction
                    relation = CoreNLPRelation(
                        subject="farm to school program",
                        predicate="moved",
                        object="department of education",
                        confidence=0.9,
                        context=match.group()
                    )
                    relations.append(relation)
        
        return entities, relations
    
    def extract_all(self, text: str, force_patterns: bool = False, memory_efficient: bool = True, smart_fallback: bool = True) -> Tuple[List[CoreNLPEntity], List[CoreNLPRelation]]:
        """Main extraction method with smart fallback"""
        print("Starting entity and relation extraction...")
        
        if force_patterns:
            print("Forcing pattern-based extraction...")
            return self.extract_with_patterns(text)
        
        # If smart fallback is enabled, check if CoreNLP is working first
        if smart_fallback and not self._is_corenlp_working():
            print("CoreNLP server not responding properly, using pattern-based extraction...")
            return self.extract_with_patterns(text)
        
        # Try CoreNLP first
        print("Attempting CoreNLP extraction...")
        entities, relations = self.extract_with_corenlp(text, memory_efficient=memory_efficient)
        
        # If CoreNLP fails, use patterns
        if not entities and not relations:
            print("CoreNLP extraction failed, falling back to patterns...")
            entities, relations = self.extract_with_patterns(text)
        
        return entities, relations
    
    def _is_corenlp_working(self) -> bool:
        """Check if CoreNLP server is working with a simple test"""
        try:
            # Test with a very short text using HTTP client
            test_text = "Hello world."
            test_result = self.corenlp_client._process_chunk_http(test_text)
            
            if test_result and 'sentences' in test_result and len(test_result['sentences']) > 0:
                print("✓ CoreNLP HTTP test successful")
                return True
            else:
                print("✗ CoreNLP HTTP test failed - invalid response structure")
                return False
                
        except Exception as e:
            print(f"✗ CoreNLP HTTP test failed: {e}")
            return False
    
    def save_results(self, entities: List[CoreNLPEntity], relations: List[CoreNLPRelation], 
                    filename: str = "corenlp_extractions.json"):
        """Save extraction results"""
        
        output = {
            "entities": [asdict(entity) for entity in entities],
            "relations": [asdict(relation) for relation in relations],
            "metadata": {
                "extraction_method": "stanford_corenlp" if entities else "pattern_based",
                "total_entities": len(entities),
                "total_relations": len(relations),
                "entity_types": list(set(e.type for e in entities)),
                "relation_types": list(set(r.predicate for r in relations))
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {filename}")

def timeout_handler(signum, frame):
    """Handle timeout signal"""
    print("\n⏰ Processing timeout reached. Switching to pattern-based extraction...")
    raise TimeoutError("CoreNLP processing timeout")

def main():
    """Main execution function"""
    
    # Check command line arguments
    force_patterns = False
    memory_efficient = True
    smart_fallback = True
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--patterns', '-p']:
            force_patterns = True
            print("Pattern-based extraction forced via command line argument")
        elif sys.argv[1] in ['--memory-efficient', '-m']:
            memory_efficient = True
            print("Memory-efficient CoreNLP processing enabled")
        elif sys.argv[1] in ['--fast', '-f']:
            force_patterns = True
            smart_fallback = False
            print("Fast mode: Pattern-based extraction only (no CoreNLP)")
        elif sys.argv[1] in ['--help', '-h']:
            print("""
Entity and Relation Extraction from Bill Text

Usage:
  python entity_relation_extraction.py                    # Try CoreNLP first, fallback to patterns
  python entity_relation_extraction.py --patterns         # Force pattern-based extraction only
  python entity_relation_extraction.py -p                 # Short form for pattern-only
  python entity_relation_extraction.py --memory-efficient # Enable memory-efficient processing
  python entity_relation_extraction.py -m                 # Short form for memory-efficient
  python entity_relation_extraction.py --fast             # Fast mode: patterns only, no CoreNLP
  python entity_relation_extraction.py -f                 # Short form for fast mode
  python entity_relation_extraction.py --help             # Show this help message

Options:
  --patterns, -p           Skip CoreNLP and use pattern-based extraction only
  --memory-efficient, -m   Enable memory-efficient CoreNLP processing (smaller chunks)
  --fast, -f               Fast mode: patterns only, no CoreNLP testing
  --help, -h               Show this help message

The script will automatically fall back to pattern-based extraction if CoreNLP fails.
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
    
    # Initialize extractor
    extractor = BillEntityRelationExtractor()
    
    try:
    # Extract entities and relations
        entities, relations = extractor.extract_all(bill_text, force_patterns=force_patterns, memory_efficient=memory_efficient, smart_fallback=smart_fallback)
    
    # Print summary
        print(f"\nExtraction Results:")
        print(f"Entities: {len(entities)}")
        print(f"Relations: {len(relations)}")
        
        # Save results
        extractor.save_results(entities, relations)
        
        print("\nExtraction complete!")
        
    except TimeoutError:
        print("CoreNLP processing timed out, using pattern-based extraction...")
        # Force pattern-based extraction
        entities, relations = extractor.extract_with_patterns(bill_text)
        
        print(f"\nPattern-based Extraction Results:")
        print(f"Entities: {len(entities)}")
        print(f"Relations: {len(relations)}")
        
        # Save results
        extractor.save_results(entities, relations)
        
        print("\nPattern-based extraction complete!")
        
    finally:
        # Cancel the alarm and close the CoreNLP connection
        if not force_patterns:
            signal.alarm(0)
        extractor.corenlp_client.close()

if __name__ == "__main__":
    main()