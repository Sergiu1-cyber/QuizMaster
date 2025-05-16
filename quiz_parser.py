import os
import re
import logging

def list_quiz_files(directory):
    """List all .txt files in the specified directory."""
    quiz_files = []
    
    try:
        # Get all .txt files in the directory
        for file in os.listdir(directory):
            if file.endswith('.txt'):
                quiz_files.append(file)
        
        return quiz_files
    except Exception as e:
        logging.error(f"Error listing quiz files: {str(e)}")
        return []

def parse_quiz_file(file_path):
    """Parse a quiz file into a structured format."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Quiz file not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split content into questions
        # Format: Question followed by options (A-D) and correct answer
        question_blocks = re.split(r'\n\s*\n', content.strip())
        
        quiz_data = {
            'title': os.path.basename(file_path).replace('.txt', ''),
            'questions': []
        }
        
        for block in question_blocks:
            lines = block.strip().split('\n')
            if not lines:
                continue
            
            question_text = lines[0].strip()
            options = []
            correct_answer = None
            
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                
                # Check if line is an option (A, B, C, D)
                option_match = re.match(r'^([A-D])\)\s*(.+)$', line)
                if option_match:
                    options.append({
                        'id': option_match.group(1),
                        'text': option_match.group(2)
                    })
                
                # Check if line specifies the correct answer
                answer_match = re.match(r'^Answer:\s*([A-D])$', line)
                if answer_match:
                    correct_answer = answer_match.group(1)
            
            # Add question to the quiz only if it has options and a correct answer
            if options and correct_answer:
                quiz_data['questions'].append({
                    'question': question_text,
                    'options': options,
                    'correct_answer': correct_answer
                })
        
        if not quiz_data['questions']:
            raise ValueError("No valid questions found in the file")
        
        return quiz_data
    
    except Exception as e:
        logging.error(f"Error parsing quiz file {file_path}: {str(e)}")
        raise
