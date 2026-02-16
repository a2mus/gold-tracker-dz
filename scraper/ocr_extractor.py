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
    '24k': [r'24\s*[kK]', r'24\s*قيراط', r'ذهب\s*24', r'999'],
    '22k': [r'22\s*[kK]', r'22\s*قيراط', r'ذهب\s*22', r'916'],
    '21k': [r'21\s*[kK]', r'21\s*قيراط', r'ذهب\s*21', r'875'],
    '18k': [r'18\s*[kK]', r'18\s*قيراط', r'ذهب\s*18', r'750'],
}

# Price number pattern - strict 3-6 digits only (realistic gold price range in DZD)
# Only match actual digits, not commas/dots that can create false matches
PRICE_PATTERN = r'(?:جد|دج|DA|DZD)?[\d\u0660-\u0669]{3,6}(?:دج|DA|DZD)?'


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
    return extract_prices_from_text(full_text)


def extract_prices_from_text(text: str) -> dict:
    """
    Extract gold prices from plain text message.
    """
    prices = {}
    
    # Clean text: replace multiple spaces/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    
    for karat, patterns in KARAT_PATTERNS.items():
        for pattern in patterns:
            # Allow common separators like ":", "=", "يبدأ من", "بـ", "سعر", "السعر", etc.
            # and common OCR misreads of these.
            separator = r'(?:\s*[:=]\s*|\s+يبدأ\s+من\s+|\s+من\s+|\s+بـ\s+|\s+السعر\s+|\s+سعر\s+|\s+)'
            match = re.search(f'({pattern}){separator}({PRICE_PATTERN})', text, re.IGNORECASE)
            if match:
                price_text = match.group(2)
                price = arabic_to_int(price_text)
                # Sanity check: Price must be between 1,000 and 100,000 DZD
                if price and 1000 < price < 100000:
                    prices[karat] = price
                    break
    
    return prices


if __name__ == "__main__":
    # Test with sample text
    sample = "سعر الذهب اليوم: 24k = 18500 دج | 21k = 16200 دج | 18k = 13900 دج"
    print(extract_prices_from_text(sample))
