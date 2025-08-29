"""
BFHL FastAPI Application
Main application file implementing the POST /bfhl endpoint.
"""
from typing import List, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import logging

from .config import USER_ID, EMAIL, ROLL_NUMBER
from .core import split_tokens, sum_numbers_as_string, alternating_caps_reverse_concat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="BFHL API",
    description="Bajaj Finserv Health API for processing arrays of data",
    version="1.0.0"
)

# Add CORS middleware (allow all origins for now - tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BFHLRequest(BaseModel):
    """Request model for BFHL endpoint."""
    data: List[Any] = Field(..., description="Array of data elements to process")
    
    @field_validator('data')
    @classmethod
    def validate_data(cls, v):
        """Ensure data is a list."""
        if not isinstance(v, list):
            raise ValueError("data must be a list")
        return v


class BFHLResponse(BaseModel):
    """Response model for BFHL endpoint."""
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str
    error: Optional[str] = None


@app.post("/bfhl", response_model=BFHLResponse, status_code=200)
async def process_bfhl_data(request: BFHLRequest) -> BFHLResponse:
    """
    Process input data according to BFHL specification.
    
    Takes an array of data and returns categorized results including:
    - Odd/even numbers (as strings)
    - Alphabetic characters (uppercased)
    - Special characters
    - Sum of all numbers (as string)
    - Concatenated alphabets in reverse with alternating caps
    
    Always returns HTTP 200, even for errors (with is_success=false).
    """
    try:
        # Convert all data elements to strings for processing
        data_strings = [str(item) for item in request.data]
        
        # Process the data using core functions
        odd_numbers, even_numbers, alphabets_upper, special_characters = split_tokens(data_strings)
        
        # Calculate sum of all numbers
        sum_str = sum_numbers_as_string(odd_numbers, even_numbers)
        
        # Generate concatenated string with alternating caps
        concat_string = alternating_caps_reverse_concat(data_strings)
        
        # Build successful response
        response = BFHLResponse(
            is_success=True,
            user_id=USER_ID,
            email=EMAIL,
            roll_number=ROLL_NUMBER,
            odd_numbers=odd_numbers,
            even_numbers=even_numbers,
            alphabets=alphabets_upper,
            special_characters=special_characters,
            sum=sum_str,
            concat_string=concat_string
        )
        
        logger.info(f"Successfully processed request with {len(data_strings)} items")
        return response
        
    except Exception as e:
        # Handle any errors gracefully - still return HTTP 200
        logger.error(f"Error processing request: {str(e)}")
        
        error_response = BFHLResponse(
            is_success=False,
            user_id=USER_ID,
            email=EMAIL,
            roll_number=ROLL_NUMBER,
            odd_numbers=[],
            even_numbers=[],
            alphabets=[],
            special_characters=[],
            sum="0",
            concat_string="",
            error=str(e)
        )
        
        return error_response


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "BFHL API is running", "user_id": USER_ID}


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "bfhl-api"}
