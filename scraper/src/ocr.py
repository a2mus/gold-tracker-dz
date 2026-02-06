"""
OCR Module for extracting prices from images
Uses PaddleOCR for table recognition
"""

import os
import re
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from io import BytesIO

from PIL import Image
from paddleocr import PaddleOCR

logger = logging.getLogger(__name__)

# Initialize PaddleOCR (download models on first run)
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',  # Use 'ar' for Arabic if needed
    show_log=False
)


@dataclass
class OCRPrice:
    """Price extracted from image via OCR"""
    karat: Optional[int]
    offer_price: Optional[float]
    demand_price: Optional[float]
    raw_text: str
    confidence: float


class GoldImageOCR:
    """Extract gold prices from images using OCR"""
    
    # Keywords to identify price tables
    KEYWORDS = {
        'offer': ['offer', 'offre', 'عرض', 'شراء', 'buy'],
        'demand': ['demand', 'demande', 'طلب', 'بيع', 'sell'],
        'karat': ['18k', '21k', '22k', '24k', '750', '875', '916', '999'],
    }
    
    @classmethod
    def extract_from_image(cls, image_data: bytes) -> List[OCRPrice]:
        """Extract prices from image bytes"""
        try:
            # Load image
            image = Image.open(BytesIO(image_data))
            
            # Run OCR
            result = ocr.ocr(image, cls=True)
            
            if not result or not result[0]:
                return []
            
            # Extract text with positions
            texts = []
            for line in result[0]:
                bbox, (text, confidence) = line
                texts.append({
                    'text': text,
                    'confidence': confidence,
                    'y': bbox[0][1]  # Y position for sorting
                })
            
            # Sort by Y position (top to bottom)
            texts.sort(key=lambda x: x['y'])
            
            # Parse prices from OCR results
            return cls._parse_ocr_results(texts)
            
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return []
    
    @classmethod
    def extract_from_file(cls, filepath: str) -> List[OCRPrice]:
        """Extract prices from image file"""
        with open(filepath, 'rb') as f:
            return cls.extract_from_image(f.read())
    
    @classmethod
    def _parse_ocr_results(cls, texts: List[Dict]) -> List[OCRPrice]:
        """Parse OCR text results into prices"""
        prices = []
        
        # Combine all text for pattern matching
        full_text = ' '.join([t['text'] for t in texts])
        
        # Look for price patterns
        # Pattern: numbers that look like prices (4-6 digits, possibly with decimals)
        price_pattern = re.compile(r'(\d{4,6}(?:\.\d{1,2})?)')
        
        matches = price_pattern.findall(full_text)
        
        if len(matches) >= 2:
            # Assume first two numbers are offer/demand
            try:
                offer = float(matches[0])
                demand = float(matches[1])
                
                prices.append(OCRPrice(
                    karat=None,  # Determine from context
                    offer_price=offer,
                    demand_price=demand,
                    raw_text=full_text[:200],
                    confidence=sum(t['confidence'] for t in texts) / len(texts)
                ))
            except ValueError:
                pass
        
        # Look for karat-specific prices
        for text_item in texts:
            text = text_item['text'].lower()
            
            # Check for karat indicators
            karat = None
            if '18' in text or '750' in text:
                karat = 18
            elif '21' in text or '875' in text:
                karat = 21
            elif '22' in text or '916' in text:
                karat = 22
            elif '24' in text or '999' in text:
                karat = 24
            
            if karat:
                # Look for associated price
                price_match = price_pattern.search(text)
                if price_match:
                    prices.append(OCRPrice(
                        karat=karat,
                        offer_price=float(price_match.group(1)),
                        demand_price=None,
                        raw_text=text,
                        confidence=text_item['confidence']
                    ))
        
        return prices


# Test function
def test_ocr(image_path: str):
    """Test OCR on a sample image"""
    results = GoldImageOCR.extract_from_file(image_path)
    
    print(f"Found {len(results)} prices:")
    for price in results:
        print(f"  Karat: {price.karat}, Offer: {price.offer_price}, "
              f"Demand: {price.demand_price}, Confidence: {price.confidence:.2f}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        test_ocr(sys.argv[1])
    else:
        print("Usage: python ocr.py <image_path>")
