import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from ..database import get_db
from ..models import PromptManagement, Company
from ..schemas import (
    PromptResponseSchema, 
    PromptQueryParams, 
    InvalidCompanyIdError, 
    NoPromptsFoundError, 
    TimeoutError, 
    InternalServerError
)
from ..security import get_current_user, get_user_with_role
from ..models import UserRole
from ..models import User

router = APIRouter(
    prefix="/api/prompts",
    tags=["prompts"]
)

@router.get(
    "/{company_id}", 
    response_model=PromptResponseSchema, 
    responses={
        400: {"model": InvalidCompanyIdError},
        401: {"description": "Unauthorized"},
        404: {"model": NoPromptsFoundError},
        504: {"model": TimeoutError},
        500: {"model": InternalServerError}
    }
)
async def get_prompts_by_company(
    company_id: str, 
    params: PromptQueryParams = Depends(),
    current_user: User = Depends(get_user_with_role(UserRole.USER)),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve prompts for a specific company with pagination
    
    - Requires authentication
    - Returns prompts for the given company_id
    - Supports pagination
    - Performance target: ≤ 3 seconds
    """
    try:
        # Validate company_id
        if not company_id or len(company_id.strip()) == 0:
            return JSONResponse(
                status_code=400, 
                content={"error": "Invalid or missing company_id"}
            )

        # Use asyncio timeout to enforce 3-second performance requirement
        try:
            async with asyncio.timeout(3):
                # Count total prompts
                total_prompts_query = select(func.count(PromptManagement.id)).where(PromptManagement.company_id == company_id)
                total_prompts = await db.scalar(total_prompts_query)

                if total_prompts == 0:
                    return JSONResponse(
                        status_code=404, 
                        content={"error": "No prompts found for this company"}
                    )

                # Fetch prompts with pagination
                offset = (params.page - 1) * params.limit
                prompts_query = select(PromptManagement, Company.name).join(Company).where(
                    PromptManagement.company_id == company_id
                ).offset(offset).limit(params.limit)
                
                result = await db.execute(prompts_query)
                prompts_data = result.all()

                # Transform results
                prompts = [
                    {
                        "prompt_id": prompt.id, 
                        "prompt_title": prompt.prompt_title, 
                        "prompt": prompt.prompt
                    } for prompt, _ in prompts_data
                ]

                return {
                    "company_id": company_id,
                    "company_name": prompts_data[0][1] if prompts_data else "Unknown",
                    "prompts": prompts,
                    "pagination": {
                        "page": params.page,
                        "limit": params.limit,
                        "total": total_prompts
                    }
                }
        except asyncio.TimeoutError:
            return JSONResponse(
                status_code=504, 
                content={"error": "Request timed out"}
            )

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": f"Internal server error: {str(e)}"}
        )
