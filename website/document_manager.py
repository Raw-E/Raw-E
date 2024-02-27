import os

# Define the path to your document
document_path = "data/project_information/current_system/current_system.md"

# Sections of the document
sections = {
    "introduction": "### Introduction\n",
    "architecture": "### System Architecture\n",
    "components": "### Components Description\n",
    "data_flow": "### Data Flow\n",
    "limitations": "### Current Limitations and Challenges\n",
    "security": "### Security and Privacy\n",
    "deployment": "### Deployment and Operations\n",
    "testing": "### Testing and Quality Assurance\n",
    "user_feedback": "### User Feedback and Observations\n",
    "improvement": "### Areas for Improvement\n",
    "conclusion": "### Conclusion\n",
}

def ensure_document_exists():
    """Ensure the document exists with all predefined section headings."""
    if not os.path.exists(document_path):
        with open(document_path, 'w') as file:
            for key in sections:
                file.write(sections[key] + "\n")

def append_to_section(section_key, content):
    """Append content to a specified section in the document."""
    ensure_document_exists()
    with open(document_path, 'r+') as file:
        lines = file.readlines()
        section_heading = sections.get(section_key, f"### {section_key.title().replace('_', ' ')}\n")
        if section_heading not in lines:
            lines.append(section_heading)
        try:
            section_index = lines.index(section_heading) + 1
            while section_index < len(lines) and not lines[section_index].startswith("### "):
                section_index += 1
            lines.insert(section_index, content + "\n\n")
        except ValueError:
            lines.append(content + "\n\n")
        file.seek(0)
        file.writelines(lines)
        file.truncate()