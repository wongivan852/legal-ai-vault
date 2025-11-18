"""
Parser for Hong Kong e-Legislation XML files
Handles both ordinances and subsidiary legislation
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)


class HKLegalXMLParser:
    """Parser for HK e-Legislation XML format"""

    # XML namespaces used in HK legal documents
    NAMESPACES = {
        'law': 'http://www.xml.gov.hk/schemas/hklm/1.0',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'dcterms': 'http://purl.org/dc/terms/',
        'xhtml': 'http://www.w3.org/1999/xhtml'
    }

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse_file(self, xml_path: str) -> Optional[Dict]:
        """
        Parse a single HK legal XML file

        Args:
            xml_path: Path to XML file

        Returns:
            Dict containing parsed document data, or None if parsing fails
        """
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Determine document type
            doc_type = root.tag.split('}')[-1]  # Remove namespace

            if doc_type == 'ordinance':
                return self._parse_ordinance(root, xml_path)
            elif doc_type == 'subLeg':
                return self._parse_subsidiary_legislation(root, xml_path)
            elif doc_type == 'lawDoc':
                return self._parse_law_document(root, xml_path)
            else:
                self.logger.warning(f"Unknown document type: {doc_type} in {xml_path}")
                return None

        except Exception as e:
            self.logger.error(f"Failed to parse {xml_path}: {e}", exc_info=True)
            return None

    def _parse_ordinance(self, root: ET.Element, xml_path: str) -> Dict:
        """Parse an ordinance document"""
        return self._parse_document(root, xml_path, 'ordinance')

    def _parse_subsidiary_legislation(self, root: ET.Element, xml_path: str) -> Dict:
        """Parse a subsidiary legislation document"""
        return self._parse_document(root, xml_path, 'subsidiary_legislation')

    def _parse_law_document(self, root: ET.Element, xml_path: str) -> Dict:
        """Parse a lawDoc (instrument) document"""
        return self._parse_document(root, xml_path, 'instrument')

    def _parse_document(self, root: ET.Element, xml_path: str, doc_category: str) -> Dict:
        """
        Common parsing logic for all document types

        Args:
            root: XML root element
            xml_path: Path to source file
            doc_category: 'ordinance' or 'subsidiary_legislation'

        Returns:
            Dict containing document data
        """
        # Parse metadata
        meta = self._parse_metadata(root)

        # Parse main content
        main_element = root.find('law:main', self.NAMESPACES)
        if main_element is None:
            main_element = root.find('main')  # Try without namespace

        content = self._parse_main_content(main_element) if main_element is not None else {}

        # Parse sections
        sections = self._parse_sections(main_element) if main_element is not None else []

        return {
            'source_file': xml_path,
            'category': doc_category,
            'doc_name': meta.get('doc_name'),
            'doc_number': meta.get('doc_number'),
            'doc_type': meta.get('doc_type'),
            'doc_status': meta.get('doc_status'),
            'identifier': meta.get('identifier'),
            'effective_date': meta.get('effective_date'),
            'language': meta.get('language', 'en'),
            'title': content.get('title'),
            'long_title': content.get('long_title'),
            'preamble': content.get('preamble'),
            'full_text': content.get('full_text'),
            'sections': sections,
            'total_sections': len(sections),
            'metadata': meta
        }

    def _parse_metadata(self, root: ET.Element) -> Dict:
        """Extract metadata from document"""
        meta_elem = root.find('law:meta', self.NAMESPACES)
        if meta_elem is None:
            meta_elem = root.find('meta')

        if meta_elem is None:
            return {}

        metadata = {}

        # Extract standard metadata fields
        fields = {
            'doc_name': 'law:docName',
            'doc_type': 'law:docType',
            'doc_number': 'law:docNumber',
            'doc_status': 'law:docStatus'
        }

        for key, tag in fields.items():
            elem = meta_elem.find(tag, self.NAMESPACES)
            if elem is None:
                elem = meta_elem.find(tag.split(':')[-1])
            if elem is not None and elem.text:
                metadata[key] = elem.text.strip()

        # Extract Dublin Core metadata
        dc_fields = {
            'identifier': 'dc:identifier',
            'date': 'dc:date',
            'title': 'dc:title',
            'language': 'dc:language',
            'publisher': 'dc:publisher'
        }

        for key, tag in dc_fields.items():
            elem = meta_elem.find(tag, self.NAMESPACES)
            if elem is None:
                elem = meta_elem.find(tag.split(':')[-1])
            if elem is not None and elem.text:
                metadata[key] = elem.text.strip()

        # Parse date
        if 'date' in metadata:
            try:
                metadata['effective_date'] = datetime.fromisoformat(metadata['date'])
            except ValueError:
                self.logger.warning(f"Could not parse date: {metadata['date']}")

        return metadata

    def _parse_main_content(self, main_elem: ET.Element) -> Dict:
        """Extract main content sections"""
        content = {}

        # Document title
        title_elem = main_elem.find('law:docTitle', self.NAMESPACES)
        if title_elem is None:
            title_elem = main_elem.find('docTitle')
        if title_elem is not None:
            content['title'] = self._extract_text(title_elem)

        # Long title
        long_title_elem = main_elem.find('law:longTitle', self.NAMESPACES)
        if long_title_elem is None:
            long_title_elem = main_elem.find('longTitle')
        if long_title_elem is not None:
            content['long_title'] = self._extract_text(long_title_elem)

        # Preamble
        preamble_elem = main_elem.find('law:preamble', self.NAMESPACES)
        if preamble_elem is None:
            preamble_elem = main_elem.find('preamble')
        if preamble_elem is not None:
            content['preamble'] = self._extract_text(preamble_elem)

        # Full text (all text content)
        content['full_text'] = self._extract_text(main_elem)

        return content

    def _parse_sections(self, main_elem: ET.Element) -> List[Dict]:
        """
        Extract all sections from document

        Returns:
            List of section dicts with id, number, heading, content
        """
        sections = []

        # Find all section elements (may be nested)
        section_elems = main_elem.findall('.//law:section', self.NAMESPACES)
        if not section_elems:
            section_elems = main_elem.findall('.//section')

        for section_elem in section_elems:
            section_data = self._parse_section(section_elem)
            if section_data:
                sections.append(section_data)

        return sections

    def _parse_section(self, section_elem: ET.Element) -> Optional[Dict]:
        """Parse a single section element"""
        try:
            section_id = section_elem.get('id', '')
            section_name = section_elem.get('name', '')

            # Extract section number
            num_elem = section_elem.find('law:num', self.NAMESPACES)
            if num_elem is None:
                num_elem = section_elem.find('num')
            section_num = num_elem.text.strip() if num_elem is not None and num_elem.text else ''

            # Extract heading
            heading_elem = section_elem.find('law:heading', self.NAMESPACES)
            if heading_elem is None:
                heading_elem = section_elem.find('heading')
            heading = self._extract_text(heading_elem) if heading_elem is not None else ''

            # Extract content (paragraphs, subsections, etc.)
            content = self._extract_text(section_elem)

            # Extract subsections
            subsections = []
            subsection_elems = section_elem.findall('law:subsection', self.NAMESPACES)
            if not subsection_elems:
                subsection_elems = section_elem.findall('subsection')

            for subsec_elem in subsection_elems:
                subsec_data = self._parse_subsection(subsec_elem)
                if subsec_data:
                    subsections.append(subsec_data)

            return {
                'section_id': section_id,
                'section_name': section_name,
                'section_number': section_num,
                'heading': heading,
                'content': content,
                'subsections': subsections,
                'has_subsections': len(subsections) > 0
            }

        except Exception as e:
            self.logger.error(f"Failed to parse section: {e}")
            return None

    def _parse_subsection(self, subsec_elem: ET.Element) -> Optional[Dict]:
        """Parse a subsection element"""
        try:
            subsec_id = subsec_elem.get('id', '')
            subsec_name = subsec_elem.get('name', '')

            # Extract subsection number
            num_elem = subsec_elem.find('law:num', self.NAMESPACES)
            if num_elem is None:
                num_elem = subsec_elem.find('num')
            subsec_num = num_elem.text.strip() if num_elem is not None and num_elem.text else ''

            # Extract content
            content = self._extract_text(subsec_elem)

            return {
                'subsection_id': subsec_id,
                'subsection_name': subsec_name,
                'subsection_number': subsec_num,
                'content': content
            }

        except Exception as e:
            self.logger.error(f"Failed to parse subsection: {e}")
            return None

    def _extract_text(self, element: Optional[ET.Element]) -> str:
        """
        Extract all text content from an element and its children

        Handles xhtml content and removes extra whitespace
        """
        if element is None:
            return ''

        # Get all text including children
        text_parts = []

        # Element text
        if element.text:
            text_parts.append(element.text)

        # Children text
        for child in element:
            child_text = self._extract_text(child)
            if child_text:
                text_parts.append(child_text)

            # Tail text after child
            if child.tail:
                text_parts.append(child.tail)

        # Join and clean up
        text = ' '.join(text_parts)
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = text.strip()

        return text

    def extract_references(self, text: str) -> List[str]:
        """
        Extract legal references from text

        Finds patterns like "Cap. 123", "s. 45", "reg. 10"
        """
        references = []

        # Pattern for Cap references: Cap. 123, Cap 123
        cap_pattern = r'Cap\.?\s*(\d+[A-Z]?)'
        references.extend(re.findall(cap_pattern, text, re.IGNORECASE))

        return references

    def batch_parse_directory(self, directory: str) -> List[Dict]:
        """
        Parse all XML files in a directory

        Args:
            directory: Path to directory containing XML files

        Returns:
            List of parsed document dicts
        """
        import os
        from pathlib import Path

        documents = []
        xml_files = list(Path(directory).rglob('*.xml'))

        self.logger.info(f"Found {len(xml_files)} XML files in {directory}")

        for i, xml_file in enumerate(xml_files, 1):
            if i % 100 == 0:
                self.logger.info(f"Parsed {i}/{len(xml_files)} files...")

            doc_data = self.parse_file(str(xml_file))
            if doc_data:
                documents.append(doc_data)

        self.logger.info(f"Successfully parsed {len(documents)} documents")
        return documents
