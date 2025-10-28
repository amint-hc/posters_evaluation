from pathlib import Path
from typing import List
from fastapi import UploadFile, HTTPException

class PosterValidator:
    """Validation utilities for poster evaluation system"""
    
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    MAX_BATCH_SIZE = 50
    
    @classmethod
    def validate_image_file(cls, file: UploadFile) -> bool:
        """Validate single image file"""
        if not file.filename:
            return False
        
        extension = Path(file.filename).suffix.lower()
        return extension in cls.ALLOWED_EXTENSIONS
    
    @classmethod
    def validate_file_size(cls, file: UploadFile) -> bool:
        """Validate file size"""
        if file.size and file.size > cls.MAX_FILE_SIZE:
            return False
        return True
    
    @classmethod
    def validate_batch_size(cls, files: List[UploadFile]) -> bool:
        """Validate batch size"""
        return len(files) <= cls.MAX_BATCH_SIZE
    
    @classmethod
    def validate_filename(cls, filename: str) -> str:
        """Clean and validate filename"""
        # Remove invalid characters for file system
        cleaned = "".join(c for c in filename if c.isalnum() or c in "._-")
        
        # Ensure filename is not empty
        if not cleaned:
            cleaned = "unknown_file"
        
        return cleaned
    
    @classmethod
    def validate_upload_request(cls, files: List[UploadFile]) -> dict:
        """Validate complete upload request"""
        results = {
            "valid_files": [],
            "invalid_files": [],
            "errors": []
        }
        
        # Check batch size
        if not cls.validate_batch_size(files):
            results["errors"].append(f"Too many files. Maximum {cls.MAX_BATCH_SIZE} files allowed.")
            return results
        
        # Validate each file
        for file in files:
            if not cls.validate_image_file(file):
                results["invalid_files"].append({
                    "filename": file.filename,
                    "error": "Invalid file type"
                })
            elif not cls.validate_file_size(file):
                results["invalid_files"].append({
                    "filename": file.filename,
                    "error": "File too large"
                })
            else:
                results["valid_files"].append(file)
        
        return results
