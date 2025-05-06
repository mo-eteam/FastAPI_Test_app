from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class PromptBase(BaseModel):
    prompt_id: int
    prompt_title: str
    prompt: str

class PaginationSchema(BaseModel):
    page: int
    limit: int
    total: int

class PromptResponseSchema(BaseModel):
    company_id: str
    company_name: str
    prompts: List[PromptBase]
    pagination: PaginationSchema

class PromptQueryParams(BaseModel):
    page: Optional[int] = Field(1, ge=1, description='Page number for pagination')
    limit: Optional[int] = Field(100, ge=1, le=100, description='Number of results per page (max 100)')

class ErrorResponseSchema(BaseModel):
    error: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Specific error response schemas for different scenarios
class InvalidCompanyIdError(ErrorResponseSchema):
    error: str = 'Invalid or missing company_id'

class NoPromptsFoundError(ErrorResponseSchema):
    error: str = 'No prompts found for this company'

class TimeoutError(ErrorResponseSchema):
    error: str = 'Request timed out'

class InternalServerError(ErrorResponseSchema):
    error: str = 'Internal server error'
