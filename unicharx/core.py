#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniCharX Core Module - Unicode Character Search Engine

Provides the core functionality for searching and exploring Unicode characters
with exact and fuzzy matching capabilities.
"""

import unicodedata
import re
from typing import List, Dict, Optional, Tuple, Iterator, Set
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from functools import lru_cache


@dataclass
class CharInfo:
    """Unicode character information container."""
    code: int
    char: str
    name: str
    category: str
    block: str = ""
    aliases: List[str] = field(default_factory=list)
    
    @property
    def hex_code(self) -> str:
        """Return hexadecimal code point."""
        return f"U+{self.code:04X}"
    
    @property
    def html_entity(self) -> str:
        """Return HTML entity code."""
        return f"&#{self.code};"
    
    @property
    def python_escape(self) -> str:
        """Return Python escape sequence."""
        if self.code <= 0xFFFF:
            return f"\\u{self.code:04X}"
        return f"\\U{self.code:08X}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "code": self.code,
            "char": self.char,
            "name": self.name,
            "category": self.category,
            "block": self.block,
            "hex_code": self.hex_code,
            "html_entity": self.html_entity,
            "python_escape": self.python_escape,
            "aliases": self.aliases,
        }


# Unicode category names
UNICODE_CATEGORIES = {
    "Lu": "Letter, uppercase",
    "Ll": "Letter, lowercase",
    "Lt": "Letter, titlecase",
    "Lm": "Letter, modifier",
    "Lo": "Letter, other",
    "Mn": "Mark, nonspacing",
    "Mc": "Mark, spacing combining",
    "Me": "Mark, enclosing",
    "Nd": "Number, decimal digit",
    "Nl": "Number, letter",
    "No": "Number, other",
    "Pc": "Punctuation, connector",
    "Pd": "Punctuation, dash",
    "Ps": "Punctuation, open",
    "Pe": "Punctuation, close",
    "Pi": "Punctuation, initial quote",
    "Pf": "Punctuation, final quote",
    "Po": "Punctuation, other",
    "Sm": "Symbol, math",
    "Sc": "Symbol, currency",
    "Sk": "Symbol, modifier",
    "So": "Symbol, other",
    "Zs": "Separator, space",
    "Zl": "Separator, line",
    "Zp": "Separator, paragraph",
    "Cc": "Other, control",
    "Cf": "Other, format",
    "Cs": "Other, surrogate",
    "Co": "Other, private use",
    "Cn": "Other, not assigned",
}

# Unicode block ranges (major blocks)
UNICODE_BLOCKS = [
    (0x0000, 0x007F, "Basic Latin"),
    (0x0080, 0x00FF, "Latin-1 Supplement"),
    (0x0100, 0x017F, "Latin Extended-A"),
    (0x0180, 0x024F, "Latin Extended-B"),
    (0x0250, 0x02AF, "IPA Extensions"),
    (0x0370, 0x03FF, "Greek and Coptic"),
    (0x0400, 0x04FF, "Cyrillic"),
    (0x2000, 0x206F, "General Punctuation"),
    (0x2070, 0x209F, "Superscripts and Subscripts"),
    (0x20A0, 0x20CF, "Currency Symbols"),
    (0x2100, 0x214F, "Letterlike Symbols"),
    (0x2190, 0x21FF, "Arrows"),
    (0x2200, 0x22FF, "Mathematical Operators"),
    (0x2300, 0x23FF, "Miscellaneous Technical"),
    (0x2600, 0x26FF, "Miscellaneous Symbols"),
    (0x2700, 0x27BF, "Dingbats"),
    (0x3000, 0x303F, "CJK Symbols and Punctuation"),
    (0x3040, 0x309F, "Hiragana"),
    (0x30A0, 0x30FF, "Katakana"),
    (0x4E00, 0x9FFF, "CJK Unified Ideographs"),
    (0x1F300, 0x1F5FF, "Miscellaneous Symbols and Pictographs"),
    (0x1F600, 0x1F64F, "Emoticons"),
    (0x1F680, 0x1F6FF, "Transport and Map Symbols"),
    (0x1F900, 0x1F9FF, "Supplemental Symbols and Pictographs"),
    (0x1FA00, 0x1FA6F, "Chess Symbols"),
    (0x1FA70, 0x1FAFF, "Symbols and Pictographs Extended-A"),
]


def get_block_name(code: int) -> str:
    """Get Unicode block name for a code point."""
    for start, end, name in UNICODE_BLOCKS:
        if start <= code <= end:
            return name
    return "Unknown"


class UniCharX:
    """
    Unicode Character Intelligent Search Engine.
    
    Provides fast, flexible searching of Unicode characters with support
    for exact matching, fuzzy matching, and category filtering.
    """
    
    # Common aliases for characters
    CHAR_ALIASES = {
        "space": "SPACE",
        "newline": "LINE FEED",
        "tab": "CHARACTER TABULATION",
        "enter": "LINE FEED",
        "slash": "SOLIDUS",
        "backslash": "REVERSE SOLIDUS",
        "at": "COMMERCIAL AT",
        "hash": "NUMBER SIGN",
        "dollar": "DOLLAR SIGN",
        "percent": "PERCENT SIGN",
        "ampersand": "AMPERSAND",
        "asterisk": "ASTERISK",
        "underscore": "LOW LINE",
        "plus": "PLUS SIGN",
        "minus": "HYPHEN-MINUS",
        "equals": "EQUALS SIGN",
        "pipe": "VERTICAL LINE",
        "tilde": "TILDE",
        "grave": "GRAVE ACCENT",
        "acute": "ACUTE ACCENT",
        "quote": "QUOTATION MARK",
        "apostrophe": "APOSTROPHE",
        "exclamation": "EXCLAMATION MARK",
        "question": "QUESTION MARK",
        "colon": "COLON",
        "semicolon": "SEMICOLON",
        "comma": "COMMA",
        "period": "FULL STOP",
        "dot": "FULL STOP",
        "bracket": "LEFT SQUARE BRACKET",
        "brace": "LEFT CURLY BRACKET",
        "paren": "LEFT PARENTHESIS",
        "angle": "LESS-THAN SIGN",
        "heart": "HEAVY BLACK HEART",
        "star": "BLACK STAR",
        "check": "CHECK MARK",
        "cross": "MULTIPLICATION SIGN",
        "arrow": "RIGHTWARDS ARROW",
        "smile": "WHITE SMILING FACE",
        "sad": "WHITE FROWNING FACE",
    }
    
    def __init__(self):
        """Initialize the Unicode search engine."""
        self._char_cache: Dict[int, CharInfo] = {}
        self._name_index: Dict[str, Set[int]] = {}
        self._category_index: Dict[str, Set[int]] = {}
        self._initialized = False
    
    def _initialize(self) -> None:
        """Build character indexes for fast searching."""
        if self._initialized:
            return
        
        # Build index for common Unicode ranges
        # Basic Multilingual Plane + Supplementary Planes (emoji, symbols)
        ranges = [
            (0x0000, 0xFFFF),  # BMP
            (0x1F000, 0x1FFFF),  # Emoji and symbols
            (0x20000, 0x2FFFF),  # CJK Extension
        ]
        
        for start, end in ranges:
            for code in range(start, min(end + 1, 0x10FFFF + 1)):
                try:
                    char = chr(code)
                    name = unicodedata.name(char, "")
                    if name:
                        category = unicodedata.category(char)
                        block = get_block_name(code)
                        
                        info = CharInfo(
                            code=code,
                            char=char,
                            name=name,
                            category=category,
                            block=block,
                        )
                        
                        self._char_cache[code] = info
                        
                        # Build name index (words)
                        words = set(name.lower().split())
                        for word in words:
                            if word not in self._name_index:
                                self._name_index[word] = set()
                            self._name_index[word].add(code)
                        
                        # Build category index
                        if category not in self._category_index:
                            self._category_index[category] = set()
                        self._category_index[category].add(code)
                        
                except (ValueError, OverflowError):
                    continue
        
        self._initialized = True
    
    def get_char_info(self, code_or_char) -> Optional[CharInfo]:
        """
        Get detailed information about a Unicode character.
        
        Args:
            code_or_char: Integer code point or single character string
            
        Returns:
            CharInfo object or None if not found
        """
        self._initialize()
        
        if isinstance(code_or_char, str):
            if len(code_or_char) == 1:
                code = ord(code_or_char)
            else:
                return None
        elif isinstance(code_or_char, int):
            code = code_or_char
        else:
            return None
        
        if code in self._char_cache:
            return self._char_cache[code]
        
        # Try to build info on demand
        try:
            char = chr(code)
            name = unicodedata.name(char, "")
            if name:
                return CharInfo(
                    code=code,
                    char=char,
                    name=name,
                    category=unicodedata.category(char),
                    block=get_block_name(code),
                )
        except (ValueError, OverflowError):
            pass
        
        return None
    
    def search(
        self,
        query: str,
        *,
        fuzzy: bool = False,
        threshold: float = 0.6,
        category: Optional[str] = None,
        block: Optional[str] = None,
        limit: int = 100,
    ) -> List[CharInfo]:
        """
        Search for Unicode characters by name.
        
        Args:
            query: Search query string
            fuzzy: Enable fuzzy matching
            threshold: Minimum similarity threshold for fuzzy matching (0.0-1.0)
            category: Filter by Unicode category (e.g., 'Sm' for math symbols)
            block: Filter by Unicode block name
            limit: Maximum number of results
            
        Returns:
            List of matching CharInfo objects
        """
        self._initialize()
        
        if not query:
            return []
        
        # Normalize query
        query = query.lower().strip()
        
        # Check for alias
        if query in self.CHAR_ALIASES:
            query = self.CHAR_ALIASES[query].lower()
        
        results = []
        seen_codes: Set[int] = set()
        
        # Exact word matching
        query_words = set(query.split())
        candidate_codes: Set[int] = set()
        
        for word in query_words:
            if word in self._name_index:
                if not candidate_codes:
                    candidate_codes = self._name_index[word].copy()
                else:
                    candidate_codes &= self._name_index[word]
        
        # If no word matches, try substring matching
        if not candidate_codes:
            for name_word, codes in self._name_index.items():
                if query in name_word or name_word in query:
                    candidate_codes.update(codes)
        
        # Filter by category
        if category and category in self._category_index:
            if candidate_codes:
                candidate_codes &= self._category_index[category]
            else:
                candidate_codes = self._category_index[category].copy()
        
        # Score and sort results
        scored_results: List[Tuple[float, CharInfo]] = []
        
        for code in candidate_codes:
            if code in seen_codes:
                continue
            
            info = self._char_cache.get(code)
            if not info:
                continue
            
            # Filter by block
            if block and block.lower() not in info.block.lower():
                continue
            
            seen_codes.add(code)
            
            # Calculate score
            name_lower = info.name.lower()
            
            if query == name_lower:
                score = 1.0
            elif query in name_lower:
                # Position bonus (earlier = better)
                pos = name_lower.find(query)
                score = 0.9 - (pos / len(name_lower)) * 0.1
            elif fuzzy:
                score = SequenceMatcher(None, query, name_lower).ratio()
            else:
                # Check if all query words are in name
                if query_words.issubset(set(name_lower.split())):
                    score = 0.8
                else:
                    continue
            
            if score >= threshold:
                scored_results.append((score, info))
        
        # Sort by score (descending)
        scored_results.sort(key=lambda x: (-x[0], x[1].code))
        
        # Return top results
        results = [info for _, info in scored_results[:limit]]
        
        return results
    
    def search_by_category(self, category: str, limit: int = 100) -> List[CharInfo]:
        """
        Get all characters in a Unicode category.
        
        Args:
            category: Unicode category code (e.g., 'Sm', 'So', 'Nd')
            limit: Maximum number of results
            
        Returns:
            List of CharInfo objects
        """
        self._initialize()
        
        if category not in self._category_index:
            return []
        
        codes = sorted(self._category_index[category])[:limit]
        return [self._char_cache[code] for code in codes if code in self._char_cache]
    
    def search_by_block(self, block: str, limit: int = 100) -> List[CharInfo]:
        """
        Get all characters in a Unicode block.
        
        Args:
            block: Unicode block name (partial match)
            limit: Maximum number of results
            
        Returns:
            List of CharInfo objects
        """
        self._initialize()
        
        results = []
        block_lower = block.lower()
        
        for info in self._char_cache.values():
            if block_lower in info.block.lower():
                results.append(info)
                if len(results) >= limit:
                    break
        
        return sorted(results, key=lambda x: x.code)
    
    def list_categories(self) -> Dict[str, str]:
        """Get all Unicode categories with descriptions."""
        return UNICODE_CATEGORIES.copy()
    
    def list_blocks(self) -> List[Tuple[int, int, str]]:
        """Get all Unicode block ranges."""
        return UNICODE_BLOCKS.copy()
    
    def get_random(self, category: Optional[str] = None, count: int = 10) -> List[CharInfo]:
        """
        Get random Unicode characters.
        
        Args:
            category: Optional category filter
            count: Number of random characters
            
        Returns:
            List of random CharInfo objects
        """
        import random
        
        self._initialize()
        
        if category and category in self._category_index:
            codes = list(self._category_index[category])
        else:
            codes = list(self._char_cache.keys())
        
        if len(codes) <= count:
            sample = codes
        else:
            sample = random.sample(codes, count)
        
        return [self._char_cache[code] for code in sample if code in self._char_cache]


# Convenience functions
_engine: Optional[UniCharX] = None


def _get_engine() -> UniCharX:
    """Get or create the global engine instance."""
    global _engine
    if _engine is None:
        _engine = UniCharX()
    return _engine


def search_unicode(query: str, **kwargs) -> List[CharInfo]:
    """
    Search for Unicode characters by name.
    
    Args:
        query: Search query string
        **kwargs: Additional search options (fuzzy, threshold, category, block, limit)
        
    Returns:
        List of matching CharInfo objects
    """
    return _get_engine().search(query, **kwargs)


def get_char_info(code_or_char) -> Optional[CharInfo]:
    """
    Get detailed information about a Unicode character.
    
    Args:
        code_or_char: Integer code point or single character string
        
    Returns:
        CharInfo object or None if not found
    """
    return _get_engine().get_char_info(code_or_char)
