AI Prompting Guide for Vocabulary Learning App
This guide outlines the core AI-driven functions for enhancing data quality, generating content, and adapting learning within a vocabulary application.
1. AI-Based Word Data Enrichment Prompt
Purpose: Automatically fetch and structure all metadata for a given word.
Input:
word: The target word to enrich (e.g., "bright").
Instructions for AI Model:
Data Retrieval:
Fetch base data for the word from various dictionary APIs (e.g., Oxford, Cambridge, Wordnik, Wiktionary).
Definition Generation & Simplification:
Provide a simple definition for the word.
Ensure the definition's CEFR level is the same or lower than the word's inherent level.
Filter for only popular and common meanings.
Example Sentence Generation:
Generate three simple example sentences that include the word.
Ensure generated sentences avoid harder vocabulary.
Synonym and Antonym Selection:
Identify and select the top three high-frequency or easy synonyms for the word.
Identify and select the top three high-frequency or simple antonyms for the word.
Collocation and Phrase Retrieval:
Retrieve relevant common phrases that include the word (collocations).
Detect and rank common idioms or phrasal uses related to the word. Consider sources like Wiktionary idioms, British National Corpus, and AI-generated phrases cross-validated with frequency lists.
Word Forms Identification:
List all inflected or derived forms of the word (e.g., “run”, “runs”, “ran”, “running” for "run").
Category Identification:
Identify up to three semantic categories for the word (e.g., "emotion", "technology").
Output Format:
Generate a WordEntry object (or equivalent JSON) with the following fields fully populated:


word (String)
pronunciation_ipa (String)
audio_uk_url (URL)
audio_us_url (URL)
part_of_speech (String)
cefr_level (Enum A1–C2)
frequency_rank (Integer)
usability_score (Float)
categories (List&lt;String>)
collocations (List&lt;String>)
word_forms (List&lt;String>)
meanings (List&lt;Meaning> - see Sub-Entity Meaning below)
For each Meaning sub-entity, populate these fields:


definition (String)
sample_image_url (URL)
synonyms (List&lt;String>)
antonyms (List&lt;String>)
example_sentences (List&lt;String>)
phrases (List&lt;String>)
2. Usability Score Engine Prompt
Purpose: Calculate a metric indicating how "useful" a word is for learners.
Input:
frequencyRank: The raw frequency rank of the word.
cefrLevel: The CEFR classification of the word (A1–C2).
collocationCount: The number of collocations identified for the word.
Instructions for AI Model:
Normalize frequencyRank: Scale frequencyRank to a value between 0 and 1 (where 0 is most frequent and 1 is least frequent).
frequencyRankNormalized = (current_rank - min_rank) / (max_rank - min_rank) (adjusting for inverse relationship where lower rank is higher frequency).
Assign cefrWeight: Assign a weight based on the CEFR level.
Example mapping: A1 = 1.0, A2 = 0.8, B1 = 0.6, B2 = 0.4, C1 = 0.3, C2 = 0.2.
Calculate collocationCountWeight: Assign a weight based on the number of collocations. Higher collocation usage should increase usability. (Specific formula for this weight can be defined here, e.g., a simple linear scale or a logarithmic scale).
Calculate Usability Score: Apply the formula: Usability Score = 0.5 * (1 - frequencyRankNormalized) + 0.3 * cefrWeight + 0.2 * collocationCountWeight.
3. Image Generation Prompt
Purpose: Generate a visual image representing the meaning of a word.
Input:
word: The target word (e.g., "bright").
definition: The simple definition of the word (e.g., "giving a lot of light").
exampleSentence: A simple example sentence using the word (e.g., "The room is bright and sunny.").
Instructions for AI Model:
Generate an image that visually represents the definition of the word.
Use the exampleSentence for additional details or context to enrich the image generation (e.g., "The room is bright and sunny" could guide the image to show a sunny room).
The generated image should be a sample_image_url for the Meaning entity.
