"""
OCR-based gold price extraction from images.
Uses PaddleOCR for Arabic/French text recognition.
"""
import re
from paddleocr import PaddleOCR
from typing import Optional

# Initialize OCR (Arabic + French support)
ocr = PaddleOCR(use_angle_cls=True, lang='ar')

# Price patterns for different karat levels
KARAT_PATTERNS = {
    '24k': [r'24\s*[kK]', r'24\s*قيراط', r'ذهب\s*24'],
    '22k': [r'22\s*[kK]', r'22\s*قيراط', r'ذهب\s*22'],
    '21k': [r'21\s*[kK]', r'21\s*قيراط', r'ذهب\s*21'],
    '18k': [r'18\s*[kK]', r'18\s*قيراط', r'ذهب\s*18'],
}

# Price number pattern (handles Arabic numerals and commas)
PRICE_PATTERN = r'[\d\u0660-\u0669,.\s]+(?:\s*(?:دج|DA|DZD))?'


def arabic_to_int(text: str) -> Optional[int]:
    """Convert Arabic numerals to integer."""
    arabic_digits = '٠١٢٣٤٥٦٧٨٩'
    western_digits = '0123456789'
    
    result = text
    for ar, wst in zip(arabic_digits, western_digits):
        result = result.replace(ar, wst)
    
    # Remove non-numeric chars except digits
    result = re.sub(r'[^\d]', '', result)
    
    if result:
        return int(result)
    return None


def extract_prices_from_image(image_path: str) -> dict:
    """
    Extract gold prices from an image.
    Returns dict with karat levels as keys and prices in DZD.
    """
    result = ocr.ocr(image_path, cls=True)
    
    if not result or not result[0]:
        return {}
    
    # Combine all detected text
    full_text = ' '.join([line[1][0] for line in result[0]])
    
    prices = {}
    
    # Try to find prices for each karat level
    for karat, patterns in KARAT_PATTERNS.items():
        for pattern in patterns:
            match = re.search(f'({pattern})\\s*[:=]?\\s*({PRICE_PATTERN})', full_text, re.IGNORECASE)
            if match:
                price_text = match.group(2)
                price = arabic_to_int(price_text)
                if price and price > 1000:  # Sanity check (gold > 1000 DZD/g)
                    prices[karat] = price
                    break
    
    return prices


def extract_prices_from_text(text: str) -> dict:
    """
    Extract gold prices from plain text message.
    """
    prices = {}
    
    for karat, patterns in KARAT_PATTERNS.items():
        for pattern in patterns:
            match = re.search(f'({pattern})\\s*[:=]?\\s*({PRICE_PATTERN})', text, re.IGNORECASE)
            if match:
                price_text = match.group(2)
                price = arabic_to_int(price_text)
                if price and price > 1000:
                    prices[karat] = price
                    break
    
    return prices


if __name__ == "__main__":
    # Test with sample text
    sample = "سعر الذهب اليوم: 24k = 18500 دج | 21k = 16200 دج | 18k = 13900 دج"
    print(extract_prices_from_text(sample))
